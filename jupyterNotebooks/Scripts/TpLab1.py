import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

#=========================================
# Función transferencia
#
#              sqrt(2) * s
# T(s) = --------------------------
#         (s + 1) (s² + s + 1)
#
# w0 = 1 rad/s, Q = 1, k = sqrt(2)
#=========================================
num = [6]                 # sqrt(2)*s
den = [1,3,3]  # (s+1)*(s²+s+1) -> [1,2,2,1]

H = signal.TransferFunction(num, den)

#=========================================
# Respuesta en frecuencia
#=========================================
w = np.logspace(-2, 2, 3000)   # 0.01 a 100 rad/s, como el gráfico original

w, mag, phase = signal.bode(H, w)

plt.figure(figsize=(8,6))

plt.subplot(2,1,1)
plt.semilogx(w, mag)
plt.axvline(1, color='r', ls='--', label='w0 = 1 rad/s')
plt.grid(True, which='both')
plt.ylabel("Magnitud (dB)")
plt.legend()

plt.subplot(2,1,2)
plt.semilogx(w, phase)
plt.axvline(1, color='r', ls='--')
plt.grid(True, which='both')
plt.ylabel("Fase (°)")
plt.xlabel("Frecuencia (rad/s)")

plt.tight_layout()
plt.show()
# %%

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# ======================================================
# TRANSFERENCIA NORMALIZADA
#
#               s³
# H(s) = ---------------------
#        (s+1)(s²+s+1)
#
# Denominador expandido:
# s³ + 2s² + 2s + 1
# ======================================================

num = [1, 0, 0, 0]
den = [1, 2, 2, 1]

H = signal.TransferFunction(num, den)

#===========================
# BODE
#===========================

w = np.logspace(-2, 2, 1000)

w, mag, phase = signal.bode(H, w)

plt.figure(figsize=(8,7))

plt.subplot(2,1,1)
plt.semilogx(w, mag)
plt.grid(True, which="both")
plt.ylabel("Magnitud (dB)")
plt.title("Diagrama de Bode")

plt.subplot(2,1,2)
plt.semilogx(w, phase)
plt.grid(True, which="both")
plt.ylabel("Fase (°)")
plt.xlabel("Frecuencia normalizada (rad/s)")

plt.tight_layout()

#===========================
# POLOS Y CEROS
#===========================

zeros = np.roots(num)
poles = np.roots(den)

plt.figure(figsize=(6,6))

plt.scatter(np.real(zeros), np.imag(zeros),
            marker='o', s=80, label='Ceros')

plt.scatter(np.real(poles), np.imag(poles),
            marker='x', s=80, label='Polos')

plt.axhline(0,color='k')
plt.axvline(0,color='k')

plt.grid(True)
plt.xlabel("Parte Real")
plt.ylabel("Parte Imaginaria")
plt.title("Diagrama de Polos y Ceros")
plt.legend()

plt.axis("equal")

plt.show()