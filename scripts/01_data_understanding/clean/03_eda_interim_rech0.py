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
# # EDA 3 (Interim) - RECH0: Geografía y Demografía del Hogar
# Este notebook audita el módulo RECH0 original, el cual contiene las variables geográficas (Urbano/Rural, Región, Altitud) y el tamaño total del hogar.

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mnp.utils.figures import save_fig
import seaborn as sns
from mnp.config import INTERIM_DATA_DIR

# Configuración de estilo
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

# %%
DATA_PATH = INTERIM_DATA_DIR / "rech0_cleaned.parquet"
print(f"Cargando datos desde: {DATA_PATH}")
df_rech0 = pd.read_parquet(DATA_PATH)
print(f"Filas (Hogares totales): {len(df_rech0):,}")
print(f"Columnas: {len(df_rech0.columns)}")
df_rech0.head()

# %% [markdown]
# ## 1. Contexto Geográfico: Urbano vs Rural (`HV025`) y Región (`HV024`)

# %%
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Urbano vs Rural
sns.countplot(data=df_rech0, x='HV025', palette='Set2', ax=axes[0])
axes[0].set_title('Tipo de Residencia (HV025)')

# Distribución por Región (Top 10 para claridad)
top_regions = df_rech0['HV024'].value_counts().iloc[:10].index
sns.countplot(data=df_rech0[df_rech0['HV024'].isin(top_regions)], y='HV024', palette='viridis', ax=axes[1], order=top_regions)
axes[1].set_title('Top 10 Regiones Encuestadas (HV024)')

plt.tight_layout()
save_fig("01_top_10_regiones_encuestadas_hv024")

# %%
# Verificación de Estabilidad Muestral a lo largo del tiempo (Sanity Check por Año)
# Nos aseguramos de que el INEI no haya cambiado radicalmente su diseño de muestra entre 2007 y 2024
# (Ej. Encuestar 80% Rural en 2007 y luego 10% Rural en 2024)

residencia_por_ano = df_rech0.groupby(['year', 'HV025']).size().unstack()
residencia_por_ano_pct = residencia_por_ano.div(residencia_por_ano.sum(axis=1), axis=0) * 100

plt.figure(figsize=(14, 5))
residencia_por_ano_pct.plot(kind='bar', stacked=True, color=['#66c2a5', '#fc8d62'], ax=plt.gca())
plt.title('Evolución de la Proporción Urbano vs Rural a través de los años (2007-2025)')
plt.ylabel('Porcentaje de la Muestra (%)')
plt.xlabel('Año de la Encuesta')
plt.legend(title='Tipo de Residencia', bbox_to_anchor=(1.05, 1), loc='upper left')
# Línea de referencia al 60%
plt.axhline(60, color='black', linestyle='--', alpha=0.5)
plt.tight_layout()
save_fig("02_evolucion_de_la_proporcion_urbano_vs")


# %%
# Verificación de Estabilidad Muestral Regional a lo largo del tiempo
# Un mapa de calor (Heatmap) nos mostrará si alguna región fue ignorada o fuertemente sobrerrepresentada en un año específico.

region_por_ano = df_rech0.groupby(['HV024', 'year']).size().unstack(fill_value=0)
# Normalizamos por año (qué porcentaje de todas las encuestas de ese año se hicieron en esa región)
region_por_ano_pct = region_por_ano.div(region_por_ano.sum(axis=0), axis=1) * 100

plt.figure(figsize=(16, 10))
sns.heatmap(region_por_ano_pct, cmap='YlGnBu', annot=False, cbar_kws={'label': '% de la muestra del año'})
plt.title('Mapa de Calor: Porcentaje de Muestra por Región a través de los Años (HV024)')
plt.ylabel('Región')
plt.xlabel('Año de la Encuesta')
plt.tight_layout()
save_fig("03_mapa_de_calor_porcentaje_de_muestra")


