#!/usr/bin/env python3
"""SignalBench F2: capture a traceable 3x3 manual-gain sweep from an RTL-SDR.

Runs on the acquisition host (Debian / Orange Pi), not on Windows.
Only standard-library Python is needed; rtl_sdr must be installed.
Data are uncalibrated, are not automatically committed, and are never overwritten.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

CENTER_HZ = 100_000_000
SAMPLE_RATE_HZ = 1_024_000
SAMPLE_COUNT = 1_024_000
GAINS_DB = ("7.7", "19.7", "32.8")
LOSS_TOKENS = ("lost at least", "overrun", "overflow", "dropped")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def sha512_file(path: Path) -> str:
    digest = hashlib.sha512()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def loss_lines(log: str) -> list[str]:
    return [
        line.strip()
        for line in log.splitlines()
        if any(token in line.lower() for token in LOSS_TOKENS)
    ]


def sigmf_metadata(sha512: str, gain: str) -> dict:
    return {
        "global": {
            "core:version": "1.2.6",
            "core:datatype": "cu8",
            "core:sample_rate": SAMPLE_RATE_HZ,
            "core:sha512": sha512,
            "core:hw": "RTL-SDR Blog V4, R828D",
            "core:recorder": "rtl_sdr",
            "core:description": (
                "REAL SDR CAPTURE; uncalibrated; center 100 MHz; "
                f"manual gain {gain} dB. No verified absolute sample-start time."
            ),
        },
        "captures": [{"core:sample_start": 0, "core:frequency": CENTER_HZ}],
        "annotations": [],
    }


def save_json_new(path: Path, value: dict) -> None:
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def run_sweep(out: Path) -> None:
    if not shutil.which("rtl_sdr"):
        raise RuntimeError("rtl_sdr is not installed or not on PATH")

    # Never reuse an existing evidence directory.
    out.mkdir(parents=True, exist_ok=False)
    results: list[dict] = []
    manifest = out / "manifest.json"
    expected_bytes = SAMPLE_COUNT * 2  # cu8 = 1 byte I + 1 byte Q.

    try:
        for repeat in range(1, 4):
            for gain in GAINS_DB:
                stem = f"f2_r{repeat:02d}_g{gain.replace('.', 'p')}"
                data_path = out / (stem + ".sigmf-data")
                meta_path = out / (stem + ".sigmf-meta")
                log_path = out / (stem + ".capture.log")
                record_path = out / (stem + ".capture.json")

                args = [
                    "rtl_sdr", "-d", "0",
                    "-f", str(CENTER_HZ),
                    "-s", str(SAMPLE_RATE_HZ),
                    "-g", gain,
                    "-n", str(SAMPLE_COUNT),
                    str(data_path),
                ]
                start_utc = utc_now()
                print(f"CAPTURE_START {stem} gain={gain}dB", flush=True)
                # stderr contains receiver configuration and sample-loss diagnostics.
                with log_path.open("xb") as log_handle:
                    process = subprocess.run(
                        args, stdout=subprocess.DEVNULL, stderr=log_handle,
                        check=False, timeout=90,
                    )
                end_utc = utc_now()
                log = log_path.read_text(encoding="utf-8", errors="replace")
                bytes_written = data_path.stat().st_size if data_path.exists() else 0
                warnings = loss_lines(log)
                result = {
                    "stem": stem,
                    "source": "REAL_SDR_UNCALIBRATED",
                    "repeat": repeat,
                    "manual_gain_db": float(gain),
                    "center_hz_as_configured": CENTER_HZ,
                    "sample_rate_hz_as_configured": SAMPLE_RATE_HZ,
                    "sample_count_requested": SAMPLE_COUNT,
                    "sample_count_from_file": bytes_written // 2,
                    "sample_format": "cu8",
                    "bytes": bytes_written,
                    "expected_bytes": expected_bytes,
                    "command_start_utc_not_sample_start": start_utc,
                    "command_end_utc": end_utc,
                    "return_code": process.returncode,
                    "sample_loss_log_lines": warnings,
                    "data_filename": data_path.name,
                    "metadata_filename": meta_path.name,
                    "capture_log_filename": log_path.name,
                }
                ok = process.returncode == 0 and bytes_written == expected_bytes
                if ok:
                    result["sha512"] = sha512_file(data_path)
                    save_json_new(meta_path, sigmf_metadata(result["sha512"], gain))
                result["file_integrity_preconditions_passed"] = ok
                save_json_new(record_path, result)
                results.append(result)
                # Update manifest only after a capture record was safely persisted.
                manifest.write_text(
                    json.dumps({
                        "status": "IN_PROGRESS",
                        "purpose": "3 repeats x 3 interleaved manual gain settings",
                        "not_rf_calibrated": True,
                        "results": results,
                    }, indent=2) + "\n", encoding="utf-8"
                )
                if not ok:
                    raise RuntimeError(
                        f"{stem}: exit={process.returncode}, "
                        f"bytes={bytes_written} (expected {expected_bytes}); "
                        "raw evidence kept; stopping sweep"
                    )
                status = "CAPTURED_WITH_LOSS_WARNINGS" if warnings else "CAPTURED_NO_LOSS_WARNING_IN_LOG"
                print(f"{stem}: {status}; bytes={bytes_written}; SHA512={result['sha512'][:16]}...", flush=True)
    except Exception:
        print(f"SWEEP_INCOMPLETE: review evidence at {out}", flush=True)
        raise

    manifest.write_text(
        json.dumps({
            "status": "NINE_FILES_CAPTURED; NOT_CALIBRATED",
            "purpose": "3 repeats x 3 interleaved manual gain settings",
            "not_rf_calibrated": True,
            "results": results,
        }, indent=2) + "\n", encoding="utf-8"
    )
    print(f"F2_CAPTURE_COUNT={len(results)}", flush=True)
    print(f"MANIFEST={manifest}", flush=True)
    print("F2_SWEEP_FILE_CHECKS=PASS (not physical accuracy)", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out", type=Path,
        default=Path.home() / "signalbench_capturas" /
        ("f2_sweep_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")),
        help="New directory for nine capture sets; must not exist",
    )
    args = parser.parse_args()
    run_sweep(args.out.expanduser())


if __name__ == "__main__":
    main()
