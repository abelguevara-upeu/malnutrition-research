# Guía de EDA — Investigación de Desnutrición Infantil (ENDES)

> **Propósito de este documento:** Describir el proceso correcto de Análisis Exploratorio de Datos (EDA)
> aplicado a este proyecto, qué se hace en cada fase, y cómo cada análisis responde preguntas concretas
> que alimentan decisiones de limpieza y modelado.

---

## El pipeline completo: de datos crudos al modelo

El EDA no termina con gráficos bonitos — es parte de un pipeline más largo donde cada etapa
alimenta a la siguiente. La clave es **no mezclar etapas**: explorar no es limpiar, y limpiar
no es seleccionar features.

```
 ENTENDER LOS DATOS                PREPARAR EL MODELO              MODELAR
 ──────────────────────────────    ───────────────────────────     ─────────

  Módulo RECH6  ─┐
  Módulo RECH0  ─┤  EDA por módulo    ─→  JOIN master   ─→  Screening X~Y
  Módulo RECH23 ─┤  (diagnóstico)         (02_join)          (03_screening)
  Módulo Mujer  ─┘  (01_eda_*)                                     │
                         │                                          ▼
                         ▼                                   Feature Selection
                     Limpieza                                 (05_features)
                    (02_join +                                      │
                    cleaning)                                       ▼
                         │                                   Feature Engineering
                         ▼                                    (05_features)
                    EDA Fase 2                                      │
                   (validación +                                    ▼
                    análisis)                                    Modelo
                  (04_eda_clean)                               (06_model)
```

---

## La diferencia entre cada etapa

| Etapa | Pregunta que responde | Herramienta | Output |
|---|---|---|---|
| **EDA Fase 1** | ¿Qué son mis datos? ¿Son válidos? | Estadística descriptiva, histogramas, missings | Decisiones de limpieza |
| **Limpieza** | ¿Qué elimino y por qué? | Criterios explícitos documentados | `master_cleaned.csv` |
| **EDA Fase 2** | ¿La limpieza fue correcta? ¿Qué veo? | Prevalencias, tendencias, subgrupos | Hallazgos descriptivos |
| **Screening** | ¿Cuáles variables se asocian con Y? | Chi², correlación + corrección FDR | Lista de candidatas X |
| **Feature Selection** | ¿Cuáles variables *mejoran* el modelo? | Lasso, RFE, importancia RF | Variables finales |
| **Feature Engineering** | ¿Puedo crear mejores variables? | Dominio + transformaciones | Nuevas columnas |

> [!IMPORTANT]
> El **screening** (EDA) y el **feature selection** (modelado) son etapas distintas.
> El screening te dice qué variables tienen señal estadística.
> El feature selection te dice qué variables el modelo realmente necesita.
> Uno sin el otro lleva a modelos con ruido o variables redundantes.

---

## Estructura de notebooks recomendada

Como el proyecto une **múltiples módulos de ENDES** con cientos de variables en total,
se recomienda perfilar **cada módulo por separado** antes de hacer el JOIN.

```
notebooks/
├── 01_eda_rech6.ipynb          ← Perfil de Antropometría (outcomes Y)
├── 01_eda_rech0.ipynb          ← Perfil de Hogar
├── 01_eda_rech23.ipynb         ← Perfil de Vivienda
├── 01_eda_mujer.ipynb          ← Perfil del módulo Mujer
│
├── 02_join_master.ipynb        ← JOIN de módulos + limpieza documentada
│                                  Output: data/interim/master_cleaned.csv
│
├── 03_screening.ipynb          ← Screening masivo: todas las X vs Y (con FDR)
│                                  Output: ranking de variables candidatas
│
├── 04_eda_clean.ipynb          ← EDA profundo solo de las variables candidatas
│                                  Validación post-limpieza + análisis descriptivo
│
├── 05_features.ipynb           ← Feature Selection + Feature Engineering
│                                  Output: data/processed/features.csv
│
└── 06_model.ipynb              ← Entrenamiento y evaluación del modelo
```

---

## Variables del proyecto

### Variables dependientes (Y) — Lo que quieres explicar/predecir

| Variable ENDES | Derivada | Indicador OMS | Umbral |
|---|---|---|---|
| `HC70` | `stunting` | Talla/Edad z-score | < −2 DE |
| `HC71` | `underweight` | Peso/Edad z-score | < −2 DE |
| `HC72` | `wasting` | Peso/Talla z-score | < −2 DE |
| `HC57A` | `anemia` | Hemoglobina ajustada | > 0 (leve/mod/severa) |

