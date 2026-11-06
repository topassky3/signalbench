# SignalBench — verification log for the 2026 Hacker Initiative application

**Date:** 2026-11-06. **Status:** working prototype and preliminary uncalibrated SDR observations; application **not submitted**.

## Software validation

- On Windows PowerShell after synchronizing **`main`** at commit **`313c61a27018f3a8e9e0da49ac90315b94cbb736`**:
  - `python -m unittest -v` returned **10 tests, OK, 0.308 s**.
  - Tests consist of **six numeric/SigMF/integrity checks** and **four hardware-free gain-sweep control tests**.
  - `git status --short --branch` reported `main...origin/main` without local modifications.
- Synthetic demonstrator: known tone at nominal +125,000 Hz; factor-0.1 amplitude corresponds to -20 dB sample-domain power difference; deliberate sample-rate metadata change shifts the inferred peak to +250,000 Hz. Synthetic scenarios do not establish hardware calibration.
- The hardware-free F2 capture test prints nine **512-byte mocked captures** and deliberately prints `SWEEP_INCOMPLETE` in a negative test. Neither output is evidence of a failed physical acquisition nor a real RF recording.

## Physical data collection

- **F1:** one original physical RTL-SDR recording at configured center 100 MHz, configured gain 19.7 dB, declared 1.024 MS/s, `cu8`, 1,024,000 complex samples. It was copied to Windows and verified via SHA512 against SigMF metadata. See `evidence/F1_REAL_CAPTURE_20261106.md`.
- **F2:** nine original physical RTL-SDR recordings, interleaving gains 7.7, 19.7 and 32.8 dB across three repeats. Each data file was 2,048,000 bytes. Local transfer and SHA512 checks against SigMF and manifest were reported **PASS** for all nine. SignalBench analyzed all nine. See `evidence/F2_GAIN_SWEEP_20261106.md`.
- **F2 plots:** two aggregate figures (power/gain and DC/rails) and a measured spectrum from locally retained raw I/Q. Plotting tool reported `MEASURED_SPECTRUM=GENERATED (SHA512 verified)` for `f2_r02_g19p7`. The chart screenshot was reviewed. Its original raw data and original plot PNG stay local; `evidence/F2_SPECTRUM_VISUAL_REVIEW_20261106.md` documents what is and is not observed.

## Interpretation boundaries

These are **uncalibrated, user-reported physical captures plus validated processing outputs**, not laboratory RF calibration or independently replicated scientific results. Digital power does **not** equal dBm; FFT bin spacing does **not** establish frequency accuracy; spectral peaks do **not** identify transmitters. Hash comparisons establish integrity relative to metadata, not independent physical provenance. Absence of sample-loss warnings does not guarantee a gap-free receiver acquisition.

## Grant status

- Program: **Hacker Initiative 2026 — Signal/Noise**.
- Amount sought: **USD 5,000**, provisional hardware/test/evidence budget; **not awarded**.
- Official online application deadline: **Monday, November 9, 2026 at 11:59 p.m. PST** (Tuesday, November 10, 2026 at 02:59 in Colombia).
- The application requires English answers in the online form. A private repository or separate PDF report is **not required** to submit; additional materials can be requested later.
- English technical answers: `docs/HACKER_INITIATIVE_2026_APPLICATION_DRAFT.md`. Final personal identity/contact, funding-from-other-sources disclosures, legal commitments and financial receipt arrangements **must be confirmed by the applicant privately**.
- No application has been submitted from this repository or by this document.

Official references:
- https://hackerinitiative.org/
- https://hackerinitiative.org/apply-now/
- https://hackerinitiative.org/application-faq/
