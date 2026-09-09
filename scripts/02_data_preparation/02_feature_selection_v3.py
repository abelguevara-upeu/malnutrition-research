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

# %% [markdown]
# # 03 - Feature Selection y Aseguramiento de Calidad (Nulos)
#
# Este notebook tiene como objetivo justificar matemáticamente cada variable que entra al modelo predictivo. Reemplazamos la eliminación manual con pruebas estadísticas formales.
#

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', None)

# 1. Cargar datos
print("Cargando datos...")
master = pd.read_parquet('../../data/interim/master_merged_v2.parquet')

# Filtramos filas sin target (Desnutrición)
master = master.dropna(subset=['HC70']).copy()
master['TARGET_DESNUTRICION'] = (master['HC70'] < -2.0).astype(int)

# Eliminamos variables de Fuga (Leakage) e identificadores que sabemos que no son predictivos
# NOTA TESIS: Hemos rescatado 'HV024', 'SHREGION', 'year' y 'HV005' para análisis posterior.
leakage_cols = [
    'HC0', 'HVIDX', 'HV112', 'HV001', 'HV002', 'HV002A', 'NCONGLOME', 'CODCCPP', 'NOMCCPP', 'ID1',
    'HC2', 'HC3', 'HC4', 'HC5', 'HC6', 'HC7', 'HC8', 'HC9', 'HC10', 'HC11', 'HC12', 'HC13', 
    'HC15', 'HC16', 'HC19', 'HC30', 'HC31', 'HC32', 'HC33', 'HC71', 'HC72', 'HC73', 'HC55', 'HC70',
    'HV004', 'HV008', 'HV015', 'HV021', 'HV022', 'QH227A',
    'SHPROVIN', 'SHDISTRI', 'SHSEMES', 
    'HV120', 'HV010', 'HV035', 'HC64', 'HV114', 'HC51', 'HC60', 
    'HV218', 'HV117', 'HHID',
    'CASEID', 'MIDX', 'BIDX', 'B16', 'extracted_HHID',
    'UBIGEO', 'LATITUDY', 'LONGITUDX'
]
cols_to_drop = [c for c in leakage_cols if c in master.columns]
df_clean = master.drop(columns=cols_to_drop)

print(f"Dimensiones base: {df_clean.shape}")


# %%
# 2. AUDITORÍA VISUAL DE NULOS
# Calculamos el porcentaje de nulos por columna
null_percentages = (df_clean.isnull().sum() / len(df_clean)) * 100
null_percentages = null_percentages[null_percentages > 0].sort_values(ascending=False)

plt.figure(figsize=(12, 6))
sns.barplot(x=null_percentages.index[:30], y=null_percentages.values[:30], palette='Reds_r')
plt.axhline(y=60, color='r', linestyle='--', label='Umbral Crítico (60% Vacío)')
plt.title('Top 30 Variables con Mayor Porcentaje de Nulos')
plt.xticks(rotation=90)
plt.ylabel('% de Nulos')
plt.legend()
plt.tight_layout()
plt.show()

# Ejecutamos la guillotina objetiva (> 60% nulos fuera)
variables_basura = null_percentages[null_percentages > 60].index.tolist()
df_clean = df_clean.drop(columns=variables_basura)
print(f"Se eliminaron {len(variables_basura)} variables por superar el 60% de nulos.")


# %%
# 3. ANÁLISIS DE COLINEALIDAD (Correlación)
# Seleccionamos solo las numéricas para la matriz
num_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
num_cols.remove('TARGET_DESNUTRICION')

corr_matrix = df_clean[num_cols].corr()

# Extraer pares altamente correlacionados (> 0.85)
high_corr_pairs = []
for i in range(len(corr_matrix.columns)):
    for j in range(i):
        if abs(corr_matrix.iloc[i, j]) > 0.85:
            high_corr_pairs.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_matrix.iloc[i, j]))

print("Pares de variables altamente colineales detectados matemáticamente (>0.85):")
for pair in high_corr_pairs:
    print(f"➜ {pair[0]} y {pair[1]} (Correlación: {pair[2]:.2f})")
    
# Visualizamos un mapa de calor simplificado con las etiquetas descriptivas
import sys
import os
sys.path.append(os.path.abspath('../../'))
try:
    from mnp.configs.column_labels import LABELS
except ImportError:
    LABELS = {}

plt.figure(figsize=(14, 10))