### Variables independientes (X) — Lo que quieres usar para explicar

| Fuente | Variable | Descripción | Tipo |
|---|---|---|---|
| `RECH6` | `HC1` | Edad del niño (meses) | Biológico |
| `RECH6` | `HC27` | Sexo del niño | Biológico |
| `RECH0` | `HV025` | Área urbana/rural | Contexto |
| `RECH0` | `HV270` | Quintil de riqueza | Socioeconómico |
| `RECH23` | `HV201` | Fuente de agua | Saneamiento |
| `RECH23` | `HV205` | Tipo de sanitario | Saneamiento |
| `REC0111` | `V106` | Nivel educativo de la madre | Educación |
| `REC0111` | `V012` | Edad de la madre | Biológico |
| `REC44` | — | Lactancia y alimentación | Conductual |
| `PS_QALIWARMA` | — | Beneficiario del programa | Intervención |
| `PS_VL` | — | Vaso de Leche | Intervención |

---

## EDA FASE 1 — Diagnóstico (`01_eda_raw.ipynb`)

**Regla de oro:** En esta fase **NUNCA modificas `df`**. Solo observas y documentas.
Cada análisis responde una pregunta que luego justificará una decisión de limpieza.

---

### §1 — Estructura y cobertura de los datos

**Pregunta que responde:** ¿Qué tengo y cuánto tengo?

```python
# ¿Cuántos registros hay por año?
df.groupby('year').size()

# ¿Qué columnas están presentes?
df.info()

# ¿El número de registros es consistente con lo esperado por ENDES?
# (ENDES 2024 debería tener ~X niños < 5 años)
```

**Resultado esperado:** Una tabla de cobertura año × módulo.
**Decisión que informa:** Si algún año tiene muy pocos registros, revisar la extracción antes de continuar.

---

### §2 — Calidad de datos: missings

**Pregunta que responde:** ¿Falta información? ¿El faltante es aleatorio o sistemático?

```python
# % de missings por variable y por año
missing = df.groupby('year')[ZSCORE_COLS + ['HC57A']].apply(
    lambda x: x.isna().mean() * 100
).round(1)
print(missing)

# ¿El % de inválidos (9996-9999) varía por año?
INVALID = {9996, 9997, 9998, 9999}
for col in ZSCORE_COLS:
    invalidos = df.groupby('year')[col].apply(
        lambda x: x.isin(INVALID).mean() * 100
    ).round(1)
    print(f"\n{col} — % de códigos inválidos por año:")
    print(invalidos)
```

**Lo que buscas detectar:**
- Si un año tiene 40% de missings en HC70 pero los demás tienen 5% → hay un problema de campo, no de datos
- Si los missings se concentran en una región o área → sesgo de no-respuesta sistemático

**Decisión que informa:** ¿Excluyo registros con missing, o imputo? ¿El missing es MCAR, MAR o MNAR?

---

### §3 — Calidad de datos: valores extremos y plausibilidad

**Pregunta que responde:** ¿Los datos son biológicamente posibles?

```python
# z-scores fuera de ±6 son biológicamente imposibles (WHO, 2006)
for col in ZSCORE_COLS:
    raw = pd.to_numeric(df[col], errors='coerce')
    raw_clean = raw[~raw.isin(INVALID)]
    extreme = (raw_clean.abs() > 600).sum()  # recuerda: aún sin dividir /100
    print(f"{col}: {extreme} registros con |z| > 6 DE ({extreme/len(raw_clean)*100:.1f}%)")

# Distribución cruda de z-scores (SIN limpiar)
df[ZSCORE_COLS].apply(pd.to_numeric, errors='coerce').describe()
```

**Lo que buscas detectar:**
- ¿Hay una masa de valores en 9996–9999 que no son NaN porque no se convirtieron?
- ¿La distribución ya parece normal/desplazada, o hay bimodalidad sospechosa?

**Decisión que informa:** El criterio exacto de corte para outliers (ej: excluir |z| > 6 DE).

---

### §4 — Calidad de datos: duplicados y unidad de análisis

**Pregunta que responde:** ¿Hay registros duplicados? ¿La unidad de análisis es un niño único?

