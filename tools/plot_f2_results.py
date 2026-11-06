#!/usr/bin/env python3
"""SignalBench F2: render descriptive plots from CSV and a verified real I/Q spectrum.

Do not substitute synthetic data for a measured spectrum. Input raw files are
opened read-only, and original recordings are never modified.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

FIELDS = ("Captura", "Repeticion", "Ganancia_dB", "Potencia_dB",
          "DC_pct", "Limite_pct", "Pico_Hz", "Integridad")


def number(s: str) -> float:
    """Accept Spanish or English decimal separators in exported CSV values."""
    return float(str(s).strip().replace(",", "."))


def load_rows(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not set(FIELDS).issubset(reader.fieldnames or []):
            raise ValueError("Missing required F2 columns")
        rows = []
        for r in reader:
            if r["Integridad"].strip() != "PASS":
                raise ValueError("Integrity check not PASS for " + r["Captura"])
            rows.append({
                "stem": r["Captura"], "repeat": int(r["Repeticion"]),
                "gain": number(r["Ganancia_dB"]),
                "power": number(r["Potencia_dB"]),
                "dc": number(r["DC_pct"]),
                "rail": number(r["Limite_pct"]),
                "peak": number(r["Pico_Hz"]),
            })
    expected = {(repeat, gain) for repeat in (1, 2, 3)
                for gain in (7.7, 19.7, 32.8)}
    found = {(r["repeat"], r["gain"]) for r in rows}
    if len(rows) != 9 or found != expected or len(found) != 9:
        raise ValueError("Expected exactly 3 repetitions at each of 3 gains")
    return rows


def series(rows: list[dict], repetition: int) -> list[dict]:
    return sorted((r for r in rows if r["repeat"] == repetition),
                  key=lambda r: r["gain"])


def plot_power(rows: list[dict], out: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.3, 4.2), layout="constrained")
    for rep in (1, 2, 3):
        rr = series(rows, rep)
        ax.plot([x["gain"] for x in rr], [x["power"] for x in rr],
                "o-", label=f"Repeat {rep}")
    gains = (7.7, 19.7, 32.8)
    means = [np.mean([r["power"] for r in rows if r["gain"] == g])
             for g in gains]
    ax.plot(gains, means, "ks--", lw=1.5, ms=5, label="Mean (dB)")
    ax.set(title="F2 | Observed digital power vs configured gain",
           xlabel="Configured manual gain (dB)",
           ylabel="Digital power (dB re unit complex sample power)")
    ax.set_xticks(gains)
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
    fig.savefig(out / "F2_fig2_power_by_gain.png", dpi=180)
    plt.close(fig)


def plot_dc_rails(rows: list[dict], out: Path) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(7.3, 5.0),
                             sharex=True, layout="constrained")
    for rep in (1, 2, 3):
        rr = series(rows, rep)
        axes[0].plot([x["gain"] for x in rr], [x["dc"] for x in rr],
                     "o-", label=f"Repeat {rep}")
    axes[0].set_title("F2 | DC fraction and unit-rail indicator")
    axes[0].set_ylabel("DC fraction of digital power (%)")
    axes[0].grid(alpha=0.25)
    axes[0].legend(fontsize=8)
    axes[1].scatter([r["gain"] for r in rows],
                    [r["rail"] for r in rows])
    axes[1].set_ylim(-0.01, 0.12)
    axes[1].text(0.02, 0.78, "All nine observed rail fractions = 0%",
                 transform=axes[1].transAxes, fontsize=9)
    axes[1].set(xlabel="Configured manual gain (dB)",
                ylabel="Components at unit rails (%)")
    axes[1].set_xticks((7.7, 19.7, 32.8))
    axes[1].grid(alpha=0.25)
    fig.savefig(out / "F2_fig3_dc_and_rails.png", dpi=180)
    plt.close(fig)


def plot_measured_spectrum(data_dir: Path, stem: str, out: Path) -> bool:
    path = data_dir / (stem + ".sigmf-data")
    meta_path = data_dir / (stem + ".sigmf-meta")
    if not path.is_file() or not meta_path.is_file():
        return False
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    gl = meta["global"]
    if gl.get("core:datatype") != "cu8":
        raise ValueError("Spectrum plot expects cu8; refusing to guess format")
    raw = path.read_bytes()
    sha512 = hashlib.sha512(raw).hexdigest()
    expected = gl.get("core:sha512")
    if not expected or sha512.lower() != str(expected).lower():
        raise ValueError("SHA512 mismatch: cannot plot unverified raw data")
    if len(raw) % 2 or len(raw) < 32768:
        raise ValueError("Invalid length for cu8 I/Q")
    fs = float(gl["core:sample_rate"])
    b = np.frombuffer(raw, dtype=np.uint8).astype(np.float64)
    iq = ((b[::2] - 127.5) + 1j * (b[1::2] - 127.5)) / 127.5
    nfft = 16384
    windows = iq[:len(iq) // nfft * nfft].reshape(-1, nfft)
    win = np.hanning(nfft)
    spec = np.fft.fft(windows * win[None, :], axis=1)
    psd = (np.abs(spec)**2 / (fs * np.sum(win**2))).mean(axis=0)
    hz = np.fft.fftshift(np.fft.fftfreq(nfft, d=1/fs)) / 1000
    power = 10 * np.log10(np.maximum(np.fft.fftshift(psd), 1e-30))
    fig, ax = plt.subplots(figsize=(7.3, 4.2), layout="constrained")
    ax.plot(hz, power, lw=0.7)
    ax.set(title=f"F2 | Measured spectrum ({stem})",
           xlabel="Offset from declared 100 MHz center (kHz)",
           ylabel="Relative PSD (dB/unit sample power/Hz)")
    ax.grid(alpha=0.25)
    ax.text(0.01, 0.02, "Hann / averaged FFT; uncalibrated; not RF dBm",
            transform=ax.transAxes, fontsize=8)
    fig.savefig(out / "F2_fig1_measured_spectrum.png", dpi=180)
    plt.close(fig)
    return True


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--csv", type=Path,
                    default=Path("evidence/f2_measurements_20261106.csv"))
    ap.add_argument("--data-dir", type=Path,
                    help="Private F2 sweep directory with original raw IQ and SigMF sidecars")
    ap.add_argument("--stem", default="f2_r02_g19p7")
    ap.add_argument("--out", type=Path,
                    default=Path("resultados_locales/f2_figures"))
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    rows = load_rows(args.csv)
    plot_power(rows, args.out)
    plot_dc_rails(rows, args.out)
    if args.data_dir and plot_measured_spectrum(args.data_dir, args.stem, args.out):
        print("MEASURED_SPECTRUM=GENERATED (SHA512 verified)")
    else:
        print("MEASURED_SPECTRUM=SKIPPED (original raw I/Q not supplied)")
    print("POWER_FIGURE=GENERATED")
    print("DC_RAIL_FIGURE=GENERATED")
    print("FIGURE_DIR=" + str(args.out.resolve()))


if __name__ == "__main__":
    main()
