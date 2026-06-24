# Hoja de Ruta del Proyecto (AI Context & CRISP-DM Roadmap)

> [!WARNING]
> **Documento Vivo y Adaptable (Living Document):** Este roadmap NO es rígido. Es un documento sujeto a modificaciones continuas a medida que avancemos empíricamente en el Análisis Exploratorio de Datos (EDA), comprendamos la verdadera naturaleza y calidad de la base de datos, y afinemos el objetivo final del modelo predictivo. No debemos dar por sentadas técnicas avanzadas (como SHAP, SMOTE o algoritmos específicos) ni cerrarnos a un único enfoque hasta que los datos mismos nos lo dicten.
>
> **Regla de Oro del Desarrollo (Cero Suposiciones):** La IA tiene terminantemente PROHIBIDO autorrellenar celdas de código, armar lógicas de filtrado o tomar decisiones analíticas sin antes haber corrido y validado los resultados previos paso a paso *junto con el usuario*. Todo avance debe ser estrictamente iterativo y basado en la salida empírica de la ejecución, asegurando que nunca se avance a ciegas en ninguna fase del proyecto.
>
> **NUNCA DAR NADA POR TERMINADO:** La IA no debe asumir que un módulo, fase o tarea está finalizada simplemente porque se superó un obstáculo inicial. Antes de cerrar cualquier hito, se deben agotar todas las dimensiones exploratorias (tipos de datos, diccionarios de valor, consistencia semántica) y SIEMPRE requerir la confirmación final y explícita del usuario.

Este documento sirve como el **punto de anclaje (Master Context)** para el asistente de Inteligencia Artificial en futuras conversaciones, y está estructurado rigurosamente bajo el método científico de **CRISP-DM**.

## Fase 1: Comprensión del Negocio (Business Understanding)

**Visión de Negocio (Public Policy Triage):** El objetivo de este modelo **NO es diagnosticar clínicamente** a nivel individual (reemplazando a un médico), sino crear un **Sistema de Triaje y Focalización de Recursos para el Estado**. A través del Machine Learning, se busca identificar un "perfil de riesgo sociodemográfico y biológico" que le permita al Ministerio de Salud optimizar la asignación de su presupuesto. En lugar de encuestar ciegamente a millones de hogares, el Estado podría usar este sistema como radar para priorizar visitas, logrando detectar hasta al 80% de los niños desnutridos (Alto Recall) invirtiendo solo una fracción del presupuesto.

**Objetivo Analítico:** Desarrollar un **"Sistema de Predicción de Perfil de Riesgo Geográfico de Desnutrición Crónica"** en el Perú utilizando más de 18 años de datos de la ENDES.

**Aporte Ingenieril:** Resolver desafíos computacionales severos (alta dimensionalidad, nulos masivos, desbalance extremo) en bases de datos gubernamentales masivas, aportando rigor de Ingeniería de Sistemas frente al enfoque estadístico tradicional de salud pública.

