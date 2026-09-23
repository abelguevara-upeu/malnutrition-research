# CAPÍTULO 2: METODOLOGÍA

**Título del Proyecto:** *Sistema Predictivo de Riesgo de Desnutrición Crónica Infantil en el Perú mediante Machine Learning y Datos de Encuesta de Hogar (ENDES 2007–2024)*  
**Línea de Investigación:** Inteligencia Artificial Aplicada / Informática de la Salud  
**Autores:** Abel Guevara Huasco, Verónica Vergara Rojas, Pamela Vallejos Cotrina  
**Institución:** Universidad Peruana Unión · Facultad de Ingeniería y Arquitectura · Escuela Profesional de Ingeniería de Sistemas  

---

## 2.1 Enfoque y Diseño Metodológico de Ingeniería

La presente investigación adopta un enfoque **cuantitativo, aplicado y de nivel explicativo-predictivo**, bajo un diseño **no experimental, longitudinal de tendencia** (Hernández-Sampieri et al., 2014). El objetivo central de ingeniería es diseñar, entrenar, validar y desplegar un sistema computacional capaz de identificar perfiles de riesgo de desnutrición crónica infantil a nivel sociodemográfico y territorial en el Perú.

Para la construcción del producto de software e inteligencia artificial, se adopta el estándar internacional **CRISP-DM** (*Cross-Industry Standard Process for Data Mining*) propuesto por Wirth y Hipp (2000), el cual articula el ciclo de vida analítico en seis fases iterativas y reproducibles:

```
                                  CICLO METODOLÓGICO CRISP-DM
                                               │
     ┌─────────────────────────────────────────┼─────────────────────────────────────────┐
     ▼                                         ▼                                         ▼
 1. Comprensión del Negocio              2. Comprensión de los Datos               3. Preparación de Datos
 • Triaje preventivo MINSA/MIDIS         • ENDES 2007–2024 (18 años)               • Anti-Leakage Protocol
 • Maximización de Recall (≥80%)         • N = 285,284 registros                  • Selección en 4 fases (43 vars)
                                               │
     ┌─────────────────────────────────────────┼─────────────────────────────────────────┐
     ▼                                         ▼                                         ▼
 4. Modelado y Benchmarking              5. Explicabilidad (XAI)                   6. Despliegue y Validación
 • 6 Algoritmos (LightGBM Campeón)       • SHAP Values (TreeExplainer)             • Prototipo Web Streamlit
 • 5-Fold CV + Ponderación HV005         • Descomposición regional/departamental   • 3 Ejes de Validación UPeU
```

---

## 2.2 Población, Muestra y Fuente de Datos

### 2.2.1 Origen de los Datos (ENDES 2007–2024)
La fuente primaria de información corresponde a los microdatos anonimizados de la **Encuesta Demográfica y de Salud Familiar (ENDES)**, recolectados y publicados anualmente por el **Instituto Nacional de Estadística e Informática (INEI)**. Se integró una serie histórica longitudinal de **18 años continuos (2007 a 2024)**.

### 2.2.2 Población Objetivo y Criterios de Inclusión
* **Población:** Niños y niñas menores de 5 años (0 a 59 meses de edad) residentes habituales en hogares peruanos.
* **Criterios de Inclusión:**
  1. Registros con entrevista individual y de hogar completa (`HV015 == 1`).
  2. Niños con medición antropométrica válida y z-score de talla para la edad calculado (`HC70` no nulo).
  3. Niños que cumplieron la auditoría biológica de consistencia en el cruce materno-infantil (coincidencia $\ge 99.9\%$ en sexo y año de nacimiento).
* **Muestra Final de Entrenamiento y Validación:** **285,284 registros individuales**, representativos a nivel nacional, por área de residencia (urbana/rural) y en los 25 departamentos del Perú.

