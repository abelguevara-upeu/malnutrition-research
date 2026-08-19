# UNIVERSIDAD PERUANA UNIÓN
## FACULTAD DE INGENIERÍA Y ARQUITECTURA
### Escuela Profesional de Ingeniería de Sistemas

---

# INFORME DE EVALUACIÓN CRÍTICA DE RESULTADOS DE INVESTIGACIÓN

**Asignatura:** Investigación V (Ciclo X – 2026-II)  
**Docente:** Mg. Nemias Saboya Rios  
**Entregable:** Sesión 01 – MOMENTO 6: CREA (Informe PDF)  
**Fecha:** Agosto 2026  

**Título del Proyecto de Tesis:**  
*Sistema Predictivo de Riesgo de Desnutrición Crónica Infantil en el Perú mediante Machine Learning y Datos de Encuesta de Hogar (ENDES 2007–2024)*

**Equipo de Trabajo:**
- Abel Guevara Huasco
- Verónica Vergara Rojas
- Pamela Vallejos Cotrina

---

## 1. INTRODUCCIÓN Y CONTEXTUALIZACIÓN DE LOS RESULTADOS

El presente informe realiza una evaluación crítica y rigurosa de los resultados obtenidos en el proyecto de tesis durante el ciclo anterior, aplicando los criterios de validez interna, validez externa y confiabilidad/calidad del software estudiados en la Sesión 01.

### 1.1 Síntesis del Proyecto
El objetivo central del proyecto es responder a la pregunta de investigación:  
> *¿Puede un modelo de Machine Learning identificar, con datos de encuesta de hogar, qué niños tienen mayor riesgo de desnutrición crónica infantil antes de que un agente de salud visite el domicilio?*

Se utilizó una base longitudinal de 18 años de la Encuesta Demográfica y de Salud Familiar (ENDES 2007–2024), con **285,284 niños menores de 5 años** y **43 variables sociodemográficas y de salud** seleccionadas algorítmicamente.

### 1.2 Métricas del Modelo Campeón (LightGBM)

| Métrica | Valor | Interpretación y Significado Clínico / Político |
|---|---|---|
| **AUC-ROC** | **0.8308** | Capacidad discriminativa global del 83% entre niños sanos y desnutridos. |
| **Recall (Sensibilidad)** | **76.49%** | Detecta a 3 de cada 4 niños desnutridos (34,400 de 45,000 en la muestra). |
| **Precision** | **37.05%** | 1 de cada 3 alertas de alto riesgo corresponde a un caso real confirmado. |
| **F1-Score** | **0.4976** | Balance armónico entre la cobertura de detección y la precisión. |
| **Umbral de Producción** | **0.50 (Fijo)** | Umbral por defecto, no optimizado previamente (deuda técnica). |
| **Explicabilidad (SHAP)** | Top 3 factores | Índice de riqueza (`HV271`), Peso al nacer (`m19`) y Altitud (`HV040`). |

---

## 2. EVALUACIÓN CRÍTICA DE LA VALIDEZ INTERNA

La validez interna evalúa si las predicciones se deben estrictamente al diseño metodológico y a las variables independientes, garantizando la ausencia de sesgos técnicos o artefactos.

| Aspecto Evaluado | Estado Actual | Análisis Crítico y Evidencia Técnica |
|---|---|---|
| **Validación Cruzada 5-Fold con Pesos** | **[Abordado Concretamente]** | Se incorporó el factor de expansión muestral del INEI (`HV005 / 1,000,000`), evitando el sesgo de sobre-representación urbana y manteniendo la prevalencia del 16% en cada fold. |
| **Selección Algorítmica de Variables** | **[Abordado Concretamente]** | Filtrado por importancia nativa (`feature_importances_ >= 10`), reduciendo de 74 a 43 variables. El modelo optimizado mejoró el AUC (`0.830779` vs. `0.830680`), eliminando ruido. |
| **Descarte de Métrica Inadecuada** | **[Abordado Concretamente]** | Se prohibió formalmente el uso de Accuracy debido al desbalance de clases (16% desnutridos / 84% sanos), el cual habría sobreestimado el rendimiento prediciendo solo la clase mayoritaria. |
| **Suboptimización del Umbral (Threshold Drift)** | **[Parcialmente Abordado]** | El umbral fijo en `0.50` limita el Recall a `76.49%`, dejando sin detectar al 23.5% de los niños desnutridos. El objetivo de política pública exige Recall ≥ 80%, alcanzable ajustando el umbral a `~0.35`. |
| **Ajuste Fino de Hiperparámetros** | **[Parcialmente Abordado]** | Los 6 algoritmos de benchmarking se evaluaron con parámetros por defecto para garantizar imparcialidad, dejando pendiente la optimización fina con `Optuna`. |
| **Significancia Estadística e IC 95%** | **[No Abordado / Brecha]** | Los resultados se presentan como puntos fijos (`AUC = 0.8308`). Falta calcular Intervalos de Confianza al 95% mediante **Bootstrap** y realizar el **Test de DeLong** entre modelos. |

