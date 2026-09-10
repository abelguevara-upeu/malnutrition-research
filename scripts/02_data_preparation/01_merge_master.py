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
# # 🏗️ Fase 3: Data Consolidation (Merge Master)
#
# Este cuaderno ejecuta la estrategia de cruce (Merge) diseñada en la Arquitectura End-to-End, transformando los módulos individuales (`RECH6`, `RECH1`, `RECH0`, `RECH23`) en un único Dataset Analítico Maestro a nivel de **Niño**.
#
# ## Reglas Epidemiológicas Aplicadas:
# 1. **Target Individual:** 1 Fila = 1 Niño (Menor de 5 años medido en `RECH6`).
# 2. **Filtro de Residencia:** Solo se incluyen niños que durmieron en el hogar la noche anterior (`HV103 == 1`).
#

# %%
import pandas as pd
from pathlib import Path

# Configuraciones
pd.set_option('display.max_columns', None)
from mnp.config import INTERIM_DATA_DIR
interim_dir = INTERIM_DATA_DIR


# %%
# 1. Cargar las 4 tablas base
print("⏳ Cargando tablas interim...")
df_rech6 = pd.read_parquet(interim_dir / 'rech6_cleaned.parquet')
df_rech1 = pd.read_parquet(interim_dir / 'rech1_cleaned.parquet')
df_rech0 = pd.read_parquet(interim_dir / 'rech0_cleaned.parquet')
df_rech23 = pd.read_parquet(interim_dir / 'rech23_cleaned.parquet')

print(f"[OK] RECH6 (Tronco): {len(df_rech6):,} filas")
print(f"[OK] RECH1 (Demografía): {len(df_rech1):,} filas")
print(f"[OK] RECH0 (Entrevista): {len(df_rech0):,} filas")
print(f"[OK] RECH23 (Hogar): {len(df_rech23):,} filas")


# %% [markdown]
# ### 🛡️ Criterios de Inclusión y Exclusión de Muestra en RECH1 (`HV103 == 1`)

# %%
# Aplicar regla del INEI: Solo miembros que durmieron en casa anoche
# HV103 puede tener múltiples tipos de datos al agrupar 18 años (float, int, string)
total_original = len(df_rech1)
valid_values = [1, 1.0, '1', '1.0', 'Sí', 'Yes', 'si']
df_rech1 = df_rech1[df_rech1['HV103'].isin(valid_values)].copy()

print(f"Se filtraron {total_original - len(df_rech1):,} personas que NO durmieron en casa.")
print(f"Quedan {len(df_rech1):,} residentes habituales válidos.")


# %% [markdown]
# ### 🛠️ Función Auxiliar para evitar columnas duplicadas

# %%
def drop_overlapping_columns(left_df, right_df, join_keys_right):
    """Elimina columnas del dataframe derecho que ya existen en el izquierdo, excepto las llaves de cruce."""
    overlap = set(right_df.columns).intersection(set(left_df.columns))
    cols_to_drop = [c for c in overlap if c not in join_keys_right]
    return right_df.drop(columns=cols_to_drop)



# %% [markdown]
# ### 🔄 Cruce 1: Base (RECH6) + Demografía (RECH1)

# %%
# Left Join por Niño
# El INEI recicla los HHID, por lo tanto la llave primaria obligatoria siempre debe incluir el año (`year`)
join_keys_child = ['year', 'HHID', 'HVIDX']
df_rech1_clean = drop_overlapping_columns(df_rech6, df_rech1, join_keys_child)

master = pd.merge(
    df_rech6, 
    df_rech1_clean, 
    left_on=['year', 'HHID', 'HC0'], 
    right_on=['year', 'HHID', 'HVIDX'], 
    how='left'
)

print(f"Filas resultantes: {len(master):,} (Debería ser exactamente igual a {len(df_rech6):,})")


# %% [markdown]
# ### 🔄 Cruce 2 y 3: Entorno del Hogar (RECH0 y RECH23)

# %%
# Left Join por Hogar
join_keys_hh = ['year', 'HHID']

df_rech0_clean = drop_overlapping_columns(master, df_rech0, join_keys_hh)
master = pd.merge(master, df_rech0_clean, on=join_keys_hh, how='left')

df_rech23_clean = drop_overlapping_columns(master, df_rech23, join_keys_hh)
master = pd.merge(master, df_rech23_clean, on=join_keys_hh, how='left')

print(f"Filas resultantes: {len(master):,} (Debería ser exactamente igual a {len(df_rech6):,})")
print(f"Columnas resultantes: {master.shape[1]}")


# %% [markdown]
# ### 🔄 Cruce 4: Historia de Embarazo y Lactancia (REC41) a través de REC21 (Tabla Puente)

# %%
# Cargar REC21 (Puente) usando el motor de ingesta (Historia completa multi-año)
from mnp.ingestion.loader import load_endes