# Seleccionamos las columnas para el mapa
cols_y = [p[0] for p in high_corr_pairs[:10]]
cols_x = [p[1] for p in high_corr_pairs[:10]]

# Obtenemos los nombres largos del diccionario (o dejamos el corto si no existe)
labels_y = [LABELS.get(c, c) for c in cols_y]
labels_x = [LABELS.get(c, c) for c in cols_x]

# Dibujamos el mapa
ax = sns.heatmap(corr_matrix.loc[cols_y, cols_x], annot=True, cmap='coolwarm')

# Aplicamos las etiquetas legibles
ax.set_xticklabels(labels_x, rotation=45, ha='right')
ax.set_yticklabels(labels_y, rotation=0)

plt.title('Mapa de Calor de Variables Altamente Correlacionadas')
plt.tight_layout()
plt.show()

# %%
# 3.1 ELIMINACIÓN DE GEMELOS COLINEALES (Redundancia)
# Eliminamos las variables matemáticamente idénticas o espejos inversos perfectos
gemelos_a_eliminar = [
    'HV105', 'HV106', 'HV109', 'HV009', 'HV013', 'M55Z', # Colinealidad matemática
    'HV104', 'HC61', 'HC53', 'HC57', # Redundancias categóricas o clínicas (Ej: HC53 cruda vs HC56 ajustada)
    'HV110', 'HV121', 'HV125', 'HV126', # Educación inválida (Bebés no asisten a escuela)
    'HV206', 'HV207', 'HV208', 'HV209', 'HV210', 'HV211', 'HV212', 'HV221', # Bienes y activos absorbidos por Índice de Riqueza
    'HV243A', 'HV243C', 'HV243D', 'HV244', 'HV246', # Más activos económicos absorbidos
    'SH61A', 'SH61B', 'SH61C', 'SH61D', 'SH61E', 'SH61J', 'SH61K', 'SH61L', 'SH61M', 'SH61N', 'SH61O', 'SH61P', 'SH61Q', 'SH61R', 'SH61S', # Electrodomésticos absurdamente detallados
    'HV270' # Eliminamos el índice categórico para quedarnos con el score continuo HV271
]

cols_to_drop = [col for col in gemelos_a_eliminar if col in df_clean.columns]
df_clean = df_clean.drop(columns=cols_to_drop)

print(f"🔪 Se eliminaron {len(cols_to_drop)} columnas redundantes.")
print(f"Columnas sobrevivientes: {df_clean.shape[1]}")


# %%
# 4. PRUEBAS ESTADÍSTICAS BIVARIADAS (P-Values)
# Verificamos si cada variable tiene una relación estadísticamente significativa con la Desnutrición
from scipy.stats import chi2_contingency, kruskal

p_values = {}
features = df_clean.drop(columns=['TARGET_DESNUTRICION'])
target = df_clean['TARGET_DESNUTRICION']

for col in features.columns:
    if pd.api.types.is_numeric_dtype(features[col]):
        # Kruskal-Wallis (alternativa no paramétrica a ANOVA)
        group1 = features.loc[target == 0, col].dropna()
        group2 = features.loc[target == 1, col].dropna()
        if len(group1) > 0 and len(group2) > 0:
            stat, p = kruskal(group1, group2)
            p_values[col] = p
    else:
        # Chi-Cuadrado para categóricas
        contingency = pd.crosstab(features[col], target)
        if contingency.shape[0] > 1 and contingency.shape[1] > 1:
            stat, p, dof, expected = chi2_contingency(contingency)
            p_values[col] = p

p_df = pd.DataFrame(list(p_values.items()), columns=['Variable', 'P_Value'])
p_df['Relevante'] = p_df['P_Value'] < 0.05 # Rechazamos hipótesis nula

print("Prueba Estadística Bivariada Completada.")
print(f"Variables RELEVANTES (P-value < 0.05): {p_df['Relevante'].sum()}")
print(f"Variables IRRELEVANTES (P-value >= 0.05): {(~p_df['Relevante']).sum()}")

# Muestra de las irrelevantes con etiquetas descriptivas
import sys
import os
sys.path.append(os.path.abspath('../../'))
try:
    from mnp.configs.column_labels import LABELS
except ImportError:
    LABELS = {}

p_df['Descripción'] = p_df['Variable'].map(lambda x: LABELS.get(x, x))

print("\nVariables estadísticamente irrelevantes para la desnutrición:")
print(p_df[~p_df['Relevante']][['Variable', 'Descripción', 'P_Value']].head(15))