# %%
# Verificación del Tamaño de Muestra Anual (Sample Size Bias)
# Si en 2007 encuestaron a 5,000 hogares y en 2024 a 50,000, el algoritmo de IA sufriría de sesgo temporal severo hacia el presente.

tamano_muestra = df_rech0['year'].value_counts().sort_index()

plt.figure(figsize=(14, 6))
ax = sns.barplot(x=tamano_muestra.index, y=tamano_muestra.values, palette='mako')
plt.title('Auditoría Longitudinal: Total de Hogares Encuestados por Año (2007-2025)')
plt.ylabel('Cantidad de Hogares Encuestados')
plt.xlabel('Año de la Encuesta')
plt.xticks(rotation=45)

# Añadimos las etiquetas de datos sobre cada barra para mayor rigor matemático
for i, v in enumerate(tamano_muestra.values):
    ax.text(i, v + 500, f"{v:,}", color='black', ha='center', fontsize=9)

plt.tight_layout()
save_fig("04_auditoria_longitudinal_total_de_hogares_encuestados")


# %% [markdown]
# > **Conclusión y Acción (Estabilidad Geográfica y Muestral - HV024, HV025)**
# > * **Observación:** El muestreo de la ENDES tiene un sesgo rural intencional valiosísimo (~40% de la muestra es rural, aunque el país es casi 80% urbano). Temporalmente, la proporción Urbano/Rural se ha mantenido estable, pero descubrimos que la cantidad de encuestas da un "Salto" gigantesco en 2015, ampliando la cobertura de ~27k a ~34k hogares anuales. El mapa de calor regional confirma que ninguna región fue ignorada históricamente.
# > * **Acción a Tomar:** **Luz Verde Longitudinal.** No existe *Data Drift* geográfico que ciegue al modelo. El aumento de datos post-2015 es excelente para Machine Learning. Al tener representación nacional equilibrada, el algoritmo podrá entrenarse cruzando regiones sin sufrir sesgos centralistas.

# %% [markdown]
# ## 2. Hacinamiento: Total de Miembros en el Hogar (`HV009`)

# %%
plt.figure(figsize=(10, 5))
sns.histplot(df_rech0['HV009'].dropna(), bins=30, color='coral', discrete=True)
plt.title('Cantidad de Miembros que Viven en el Hogar (HV009)')
plt.xlabel('Número de Personas')
plt.xlim(0, 20)
save_fig("05_cantidad_de_miembros_que_viven_en")

# %%
# Evolución del Tamaño del Hogar a través de los años (Transición Demográfica)
# Verificamos si la tendencia nacional de tener familias más pequeñas se refleja en los datos.

tamano_hogar_ano = df_rech0.groupby('year')['HV009'].mean()

plt.figure(figsize=(12, 4))
sns.lineplot(x=tamano_hogar_ano.index, y=tamano_hogar_ano.values, marker='o', color='crimson', linewidth=2)
plt.title('Promedio de Personas por Hogar a través de los Años (HV009)')
plt.ylabel('Promedio de Miembros')
plt.xlabel('Año de la Encuesta')
plt.xticks(tamano_hogar_ano.index, rotation=45)
plt.grid(True, linestyle='--', alpha=0.5)

# Forzamos los límites de Y para que el cambio no se exagere visualmente
plt.ylim(tamano_hogar_ano.min() - 0.5, tamano_hogar_ano.max() + 0.5) 

plt.tight_layout()
save_fig("06_promedio_de_personas_por_hogar_a")


# %% [markdown]
# > **Conclusión y Acción (Hacinamiento y Evolución Demográfica - HV009)**
# > * **Observación:** La muestra revela el clásico "hacinamiento de riesgo" (hogares con 7 a 12 miembros). Al ver la evolución temporal, descubrimos una conexión perfecta: en 2014-2015 ocurre un salto violento en el promedio de miembros del hogar. Esto prueba matemáticamente que la ampliación de muestra del INEI en 2015 (descubierta arriba) fue dirigida específicamente a capturar familias más numerosas/periféricas que antes no eran mapeadas.
# > * **Acción a Tomar:** **Estatus de Predictor Crítico.** El tamaño del hogar es un proxy directo de pobreza extrema e infecciones (causas de desnutrición). El algoritmo debe aprender que este incremento estadístico post-2015 no significa una "explosión de natalidad repentina", sino la mejora en la focalización de la encuesta hacia zonas vulnerables.

