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
import numpy as np
import gc
from mnp.config import analysis_years
from mnp.ingestion.loader import load_endes
from mnp.utils.cleaning import run_phase1_engine
# Configuración visual
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

print("[OK]")

# %%
# Carga de datos
history = load_endes(
        year=analysis_years(),
        module="housing",
        record="rech23h",
        meta=True
    )

dfs = []
col_labels_hist = {}
val_labels_hist = {}

for year in sorted(list(history.keys())):
    year_df, year_meta = history.pop(year)
    col_labels_hist[year] = year_meta.column_names_to_labels
    val_labels_hist[year] = year_meta.variable_value_labels
    
    dfs.append(year_df.assign(year=year))

df_raw = pd.concat(dfs, ignore_index=True)
del dfs
gc.collect()

print(f"[OK] Data RECH23 cargada: {len(df_raw)} filas y {df_raw.shape[1]} columnas.")
print(f"[OK] Diccionario cargado: {len(col_labels_hist)} Column Labels, {len(val_labels_hist)} Value Labels")

# %%
# Inspeccionar variable
print(df_raw['SH107'].value_counts(dropna=False))
print(df_raw['SH124'].value_counts(dropna=False))
print(df_raw['SH224'].value_counts(dropna=False))
print(df_raw['HV234'].value_counts(dropna=False))

# %%
# Inspeccionar variable
print(df_raw['SHSEMES'].value_counts(dropna=False))
print(df_raw['SHTRIMES'].value_counts(dropna=False))

# %%
df_raw.head(10)

# %%
import numpy as np
from mnp.utils.cleaning import run_phase1_engine
from mnp.configs.rech23 import config_f1

# --- 1. CURA MASIVA PARA EL DICCIONARIO CORRUPTO DE YODO ---
# Convertimos las categorías 1-4 a PPM puros.
# El 5 y 9 se van a la zona de purga (995 y 994) para que Fase 1 los vuelva NaN.
diccionario_yodo = {
    1.0: 0.0, 2.0: 7.0, 3.0: 15.0, 4.0: 30.0,
    5.0: 995.0, 9.0: 994.0
}
columnas_yodo = ['SH107', 'SH124', 'SH224']
for col in columnas_yodo:
    if col in df_raw.columns:
        df_raw[col] = df_raw[col].replace(diccionario_yodo)


# --- 2. SPLITS MANUALES POR COLUMNAS RECICLADAS DEL INEI ---
# Agua y Basura
df_raw['SH42_Agua_Todo_El_Dia'] = np.where(df_raw['year'] >= 2010, df_raw['SH42'], np.nan)
df_raw['SH48_Conserva_Agua'] = np.where(df_raw['year'] >= 2010, df_raw['SH48'], np.nan)
df_raw['SH48_Basura'] = np.where(df_raw['year'] == 2009, df_raw['SH48'], np.nan)

# Limpieza, Basura y Luz (SH60)
df_raw['SH56_Frec_Limpieza'] = np.where(df_raw['year'] >= 2010, df_raw['SH56'], np.nan)
df_raw['SH56_Limpió_Baño'] = np.where(df_raw['year'] == 2009, df_raw['SH56'], np.nan)
df_raw['SH59_Frec_Recojo'] = np.where(df_raw['year'] >= 2010, df_raw['SH59'], np.nan)
df_raw['SH59_Recogen_Basura'] = np.where(df_raw['year'] == 2009, df_raw['SH59'], np.nan)
df_raw['SH60_Tipo_Basurero'] = np.where(df_raw['year'] >= 2010, df_raw['SH60'], np.nan)
df_raw['SH60_Fuente_Luz'] = np.where(df_raw['year'] == 2009, df_raw['SH60'], np.nan)

# Split de Luz y Hectáreas (SH70)
df_raw['SH70_Fuente_Luz'] = np.where(df_raw['year'] >= 2010, df_raw['SH70'], np.nan)
df_raw['SH70_Hectareas'] = np.where(df_raw['year'] == 2009, df_raw['SH70'], np.nan)


# Drop
df_raw = df_raw.drop(columns=['SH42', 'SH48', 'SH56', 'SH59', 'SH60', 'SH70'])

df_clean = run_phase1_engine(df_raw, config_f1)

print(f'[OK] Limpieza biológica completa. Shape: {df_clean.shape}')
df_clean.head(5)

# %%
from importlib import reload
import mnp.utils.cleaning
reload(mnp.utils.cleaning)
from mnp.utils.cleaning import apply_standard_labels
from mnp.configs.rech23 import config_f1, config_f3

# 1. El motor estandariza todas las variables normales leyendo config_f3
df_final = apply_standard_labels(df_clean, val_labels_hist, config_f3, config_f1)

# 2. Mapeos manuales EXCLUSIVOS para las columnas del Split (que el diccionario no reconoce)
dict_binario = {1.0: "Sí", 2.0: "No", 0.0: "No"}
columnas_manuales = [
    'SH42_Agua_Todo_El_Dia', 
    'SH48_Conserva_Agua', 
    'SH56_Limpió_Baño', 
    'SH59_Recogen_Basura'
]

for col in columnas_manuales:
    if col in df_final.columns:
        df_final[col] = df_final[col].map(dict_binario)

print(f"[OK] (Estandarización de Etiquetas) completada.")
df_final.head(15)


# %%
from mnp.config import INTERIM_DATA_DIR
import os
# Aseguramos que la carpeta interim exista
os.makedirs(INTERIM_DATA_DIR, exist_ok=True)
# Ruta del archivo final
output_path = INTERIM_DATA_DIR / "rech23_cleaned.parquet"
# Guardamos en formato parquet (preserva tipos de datos y ahorra RAM)
df_final.to_parquet(output_path, index=False)
print(f"[OK] Datos RECH23 guardados exitosamente en:")
print(f"-> {output_path}")

# %%
df_final['HV270'].value_counts(dropna=False)
