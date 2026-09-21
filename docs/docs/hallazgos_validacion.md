# Hallazgos de validación del modelo

Registro de las comprobaciones hechas sobre el modelo campeón, con el procedimiento
seguido y la lectura de cada resultado. Sirve como respaldo para responder preguntas
del panel de expertos y como material para la sección de discusión del artículo.

---

## 1. Aporte de la hemoglobina (`HC56`)

**Por qué se midió.** De las 45 variables del modelo, `HC56` es la única que exige un
procedimiento sobre el niño —una punción para el tamizaje de anemia—. El resto se obtiene
por entrevista al hogar. Si su aporte fuera pequeño, el sistema podría operar en zonas
donde ese tamizaje no está disponible.

**Procedimiento.** `mnp/evaluation/ablation_hemoglobina.py`. Se entrenan dos
configuraciones bajo el protocolo del benchmark —`StratifiedKFold` de 5 pliegues,
`random_state = 42`, ponderación `HV005` en entrenamiento y evaluación, mismos
hiperparámetros— de modo que la única fuente de variación sea la ausencia de la variable.
Sobre las probabilidades *out-of-fold* se remuestrea la diferencia de AUC 1,000 veces.

**Resultado.**

| Configuración | AUC | Cobertura | Precisión |
|---|---:|---:|---:|
| Con hemoglobina (45 variables) | 0.8294 | 76.43% | 36.36% |
| Sin hemoglobina (44 variables) | 0.8281 | 76.30% | 36.19% |
| **Diferencia** | **−0.0014** | −0.13 pts | −0.17 pts |

Bootstrap de la diferencia: **−0.0014, IC 95% [−0.0019, −0.0009]**.

**Lectura.** El intervalo no cruza el cero, de modo que la diferencia es estadísticamente
distinguible. Eso era previsible: con 304,271 registros, diferencias muy pequeñas alcanzan
significación. Lo relevante es la magnitud: **trece casos menos detectados por cada diez
mil niños evaluados**.

La conclusión defendible es que la hemoglobina **aporta, pero poco**. El sistema puede
operar solo con datos de entrevista a un costo bajo, lo que amplía su aplicabilidad a
contextos sin tamizaje rutinario.

> **Nota sobre una versión anterior.** Una primera corrida exploratoria, sin intervalos de
> confianza, llevó a describir la diferencia como «inapreciable». Al formalizar el
> experimento con bootstrap, esa caracterización resultó inexacta y se corrigió tanto aquí
> como en la presentación al panel.

---

## 2. Suficiencia del subconjunto de variables

**Por qué se midió.** Para descartar que la reducción de más de 180 variables a 45 hubiera
dejado fuera señal predictiva relevante.

**Procedimiento.** `mnp/evaluation/feature_ablation.py`. Se ordenan las 33 columnas
descartadas por su señal marginal frente al objetivo y se reincorporan las diez de mayor
señal —material de paredes, piso y techo, fuente de agua, departamento, cloro residual,
combustible de cocina y servicio higiénico— en tres configuraciones sucesivas.

**Resultado.** El AUC, la cobertura y la precisión permanecen invariables hasta la cuarta
cifra decimal en las tres ampliaciones (0.8295 y 76.44% en todas).

**Lectura.** Las variables candidatas no aportan porque el subconjunto retenido **ya
representa el mismo constructo** a través de diecinueve atributos correlacionados de
vivienda, agua y saneamiento. Su exclusión fue una decisión correcta, no una omisión.

Un clasificador entrenado *solo* con el bloque de agua, saneamiento y vivienda alcanza AUC
0.6895, de modo que la señal existe; simplemente está ya capturada.

---

## 3. Estabilidad frente a la incorporación de un año nuevo

**Por qué se midió.** El INEI publicó la ENDES 2025 durante la ejecución del proyecto, y
convenía comprobar si el modelo se sostenía al ampliar la serie de 18 a 19 años.

**Resultado.**

| | 18 años (2007–2024) | 19 años (2007–2025) |
|---|---:|---:|
| Registros | 285,284 | 304,271 |
| AUC | 0.8308 | 0.8295 |
| Cobertura | 76.49% | 76.44% |
| Variables | 43 | 45 |

**Lectura.** El desplazamiento del AUC (−0.0013) queda dentro de la dispersión entre
pliegues (0.8230–0.8353), de modo que el modelo es estable. LightGBM se mantiene como
campeón y el orden del *benchmarking* no varía.

Dos variables nuevas —`HV219`, sexo del jefe del hogar, y `SH77F`, otro tipo de
transporte— cruzaron el umbral de importancia con el año adicional, sin que ninguna de las
43 originales fuera descartada. Esto refuerza el resultado del punto 2: cuando una variable
descartada tiene señal real, el propio criterio de importancia la recupera al haber más
datos.