---

## 3. EVALUACIÓN CRÍTICA DE LA VALIDEZ EXTERNA

La validez externa analiza la capacidad de generalizar los hallazgos a otros periodos temporales, geografías o sistemas reales de salud pública.

| Aspecto Evaluado | Estado Actual | Análisis Crítico y Evidencia Técnica |
|---|---|---|
| **Explicabilidad Territorial y SHAP** | **[Abordado Concretamente]** | Validación sobre 285,284 registros representativos de los 25 departamentos. Se demostró la variación del riesgo por región (Costa: Riqueza; Sierra: Altitud y Hemoglobina; Selva: Peso al nacer). |
| **Sensibilidad al Target Drift Temporal** | **[Parcialmente Abordado]** | La prevalencia nacional cayó del 30% (2007) al 11% (2024). Aunque el 5-Fold CV aleatorio incluyó muestras de todos los años, no se evaluó la degradación temporal separada por épocas. |
| **Validación Temporal Out-of-Time (OOT)** | **[No Abordado / Brecha]** | Ausencia de un split temporal estricto (ej. entrenar en 2007–2021 y evaluar prospectivamente en 2022–2024), paso indispensable para certificar resiliencia operacional. |
| **Generalización en Datasets Externos** | **[No Abordado / Brecha]** | Dependencia total de la estructura SPSS de la ENDES. No se ha probado en registros administrativos de establecimientos de salud (MINSA/HIS) o padrones municipales. |
| **Gobernanza Ética de Datos** | **[No Abordado / Brecha]** | Carece de un protocolo formal de ética e interoperabilidad institucional para despliegue en entidades estatales. |

---

## 4. CONFIABILIDAD Y CALIDAD DEL SISTEMA (ISO/IEC 25010)

La confiabilidad evalúa la consistencia de los experimentos y la calidad del software según el estándar **ISO/IEC 25010**.

| Aspecto Evaluado | Estado Actual | Análisis Crítico y Evidencia Técnica |
|---|---|---|
| **Replicabilidad del Pipeline** | **[Abordado Concretamente]** | Repositorio estructurado en Python con semillas fijas (`random_state=42`), permitiendo reproducir exactamente cada métrica reportada. |
| **Prototipo Funcional de Despliegue** | **[Abordado Concretamente]** | Aplicación web interactiva desarrollada en Streamlit + Plotly, con respuesta en menos de 1 segundo por predicción individual. |
| **Control Dinámico de Umbral** | **[Parcialmente Abordado]** | La app permite simular visualmente la cobertura deseada (ej. 80% Recall), pero no persiste sesiones ni genera reportes descargables. |
| **Evaluación de Usabilidad (SUS)** | **[No Abordado / Brecha]** | No se ha aplicado el cuestionario estandarizado **SUS (System Usability Scale)** con personal sanitario en campo. |
| **Auditoría de Seguridad y Carga** | **[No Abordado / Brecha]** | Ausencia de autenticación de usuarios, encriptación de datos sensibles y pruebas de carga concurrente. |

---

## 5. MATRIZ RESUMEN DE EVALUACIÓN CRÍTICA