```python
# ¿Hay duplicados por clave única?
clave = ['HHID', 'HVIDX', 'year']  # ajusta según tu esquema
duplicados = df[df.duplicated(subset=clave, keep=False)]
print(f"Registros duplicados: {len(duplicados)}")

# ¿Hay niños con edad fuera del rango objetivo (<5 años = <60 meses)?
df['HC1'] = pd.to_numeric(df['HC1'], errors='coerce')
print(df['HC1'].describe())
print(f"Niños >= 60 meses: {(df['HC1'] >= 60).sum()}")
print(f"Edad negativa o cero: {(df['HC1'] <= 0).sum()}")
```

**Decisión que informa:** Criterios de inclusión/exclusión (niños 0–59 meses, un registro por niño por año).

---

### §5 — Exploración univariada cruda (SIN limpiar)

**Pregunta que responde:** ¿Las distribuciones tienen la forma esperada en datos crudos?

```python
# Histograma de HC70 crudo (antes de dividir /100)
# Debería verse centrado alrededor de 0 con cola izquierda (población desnutrida)
raw_hc70 = pd.to_numeric(df['HC70'], errors='coerce')
raw_hc70_valid = raw_hc70[~raw_hc70.isin(INVALID)]
plt.hist(raw_hc70_valid / 100, bins=60)
plt.axvline(-2, color='red', label='Umbral OMS')
plt.title('HC70 crudo (antes de limpieza)')
```

**Lo que buscas detectar:**
- Picos artificiales en valores redondos (errores de entrada de datos)
- Distribución completamente inesperada (datos mal cargados)
- Comparar visualmente con la curva de referencia OMS

**Decisión que informa:** ¿La distribución es coherente con la literatura? ¿El desplazamiento hacia la izquierda es el esperado para Perú?

---

## LIMPIEZA — Documentada (`02_cleaning_decisions.ipynb`)

Cada bloque de código debe tener un comentario `# DECISIÓN:` con:
1. Qué se hace
2. Por qué (con referencia si es posible)
3. Cuántos registros afecta

**Ejemplo de buena documentación de limpieza:**

```python
# DECISIÓN: Convertir códigos inválidos (9996–9999) a NaN
# Justificación: Son códigos estándar ENDES para "no medido", "fuera de rango",
#                "no aplicable". No representan valores reales.
# Impacto: Ver §2 del EDA-1 — X% de registros por año
INVALID = {9996, 9997, 9998, 9999}
for col in ZSCORE_COLS:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df.loc[df[col].isin(INVALID), col] = np.nan

# DECISIÓN: Excluir z-scores con |valor| > 6 DE
# Justificación: WHO Child Growth Standards (2006) — valores fuera de ±6 son
#                biológicamente implausibles y se consideran errores de medición.
# Impacto: ~X registros (Y%) — ver §3 del EDA-1
for col in ZSCORE_COLS:
    df[col] = df[col] / 100  # convertir a escala real primero
    df.loc[df[col].abs() > 6, col] = np.nan

# DECISIÓN: Restringir a niños 0–59 meses
# Justificación: Los indicadores OMS (stunting, wasting, underweight) están
#                definidos solo para menores de 5 años (0–59 meses).
# Impacto: X registros excluidos
df = df[df['HC1'].between(0, 59)]
```

---

## EDA FASE 2 — Validación y Análisis (`03_eda_clean.ipynb`)

**Objetivo:** Dos cosas a la vez:
1. Verificar que la limpieza no introdujo sesgos
2. Responder las preguntas de investigación reales

---

### §1 — Validación de la limpieza

**Pregunta que responde:** ¿La limpieza fue correcta o perdí información importante?

```python
# Comparar prevalencias antes y después de la limpieza
# Si stunting baja de 22% a 10%, algo salió mal en la limpieza
print("Prevalencias post-limpieza:")
print(df.groupby('year')[['stunting','underweight','wasting','anemia']].mean() * 100)

# ¿El N por año cambió radicalmente?
print(df.groupby('year').size())

# ¿Los subgrupos (sexo, área) siguen balanceados?
print(df.groupby(['year', 'sexo']).size().unstack())
```

---

### §2 — Prevalencias longitudinales con intervalos de confianza

**Pregunta que responde:** ¿Existe una tendencia temporal real en stunting/anemia 2020–2024?

```python
from scipy.stats import kendalltau
import statsmodels.api as sm

# Cálculo de IC 95% con proporción binaria
from statsmodels.stats.proportion import proportion_confint

prev_ic = []
for yr in YEARS:
    sub = df[df.year == yr]['stunting'].dropna()
    n, k = len(sub), sub.sum()
    lo, hi = proportion_confint(k, n, alpha=0.05, method='wilson')
    prev_ic.append({'year': yr, 'prev': k/n*100, 'lo': lo*100, 'hi': hi*100})

# Test de tendencia de Mann-Kendall
tau, p = kendalltau(YEARS, [x['prev'] for x in prev_ic])
print(f"Mann-Kendall τ={tau:.3f}, p={p:.4f}")
print("→ Tendencia significativa" if p < 0.05 else "→ Sin tendencia estadística")
```