# %% [markdown]
# ## 3. Factor Clínico: Altitud del Conglomerado (`HV040`) en m.s.n.m.
# La altitud es vital porque altera fisiológicamente los niveles de hemoglobina, lo que impacta directamente en el diagnóstico oficial de la Anemia.

# %%
plt.figure(figsize=(10, 5))
sns.histplot(df_rech0['HV040'].dropna(), bins=50, color='teal')
plt.title('Distribución de Altitud (m.s.n.m) de los Hogares (HV040)')
plt.xlabel('Altitud (Metros Sobre Nivel del Mar)')
save_fig("07_distribucion_de_altitud_m_s_n")

nulos_alt = round(df_rech0['HV040'].isna().mean() * 100, 2)
print(f"Porcentaje de nulos en Altitud (HV040): {nulos_alt}%")

# %% [markdown]
# > **Conclusión y Acción (Factor Clínico: Altitud - HV040)**
# > * **Observación:** Aunque la mayoría vive en la costa (0-500m), existe una "Meseta Andina" gigantesca de más de 100,000 hogares entre los 2,500m y 4,500m de altitud. 
# > * **Acción a Tomar:** **Ajuste Fisiológico Obligatorio.** Este hallazgo es de vida o muerte para el proyecto. A más de 2,500 metros, la hipoxia obliga al cuerpo a producir más hemoglobina. Si usamos la variable de Anemia (`HC57`) en bruto para un niño de Puno (4,000m), el modelo lo considerará "Sano" cuando en realidad tiene Anemia severa. Usaremos esta altitud exacta (`HV040`) en la Fase de *Feature Engineering* para aplicar la fórmula de penalización de la OMS sobre la hemoglobina.

# %% [markdown]
# ## 4. Auditoría de Variables Geoespaciales (GPS y UBIGEO)
#
# A diferencia de otras encuestas, el módulo `RECH0` contiene variables de geolocalización profunda (`UBIGEO`, `CODCCPP`, `NOMCCPP`, `LONGITUDX`, `LATITUDY`). 
#
# **Limitaciones para el Análisis Visual Bidimensional (EDA)**
# La representación gráfica convencional (ej. gráficos de barras) no es estadísticamente viable para el `UBIGEO` (debido a su altísima cardinalidad de >1,800 distritos) ni para las coordenadas continuas `LONGITUDX` y `LATITUDY`. Por ende, no se incluyeron en las gráficas superiores.
#
# En las siguientes celdas de código, procederemos a realizar una **Auditoría Forense de Calidad de Datos Espaciales (Nulos y Rangos de Coordenadas)** para definir nuestra estrategia de modelado futuro.

# %%
# Auditoría Rápida de Nulos en Variables Geoespaciales
geo_cols = ['UBIGEO', 'NOMCCPP', 'LONGITUDX', 'LATITUDY']
nulos_geo = df_rech0[geo_cols].isna().mean() * 100

print("=== PORCENTAJE DE NULOS EN VARIABLES GEOESPACIALES ===")
print(nulos_geo.round(2).astype(str) + " %")


# %%
# Nulos Geoespaciales Desglosados por Año
# Esta tabla revela si el INEI omitió el UBIGEO o el GPS en años específicos (Problema estructural)
geo_nulos_por_ano = df_rech0.groupby('year')[geo_cols].apply(lambda x: x.isna().mean() * 100).round(1)

print("=== % NULOS GEOESPACIALES POR AÑO ===")
print(geo_nulos_por_ano)