| Dimensión | Aspecto Evaluado | Estado Actual | Evidencia / Brecha Identificada |
|---|---|---|---|
| **Validez Interna** | Validación Cruzada 5-Fold con Pesos (`HV005`) | **[Abordado Concretamente]** | Ponderación muestral y estratificación en 5 folds. |
| **Validez Interna** | Selección de Variables (43 cols) | **[Abordado Concretamente]** | `feature_importances_ >= 10` superó al modelo de 74 vars. |
| **Validez Interna** | Optimización de Umbral | **[Parcialmente Abordado]** | Umbral fijo en `0.50`; ajustar a `~0.35` para Recall ≥ 80%. |
| **Validez Interna** | Intervalos de Confianza (95% IC) | **[No Abordado / Brecha]** | Ausencia de Bootstrap (95% IC) y test de DeLong. |
| **Validez Externa** | Explicabilidad SHAP Regional | **[Abordado Concretamente]** | SHAP beeswarm y heatmaps en 25 departamentos. |
| **Validez Externa** | Validación Temporal Out-of-Time | **[No Abordado / Brecha]** | Falta evaluar split OOT: Train 2007–2021 / Test 2022–2024. |
| **Validez Externa** | Replicación en Datasets Externos | **[No Abordado / Brecha]** | Dependencia exclusiva de la estructura ENDES. |
| **Confiabilidad** | Replicabilidad del Pipeline | **[Abordado Concretamente]** | Pipeline modular con `random_state=42`. |
| **Calidad Software** | Evaluación de Usabilidad (SUS) | **[No Abordado / Brecha]** | Cuestionario SUS pendiente de aplicación a operadores. |
| **Calidad Software** | Pruebas de Seguridad y Carga | **[No Abordado / Brecha]** | Prototipo Streamlit sin login ni cifrado. |

---

## 6. PLAN DE ACCIÓN PRIORIZADO Y MATRIZ DE ABORDAJE

Considerando la carga académica del semestre (5 asignaturas adicionales) y los compromisos laborales de prácticas pre-profesionales del equipo, se ha diseñado un **Plan de Acción Gradual y Viable**, distribuido de manera equilibrada a lo largo del semestre académico:

### 6.1 Matriz de Abordaje Distribuida

| N.º | Brecha Identificada | Acción Correctiva Propuesta | Recursos y Método | Resultado Esperado | Plazo Distribuido |
|---|---|---|---|---|---|
| **1** | Umbral `0.50` deja el Recall en `76.49%` (meta ≥ 80%). | **Optimización del Umbral (Threshold Tuning):** Barrido Grid del umbral de `0.10` a `0.50` en los 5 folds para seleccionar el corte que garantice Recall ≥ 80% con menor costo de Falsos Positivos. | Python (`scikit-learn`), `Precision-Recall Curve`, `Notebook 03`. | Recall ≥ 80.0%, Umbral óptimo `~0.35` documentado y aplicado en la app web. | **Semanas 2 – 3** *(Trabajo inicial)* |
| **2** | Falta de intervalos de confianza y p-values. | **Cálculo de IC al 95% (Bootstrap):** Muestreo Bootstrap (1,000 iteraciones) sobre el test fold para AUC y Recall. | Python (`scipy.stats`, `numpy` bootstrap). | Tablas formalizadas `AUC [IC 95%]` y `Recall [IC 95%]` para el manuscrito. | **Semanas 4 – 5** *(Previo a Parciales)* |
| **3** | Ausencia de validación ante el Target Drift histórico. | **Validación Temporal Out-of-Time (OOT):** Re-entrenar LightGBM en el periodo 2007–2021 y evaluar prospectivamente en el bloque 2022–2024. | Python, dataset ENDES separado por año (`HV007`). | Matriz de confusión OOT y curva ROC demostrando estabilidad temporal. | **Semanas 6 – 8** *(Bloque medio)* |
| **4** | Ausencia de evaluación de usabilidad según ISO 25010. | **Evaluación de Usabilidad con Escala SUS:** Aplicar cuestionario SUS a una muestra de 10 usuarios (estudiantes/agentes de salud) evaluando el prototipo Streamlit. | Cuestionario SUS (10 ítems), prototipo Streamlit desplegado. | Score SUS (meta > 75 puntos - Nivel Aceptable) en el informe final. | **Semanas 9 – 11** *(Fase final)* |

### 6.2 Compromiso de Ejecución Técnica
El plan permite balancear adecuadamente las exigencias laborales de prácticas pre-profesionales y la carga académica del ciclo. Las **Acciones 1 y 2** se ejecutarán durante la primera mitad del semestre por ser de naturaleza estrictamente computacional y de bajo requerimiento de tiempo. Las **Acciones 3 y 4** se abordarán progresivamente en la segunda mitad del ciclo.

---
*Informe elaborado y validado por el equipo de investigación – EP Ingeniería de Sistemas, UPeU.*
