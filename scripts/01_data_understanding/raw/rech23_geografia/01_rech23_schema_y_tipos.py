# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_colwidth", None)
import gc
from mnp.config import analysis_years
from mnp.ingestion.loader import load_endes


# Carga de historial desde 2007 para RECH1
history = load_endes(
        year=analysis_years(),
        module="housing",
        record="rech23h",
        meta=True
    )

frames = []
latest_year_labels = {}
col_labels_hist = {}
value_labels_history = {}

for year in sorted(list(history.keys())):
    year_df, year_meta = history.pop(year)
    frames.append(year_df.assign(year=year))
    latest_year_labels.update(year_meta.column_names_to_labels)
    col_labels_hist[year] = year_meta.column_names_to_labels
    value_labels_history[year] = year_meta.variable_value_labels

df_rech23 = pd.concat(frames, ignore_index=True)
del frames
gc.collect()

all_cols = set()
for cols in col_labels_hist.values():
    all_cols.update(cols)

print(f"Registros RECH23 totales: {len(df_rech23)}")
print(f"Columnas RECH23 totales: {df_rech23.shape[1]}")
df_rech23.head(3)

# %% [markdown]
# ## 1.1. Schema Drift (Mutación de Column Labels)

# %%
from mnp.utils.profiler import analyze_schema_drift, print_schema_drift_report

all_cols_sch, stable_schema, mutated_schema = analyze_schema_drift(col_labels_hist)
print_schema_drift_report(all_cols_sch, stable_schema, mutated_schema)

# %% [markdown]
# ## 1.2. Schema Drift (Mutación de Value Labels)

# %%
from mnp.utils.profiler import analyze_val_drift, print_val_drift_report

all_val_cols, stable_val_labels, mutated_val_labels = analyze_val_drift(value_labels_history)
print_val_drift_report(all_val_cols, stable_val_labels, mutated_val_labels, latest_year_labels=latest_year_labels)

# %%
# Filas = Años, Columnas = Variables
df_history_matrix = pd.DataFrame(col_labels_hist).T.sort_index()

# Reemplazamos los valores por el nombre de la propia variable (si existe) o vacío si no existía ese año
for col in df_history_matrix.columns:
    df_history_matrix[col] = df_history_matrix[col].where(df_history_matrix[col].isna(), col)

df_history_matrix = df_history_matrix.fillna("")

print(df_history_matrix)

# %% [markdown]
# ## 2. Tipos Lógicos y Reporte Global (Master Data Dictionary)

# %%
import pandas as pd
from mnp.utils.profiler import (
    analyze_logical_types, metric_latest_label, metric_logical_type, 
    metric_pandas_dtype, metric_has_value_labels, metric_nulls, 
    metric_years_present, metric_total_years
)

# 💡 ENFOQUE HÍBRIDO: IDs locales o conocidos
known_ids = ["HHID", "HV000", "HV001", "HV002", "HV002A", "HV003"]
logical_types_dict = analyze_logical_types(df_rech23, all_cols, value_labels_history, col_labels_hist, forced_ids=known_ids)

# 1. El DataFrame base son las variables originales
df_report = pd.DataFrame(index=sorted(list(all_cols)))
df_report.index.name = "Variable"

# 2. Los "Enchufes" explícitos usando el map() nativo de Pandas
df_report["Latest Column Label"] = df_report.index.map(lambda c: metric_latest_label(c, latest_year_labels))
df_report["Tipo Lógico"]         = df_report.index.map(lambda c: metric_logical_type(c, logical_types_dict))
df_report["Pandas Dtype"]        = df_report.index.map(lambda c: metric_pandas_dtype(c, df_rech23.dtypes))
df_report["Value Labels"]        = df_report.index.map(lambda c: metric_has_value_labels(c, value_labels_history))
df_report["Años Presente"]       = df_report.index.map(lambda c: metric_years_present(c, col_labels_hist))
df_report["Total Años"]          = df_report.index.map(lambda c: metric_total_years(c, col_labels_hist))
df_report["% Nulos"]             = df_report.index.map(lambda c: metric_nulls(c, df_rech23))

df_report.sort_values(by=["Tipo Lógico", "% Nulos"], ascending=[True, False], inplace=True)
print(df_report)

# %% [markdown]
# ## 3. Análisis de Nulos por Tipo Lógico
# Al agrupar por Tipo Lógico universal (en lugar de categorías de negocio manuales), podemos aplicar reglas de limpieza automáticas más adelante.

# %%
from mnp.utils.profiler import analyze_nulls_evolution

analyze_nulls_evolution(
    df=df_rech23, 
    cols=logical_types_dict.get("Categorical", []), 
    group_name="Categorical", 
    latest_year_labels=latest_year_labels, 
    cmap="Blues_r", 
    figsize=(14, 8)
)


# %%
from mnp.utils.profiler import analyze_nulls_evolution

analyze_nulls_evolution(
    df=df_rech23, 
    cols=logical_types_dict.get("Numerical", []), 
    group_name="Numerical", 
    latest_year_labels=latest_year_labels, 
    cmap="Purples_r", 
    figsize=(14, 8)
)


# %%
from mnp.utils.profiler import analyze_nulls_evolution

analyze_nulls_evolution(
    df=df_rech23,
    cols=logical_types_dict.get("Identifier", []), 
    group_name="Identifier", 
    latest_year_labels=latest_year_labels, 
    cmap="Oranges_r", 
    figsize=(14, 8)
)