print("⏳ Cargando REC21 (Historia de Nacimientos) como Puente...")
# Cargamos toda la historia de REC21 inyectando el AÑO para evitar el producto cartesiano
dict_rec21 = load_endes(module='birth_history', record='rec21', usecols=['CASEID', 'BIDX', 'B16'])
dfs = []
for y, df in dict_rec21.items():
    df['year'] = int(y)
    dfs.append(df)
df_rec21 = pd.concat(dfs, ignore_index=True)

# Castear llaves a string (mismo trato que la fase de limpieza)
df_rec21['CASEID'] = df_rec21['CASEID'].astype(str).str.strip()

# Filtrar nulos (B16 es 0 o nulo si el hijo no reside en el hogar o falleció)
df_rec21 = df_rec21.dropna(subset=['B16'])
df_rec21 = df_rec21[df_rec21['B16'].astype(float) > 0].copy()

# Castear BIDX y B16 a string limpio (eliminando .0)
df_rec21['BIDX'] = df_rec21['BIDX'].astype(float).astype(int).astype(str)
df_rec21['B16'] = df_rec21['B16'].astype(float).astype(int).astype(str)

# Cargar REC41 (Features limpios)
print("⏳ Cargando REC41 (Features)...")
df_rec41 = pd.read_parquet(interim_dir / 'rec41_features.parquet')

# Castear MIDX de REC41 a string limpio para que cruce con BIDX
df_rec41['MIDX'] = df_rec41['MIDX'].astype(float).astype(int).astype(str)

# 1. Cruzar REC41 con REC21 para inyectar B16 (El HVIDX/HC0 universal del niño)
print("🔗 Cruzando REC41 con el Puente REC21...")
df_rec41_bridged = pd.merge(
    df_rec41,
    df_rec21,
    left_on=['year', 'CASEID', 'MIDX'],
    right_on=['year', 'CASEID', 'BIDX'],
    how='inner' # Nos quedamos solo con los que tienen B16 válido (viven en el hogar)
)

# 2. Reconstruir HHID desde CASEID para el cruce maestro
# CASEID en ENDES siempre termina con la línea de la madre (3 caracteres). El resto es HHID.
df_rec41_bridged['extracted_HHID'] = df_rec41_bridged['CASEID'].str[:-3].str.strip()

# 3. Cruzar al Master!
# HHID = extracted_HHID  Y  HC0 = B16
print("🔗 Inyectando REC41 al Master...")
df_rec41_clean = drop_overlapping_columns(master, df_rec41_bridged, ['year', 'extracted_HHID', 'B16'])

master = pd.merge(
    master,
    df_rec41_clean,
    left_on=['year', 'HHID', 'HC0'],
    right_on=['year', 'extracted_HHID', 'B16'],
    how='left'
)

print(f"Filas resultantes: {len(master):,} (Debería ser exactamente igual a 294,109)")
print(f"Columnas resultantes: {master.shape[1]}")

# %% [markdown]
# ### 🍼 Cálculo de KPI 5 (Lactancia Materna Exclusiva)

# %%
# Regla Oficial del MINSA/INEI (Ficha Técnica KPI 5)
# 1. Niño menor de 6 meses (HC1 < 6)
# 2. Aún le está dando pecho (M4 == 95.0)
# (Nota: La lógica oficial también valida REC42 para líquidos. Como proxy de alta pureza 
# usamos M55A para asegurar exclusividad en primeros días o simplemente la intención principal).

master['kpi5_lactancia_exclusiva'] = ((master['M4'] == 95.0) & (master['HC1'] < 6)).astype(int)

# IMPORTANTE: Arreglar M4 para XGBoost
# Si dejamos el código 95.0, XGBoost pensará que el niño lactó 95 meses.
# Matemáticamente, si el niño "aún lacta" (95.0), los meses reales de lactancia 
# son idénticos a su edad actual en meses (HC1).
mask_aun_lacta = master['M4'] == 95.0
master.loc[mask_aun_lacta, 'M4'] = master.loc[mask_aun_lacta, 'HC1']

print("KPI 5 Calculado y M4 matematizado.")
print(master['kpi5_lactancia_exclusiva'].value_counts(dropna=False))

# %%
# Vamos a demostrar matemáticamente que el niño que unimos desde REC41 es EXACTAMENTE el mismo niño de RECH6.
# Para esto, traeremos la variable Sexo (B4) y Año de Nacimiento (B2) desde la historia clínica REC21.
# Y las compararemos contra el Sexo (HC27) y Año de Nacimiento (HC31) de la Antropometría RECH6.

print("⏳ Cargando datos biológicos de REC21 para auditoría...")
dict_audit = load_endes(module='birth_history', record='rec21', usecols=['CASEID', 'BIDX', 'B2', 'B4'])
dfs_audit = []
for y, df in dict_audit.items():
    df['year'] = int(y)
    dfs_audit.append(df)
df_audit = pd.concat(dfs_audit, ignore_index=True)

