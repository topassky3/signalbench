"""Small offline SignalBench demonstrator. All bundled examples are SYNTHETIC.

Measures sample-domain quantities; it does not certify a receiver or RF power.
Copyright 2026 Juan Felipe Orozco Cortes. SPDX-License-Identifier: MIT
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np


def analyze(iq: np.ndarray, sample_rate: float) -> dict:
    iq = np.asarray(iq, dtype=np.complex128)
    if iq.ndim != 1 or iq.size < 256:
        raise ValueError("At least 256 one-dimensional complex samples are required")
    if not np.isfinite(sample_rate) or sample_rate <= 0:
        raise ValueError("Sample rate must be finite and positive")
    if not np.isfinite(iq).all():
        raise ValueError("Samples must be finite")
    power = float(np.mean(np.abs(iq) ** 2))
    dc_power = float(abs(np.mean(iq)) ** 2)
    rail_fraction = float(np.mean(np.abs(np.stack([iq.real, iq.imag])) >= 1.0))
    window = np.hanning(iq.size)
    spectrum = np.fft.fftshift(np.fft.fft(iq * window))
    psd = np.abs(spectrum) ** 2 / (sample_rate * np.sum(window ** 2))
    freqs = np.fft.fftshift(np.fft.fftfreq(iq.size, 1.0 / sample_rate))
    # Select a non-DC peak for the report; raw samples and total power are unchanged.
    scores = psd.copy()
    scores[np.abs(freqs) <= 2 * sample_rate / iq.size] = 0
    peak_hz = None if np.max(scores) == 0 else float(freqs[np.argmax(scores)])
    return {
        "sample_count": int(iq.size),
        "sample_rate_hz_as_supplied": float(sample_rate),
        "fft_bin_hz": float(sample_rate / iq.size),
        "mean_sample_power": power,
        "mean_sample_power_db_re_unit": float(10 * np.log10(max(power, 1e-300))),
        "dc_sample_power": dc_power,
        "dc_power_fraction": dc_power / power if power else 0.0,
        "component_rail_fraction_at_unit_limit": rail_fraction,
        "largest_non_dc_peak_offset_hz": peak_hz,
        "psd_integral_window_weighted_sample_power": float(np.sum(psd) * sample_rate / iq.size),
        "reference": "Unit complex-sample mean-square power; not calibrated RF dBm",
        "interpretation": [
            "A component rail count can flag hard clipping, but cannot rule out analog compression.",
            "DC can come from a receiver or a real baseband component; this report does not decide its cause.",
            "Frequency is conditional on the supplied sample rate, which is not independently verified.",
            "No measured RF sensitivity, radiation, certification or interference attribution is claimed.",
        ],
    }


def read_recording(meta_path: Path) -> tuple[np.ndarray, dict, bool | None]:
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    g = meta["global"]
    if g.get("core:num_channels", 1) != 1 or g.get("core:offset", 0) != 0:
        raise ValueError("This demonstrator supports only one channel and zero offset")
    if g.get("core:metadata_only") or g.get("core:trailing_bytes", 0):
        raise ValueError("Metadata-only and trailing-byte datasets are unsupported")
    if "core:dataset" in g:
        raise ValueError("External dataset paths are unsupported; use a neighboring SigMF dataset")
    data_path = meta_path.with_name(meta_path.name.removesuffix(".sigmf-meta") + ".sigmf-data")
    raw = data_path.read_bytes()
    fmt = g["core:datatype"]
    if fmt == "cf32_le":
        if len(raw) % 8:
            raise ValueError("A cf32_le dataset must contain complete 8-byte complex samples")
        iq = np.frombuffer(raw, dtype="<c8")
    elif fmt == "cu8":
        if len(raw) % 2:
            raise ValueError("A cu8 dataset must contain complete I/Q byte pairs")
        a = (np.frombuffer(raw, dtype=np.uint8).astype(float) - 127.5) / 127.5
        iq = a[0::2] + 1j * a[1::2]
    else:
        raise ValueError("Only cf32_le and cu8 are supported")
    expected = g.get("core:sha512")
    integrity_ok = None if expected is None else hashlib.sha512(raw).hexdigest() == expected
    return iq, meta, integrity_ok


def write_synthetic(path: Path, iq: np.ndarray, fs: float, description: str) -> Path:
    raw = np.asarray(iq, dtype="<c8").tobytes()
    data_path = path.with_suffix(".sigmf-data")
    data_path.write_bytes(raw)
    meta_path = path.with_suffix(".sigmf-meta")
    meta = {
        "global": {
            "core:datatype": "cf32_le", "core:version": "1.2.6", "core:sample_rate": fs,
            "core:sha512": hashlib.sha512(raw).hexdigest(),
            "core:description": "SYNTHETIC, NOT A HARDWARE MEASUREMENT. " + description,
            "core:recorder": "signalbench synthetic demonstration 0.1",
        },
        "captures": [{"core:sample_start": 0}],
        "annotations": [{"core:sample_start": 0, "core:sample_count": len(iq), "core:label": "SYNTHETIC"}],
    }
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return meta_path


def demo(out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(20261106)
    fs, count, frequency = 1_024_000.0, 16384, 125_000.0
    t = np.arange(count) / fs
    tone = np.exp(2j * np.pi * frequency * t)
    noise = .005 / np.sqrt(2) * (rng.normal(size=count) + 1j * rng.normal(size=count))
    cases = {"clean": .2 * tone + noise,
             "attenuated_20db": (.2 * tone + noise) / 10,
             "dc_added": .2 * tone + noise + .15,
             "hard_clipped": np.clip((1.3 * tone + noise).real, -1, 1)
                             + 1j * np.clip((1.3 * tone + noise).imag, -1, 1)}
    results = {}
    for name, iq in cases.items():
        mp = write_synthetic(out / name, iq, fs, name)
        data, meta, ok = read_recording(mp)
        results[name] = {"source": "SYNTHETIC", "sha512_matches_metadata": ok,
                         **analyze(data, meta["global"]["core:sample_rate"])}
    results["wrong_sample_rate"] = {"source": "SYNTHETIC; metadata-error illustration",
                                     **analyze(cases["clean"], fs * 2)}
    summary = {
        "status": "SIMULATION ONLY; NO RECEIVER OR RF HARDWARE HAS BEEN VALIDATED",
        "expected_tone_hz": frequency,
        "measured_simulated_amplitude_change_db": (
            results["attenuated_20db"]["mean_sample_power_db_re_unit"]
            - results["clean"]["mean_sample_power_db_re_unit"]),
        "cases": results,
    }
    (out / "demo_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    d = sub.add_parser("demo")
    d.add_argument("--out", type=Path, default=Path("demo_output"))
    a = sub.add_parser("analyze")
    a.add_argument("metadata", type=Path)
    args = p.parse_args()
    if args.command == "demo":
        result = demo(args.out)
    else:
        iq, meta, integrity = read_recording(args.metadata)
        if integrity is False:
            raise SystemExit("INTEGRITY FAILURE: dataset does not match its declared SHA512")
        result = {"sha512_matches_metadata": integrity,
                  "recording_description": meta["global"].get("core:description", "unverified source"),
                  **analyze(iq, meta["global"]["core:sample_rate"])}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
