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
        module="household",
        record="household_characteristics",
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

print(f"[OK] Data RECH6 cargada: {len(df_raw)} filas y {df_raw.shape[1]} columnas.")
print(f"[OK] Diccionario cargado: {len(col_labels_hist)} Column Labels, {len(val_labels_hist)} Value Labels")

# %%
# Inspeccionar variable
# df_raw['HC51'].value_counts(dropna=False)
df_raw.head(10)

# %%
from mnp.utils.cleaning import run_phase1_engine
from mnp.configs.rech0 import config_f1

# 3. Limpiar
df_clean = run_phase1_engine(df_raw, config_f1)

print(f'[OK] Limpieza biológica completa. Shape: {df_clean.shape}')
df_clean.head(5)

# %%
from importlib import reload
import mnp.utils.cleaning
reload(mnp.utils.cleaning)
from mnp.utils.cleaning import apply_standard_labels
from mnp.configs.rech0 import config_f1, config_f3
# Le pasamos config_f1 para que el motor sepa mágicamente dónde buscar 
# gracias a tus propias reglas de Coalesce.
df_final = apply_standard_labels(df_clean, val_labels_hist, config_f3, config_f1)
print(f"[OK] Fase 3 (Estandarización de Etiquetas) completada.")
df_final.head(15)

# %%
from mnp.config import analysis_years, INTERIM_DATA_DIR
import os
# Aseguramos que la carpeta interim exista
os.makedirs(INTERIM_DATA_DIR, exist_ok=True)
# Ruta del archivo final
output_path = INTERIM_DATA_DIR / "rech0_cleaned.parquet"
# Guardamos en formato parquet (preserva tipos de datos y ahorra RAM)
df_final.to_parquet(output_path, index=False)
print(f"[OK] Datos RECH0 (Fase 1, 2 y 3) guardados exitosamente en:")
print(f"-> {output_path}")
