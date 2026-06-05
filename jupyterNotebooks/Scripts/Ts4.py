# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 11:13:25 2026

@author: valen
"""

import numpy as np
import matplotlib.pyplot as plt

# ─── Componentes normalizados ───────────────────────────────────────────────
R1, R2, R3 = 1, 1, 1
C1 = 0.2847
C2 = 0.5438
C3 = 0.4307

G1, G2, G3 = 1/R1, 1/R2, 1/R3

# ─── Coeficientes exactos de tu T(s) ────────────────────────────────────────
p1    = 1 / (C3 * R3)          # polo RC
w0_sq = (G1 * G2) / (C1 * C2)  # w0^2 Sallen-Key
coef_s = (G1 + G2) / C2        # coef de s

# Numerador: (1/C3) * (G1G2/C1C2)
NUM_circ = [(1/C3) * w0_sq]

# Denominador: (s + 1/C3R3)(s^2 + coef_s*s + w0_sq)
DEN_circ = [1,
            p1 + coef_s,
            p1 * coef_s + w0_sq,
            p1 * w0_sq]


# ─── Respuesta en frecuencia ────────────────────────────────────────────────
N = 2000
ws = np.logspace(np.log10(0.01), np.log10(10), N)

def freq_resp(w, num, den):
    s = 1j * w
    return np.polyval(num, s) / np.polyval(den, s)

H_circ = np.array([freq_resp(w, NUM_circ, DEN_circ) for w in ws])

mag_circ = 20 * np.log10(np.abs(H_circ))


gd_circ = -np.gradient(np.unwrap(np.angle(H_circ)), ws)

# ─── Valores clave ──────────────────────────────────────────────────────────
D0_c  = np.interp(0.001, ws, gd_circ)
D25_c = np.interp(2.5,   ws, gd_circ)


print(f"\n  Circuito → D(0)={D0_c:.4f}s  D(2.5)={D25_c:.4f}s  Error={abs(D25_c-D0_c)/D0_c*100:.2f}%")

# ─── Graficas ───────────────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 7), sharex=True)


ax1.semilogx(ws, mag_circ, color='#993C1D', linewidth=1.5, label='Circuito')
ax1.axvline(x=1,   color='green',  linestyle='--', linewidth=1, label='ωp=1')
ax1.axvline(x=2.5, color='orange', linestyle='--', linewidth=1, label='ωs=2.5')
ax1.axhline(y=-1,  color='gray',   linestyle=':',  linewidth=1, label='αmax=1dB')
ax1.set_ylabel('Magnitud [dB]')
ax1.set_title('Bessel N=3 - Circuito')
ax1.legend(fontsize=9)
ax1.grid(True, which='both', alpha=0.3)


ax2.semilogx(ws, gd_circ, color='#993C1D', linewidth=1.5, label=f'Circuito   D(0)={D0_c:.4f}s')
ax2.axvline(x=1,   color='green',  linestyle='--', linewidth=1)
ax2.axvline(x=2.5, color='orange', linestyle='--', linewidth=1)
ax2.scatter([2.5], [D25_c], color='#993C1D', zorder=5, s=60, label=f'D(2.5) Circuito={D25_c:.4f}s')
ax2.set_ylabel('Retardo de grupo [s]')
ax2.set_xlabel('ω [rad/s]')
ax2.legend(fontsize=9)
ax2.grid(True, which='both', alpha=0.3)

plt.tight_layout()