**Responde:** La línea temporal del notebook anterior mostraba tendencia. Ahora sabes si es *estadísticamente* real.

---

### §3 — Heterogeneidad por subgrupos

**Pregunta que responde:** ¿Quiénes son los más vulnerables? ¿La desigualdad cambia en el tiempo?

```python
# Stunting por área (urbana/rural) — brecha histórica clave en Perú
df.groupby(['year', 'area'])['stunting'].mean().mul(100).unstack().plot(marker='o')

# Stunting por quintil de riqueza
df.groupby(['year', 'quintil_riqueza'])['stunting'].mean().mul(100).unstack()

# Stunting por grupo de edad (ventana crítica 12–23 meses)
df.groupby('grupo_edad')['stunting'].mean().mul(100).sort_index()
```

**Responde:** Identifica grupos prioritarios para el modelo y variables candidatas a ser independientes.

---

### §4 — Asociación entre variables independientes y outcomes

**Pregunta que responde:** ¿Qué factores se asocian con mayor stunting?

```python
# Regresión logística bivariada: cada X vs stunting
from sklearn.linear_model import LogisticRegression

variables_X = ['HV025_rural', 'quintil_bajo', 'sin_agua_segura', 'madre_sin_edu']
for var in variables_X:
    sub = df[['stunting', var]].dropna()
    # OR simple
    tabla = pd.crosstab(sub[var], sub['stunting'])
    or_val = (tabla.iloc[1,1] * tabla.iloc[0,0]) / (tabla.iloc[1,0] * tabla.iloc[0,1])
    print(f"{var}: OR = {or_val:.2f}")
```

**Responde:** ¿Qué variables independientes tienen asociación suficiente para incluirlas en el modelo?

---

### §5 — Correlación entre outcomes e implicaciones para el modelo

**Pregunta que responde:** ¿Los outcomes están correlacionados? ¿Puedo modelarlos por separado o necesito un modelo multivariado?

```python
# Heatmap de correlaciones
corr = df[['HC70', 'HC71', 'HC72']].corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm')

# Co-ocurrencia: niños con más de un déficit simultáneo
df['n_deficits'] = df[['stunting','underweight','wasting']].sum(axis=1)
df['n_deficits'].value_counts(normalize=True).mul(100).round(1)
```

**Responde:** Si HC70 y HC71 tienen r > 0.8, modelarlos juntos tiene problemas de multicolinealidad.

---

### §6 — Resumen de hallazgos (tabla ejecutiva)

**Pregunta que responde:** ¿Cuáles son los 3–5 hallazgos más importantes para reportar?

```python
# Esta tabla SÍ se llena con valores reales
resumen = df.groupby('year')[['stunting','underweight','wasting','anemia']].mean().mul(100).round(1)
resumen.columns = ['Stunting (%)', 'Underweight (%)', 'Wasting (%)', 'Anemia (%)']
```

**Formato del hallazgo:**

> "La prevalencia de stunting mostró una tendencia [descendente/ascendente/estable]
> entre 2020 y 2024 (Mann-Kendall τ = X, p = Y). Los niños de área rural presentaron
> una prevalencia X puntos porcentuales mayor que los urbanos (p < 0.05).
> La co-ocurrencia de stunting y anemia afectó al X% de los niños evaluados."

---

## SCREENING — Variables candidatas (`03_screening.ipynb`)

Cuando tienes cientos de variables no puedes inspeccionarlas manualmente.
Necesitas un proceso automatizado que filtre cuáles tienen asociación real con el outcome.

> [!WARNING]
> Si haces 200 tests estadísticos con `p < 0.05`, por azar puro ~10 saldrán
> significativas sin serlo. **Siempre corrige por múltiples comparaciones (FDR)**.

---

### §1 — Perfil automático con ydata-profiling

**Pregunta que responde:** ¿Qué hay en las cientos de variables del master?

```python
from ydata_profiling import ProfileReport

# Genera reporte HTML completo para todas las variables
profile = ProfileReport(df_master, title="ENDES Master — Perfil EDA", explorative=True)
profile.to_file("reports/eda_master_profile.html")
```