### 2.2.3 Definición Operacional de la Variable Objetivo ($Y$)
La variable dependiente es la **Desnutrición Crónica Infantil (DCI)**, codificada como una variable binaria:
$$Y = \begin{cases} 1, & \text{si } \text{HAZ} < -2.00\text{ Desviaciones Estándar (Caso positivo)} \\ 0, & \text{si } \text{HAZ} \ge -2.00\text{ Desviaciones Estándar (No desnutrido)} \end{cases}$$
Donde $\text{HAZ}$ representa el puntaje $Z$ de la Talla para la Edad (*Height-for-Age Z-score*, variable `HC70` dividida entre 100), según los estándares antropométricos de la Organización Mundial de la Salud (OMS, 2006). La prevalencia global en la muestra es del **16.1%** (desbalance de clases 1:5.2).

### 2.2.4 Arquitectura de Integración Relacional de Módulos
Para consolidar las dimensiones del niño, la madre y el hogar, se diseñó un pipeline de unión relacional (*joins*) a través de llaves primarias compuestas (`HHID` y `CASEID`):

| Módulo ENDES | Denominación Técnica | Dimensiones Aportadas |
|---|---|---|
| **`RECH0`** | Características de la Entrevista | Estado de participación, fecha y resultado de visita. |
| **`RECH1`** | Padrón del Hogar (*Household Roster*) | Demografía básica, parentesco, edad y sexo de miembros. |
| **`RECH6`** | Salud Infantil y Antropometría | Diagnóstico de anemia (`HC56`/`HC57`), target `HC70` y edad en meses (`HC1`). |
| **`RECH23`** | Características del Hogar y Vivienda | Acceso a agua potable, saneamiento, pisos, combustible y altitud (`HV040`). |
| **`REC41`** | Salud Materna e Historia del Embarazo | Controles prenatales, peso al nacer (`m19`), tamaño al nacer y lactancia materna. |
| **`REC21`** | Tabla Puente Materno-Infantil | Vinculación foránea segura entre el niño (`RECH6`) y su madre biológica (`REC41`). |

---

## 2.3 Preparación de Datos e Ingeniería de Características

### 2.3.1 Protocolo de Prevención de Fuga de Datos (*Anti-Leakage Protocol*)
Para garantizar la validez metodológica y evitar el sobreajuste artificial (*data leakage*):
1. **Exclusión de Métricas Antropométricas Crudas:** Se prohibió terminantemente el uso de la talla en centímetros (`HC3`) y peso crudo (`HC2`), dado que definen matemáticamente la variable objetivo.
2. **Restricción de Temporalidad Estricta:** Se eliminaron variables que representan eventos o tratamientos médicos posteriores al diagnóstico.

### 2.3.2 Pipeline de Selección de Variables en Cuatro Fases
El conjunto inicial de 189 columnas crudas fue depurado mediante un protocolo estadístico riguroso:

```
 [189 Variables Crudas]
         │
         ▼ (Fase 1: Guillotina de Nulos > 60%)
  [146 Variables con Información Suficiente]
         │
         ▼ (Fase 2: Filtro de Colinealidad VIF / r > 0.80)
  [103 Variables No Redundantes]
         │
         ▼ (Fase 3: Pruebas Bivariadas χ² y Kruskal-Wallis, p < 0.05)
  [74 Variables Significativas]
         │
         ▼ (Fase 4: Importancia Multivariada LightGBM/XGBoost ≥ 10)
  [43 Variables Finales de Producción]
```

1. **Fase 1 (Completitud de Datos):** Eliminación de columnas con más del 60% de valores ausentes estructurales históricos.
2. **Fase 2 (Colinealidad):** Descarte de 43 variables redundantes (coeficiente de Pearson/Spearman $r > 0.80$ y Factores de Inflación de Varianza $\text{VIF} > 5$).
3. **Fase 3 (Filtro Bivariado):** Pruebas de $\chi^2$ de Independencia para atributos categóricos y pruebas no paramétricas de Kruskal-Wallis para numéricos ($p < 0.05$).
4. **Fase 4 (Selección Multivariada):** Selección de las 43 variables con peso algorítmico ($\text{feature importance} \ge 10$) en árboles de gradiente, preservando el 100% de la capacidad discriminativa del modelo.

---

## 2.4 Modelado y Benchmarking de Algoritmos

