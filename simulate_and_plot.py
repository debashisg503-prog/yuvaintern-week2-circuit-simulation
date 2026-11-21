import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

R1 = 11.25e3
R2 = 11.25e3
C1 = 20.0e-9
C2 = 10.0e-9

def transfer_function(freq_hz, r1=R1, r2=R2, c1=C1, c2=C2, av=1.0):
    s = 1j * 2.0 * np.pi * freq_hz
    # General Sallen-Key transfer function with gain av:
    # H(s) = av / (1 + s*(c2*(r1+r2) + c1*r1*(1-av)) + s^2*r1*r2*c1*c2)
    denom = 1.0 + s * (c2 * (r1 + r2) + c1 * r1 * (1.0 - av)) + (s ** 2) * r1 * r2 * c1 * c2
    return av / denom

def run_ac_analysis(out_dir="figures"):
    os.makedirs(out_dir, exist_ok=True)
    f = np.logspace(1, 5, 1000)
    H = transfer_function(f)
    mag_db = 20.0 * np.log10(np.abs(H))
    phase_deg = np.angle(H, deg=True)

    fc_sim = f[np.argmin(np.abs(mag_db - (-3.01)))]
    print(f"Nominal Cutoff Frequency (-3.01 dB): {fc_sim:.2f} Hz")
    print(f"Gain at 100 Hz: {mag_db[np.argmin(np.abs(f - 100))]:.4f} dB")
    print(f"Gain at 10 kHz: {mag_db[np.argmin(np.abs(f - 10000))]:.2f} dB")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9.5, 6.2), dpi=300, sharex=True)
    fig.patch.set_facecolor('#FFFFFF')
    ax1.semilogx(f, mag_db, color='#1B365D', lw=2.2, label='Simulated |H(jω)| (Butterworth Q = 0.707)')
    ax1.axhline(-3.01, color='#C0392B', linestyle='--', lw=1.2, label='−3.01 dB Cutoff Threshold')
    ax1.axvline(1000, color='#2E7D32', linestyle=':', lw=1.4, label='Cutoff Frequency f_c = 1.00 kHz')
    ax1.set_ylabel('Magnitude |Vout/Vin| (dB)', fontsize=10, fontweight='bold', color='#1B365D')
    ax1.set_title('AC Small-Signal Frequency Response — Sallen-Key Low-Pass Filter', fontsize=11.5, fontweight='bold', color='#1B365D')
    ax1.set_ylim(-85, 8)
    ax1.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
    ax1.legend(loc='lower left', fontsize=8.5)

    ax2.semilogx(f, phase_deg, color='#00695C', lw=2.2, label='Phase ∠H(jω) (Degrees)')
    ax2.axhline(-90, color='#C0392B', linestyle='--', lw=1.2, label='−90.0° Phase Shift at f_c')
    ax2.axvline(1000, color='#2E7D32', linestyle=':', lw=1.4)
    ax2.set_ylabel('Phase Shift (Degrees)', fontsize=10, fontweight='bold', color='#00695C')
    ax2.set_xlabel('Frequency (Hz) — Logarithmic Sweep (10 Hz to 100 kHz)', fontsize=10, fontweight='bold')
    ax2.set_ylim(-190, 10)
    ax2.set_yticks([0, -45, -90, -135, -180])
    ax2.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
    ax2.legend(loc='lower left', fontsize=8.5)

    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "fig2_ac_bode_response.png"), dpi=300, bbox_inches='tight')
    plt.close()

def run_monte_carlo(runs=100, out_dir="figures"):
    os.makedirs(out_dir, exist_ok=True)
    np.random.seed(42)
    f = np.logspace(2, 4, 400)
    fcs = []
    for _ in range(runs):
        r1 = R1 * np.random.uniform(0.95, 1.05)
        r2 = R2 * np.random.uniform(0.95, 1.05)
        c1 = C1 * np.random.uniform(0.90, 1.10)
        c2 = C2 * np.random.uniform(0.90, 1.10)
        mdb = 20.0 * np.log10(np.abs(transfer_function(f, r1, r2, c1, c2, av=1.0)))
        fcs.append(f[np.argmin(np.abs(mdb - (-3.01)))])
    fcs = np.array(fcs)
    print(f"Monte Carlo ({runs} runs) — Mean fc: {np.mean(fcs):.1f} Hz, Std Dev: {np.std(fcs):.1f} Hz")
    return fcs

if __name__ == "__main__":
    run_ac_analysis()
    run_monte_carlo()
