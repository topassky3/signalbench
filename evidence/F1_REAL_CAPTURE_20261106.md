# F1: First physical SDR capture — 2026-11-06

**Status:** Observed acquisition, transfer, integrity check, and SignalBench analysis. **This is not a calibrated RF measurement or an independent replication.**

## Setup and acquisition

| Field | Recorded value |
| --- | --- |
| Receiver | RTL-SDR Blog V4; R828D tuner |
| Host | Debian 12, ARM64 single-board computer |
| Capture tool | `rtl_sdr` |
| Declared center frequency | 100,000,000 Hz |
| Declared sample rate | 1,024,000 complex samples/s |
| Configured manual gain | 19.7 dB |
| Sample encoding | Interleaved unsigned 8-bit I/Q (`cu8`) |
| Requested sample count | 1,024,000 |
| Dataset size | 2,048,000 bytes |
| Timestamp in filename / metadata | 2026-11-06T16:45:34Z (command-side timestamp, **not** calibrated sample-start time) |
| Data filename | `f1_100mhz_g19p7_20261106T164534Z.sigmf-data` |

The `rtl_sdr` process reported `CAPTURE_EXIT_CODE=0` and produced the expected byte count. Its acquisition log did not display an explicit sample-loss warning, but it ended with `User cancel, exiting...`; these observations do **not** independently prove gap-free sampling. An earlier, separate `rtl_test -s 1024000` run reported `lost at least 100 bytes`, followed by a rounded minimum-loss-per-million count of zero. That diagnostic result must not be described as an error-free stress test.

## Integrity and transfer

The original raw dataset was retained on the acquisition host. A SigMF metadata sidecar was generated without modifying those bytes. The dataset, sidecar, and original acquisition log were copied to a Windows workstation, where SHA-512 was independently recomputed and compared with `core:sha512` in the sidecar.

- Transferred dataset size: **2,048,000 bytes**
- SHA-512: `68f7dca276f95b09894d8f27b1b7cbbd66d0a531b17fe08530f028f896ceb194d74654f83f6f39b7bd89bf54d46875e4dd6abc30776ee9e912d7919d3ed5e0b2`
- Transfer integrity: **PASS**
- SigMF reader integrity field: `sha512_matches_metadata = true`
- Source data are **not committed** to this repository; see `.gitignore`.

SHA-512 equality establishes correspondence between the transferred bytes and the recorded digest, not their absolute physical provenance or measurement accuracy.

## SignalBench v0.1 analysis

Values below were transcribed from the local `signalbench.py analyze` output for the named dataset.

| Metric | Result |
| --- | ---: |
| `sample_count` | 1,024,000 |
| `sample_rate_hz_as_supplied` | 1,024,000 |
| `fft_bin_hz` | 1.0 |
| `mean_sample_power` | 9.501633986928107e-05 |
| `mean_sample_power_db_re_unit` | -40.22201703081094 dB |
| `dc_sample_power` | 2.058028358949326e-06 |
| `dc_power_fraction` | 0.021659730966070285 (2.166%) |
| `component_rail_fraction_at_unit_limit` | 0.0 |
| `largest_non_dc_peak_offset_hz` | +40,270 Hz |
| `psd_integral_window_weighted_sample_power` | 9.338291755363955e-05 |
| Local analysis process | Exit status 0; report saved as `f1_analysis.json` |

The **+40,270 Hz** spectral peak is an offset relative to the *declared* 100 MHz center (nominal 100.040270 MHz); it does not establish an identified transmitter or absolute frequency accuracy. The **1 Hz bin spacing** is not a statement of frequency accuracy. The **-40.22 dB** value is referenced to unit complex-sample mean-square power, **not dBm**. The DC fraction is descriptive, not an attribution of cause. No samples at the digital rails does not rule out analog compression.

## Local reproduction (Windows PowerShell)

After securely copying the original data and sidecar into `resultados_locales/real_f1/`:

```powershell
$Stem = "f1_100mhz_g19p7_20261106T164534Z"
$Dir = ".\resultados_locales\real_f1"
$Data = Join-Path $Dir "$Stem.sigmf-data"
$Meta = Join-Path $Dir "$Stem.sigmf-meta"
$Expected = (Get-Content $Meta -Raw | ConvertFrom-Json).global.'core:sha512'
$Actual = (Get-FileHash $Data -Algorithm SHA512).Hash
if ($Expected -ine $Actual) { throw "SHA512 mismatch" }
& .\.venv\Scripts\python.exe .\signalbench.py analyze $Meta
```

The private raw file, sidecar, acquisition log and `f1_analysis.json` should remain together for traceability. Do not publish those files without a separate sharing and privacy review.

## Limitations and next experiment

1. This is **one real, uncalibrated acquisition**, with no known RF reference, and no independent reference instrument.
2. The exact time of the first acquired sample and independent receiver-frequency accuracy have not been established.
3. The source data have not been externally distributed; a reviewer cannot independently recompute the numeric results from this repository alone.
4. Next: take **three repeated captures at each of three supported manual gain values** with the antenna, frequency and declared sample rate held fixed. Record per-capture metadata, byte count, SHA-512, acquisition logs and processing metrics; analyze repeatability without claiming gain calibration.

This file records the observed F1 milestone for a funding application; it does not claim receiver calibration, physical sensitivity, or independent verification.