### 2.4.1 Validación Cruzada Estratificada y Ponderación Demográfica
Para reflejar la estructura poblacional del Perú y evitar sesgos de sobremuestreo urbano, cada iteración incorporó el **factor de ponderación muestral de la ENDES**:
$$w_i = \frac{\text{HV005}_i}{1,000,000}$$
Se utilizó **Stratified 5-Fold Cross-Validation**, preservando la prevalencia de desnutrición (16.1%) en cada partición de entrenamiento y test.

### 2.4.2 Algoritmos Evaluados
Se implementó un benchmarking controlado sobre 6 familias de algoritmos:
1. **Regresión Logística (L2 Regularized):** Modelo lineal paramétrico de línea base.
2. **Árbol de Decisión (CART):** Algoritmo no lineal de corte único.
3. **XGBoost (*Extreme Gradient Boosting*):** Ensamble de árboles con One-Hot Encoding.
4. **CatBoost:** Ensamble optimizado para variables categóricas con particiones simétricas.
5. **Red Neuronal Perceptrón Multicapa (MLP 3×200):** Arquitectura profunda de aprendizaje denso.
6. **LightGBM (*Light Gradient Boosting Machine*):** Ensamble basado en histogramas con soporte nativo para variables categóricas.

### 2.4.3 Selección del Modelo Campeón (LightGBM)
LightGBM fue seleccionado como el algoritmo de producción debido a:
* **Mayor Capacidad Discriminativa:** $\text{AUC-ROC} = 0.8308$ y $\text{Recall} = 76.49\%$ (a umbral 0.50).
* **Manejo Categórico Nativo:** Agrupamiento óptimo de categorías sin explosión dimensional.
* **Eficiencia Computacional:** Tiempo de entrenamiento $< 3.5\text{ segundos}$ sobre 285,284 filas.

---

## 2.5 Inteligencia Artificial Explicable (XAI con SHAP)

Para garantizar la auditabilidad del modelo y evitar el efecto "caja negra", se implementó el framework **SHAP (SHapley Additive exPlanations)** propuesto por Lundberg y Lee (2017), fundamentado en la teoría de juegos cooperativos:
$$f(x) = \phi_0 + \sum_{j=1}^{M} \phi_j(x)$$
Donde $\phi_j$ representa la contribución marginal neta de la variable $j$ sobre la predicción del niño.

* **Explicabilidad Local:** Cada predicción en la app Streamlit descompone el riesgo individual en factores agravantes (rojo) y protectores (azul).
* **Explicabilidad Global y Territorial:** Se calcularon los valores SHAP sobre una muestra representativa de 10,000 niños, generando perfiles de riesgo específicos para los 25 departamentos y las 3 regiones naturales (Costa, Sierra y Selva).

---

## 2.6 Protocolo de Validación (Los 3 Ejes)

Para certificar los resultados ante la comunidad científica y académica, se estableció un plan estructurado en 3 ejes:

```
                            PLAN DE VALIDACIÓN METODOLÓGICA
                                          │
     ┌────────────────────────────────────┼────────────────────────────────────┐
     ▼                                    ▼                                    ▼
 📊 EJE 1: CONFIABILIDAD              🔬 EJE 2: REPLICABILIDAD             💻 EJE 3: PERTINENCIA TÉCNICA
 • Bootstrap 1,000 iters (IC 95%)     • Modularización en mnp/ (.py)       • Juicio de 3 Expertos en DS/ML
 • Test de DeLong (p < 0.001)         • Contenedor Docker + pyproject.toml • Coeficiente V de Aiken ≥ 0.80
 • Calibración Umbral (Recall ≥ 80%)  • Pipeline reproducible (Makefile)   • Evaluación de Usabilidad SUS ≥ 75
 • Determinismo (random_state = 42)   • Depósito Zenodo con DOI citable    • Auditoría Cero Data Leakage
```

1. **Confiabilidad:**
   * *Bootstrapping no paramétrico ($B=1,000$ iters):* Estimación de Intervalos de Confianza al 95% para $\text{AUC} \in [0.820, 0.840]$ y $\text{Recall} \in [75.0\%, 78.5\%]$.
   * *Test de DeLong:* Verificación de superioridad estadística ($p < 0.001$) frente a baselines.
   * *Calibración de Umbral:* Optimización del punto de corte ($\tau \approx 0.35$) para garantizar $\text{Recall} \ge 80.0\%$.