**Lo que genera automáticamente por cada variable:**
- Tipo de dato, % de missings, valores únicos
- Distribución (histograma o barplot)
- Alertas: alta cardinalidad, constante, sesgada, duplicada
- Correlaciones entre variables

**Decisión que informa:** Qué variables descartar antes siquiera de hacer el screening
(constantes, casi-constantes, >70% missings, identificadores).

---

### §2 — Screening masivo con corrección FDR

**Pregunta que responde:** ¿Cuáles de las X variables se asocian significativamente con stunting/anemia?

```python
from scipy.stats import chi2_contingency, pointbiserialr
from statsmodels.stats.multitest import multipletests

outcome = 'stunting'
p_values = {}

for col in variables_X:
    sub = df_master[[outcome, col]].dropna()

    if df_master[col].dtype == 'object' or df_master[col].nunique() < 10:
        # Variable categórica → Chi²
        tabla = pd.crosstab(sub[col], sub[outcome])
        _, p, _, _ = chi2_contingency(tabla)
    else:
        # Variable continua → correlación punto-biserial
        _, p = pointbiserialr(sub[outcome], sub[col])

    p_values[col] = p

# Corrección FDR (Benjamini-Hochberg)
vars_list = list(p_values.keys())
p_list = list(p_values.values())
reject, p_corrected, _, _ = multipletests(p_list, method='fdr_bh')

# Variables que sobreviven el filtro
candidatas = [v for v, r in zip(vars_list, reject) if r]
print(f"Variables candidatas tras FDR: {len(candidatas)} de {len(vars_list)}")
```

**Resultado:** Un ranking de variables ordenadas por p-value corregido.
**Decisión que informa:** Qué variables llevar al EDA profundo (04) y al Feature Selection (05).

---

## EDA PROFUNDO — Variables candidatas (`04_eda_clean.ipynb`)

Esta es la continuación del EDA Fase 2, pero ahora **solo sobre las variables que pasaron el screening**.
Aquí ya no son cientos de variables, sino las 20–50 candidatas.

> Lo que hacías en EDA-2 §3–§6 (heterogeneidad, asociación bivariada, correlaciones,
> resumen ejecutivo) se ejecuta aquí, pero ya con propósito concreto.

Adicionalmente, en esta fase validas con literatura:
- ¿Las variables que "salieron" tienen sentido biológico o social?
- ¿Alguna variable importante según la literatura *no* salió? → revisar calidad del dato
- ¿Hay variables sorpresivas que no esperabas? → potencial hallazgo original

---

## FEATURE SELECTION (`05_features.ipynb`)

El Feature Selection es parte del **pipeline de modelado**, no del EDA.
El screening te dio candidatas con señal estadística; el feature selection elige
cuáles el modelo realmente necesita.

---

### §1 — Filter methods (independientes del modelo)

**Pregunta que responde:** ¿Hay variables redundantes o con varianza casi cero?

```python
from sklearn.feature_selection import VarianceThreshold

# Elimina variables casi-constantes (varían en < 1% de los casos)
selector = VarianceThreshold(threshold=0.01)
X_filtered = selector.fit_transform(X_candidatas)
```

---

### §2 — Embedded method: Lasso (recomendado)

**Pregunta que responde:** ¿Qué variables contribuyen al modelo de regresión logística?

```python
from sklearn.linear_model import LogisticRegressionCV
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_filtered)

# Lasso: penaliza coeficientes → los irrelevantes se van a 0
model = LogisticRegressionCV(
    penalty='l1',
    solver='liblinear',
    cv=5,
    scoring='roc_auc'
)
model.fit(X_scaled, y_stunting)

# Variables con coeficiente ≠ 0 son las seleccionadas
seleccionadas = X_candidatas.columns[model.coef_[0] != 0].tolist()
print(f"Variables seleccionadas por Lasso: {len(seleccionadas)}")
```

---

### §3 — Wrapper method: RFE (alternativa)

**Pregunta que responde:** ¿Cuál es el subconjunto óptimo de N variables?

```python
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

rfe = RFE(LogisticRegression(max_iter=1000), n_features_to_select=15)
rfe.fit(X_scaled, y_stunting)

seleccionadas_rfe = X_candidatas.columns[rfe.support_].tolist()
```

---

### §4 — Feature Engineering

**Pregunta que responde:** ¿Puedo construir variables más informativas combinando las existentes?

Ejemplos para este proyecto:

