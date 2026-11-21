# yuvaintern-week2-circuit-simulation

## Circuit Overview
- **Topology:** 2nd-Order Unity-Gain Sallen-Key Active Low-Pass Filter (Butterworth Alignment)
- **Design Cutoff Frequency ($f_c$):** `1.00 kHz` (`-3.01 dB`)
- **Quality Factor ($Q$) / Damping ($\zeta$):** `0.7071` / `0.7071` (maximally flat passband)
- **Stopband Roll-Off:** `-40 dB/decade` (`-12 dB/octave`)
- **Component Values:** $R_1 = R_2 = 11.25	ext{ k}\Omega$, $C_1 = 20	ext{ nF}$, $C_2 = 10	ext{ nF}$, $R_L = 10	ext{ k}\Omega$, bipolar supply $\pm 15	ext{ V}$

## Repository Contents
- `spice/sallen_key_lpf_1khz.cir` — Ready-to-run SPICE netlist for LTspice (`10 Hz – 100 kHz` AC sweep, transient analysis, and `.step` sweep)
- `scripts/simulate_and_plot.py` — Reproducible Python script for transfer-function analysis, Bode plotting, and 100-run Monte Carlo tolerance evaluation
- `figures/` — Circuit schematic and simulation plots (`fig1` through `fig5`)
- `report/YuvaIntern_Week2_Circuit_Simulation_Analysis_Report-v2.docx` — Complete formatted Word report for portal upload

## How to Run the Simulation
1. **LTspice:** Open `spice/sallen_key_lpf_1khz.cir` in LTspice and run the AC sweep (`10 Hz` to `100 kHz`) or uncomment `.tran` / `.step param C2`.
2. **Python:** Run `python scripts/simulate_and_plot.py` to reproduce numerical metrics and Bode plots.