2. **Replicabilidad (Principios FAIR):**
   * *Migración a Python Puro:* Modularización del código en el paquete `mnp/` para ejecución vía `make pipeline`.
   * *Aislamiento:* Contenedorización completa con Docker y dependencias congeladas en `pyproject.toml`.
   * *Datos Abiertos:* Registro público del dataset final y artefactos serializados en **Zenodo** con **DOI citable**.
3. **Pertinencia Técnica (Juicio de Expertos):**
   * Evaluación por un panel de **3 profesionales e investigadores en Ciencia de Datos y Machine Learning**.
   * Medición de validez de contenido mediante el **Coeficiente V de Aiken ($\ge 0.80$)** y usabilidad técnica del software con la escala **SUS ($\ge 75\text{ puntos}$)**.

---

## 2.7 Arquitectura de Software y Despliegue

El sistema predictivo fue empaquetado como una solución interactiva de toma de decisiones utilizando **Streamlit**, estructurada en tres capas de arquitectura:

```
 ┌────────────────────────────────────────────────────────────────────────┐
 │                      CAPA DE PRESENTACIÓN (UI)                         │
 │   • Tab 1: Mapa Coroplético Territorial (GeoJSON 25 Departamentos)    │
 │   • Tab 2: Predictor Individual con Descomposición de Factores SHAP    │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │
 ┌───────────────────────────────────▼────────────────────────────────────┐
 │                     CAPA LÓGICA Y MODELADO (ML)                        │
 │   • Motor de Inferencia LightGBM (`champion_lightgbm.pkl`)             │
 │   • Calibrador de Umbral Dinámico de Triaje (Target Recall ≥ 80%)      │
 │   • Explicador SHAP TreeExplainer en Tiempo Real                       │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │
 ┌───────────────────────────────────▼────────────────────────────────────┐
 │                     CAPA DE DATOS Y PERSISTENCIA                       │
 │   • Dataset Maestro Procesado (`master_preprocessed_v2.parquet`)       │
 │   • Metadatos y Configuración (`champion_metadata.json`)               │
 └────────────────────────────────────────────────────────────────────────┘
```

---

## Referencias Bibliográficas del Capítulo

* Aiken, L. R. (1985). Three coefficients for analyzing the reliability and validity of ratings. *Educational and Psychological Measurement*, 45(1), 131–142.
* Bangor, A., Kortum, P. T., & Miller, J. T. (2008). An empirical evaluation of the System Usability Scale. *International Journal of Human-Computer Interaction*, 24(6), 574–594.
* Davis, F. D. (1989). Perceived usefulness, perceived ease of use, and user acceptance of information technology. *MIS Quarterly*, 13(3), 319–340.
* DeLong, E. R., DeLong, D. M., & Clarke-Pearson, D. L. (1988). Comparing the areas under two or more correlated receiver operating characteristic curves: a nonparametric approach. *Biometrics*, 44(3), 837–845.
* Efron, B., & Tibshirani, R. J. (1994). *An introduction to the bootstrap*. CRC Press.
* Hernández-Sampieri, R., Fernández-Collado, C., & Baptista-Lucio, P. (2014). *Metodología de la investigación* (6ta ed.). McGraw-Hill.
* Kohavi, R. (1995). A study of cross-validation and bootstrap for accuracy estimation and model selection. *IJCAI*, 2, 1137–1143.
* Lipton, Z. C., Elkan, C., & Narayanaswamy, B. (2014). Optimal thresholding of classifiers to maximize F1 measure. *ECML PKDD 2014*, 225–239.
* Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. *Advances in Neural Information Processing Systems (NeurIPS 30)*, 4765–4774.
* Organización Mundial de la Salud. (2006). *WHO Child Growth Standards: Length/height-for-age, weight-for-age, weight-for-length, weight-for-height and body mass index-for-age*. OMS.
* Wilkinson, M. D. et al. (2016). The FAIR Guiding Principles for scientific data management and stewardship. *Scientific Data*, 3, 160018.
* Wirth, R., & Hipp, J. (2000). CRISP-DM: Towards a standard process model for data mining. *Proceedings of the 4th International Conference on the Practical Applications of Knowledge Discovery and Data Mining*, 29–39.

