# SignalBench F2: regenerate the three figures

The CSV contains nine numerical measurements transcribed from the 2026-11-06 Windows processing output. Two charts can be generated from this table alone. The **measured** spectrum requires the privately retained raw I/Q data and SigMF metadata; the plotting code refuses to synthesize or guess a spectrum.

## Windows PowerShell (inside SignalBench folder)

```powershell
# Work on the F2 branch, with no uncommitted changes.
git fetch origin feat/f2-repeatable-gain-capture
git switch feat/f2-repeatable-gain-capture
git pull --ff-only

# Matplotlib is a plotting-only dependency; it is not needed for the analyzer.
& ".\.venv\Scripts\python.exe" -m pip install "matplotlib>=3.9,<4"

$DataDir = ".\resultados_locales\real_f2\f2_sweep_20261106T171015Z"
& ".\.venv\Scripts\python.exe" ".\tools\plot_f2_results.py" `
    --csv ".\evidence\f2_measurements_20261106.csv" `
    --data-dir $DataDir `
    --stem "f2_r02_g19p7" `
    --out ".\resultados_locales\f2_figures"
if ($LASTEXITCODE -ne 0) { throw "F2 plot generation failed" }

Get-ChildItem ".\resultados_locales\f2_figures\*.png"
```

Expected filenames:

- `F2_fig1_measured_spectrum.png`: **only** if SHA512-verified raw `cu8` samples and SigMF sidecar are present.
- `F2_fig2_power_by_gain.png`: nine reported digital powers, three gain settings, three repeats.
- `F2_fig3_dc_and_rails.png`: DC fractions and the digital unit-rail indicator.

The spectral figure uses a Hann-windowed FFT of 16,384 samples, averages non-overlapping windows, and reports relative PSD. It is a *different estimator* from the full-record FFT used by `signalbench.py analyze`. Frequency axes are offsets from **declared** 100 MHz, not a calibrated measurement of absolute frequency. Power is digital and is **not RF dBm**.

Do not add raw recordings, `resultados_locales/`, environment files, personal SSH configuration, or private data to GitHub. Review plots and captions before sharing them. For a submission, the technical report must remain labeled a **draft** until the measured spectrum is generated, reproducibility is checked, and all claims are reviewed.