```python
# Índice compuesto de vulnerabilidad (0-3 puntos)
df['vulnerabilidad'] = (
    (df['area'] == 'Rural').astype(int) +
    (df['quintil_riqueza'] <= 2).astype(int) +
    (df['madre_educacion'] == 'Sin educación').astype(int)
)

# Interacción entre edad y área (el gap rural/urbano varía por edad)
df['edad_x_rural'] = df['HC1'] * (df['area'] == 'Rural').astype(int)

# Binning de edad en ventanas críticas de desarrollo
df['ventana_critica'] = (df['HC1'].between(6, 23)).astype(int)
```

---

## Resumen: qué pregunta responde cada notebook

| Notebook | Etapa | Pregunta central | Output concreto |
|---|---|---|---|
| **01_eda_rech6** | EDA-1 por módulo | ¿Qué hay en Antropometría? ¿Es válido? | Diagnóstico de missings, outliers, distribuciones |
| **01_eda_rech0/23/mujer** | EDA-1 por módulo | ¿Qué hay en Hogar/Vivienda/Mujer? | Idem por módulo |
| **02_join_master** | Limpieza + JOIN | ¿Cómo uno los módulos correctamente? | `master_cleaned.csv` con decisiones documentadas |
| **03_screening** | Screening | ¿Cuáles de las ~200 X se asocian con Y? | Ranking FDR → lista de candidatas (20–50 vars) |
| **04_eda_clean** | EDA-2 profundo | ¿Qué nos dicen las candidatas? ¿Validación post-limpieza? | Hallazgos descriptivos + validación con literatura |
| **05_features** | Feature Selection | ¿Cuáles variables necesita el modelo? | `features.csv` con 10–20 variables finales |
| **06_model** | Modelado | ¿Qué predice el stunting/anemia? | Modelo entrenado + métricas de evaluación |

---

## Resumen: qué pregunta responde cada sección dentro del EDA

| Sección | Pregunta central | Output concreto |
|---|---|---|
| **EDA-1 §1** | ¿Qué y cuánto tengo por módulo? | Tabla de cobertura año × módulo |
| **EDA-1 §2** | ¿Cuánto falta y por qué? | % missings por variable y año |
| **EDA-1 §3** | ¿Los valores son posibles? | Criterio de corte para outliers |
| **EDA-1 §4** | ¿Hay duplicados? ¿Cuál es la unidad? | Criterio de inclusión/exclusión |
| **EDA-1 §5** | ¿Las distribuciones son coherentes? | Histogramas crudos vs. referencia OMS |
| **Limpieza** | ¿Qué se elimina y por qué? | Log de decisiones con referencias |
| **Screening §1** | ¿Qué hay en todas las variables? | Reporte HTML de ydata-profiling |
| **Screening §2** | ¿Cuáles X se asocian con Y? | Ranking de variables por p-value FDR |
| **EDA-2 §1** | ¿La limpieza fue correcta? | Comparación N y prevalencias antes/después |
| **EDA-2 §2** | ¿Hay tendencia real en el tiempo? | Test Mann-Kendall + IC 95% |
| **EDA-2 §3** | ¿Quiénes son más vulnerables? | Prevalencias por área, quintil, edad, sexo |
| **EDA-2 §4** | ¿Qué factores se asocian con el outcome? | Odds Ratios bivariados de candidatas |
| **EDA-2 §5** | ¿Los outcomes son independientes? | Matriz de correlaciones + co-ocurrencia |
| **EDA-2 §6** | ¿Cuáles son los hallazgos clave? | Tabla ejecutiva + texto interpretativo |
| **Features §1** | ¿Hay variables redundantes? | Variables post-filtro de varianza |
| **Features §2** | ¿Cuáles mejoran el modelo (Lasso)? | Variables con coeficiente ≠ 0 |
| **Features §3** | ¿Cuál es el subconjunto óptimo (RFE)? | N variables seleccionadas |
| **Features §4** | ¿Puedo crear mejores variables? | Nuevas columnas derivadas |

---

## Referencias metodológicas

- **WHO Child Growth Standards** (2006) — criterios de z-scores y valores extremos
- **ENDES — Manual del Entrevistador** — codificación de variables HC70, HC71, HC72
- **Rubin (1976)** — tipología de missings: MCAR, MAR, MNAR
- **Mann-Kendall test** — test no paramétrico para tendencias temporales
- **Wilson interval** — intervalo de confianza para proporciones pequeñas
- **Benjamini & Hochberg (1995)** — corrección FDR para múltiples comparaciones
- **Tibshirani (1996)** — Lasso para selección de variables en regresión