- [Propuesta Ingenieril y Defensa Académica](file:///Users/abelguevarah/Desktop/invs/malnutrition-research/docs/docs/engineering_proposal.md)

## Fase 2: Comprensión de los Datos (Data Understanding)

**Estado Actual: COMPLETADO**

*Exploración RAW (Limpieza Básica):*

- [X] `RECH6` -> `rech6` (Diagnóstico Clínico / Target).
- [X] `RECH1` -> `household_roster` (Demografía y Criterios de Inclusión).
- [X] `RECH0` -> `household_characteristics` (Datos de Entrevista).
- [X] `RECH23` -> `rech23` (Características del Hogar y Geografía).
- [X] `REC41` -> `rec41_salud_materna` (Embarazo, Parto, Lactancia y Peso al nacer). *Integración completada mediante tabla puente REC21. Auditoría biológica: 99.99% coincidencia de sexo, 99.67% año de nacimiento.*

*Análisis Exploratorio Profundo (Interim EDA):*

- [X] **`RECH6` (Análisis del Target):** ¡COMPLETADO!
  - Se validó `HC70` (Z-score Talla/Edad) como target.
  - Se identificó un salto masivo en el muestreo post-2015, exigiendo el uso de un **Time-Series Split**.
  - Se demostró la no-linealidad biológica de la caída nutricional, forzando algoritmos basados en árboles (RF, XGBoost).
  - La Anemia (`HC57`) fue coronada como *Super-Predictor*, mientras que Peso y Talla cruda fueron vetados (*Data Leakage*).
- [X] **`RECH0` y `RECH1` (Criterios Base):** COMPLETADOS. Filtros estructurales de participación y residentes habituales validados, listos para hacer los *joins* correctos.
- [X] **`RECH23` (Hogares y Geografía):** ¡COMPLETADO!
  - 93 variables auditadas y categorizadas.
  - Se identificaron dinámicas históricas críticas: el estancamiento de cocinar con leña (Humo) en un 25%, y cómo el celular ya no sirve para medir riqueza (96% cobertura) comparado con tener refrigeradora.
  - Se estableció la guillotina del 60% para los Valores Nulos en todos los módulos pasados.

## Fase 3: Preparación de Datos (Data Preparation)

**Estado Actual: COMPLETADO**

- **Consolidación (Merge Final):** 4 módulos + REC41 (vía puente REC21) unificados en `master_merged_v2.parquet`. Dataset resultante: 294,109 niños × 189 columnas.
- **Feature Selection Matemática:** Pipeline completo ejecutado en `02_feature_selection_v3.ipynb`:
  - Guillotina de nulos (>60%): eliminadas las columnas con datos insuficientes.
  - Eliminación de colinealidad: 43 columnas redundantes descartadas.
  - Pruebas bivariadas (Kruskal-Wallis + Chi²): 74 variables relevantes confirmadas.
  - Validación multivariada (XGBoost): 7 variables con cero poder predictivo eliminadas.
  - Dataset final para modelado: `master_preprocessed_v2.parquet` — 285,284 filas × 79 columnas.
- **Deuda técnica pendiente:** `kpi5_lactancia_exclusiva` resultó con cero varianza (todos los valores = 0). Investigar si es un bug de la condición `M4 == 95.0 & HC1 < 6` o un artefacto del cruce con REC41.

## Fase 4: Modelado (Modeling)

**Estado Actual: COMPLETADO**

- **Enfoque Implementado:** Benchmarking riguroso de 6 algoritmos (Logistic Regression, XGBoost, LightGBM, CatBoost, Decision Tree, Neural Network MLP 3×200) usando 5-Fold Cross Validation Estratificado.
- **Manejo de Desbalance:** Se usó la ponderación demográfica real de la ENDES (`HV005`), eliminando la necesidad de balanceo físico.
- **Resultado Científico:** LightGBM fue coronado como el Campeón Absoluto (AUC: 0.8308, Recall: 76.49%), demostrando que procesar variables categóricas de forma nativa supera al clásico One-Hot Encoding de XGBoost/LogReg.
- **Reducción de variables:** El modelo con Top 43 features (peso algorítmico ≥ 10) igualó al modelo con las 74 variables completas — sin pérdida de rendimiento al eliminar ruido.
- **Guardado:** Modelo de producción (`champion_lightgbm.pkl`) y metadatos (`champion_metadata.json`) exportados con 43 variables.
- **Deuda técnica pendiente:** El umbral de decisión actual es **0.5** (exportado en el JSON). Falta ejecutar la búsqueda matemática del umbral óptimo que maximice el Recall al 80% objetivo de política pública, y actualizar `champion_metadata.json` con el valor correcto.

## Fase 5: Evaluación y Explicabilidad (SHAP)

**Estado Actual: COMPLETADO**

- **Interpretabilidad (XAI):** Summary Plot global ejecutado sobre muestra representativa de 10,000 niños. Se extrajo el ADN de la desnutrición con SHAP Values (TreeExplainer).
- **Evaluación Regional (Perfiles Geográficos):** Análisis de impacto por Región Natural (Costa / Sierra / Selva) y mapa de calor normalizado por Departamento completados. El análisis confirma que los factores de riesgo mutan drásticamente según la geografía (ej. la Altitud es letal en Sierra, irrelevante en Selva).
- **Exportación:** `shap_dept_impact.csv` generado y listo para consumo por la app Streamlit.

## Fase 6: Despliegue (Deployment en Streamlit)

**Estado Actual: PENDIENTE**

- Construcción de un **Sistema Web Interactivo en Streamlit**.
- La aplicación permitirá a los tomadores de decisiones del Estado simular perfiles demográficos e identificar visualmente los factores de riesgo geográficos extraídos en la Fase 5.

---

### Próximo Paso Inmediato para la IA (Next Action)

**Fase 6 (Deployment Streamlit):** El modelo, el umbral y los datos SHAP geográficos ya están listos. Construir la app interactiva en Streamlit.

Antes de arrancar Streamlit, resolver la deuda técnica de la Fase 4:

- **Umbral óptimo:** Iterar sobre el rango [0.3, 0.6] en el dataset de validación para encontrar el umbral que maximice Recall ≥ 80%, y actualizar `models/champion_metadata.json`.