---

## 4. Confiabilidad estadística del modelo campeón

**Procedimiento.** `mnp/evaluation/bootstrap_validation.py`. Remuestreo no paramétrico de
1,000 repeticiones sobre las probabilidades *out-of-fold*, y prueba de DeLong sobre curvas
ROC correlacionadas frente a los dos algoritmos de referencia.

**Resultado.**

| Métrica | Estimación | IC 95% |
|---|---:|---|
| AUC-ROC | 0.8294 | [0.8267, 0.8324] |
| Cobertura | 76.43% | [75.88%, 76.98%] |
| Precisión | 36.36% | [35.94%, 36.71%] |

Prueba de DeLong: LightGBM supera a XGBoost (*z* = 62.32) y a Regresión Logística
(*z* = 61.48), ambos con *p* < 10⁻³⁰⁰.

**Lectura.** La amplitud de los intervalos es inferior a medio punto porcentual, lo que
indica que las estimaciones no dependen del subconjunto de evaluación. La superioridad
sobre los modelos de referencia no es atribuible al azar.

> **Precisión metodológica.** El estadístico de DeLong se define sobre rangos y no admite
> ponderación muestral, de modo que los AUC de ese contraste (0.8193, 0.7775 y 0.7767) van
> sin expandir por `HV005` y quedan sistemáticamente por debajo de los ponderados. La
> comparación sigue siendo válida porque los tres modelos se evalúan sobre los mismos
> individuos.

---

## 5. Calibración del umbral de decisión

**Procedimiento.** `mnp/evaluation/threshold_curve.py`. Barrido del punto de corte sobre
probabilidades *out-of-fold*, con el mismo protocolo del benchmark.

**Resultado.** El valor mínimo que garantiza una cobertura ≥ 80% es **τ = 0.45**, con
cobertura 80.46% y precisión 34.04%.

**Lectura.** Los documentos del ciclo anterior consignaban τ ≈ 0.35 para esa meta. Ese
valor produce en realidad 87.95% de cobertura y 29.36% de precisión: sobrepasa el objetivo
y sacrifica precisión sin necesidad. La cifra fue corregida en la metodología y en el plan
de validación.

---

## 6. Figuras disponibles para la presentación

Inventario de las 45 figuras que generan los scripts, con su aptitud para un panel clínico.
Ruta base: `reports/figures/`.

### Recomendadas

| Figura | Ruta | Por qué |
|---|---|---|
| Evolución del desbalance de clases | `01_data_understanding/clean/01_eda_interim_rech6/09_*` | Muestra la caída de la desnutrición crónica del 32% en 2007 al 12% en 2025. Autoexplicativa, sin vocabulario técnico, y justifica de un vistazo por qué el problema sigue vigente pese a la mejora |
| Curva de acumulación clínica | `01_data_understanding/clean/01_eda_interim_rech6/11_*` | El Z-score cae entre los 15 y 22 meses de edad: es la ventana de los primeros 1000 días que el panel conoce bien. Requiere recortarla a un solo año y corregir el título, que aún dice 2019-2024 |
| Distribución del Z-score | `01_data_understanding/clean/01_eda_interim_rech6/10_*` | Sitúa el umbral de −2 DE sobre la distribución real, y explica el criterio diagnóstico sin recurrir a la definición formal |

### Solo si hay preguntas técnicas

| Figura | Ruta | Observación |
|---|---|---|
| Curvas ROC | `03_modeling/03_model_benchmarking_extended/01_*` | Estándar para comparar los seis algoritmos, pero exige explicar qué es una curva ROC. Reservar para el anexo |
| Mapa de calor SHAP por departamento | `03_modeling/03_model_explainability/02_*` | El contenido es el más valioso del proyecto —los factores cambian según el departamento— pero los ejes llevan nombres de variable ENDES (`HV271_Factor_de_puntuacion...`) y resulta ilegible para quien no conoce el diccionario. Conviene rehacerla con etiquetas en lenguaje natural y menos columnas |

### No recomendadas para esta sesión

Las figuras de auditoría de nulos, deriva de esquema y evolución de materiales de vivienda
(`05_evolucion_de_las_excusas_de_no`, `15_variables_con_mayor_de_valores_nulos`,
`03_evolucion_historica_del_material_de_techos`, entre otras) documentan el trabajo de
preparación de datos. Son pertinentes para el artículo y para un jurado de ingeniería, pero
no aportan al juicio de utilidad que se pide al panel clínico.

> **Preferible a cualquier figura:** la demostración en vivo del aplicativo. El panel valora
> la facilidad de uso, y para responder esa mitad del instrumento necesita haber visto la
> interfaz en funcionamiento.
