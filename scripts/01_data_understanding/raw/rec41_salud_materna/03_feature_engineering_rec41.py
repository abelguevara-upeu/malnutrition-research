# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
#   kernelspec:
#     display_name: .venv
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
from mnp.config import INTERIM_DATA_DIR
import numpy as np

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

# Cargar parquet limpio
path = INTERIM_DATA_DIR / "v1" / "rec41_cleaned.parquet"
df = pd.read_parquet(path)
print(f"[OK] Cargado: {df.shape}")


# %%
# 1. Decodificación Geométrica de M34 (Cuando empezó a darle el pecho)
# 0 -> 0 horas
# 1xx -> xx horas
# 2xx -> xx días -> xx * 24 horas

def decode_m34(val):
    if pd.isna(val):
        return np.nan
    if val == 0.0:
        return 0.0
    if 100 <= val < 200:
        return val - 100
    if 200 <= val < 300:
        return (val - 200) * 24
    return np.nan # Para casos raros

df['m34_horas_inicio_lactancia'] = df['M34'].apply(decode_m34)

print("--- Auditoría de nueva variable ---")
print(df[['M34', 'm34_horas_inicio_lactancia']].value_counts(dropna=False).head(15))

# %%
# 2. Imputación Condicionada de Suplementación (M46)
# Si no tomó hierro (M45 == 0), entonces días que tomó hierro (M46) es 0.
df.loc[df['M45'] == 0, 'M46'] = 0.0

# 3. Escalamiento de Peso al Nacer (M19)
# Está en gramos (Ej. 3500.0), lo pasamos a Kilos.
df['m19_peso_nacer_kg'] = df['M19'] / 1000.0

print("Imputaciones y escalamientos completados.")

# %%
# 5. Agrupación Categórica de Lugar de Parto (M15)
institucional = [
    'Hospital MINSA', 'Centro de salud MINSA', 'Hospital ESSALUD',
    'Clínica privada', 'Puesto de salud MINSA', 'Consultorio médico privado',
    'Center/Posta ESSALUD', 'Hospital FF.AA / Policiales', 'Clínica de la iglesia/entidad religiosa'
]
domiciliario = [
    'Su domicilio', 'Domicilio de partera', 'Otro'
]

def clasificar_lugar(val):
    if pd.isna(val):
        return np.nan
    if val in institucional:
        return 'Institucional'
    return 'Domiciliario' # Por defecto si es otro o en casa

df['m15_lugar_parto_agrupado'] = df['M15'].apply(clasificar_lugar)

print(df['m15_lugar_parto_agrupado'].value_counts(dropna=False))

# %%
# 5.5 Limpieza de Variables Crudas (Early Drop)
# Eliminamos las variables originales que ya fueron transformadas a features,
# más el clon perfecto (M5 = M4) para evitar que viajen al Master.
cols_a_eliminar = ['M19', 'M34', 'M15', 'M5']
df = df.drop(columns=[c for c in cols_a_eliminar if c in df.columns])
print(f"Bajas crudas confirmadas. Columnas restantes: {df.shape[1]}")

# 6. Exportar a Features
output_path = INTERIM_DATA_DIR / "rec41_features.parquet"
df.to_parquet(output_path, index=False)
print(f"[OK] Guardado en: {output_path}")
