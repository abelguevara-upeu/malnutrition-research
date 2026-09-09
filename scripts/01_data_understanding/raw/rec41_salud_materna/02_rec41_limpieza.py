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
from mnp.config import analysis_years, INTERIM_DATA_DIR
import numpy as np
import gc
from mnp.ingestion.loader import load_endes
from mnp.utils.cleaning import run_phase1_engine, apply_standard_labels

# Configuración visual
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

print("[OK]")

# %%
# Carga de datos
history = load_endes(
        year=analysis_years(),
        module="maternal_health",
        record="rec41",
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

print(f"[OK] Data REC41 cargada: {len(df_raw)} filas y {df_raw.shape[1]} columnas.")
print(f"[OK] Diccionario cargado: {len(col_labels_hist)} Column Labels, {len(val_labels_hist)} Value Labels")

# %%
from mnp.configs.rec41 import config_f1

# 3. Limpiar Fase 1 (Numéricos / Falsos Numéricos / Casteos)
df_clean = run_phase1_engine(df_raw, config_f1)

print(f'[OK] Limpieza biológica Fase 1 completa. Shape: {df_clean.shape}')
df_clean.head(10)

# %%
from mnp.configs.rec41 import config_f3

# 4. Limpiar Fase 3 (Estandarización de Etiquetas)
df_clean = apply_standard_labels(df_clean, val_labels_hist, config_f3)

print(f'[OK] Estandarización de Etiquetas completa.')
df_clean.head(10)

# %%
# 4.5 Revisión de Frecuencias (Auditoría Post-Limpieza)
# Variables objetivo a auditar
vars_to_check = [
    'M13', 'M14', 'M15', 'M17', 'M18', 'M19', 
    'M34', 'M4', 'M5', 'M45', 'M46', 'M54', 'M60', 'M70', 'M55A'
]

print("=== AUDITORÍA DE FRECUENCIAS (Con Nulos) ===")
for col in vars_to_check:
    if col in df_clean.columns:
        print(f"\n--- {col} ---")
        print(df_clean[col].value_counts(dropna=False).head(10)) # Mostramos el top 10


# %%
# 4.8 Filtrado estricto de variables (Selección del Diccionario)
cols_to_keep = [
    'CASEID', 'MIDX', 'year', # Llaves maestras
    'M13', 'M14', 'M15', 'M17', 'M18', 'M19', 'M34', 'M4', 'M5', 
    'M45', 'M46', 'M54', 'M60', 'M70', 
    'M55A', 'M55B', 'M55C', 'M55E', 'M55F', 'M55G', 'M55H', 'M55I', 'M55X', 'M55Z'
]

# Quedarnos solo con las variables aprobadas
df_clean = df_clean[[c for c in cols_to_keep if c in df_clean.columns]]

print(f"Dataset podado a {df_clean.shape[1]} variables doradas. Shape: {df_clean.shape}")

# %%
# 5. Guardar Parquet
output_path = INTERIM_DATA_DIR / "v1" / "rec41_cleaned.parquet"
output_path.parent.mkdir(parents=True, exist_ok=True)
df_clean.to_parquet(output_path, index=False)
print(f"[OK] Guardado en: {output_path}")