# %%
# 5. IMPORTANCIA MULTIVARIADA (XGBoost Feature Selection)
# Las pruebas bivariadas analizan variables de 1 en 1. XGBoost las analiza todas juntas.
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder

# Preparamos una copia rápida convirtiendo categóricas
X_test_xgb = features.copy()
for col in X_test_xgb.columns:
    if not pd.api.types.is_numeric_dtype(X_test_xgb[col]):
        X_test_xgb[col] = X_test_xgb[col].astype(str).astype('category')

# Entrenamos un árbol rápido (sin balanceo, solo para ver poder puro)
print("Entrenando Árbol de Selección...")
xgb_selector = xgb.XGBClassifier(n_estimators=100, random_state=42, enable_categorical=True, tree_method='hist')
xgb_selector.fit(X_test_xgb, target)

# Resultados
importances = xgb_selector.feature_importances_
importance_df = pd.DataFrame({'Variable': X_test_xgb.columns, 'Importancia': importances})
importance_df = importance_df.sort_values('Importancia', ascending=False)

import sys
import os
sys.path.append(os.path.abspath('../../'))
try:
    from mnp.configs.column_labels import LABELS
except ImportError:
    LABELS = {}

basura_cols = importance_df[importance_df['Importancia'] == 0]['Variable'].tolist()

print("\nLas variables con CERO poder predictivo en conjunto (Basura algorítmica):")
for col in basura_cols:
    print(f"🗑️ {LABELS.get(col, col)}")

# %%
# 6. EXPORTACIÓN DEL DATASET PREPROCESADO (LISTO PARA MODELADO)
print("Aplicando guillotina final a las variables basura detectadas por XGBoost...")

# Eliminamos la basura algorítmica
df_final = df_clean.drop(columns=[col for col in basura_cols if col in df_clean.columns])

print(f"Dimensiones finales para Modelado: {df_final.shape}\n")

import sys
import os
sys.path.append(os.path.abspath('../../'))
try:
    from mnp.configs.column_labels import LABELS
except ImportError:
    LABELS = {}

# Mostrar la lista de columnas finales ordenadas alfabéticamente con su descripción
columnas_finales = sorted(df_final.columns.tolist())
print("📝 LISTA DE COLUMNAS FINALES (Sobrevivientes):")
for col in columnas_finales:
    desc = LABELS.get(col, col)
    print(f" {desc}")

print("\n👀 VISTAZO AL DATASET (Primeras 3 filas):")
print(df_final.head(3))

# Guardamos en la carpeta processed
output_path = '../../data/processed/master_preprocessed_v2.parquet'
df_final.to_parquet(output_path, index=False)
print(f"\n Dataset definitivo guardado exitosamente en:\n{output_path}")

# %%
# 7. PROPORCIÓN TEMPORAL (Evaluados por Año)
# Aprovechamos que la variable 'year' sigue viva en el dataframe original 'master' 
# (antes de la guillotina) para visualizar la distribución histórica.

plt.figure(figsize=(14, 6))
ax = sns.countplot(data=master, x='year', palette='viridis')
plt.title('Distribución Histórica de Niños Evaluados (ENDES 2004-2022)')
plt.xlabel('Año de Encuesta')
plt.ylabel('Cantidad de Niños Evaluados')
plt.xticks(rotation=45)

# Añadir los números encima de las barras
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontsize=9)

plt.tight_layout()
plt.show()

# Proporción en porcentajes
print("Proporción por año (%):")
print((master['year'].value_counts(normalize=True).sort_index() * 100).round(2).to_string())

#%%
# 7. PROPORCIÓN TEMPORAL (Evaluados por Año)
# Aprovechamos que la variable 'year' sigue viva en el dataframe original 'master' 
# (antes de la guillotina) para visualizar la distribución histórica.

plt.figure(figsize=(14, 6))
ax = sns.countplot(data=master, x='year', palette='viridis')
plt.title('Distribución Histórica de Niños Evaluados (ENDES 2004-2022)')
plt.xlabel('Año de Encuesta')
plt.ylabel('Cantidad de Niños Evaluados')
plt.xticks(rotation=45)

# Añadir los números encima de las barras
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontsize=9)

plt.tight_layout()
plt.show()

# Proporción en porcentajes
print("Proporción por año (%):")
print((master['year'].value_counts(normalize=True).sort_index() * 100).round(2).to_string())
# %%