# Gráfico de líneas para visualizar la evolución de la calidad de datos geográficos
plt.figure(figsize=(14, 4))
sns.lineplot(data=geo_nulos_por_ano, markers=True, dashes=False)
plt.title('Evolución Histórica de los Nulos en UBIGEO y GPS (2007-2025)')
plt.ylabel('% de Nulos')
plt.xlabel('Año de la Encuesta')
plt.xticks(geo_nulos_por_ano.index, rotation=45)
plt.legend(title='Variable', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
save_fig("08_evolucion_historica_de_los_nulos_en")


# %%
# Validación Visual de Coordenadas GPS y Outliers
# Si las coordenadas están bien, todos los puntos deberían caer dentro de la "caja delimitadora" del Perú.
# (Aprox: Latitud de 0 a -19, Longitud de -68 a -82)

df_gps = df_rech0.dropna(subset=['LONGITUDX', 'LATITUDY']).copy()

print("=== RANGOS DE COORDENADAS (Global) ===")
print(df_gps[['LONGITUDX', 'LATITUDY']].agg(['min', 'max', 'mean']))
print("\n")

print("=== RANGOS DE COORDENADAS POR AÑO (Buscando al Culpable) ===")
# Agrupamos por año para rastrear en qué año exacto los encuestadores cometieron errores extremos (ej. Lat -79)
outliers_por_ano = df_gps.groupby('year')[['LONGITUDX', 'LATITUDY']].agg(['min', 'max'])
print(outliers_por_ano)

plt.figure(figsize=(7, 9))
sns.scatterplot(
    data=df_gps, 
    x='LONGITUDX', 
    y='LATITUDY', 
    alpha=0.1, 
    s=5, 
    color='purple'
)
plt.title('Sanity Check: Mapa de Coordenadas Recolectadas (Incluye Outliers)')
plt.xlabel('Longitud (Oeste a Este)')
plt.ylabel('Latitud (Norte a Sur)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
save_fig("09_sanity_check_mapa_de_coordenadas_recolectadas")


# %% [markdown]
# > **Conclusión y Acción (Auditoría Geoespacial y GPS)**
# > * **Observación:** El UBIGEO histórico es un desastre (57% de nulos estructurales porque el INEI no lo publicó entre 2007-2017). Sin embargo, el GPS tiene altísima calidad ininterrumpida desde 2010. Al mapear las coordenadas, se revelaron valores atípicos (outliers) cayendo en la Antártida o el océano atlántico por evidentes errores humanos de tipeo en el campo.
# > * **Acción a Tomar:** **Filtro Espacial y Spatial Join.** El GPS salvará el proyecto. En la fase de preparación, aplicaremos un "Bounding Box Filter" (Latitud 0 a -19, Longitud -68 a -82) para purgar las coordenadas basura. Luego, cruzaremos las coordenadas válidas contra el polígono oficial de Perú (*Spatial Join* con Geopandas) para "rescatar" algorítmicamente el distrito/UBIGEO perdido de esos 7 años de ceguera institucional.

# %% [markdown]
# ## 5. Justificación de Variables Excluidas del Análisis Visual
#
# Para mantener el rigor científico de esta auditoría, documentamos explícitamente el destino de las columnas restantes del `RECH0` que no ameritaron evaluación visual:
#
# 1. **Llaves Primarias y Punteros Geográficos (`HHID`, `HV001`, `HV002`, `NCONGLOME`, `ID1`)**:
#    *   **Naturaleza**: Tienes toda la razón: `NCONGLOME` (Conglomerado) no es un simple ID aleatorio, es una **ubicación micro-geográfica** (representa una manzana específica en la ciudad o un poblado en el campo). De hecho, las coordenadas GPS que auditamos arriba están medidas a nivel de Conglomerado para proteger la privacidad de las casas. Sin embargo, al ser un número categórico de altísima cardinalidad, no se puede graficar ni meter directo a un modelo matemático.
#    *   **Uso futuro**: Son intocables en esta etapa. Actuarán en la Fase 3 como llaves maestras (`ON HHID`, `ON NCONGLOME`, etc.) para ejecutar el `INNER JOIN` con el módulo de Niños (`RECH6`). Tras la fusión, se descartarán para que la ubicación del modelo recaiga puramente en el GPS y el UBIGEO, evitando sobreajuste (*Overfitting*).
#
# 2. **Metadatos de Control Cartográfico (`HV004`, `HV021`, `HV022`)**:
#    *   **Naturaleza**: Representan estratos matemáticos internos que usa el INEI para sortear manzanas. Carecen de poder predictivo directo para la desnutrición.
#
# 3. **Ponderador Poblacional (`HV005`)**:
#    *   **Naturaleza**: Factor de expansión matemático (Weight). Indica a cuántos miles de peruanos representa ese hogar. 
#    *   **Uso futuro**: No es una variable predictiva (Feature). Se usará para balancear la función de pérdida (*Loss Function*) del modelo de Machine Learning.
#
# 4. **Logística de la Entrevista (`HV008`, `HV015`, `HV035`)**:
#    *   **Naturaleza**: Detalles operativos (fecha, resultado de visita). Al haber retenido solo entrevistas exitosas, tienen varianza cero.
#
# 5. **Visitantes Temporales (`HV012`, `HV013`, `HV014`)**:
#    *   **Naturaleza**: Cuentan personas "de paso" que durmieron anoche en la vivienda. Para medir el hacinamiento estructural, usamos el `HV009` (Residentes habituales) que es clínicamente superior.
#

# %% [markdown]
# ## Análisis de Nulidad Estructural (Missing Values) - RECH0 (Datos de la Entrevista)
#
# Para garantizar la integridad del modelo de Machine Learning, sometemos las variables preservadas en este módulo a una prueba de nulidad histórica. 
# Cualquier variable que supere el **umbral de riesgo del 60%** será considerada ruido estadístico (Data Drift) y será una candidata principal para su eliminación en la fase de *Feature Engineering*.

# %%
from mnp.config import INTERIM_DATA_DIR
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_missing = pd.read_parquet(INTERIM_DATA_DIR / 'rech0_cleaned.parquet')

nulls = df_missing.isnull().sum()
nulls_pct = (nulls / len(df_missing)) * 100
df_nulls = pd.DataFrame({'Variable': nulls_pct.index, 'Nulidad_Porcentaje': nulls_pct.values})
from mnp.configs.column_labels import LABELS
df_nulls['Desc'] = df_nulls['Variable'].map(lambda x: LABELS.get(x, x))
import textwrap
df_nulls['Desc'] = df_nulls['Desc'].apply(lambda x: textwrap.fill(str(x), width=50))
df_nulls = df_nulls[df_nulls['Nulidad_Porcentaje'] > 0].sort_values('Nulidad_Porcentaje', ascending=False)

plt.figure(figsize=(14, 8))
if len(df_nulls) > 0:
    sns.barplot(data=df_nulls.head(30), x='Nulidad_Porcentaje', y='Desc', palette='Reds_r')
    plt.title('Variables con mayor % de Valores Nulos (Data Drift Histórico) en RECH0 (Datos de la Entrevista)')
    plt.xlabel('% de Valores Nulos (NaN)')
    plt.ylabel('Código de Variable')
    plt.axvline(x=60, color='black', linestyle='--', linewidth=2, label='Umbral de Riesgo ML (60% Nulos)')
    plt.legend()
else:
    plt.text(0.5, 0.5, '¡Cero Valores Nulos detectados en este Dataset!', 
             horizontalalignment='center', verticalalignment='center', fontsize=20, color='green')
    plt.axis('off')

plt.tight_layout()
save_fig("10_variables_con_mayor_de_valores_nulos")

# %% [markdown]
# > **Implicación para el Modelado:** Todo aquello que cruce la línea punteada negra (60%) nos indica que la pregunta no se realizó sistemáticamente a lo largo de los 18 años, o bien dependía de una sub-muestra muy pequeña. Intentar imputar estas variables destruiría la varianza del modelo.
