# F2 measured-spectrum visual review and grant evidence status — 2026-11-06

## Status

- User-reported Windows execution of `tools/plot_f2_results.py` completed successfully with `MEASURED_SPECTRUM=GENERATED (SHA512 verified)`, `POWER_FIGURE=GENERATED` and `DC_RAIL_FIGURE=GENERATED`.
- The measured spectrum was generated from the original local `f2_r02_g19p7.sigmf-data` and matching SigMF sidecar, rather than from synthetic test cases. The code checks SHA512 before interpreting raw `cu8` samples.
- A screenshot of that chart was visually reviewed: narrow features across the baseband and a wider elevated region centered roughly at -300 kHz. A notable feature near +101 kHz is consistent with SignalBench's reported strongest-peak offset (~+101,293 Hz) for this specific capture.
- The screenshot is **not** an independently exported raw plot or a separate re-analysis of the IQ data. Original PNG, raw samples and logs stay on the developer's local Windows machine.
- Digital relative PSD is **not** RF dBm. Spectral peaks are not transmitter identities, FFT bin spacing is not RF frequency accuracy, and no physical calibration has been performed.

## Evidence chain

1. F1: one physical RTL-SDR recording at nominal center 100 MHz / 1.024 MS/s; data integrity checked on transfer and analyzer output saved locally.
2. F2: nine physical captures at manual gains 7.7, 19.7, 32.8 dB in three repetitions; all nine full-length sample files checked via SHA512 against both metadata and the sweep manifest.
3. Six SignalBench analysis controls and four hardware-free gain-sweep controls passed (10/10) on Windows; the updated plotting script was executed successfully on Windows.
4. CSV and two aggregate figures are reproducible from this repository; the third figure requires the private original IQ and matching sidecar.
5. A two-page grant-support technical report was prepared externally, including a crop of the actual user-supplied spectrum screenshot. It is an **evidence summary**, not independent external validation or instrument certification.

## Open gates before grant submission

- Rerun `python -m unittest -v` after pulling the latest branch and capture the 10/10 output.
- Review repository and privacy before making code/documentation accessible to external assessors. Do **not** commit raw antenna data automatically.
- Confirm the applicant's full legal and contact details, tax/payment readiness for an international check, any other expected project-specific funding, and voluntary compliance with the application requirements.
- The proposed USD 5,000 budget is a **planning allocation**, not a supplier-verified quote. Genuine compatible receivers should be considered because the RTL-SDR Blog V4 is end-of-line.
- Submit through the official Google form. The current project is **NOT SUBMITTED**.

Form and official deadline: https://docs.google.com/forms/d/e/1FAIpQLSc_6C9WO9PEXS3r1BN_Qq5LOL9xtoEux0pC6xTmxUlpxlanxg/viewform — Monday, Nov 9, 2026, 11:59 p.m. PST.