# Limpieza de llaves
df_audit['CASEID'] = df_audit['CASEID'].astype(str).str.strip()
df_audit['BIDX'] = df_audit['BIDX'].astype(float).astype(int).astype(str)

# Pegamos esta info de auditoría al master (usando CASEID y MIDX que sobrevivieron al cruce anterior)
master_audit = pd.merge(
    master,
    df_audit,
    left_on=['year', 'CASEID', 'MIDX'],
    right_on=['year', 'CASEID', 'BIDX'],
    how='inner'
)

# Comparativa 1: SEXO
# HC27 ya está decodificado como string ("Hombre", "Mujer") en el Master.
# B4 viene crudo como numérico (1=Hombre, 2=Mujer)
map_sexo = {'Hombre': 1, 'Masculino': 1, 'Mujer': 2, 'Femenino': 2}
master_audit['HC27_num'] = master_audit['HC27'].str.strip().str.capitalize().map(map_sexo)

sexo_match = (master_audit['HC27_num'] == master_audit['B4'].astype(float)).mean() * 100

# Comparativa 2: AÑO DE NACIMIENTO
year_match = (master_audit['HC31'].astype(float) == master_audit['B2'].astype(float)).mean() * 100

print(f"✅ Coincidencia de Sexo Biológico entre módulos: {sexo_match:.2f}%")
print(f"✅ Coincidencia de Año de Nacimiento entre módulos: {year_match:.2f}%")
print("\nSi ambos números son 100% (o 99.9%), es la prueba absoluta de que el cruce MIDX -> HC0 fue perfecto.")


# %% [markdown]
# ### 📅 Resumen de Casos por Año

# %%
# Distribución de niños evaluados a lo largo de los 18 años
resumen_year = master['year'].value_counts().sort_index().reset_index()
resumen_year.columns = ['Año', 'Niños Evaluados']
resumen_year['% del Total'] = (resumen_year['Niños Evaluados'] / len(master) * 100).round(1).astype(str) + '%'

print(resumen_year)


# %% [markdown]
# ### 🧹 Limpieza Final: Poda de Columnas Muertas (>70% Nulos)

# %%
# Cuando unimos 20 años de encuestas, es normal que aparezcan "Columnas Fantasma".
# Son preguntas que el INEI hizo en un solo año (ej. 2008) y nunca más volvió a preguntar, 
# o preguntas que solo aplican a adultos (ej. Estado Civil HV115 en niños de 5 años).

# 1. Calcular porcentaje de nulos
null_pct = (master.isnull().mean() * 100).sort_values(ascending=False)

# 2. Identificar columnas con más del 70% de nulos
bad_columns = null_pct[null_pct > 70].index.tolist()

print(f"🗑️ Se detectaron {len(bad_columns)} columnas con más del 70% de nulos.")
print("Columnas a eliminar:", bad_columns)

# 3. Eliminar esas columnas del Master (excepto si hay alguna que queramos salvar)
# whitelist = ['alguna_columna_importante']
# bad_columns = [col for col in bad_columns if col not in whitelist]

master = master.drop(columns=bad_columns)

print(f"✅ Limpieza completada. Columnas finales en el Master: {master.shape[1]}")


# %%
# Guardar resultado maestro
output_path = interim_dir / 'master_merged_v2.parquet'
master.to_parquet(output_path, index=False)
print(f"🎉 Dataset maestro guardado con éxito: {output_path}")


# %% [markdown]
# ### 👀 Vista Previa con Etiquetas (Diccionario INEI)

# %%
import sys
sys.path.append('../../')
from mnp.configs.column_labels import LABELS

# Tomamos las primeras 30 filas
vis_df = master.head(30).copy()

# Creamos un MultiIndex para las columnas: (Código_Variable, Etiqueta_Descriptiva)
multi_columns = [(col, LABELS.get(col.upper(), 'Sin Etiqueta')) for col in vis_df.columns]
vis_df.columns = pd.MultiIndex.from_tuples(multi_columns, names=['Variable', 'Descripción'])

print(vis_df)


# %% [markdown]
# ### 📉 Análisis de Valores Nulos (Missing Data)

# %%
# Calcular porcentaje de nulos por columna
null_percentages = (master.isnull().sum() / len(master) * 100).round(2)
null_df = null_percentages.reset_index()
null_df.columns = ['Variable', '% de Nulos']

# Añadir etiqueta descriptiva
null_df['Descripción'] = null_df['Variable'].apply(lambda x: LABELS.get(x.upper(), 'Sin Etiqueta'))

# Ordenar de mayor a menor porcentaje de nulos
null_df = null_df.sort_values(by='% de Nulos', ascending=False).reset_index(drop=True)

# Reordenar columnas para mejor lectura
null_df = null_df[['Variable', 'Descripción', '% de Nulos']]

# Mostrar el reporte completo (solo las que tienen algún nulo)
print(null_df[null_df['% de Nulos'] > 50])

