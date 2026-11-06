# SignalBench F2 — uncalibrated SDR gain sweep (2026-11-06)

**Status:** Nine real RTL-SDR captures transferred to a Windows host, each checked against SHA512 metadata and manifest, and processed by the existing SignalBench analyzer. Figures, external replication, and RF calibration are not yet complete.

> These values were transcribed from the user's PowerShell terminal output for the 2026-11-06 experiment; repository maintainers have not uploaded or independently reprocessed the raw IQ data.

## Recorded setup

- RTL-SDR Blog V4, R828D tuner; Debian 12 single-board acquisition host; Windows analysis host
- Frequency center **100,000,000 Hz** as configured; sample rate **1,024,000 complex samples/s** as configured; `cu8`
- **1,024,000 complex samples / 2,048,000 bytes per capture**, nine captures; ~18.432 MB of raw data
- Manual gain settings: **7.7, 19.7, 32.8 dB**, each repeated three times, interleaved by repetition
- Raw data, SigMF metadata, command logs, and per-capture records retained off-repository
- Manifest: `f2_sweep_20261106T171015Z/manifest.json` on acquisition host, transferred to Windows under ignored `resultados_locales/real_f2/`
- Process outcome: `F2_CAPTURE_COUNT=9`, `F2_SWEEP_FILE_CHECKS=PASS`; local `F2_TRANSFER=PASS`, `F2_INTEGRITY=PASS`, all nine analyses completed
- No sample-loss warning recognized by the capture tool in the nine logs. **This does not prove gap-free sampling.**

## Per-capture numerical results

Digital power: decibels relative to **unit complex-sample mean-square power**, not dBm. DC and digital-rail columns are fractions of sample-domain quantities. Peak is **offset relative to the declared center frequency**, not independently calibrated absolute frequency.

| Capture | Gain (dB) | Power (dB re unit) | DC (%) | At unit rail (%) | Non-DC peak offset (Hz) | Hash |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| f2_r01_g7p7 | 7.7 | -45.0605 | 11.501 | 0.0 | +37604 | PASS |
| f2_r01_g19p7 | 19.7 | -40.6002 | 2.342 | 0.0 | +101296 | PASS |
| f2_r01_g32p8 | 32.8 | -27.8066 | 0.125 | 0.0 | +101295 | PASS |
| f2_r02_g7p7 | 7.7 | -45.0618 | 11.554 | 0.0 | +101294 | PASS |
| f2_r02_g19p7 | 19.7 | -40.3943 | 2.230 | 0.0 | +101293 | PASS |
| f2_r02_g32p8 | 32.8 | -29.3017 | 0.172 | 0.0 | +40227 | PASS |
| f2_r03_g7p7 | 7.7 | -45.0619 | 11.507 | 0.0 | +101292 | PASS |
| f2_r03_g19p7 | 19.7 | -40.6534 | 2.374 | 0.0 | +101292 | PASS |
| f2_r03_g32p8 | 32.8 | -29.3376 | 0.174 | 0.0 | +101292 | PASS |

## Summary by gain (averages and within-gain range computed from rounded measurements)

| Gain setting | N | Mean power (dB re unit) | Range (dB) |
| --- | ---: | ---: | ---: |
| 7.7 dB | 3 | -45.0614 | 0.0014 |
| 19.7 dB | 3 | -40.5493 | 0.2591 |
| 32.8 dB | 3 | -28.8153 | 1.5310 |

Changing configured gain 7.7 -> 19.7 dB corresponds to ~**+4.512 dB** change in mean *digital* power; 19.7 -> 32.8 dB corresponds to ~**+11.734 dB**. These differences **must not** be used to infer calibrated RF gain linearity: the input was received through an antenna and was not independently controlled.

## Interpretation and limitations

1. The 7.7 dB group has very small power variation, while the 32.8 dB group varies by ~1.531 dB. The cause is **undetermined** (e.g. incoming signal variation, receiver behavior, environmental factors).
2. The largest non-DC spectral peak switches across captures between offsets near +37.6 kHz, +40.2 kHz and +101.29 kHz. This may reflect competing signals or temporal changes; inspect full spectra before identifying emitters.
3. DC power fraction decreases with higher configured gain in these captures; no attribution to a specific cause.
4. All captures report 0% components at unit digital rails, which **does not exclude analog compression**.
5. FFT bin spacing (1 Hz for a nominal one-second capture) is not absolute frequency accuracy. The data are **not calibrated in dBm**, and this is not an independent external replication.
6. A PSReadLine console-rendering exception occurred during typing, but the subsequent PowerShell operations completed, producing all nine analysis JSON files and a CSV. It was a terminal UI issue, not an observed SignalBench failure.
7. The nine calculated SHA512 values were checked against SigMF and manifest fields locally. The raw dataset has **not** been made available in this repository for independent verification.

## Evidence and next tasks

- Preserve locally: complete sweep folder, manifest, nine raw files, nine SigMF sidecars, capture logs, analysis JSONs, and `analysis/f2_results.csv`. Do not overwrite or automatically publish them.
- Next: inspect at least representative full spectra; plot power by gain (individual repeats), DC and rail diagnostics; provide source-labeled figures.
- Draft a two-page technical report distinguishing simulated numerical tests, one F1 SDR capture, and this F2 nine-capture sweep.
- Retain this PR as draft until code review and confirmation that all data, values and privacy choices are correct.
