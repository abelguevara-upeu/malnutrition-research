import pandas as pd
import numpy as np
import joblib
import json
import shap
import os

print("Cargando modelo y datos...")
model = joblib.load('models/champion_lightgbm.pkl')
with open('models/champion_metadata.json', 'r') as f:
    metadata = json.load(f)

df = pd.read_parquet('data/processed/master_preprocessed_v2.parquet')

# Restaurar columnas
import sys
import unicodedata
sys.path.append('.')
from mnp.configs.column_labels import LABELS

cols_to_drop = [c for c in ['UBIGEO', 'LATITUDY', 'LONGITUDX', 'TARGET_DESNUTRICION', 'year', 'SHREGION', 'HV005', 'hv005'] if c in df.columns]
X = df.drop(columns=cols_to_drop).rename(columns=LABELS)

import re
clean_cols = []
for col in X.columns:
    col_str = unicodedata.normalize('NFKD', str(col)).encode('ASCII', 'ignore').decode('utf-8')
    col_str = re.sub(r'[^a-zA-Z0-9]+', '_', col_str).strip('_')
    clean_cols.append(col_str)
X.columns = clean_cols

for col in metadata['cat_features']:
    X[col] = X[col].astype('category')

# Usar una muestra de 5000 para rapidez
X_sample = X.sample(n=5000, random_state=42)

print("Calculando SHAP values...")
explainer = shap.TreeExplainer(model)
shap_values = explainer(X_sample)

# Recuperar departamento
print("Agrupando por departamento...")
df_original = pd.read_parquet('data/interim/master_merged_v2.parquet', columns=['HV024'])
dept_sample = df_original.loc[X_sample.index, 'HV024']

shap_abs_df = pd.DataFrame(np.abs(shap_values.values), columns=X_sample.columns)
shap_abs_df['DEPARTAMENTO'] = dept_sample.values

# Promedios
dept_impact = shap_abs_df.groupby('DEPARTAMENTO').mean()

# Normalizamos del 0 al 1
dept_impact_norm = (dept_impact - dept_impact.min()) / (dept_impact.max() - dept_impact.min())

# Exportamos
output_path = 'data/processed/shap_dept_impact.csv'
dept_impact_norm.to_csv(output_path)
print(f"✅ ¡Datos geográficos exportados exitosamente a {output_path}!")
