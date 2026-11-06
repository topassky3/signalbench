# SignalBench — reproducible, limitation-aware SDR analysis

**Status (2026-11-06): working open-source prototype with synthetic numerical controls and user-reported physical RTL-SDR acquisition results. Not an RF-calibrated instrument.** This repository is currently private while the proposal and privacy review are completed.

SignalBench helps hardware hackers and STEM learners inspect low-cost software-defined radio I/Q recordings without confusing sample-domain measurements with physical RF calibration. It focuses on explicit assumptions, integrity checks and reproducible diagnostics.

## What works

- Generate controlled synthetic I/Q examples and SigMF metadata.
- Analyze a focused subset of SigMF data: `cf32_le` and interleaved `cu8`, single channel with zero offset, adjacent data.
- Verify SHA-512 against the SigMF `core:sha512` value; reject changed data bytes.
- Report sample-domain mean power (linear and dB relative to unit complex-sample power), DC contribution, at-unit-rail indicators and FFT peak offsets.
- Execute an RTL-SDR capture sweep using `tools/capture_gain_sweep.py` on Debian/Linux with `rtl_sdr`, producing nine real IQ files, SigMF sidecars, per-capture logs and a manifest.
- Create gain/DC graphs and one *measured spectrum* from SHA-512-verified local raw IQ with `tools/plot_f2_results.py`.

## Evidence collected (2026-11-06)

- **Synthetic:** six numerical/integrity tests and four hardware-free capture-tool tests passed on the Windows development environment (**10/10**). Hardware-free F2 test outputs are **not** real RF measurements.
- **Physical F1:** one second of uncalibrated RTL-SDR Blog V4 recording at declared 100 MHz center, 1.024 MS/s, gain 19.7 dB. 2,048,000 bytes were copied and their SHA-512 matched the sidecar; processed successfully. See `evidence/F1_REAL_CAPTURE_20261106.md` on the separate documentation PR until it merges.
- **Physical F2:** nine one-second recordings using configured gains 7.7, 19.7 and 32.8 dB, three replicates each, at declared 100 MHz center and 1.024 MS/s. Each 2,048,000-byte recording passed local SHA-512 checks against metadata and manifest, and SignalBench processed all nine. See `evidence/F2_GAIN_SWEEP_20261106.md` and the CSV.
- **Figures:** power by gain, DC/rail diagnostics and one full baseband spectrum generated locally after the plotting script reported SHA-512 verification. The original capture data and figure files are retained locally and are **not** bundled with the repository.

**Not established:** absolute RF frequency/power accuracy, dBm calibration, analog compression status, guaranteed gap-free sample transport, transmitter identity or third-party replication. A digital FFT-bin width is not an instrument accuracy claim.

## Quick start (Python 3.10+)

```bash
python -m pip install numpy
python -m unittest -v
python signalbench.py demo --out demo_output
python signalbench.py analyze demo_output/clean.sigmf-meta
```

The demo outputs are **synthetic**, even if they use SigMF file extensions.

## F2 acquisition (only on a Linux host with an RTL-SDR receiver)

```bash
python3 tools/capture_gain_sweep.py --out "$HOME/signalbench_capturas/my_new_f2_run"
```

The output folder must not already exist; data are not overwritten. Review the `rtl_sdr` requirements, configured gain values and possible reception/sample-loss limitations before capturing. The tool produces real I/Q files only when actual supported hardware is connected; it does not claim calibration.

## Recreate figures from the F2 data table

```bash
python -m pip install numpy 'matplotlib>=3.9,<4'
python tools/plot_f2_results.py \
  --csv evidence/f2_measurements_20261106.csv \
  --out resultados_locales/f2_figures
```

This command produces **two plots only** from reported summary data. To obtain the measured baseband spectrum, supply the original local capture directory and the matching SigMF sidecar:

```bash
python tools/plot_f2_results.py \
  --csv evidence/f2_measurements_20261106.csv \
  --data-dir /path/to/private/f2_sweep_20261106T171015Z \
  --stem f2_r02_g19p7 \
  --out resultados_locales/f2_figures
```

The spectrum is not generated if the real data cannot be found, and a mismatched SHA-512 raises an error. See `docs/F2_FIGURES_REPRODUCTION.md` for Windows PowerShell steps.

## Scientific and privacy boundaries

SigMF import is intentionally limited; no full standard compatibility is claimed. No sample-domain power value is RF dBm. A hash match verifies correspondence to a recorded digest, **not** physical provenance or data integrity at the SDR sampling instant. Receiver gain settings are not independent calibrations. Do not identify transmitters from spectral features without corroboration.

Raw `*.sigmf-data`, `*.sigmf-meta` files and `resultados_locales/` are ignored by Git. Do not release raw captures, logs or personal/private data without checking the permissions, signals involved, retention, and applicable law. Future replication releases will use controlled, shareable bench signals.

**Funding application:** Hacker Initiative 2026; a grant request is not an award. Working drafts are in `docs/HACKER_INITIATIVE_2026_APPLICATION_DRAFT.md`.

## License / references

MIT. Related standards and tools: [SigMF](https://sigmf.org/) and [GNU Radio](https://www.gnuradio.org/about/).

---

### Español — resumen

SignalBench es un prototipo abierto para analizar capturas I/Q y verificar integridad SHA-512, con pruebas sintéticas y adquisiciones físicas no calibradas. Se han comunicado **10 pruebas de software superadas y 10 capturas reales (1 F1 + 9 F2)**. Los valores de potencia digital **no son dBm**, los picos espectrales no identifican emisoras y todavía no existe una calibración RF ni reproducción independiente. Los archivos IQ originales permanecen privados.
