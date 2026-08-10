"""
Grafica el diagrama de Bode (Modulo en dB y Fase en grados) a partir de los
archivos CSV exportados por el analizador de redes.

Estructura esperada de cada CSV (formato "Sweep" con múltiples bloques):
    "Sweep - Function 1"
    "Frequency vs Frequency"
    "X (Hz)","Ch-1 (Hz)", ...
    <datos...>
    <línea en blanco>
    "Sweep - Function 2"
    "Vac vs Frequency"  (o "Phase vs Frequency")
    "X (Hz)","Ch-1 (dBr)"  (o "Ch-1 (deg)","Ch-2 (deg)")
    <datos...>

- Sweep_Modulo.csv   -> Function 2 = Módulo (dBr) en Ch-1
- Sweep_Data_0.csv   -> Function 2 = Fase (deg); Ch-1 es el canal de
                        referencia (siempre 0) y Ch-2 tiene la fase real.

Requisitos: pip install pandas matplotlib --break-system-packages
"""

import pandas as pd
import matplotlib.pyplot as plt

ARCHIVO_MODULO = r"C:\Users\valen\OneDrive\Documentos\Facultad\2026\tc2\myRepo\jupyterNotebooks\Scripts\Sweep_Modulo.csv"
ARCHIVO_FASE = r"Sweep_Data_0.csv"


def leer_bloque(path, nombre_funcion_contiene, n_filas_max=200):
    """
    Lee un CSV multi-bloque tipo 'Sweep' y devuelve el DataFrame del bloque
    cuyo título (2da línea del bloque) contiene 'nombre_funcion_contiene'.
    """
    with open(path, encoding="utf-8-sig") as f:
        lineas = f.readlines()

    # Encontrar los índices donde arranca cada bloque ("Sweep - Function N")
    inicios = [i for i, l in enumerate(lineas) if l.startswith('"Sweep - Function')]
    inicios.append(len(lineas))  # centinela final

    for k in range(len(inicios) - 1):
        inicio, fin = inicios[k], inicios[k + 1]
        titulo = lineas[inicio + 1]
        if nombre_funcion_contiene.lower() in titulo.lower():
            encabezado = inicio + 2  # línea con nombres de columnas
            bloque = lineas[encabezado:fin]
            # Filtrar líneas vacías al final del bloque
            bloque = [l for l in bloque if l.strip() != ""]
            from io import StringIO
            df = pd.read_csv(StringIO("".join(bloque)))
            df.columns = [c.strip().strip('"') for c in df.columns]
            return df

    raise ValueError(f"No se encontró un bloque que contenga '{nombre_funcion_contiene}' en {path}")


# ---------------------------------------------------------------
# 1) Leer módulo (dB) y fase (deg)
# ---------------------------------------------------------------
df_mod = leer_bloque(ARCHIVO_MODULO, "Vac vs Frequency")
df_fase = leer_bloque(ARCHIVO_FASE, "Phase vs Frequency")

freq_mod = df_mod["X (Hz)"]
mod_db = df_mod["Ch-1 (dBr)"]

freq_fase = df_fase["X (Hz)"]
fase_deg = df_fase["Ch-2 (deg)"]  # Ch-1 es el canal de referencia (siempre 0)

# ---------------------------------------------------------------
# 2) Diagrama de Bode: Módulo (dB) y Fase, ambos vs frecuencia (log)
# ---------------------------------------------------------------
fig, (ax_mod, ax_fase) = plt.subplots(2, 1, figsize=(9, 8), sharex=True)

ax_mod.semilogx(freq_mod, mod_db, marker='o', markersize=3, color='tab:blue', linewidth=1.5)
ax_mod.axhline(-3, color='gray', linestyle='--', linewidth=1, label='-3 dB')
ax_mod.set_ylabel('Módulo (dB)')
ax_mod.set_title('Diagrama de Bode - Analizador de redes')
ax_mod.grid(True, which='both', linestyle=':', alpha=0.7)
ax_mod.legend(loc='lower left')

ax_fase.semilogx(freq_fase, fase_deg, marker='o', markersize=3, color='tab:red', linewidth=1.5)
ax_fase.set_ylabel('Fase (grados)')
ax_fase.set_xlabel('Frecuencia (Hz)')
ax_fase.grid(True, which='both', linestyle=':', alpha=0.7)

plt.tight_layout()
plt.savefig('bode_analizador_redes.png', dpi=150)
plt.show()

print("Gráfico guardado: bode_analizador_redes.png")
print(f"Puntos módulo: {len(freq_mod)} | Puntos fase: {len(freq_fase)}")
