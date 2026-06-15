# Hoja de Ruta del Proyecto (AI Context & CRISP-DM Roadmap)

> [!WARNING]
> **Documento Vivo y Adaptable (Living Document):** Este roadmap NO es rígido. Es un documento sujeto a modificaciones continuas a medida que avancemos empíricamente en el Análisis Exploratorio de Datos (EDA), comprendamos la verdadera naturaleza y calidad de la base de datos, y afinemos el objetivo final del modelo predictivo. No debemos dar por sentadas técnicas avanzadas (como SHAP, SMOTE o algoritmos específicos) ni cerrarnos a un único enfoque hasta que los datos mismos nos lo dicten.
>
> **Regla de Oro del Desarrollo (Cero Suposiciones):** La IA tiene terminantemente PROHIBIDO autorrellenar celdas de código, armar lógicas de filtrado o tomar decisiones analíticas sin antes haber corrido y validado los resultados previos paso a paso *junto con el usuario*. Todo avance debe ser estrictamente iterativo y basado en la salida empírica de la ejecución, asegurando que nunca se avance a ciegas en ninguna fase del proyecto.
>
> **NUNCA DAR NADA POR TERMINADO:** La IA no debe asumir que un módulo, fase o tarea está finalizada simplemente porque se superó un obstáculo inicial. Antes de cerrar cualquier hito, se deben agotar todas las dimensiones exploratorias (tipos de datos, diccionarios de valor, consistencia semántica) y SIEMPRE requerir la confirmación final y explícita del usuario.

Este documento sirve como el **punto de anclaje (Master Context)** para el asistente de Inteligencia Artificial en futuras conversaciones, y está estructurado rigurosamente bajo el método científico de **CRISP-DM**.

## Fase 1: Comprensión del Negocio (Business Understanding)

**Objetivo:** Desarrollar un **Sistema Predictivo Sociodemográfico y Estructural** (Machine Learning) para pronosticar la Desnutrición Crónica Infantil en el Perú utilizando datos de la ENDES.
*Nota conceptual:* Se evita el término estricto "Geográfico" para no limitarnos a modelos de coordenadas (Lat/Lon) y se prefiere "Estructural/Sociodemográfico" para englobar de manera más realista las variables de vivienda, saneamiento e identidad que provee la encuesta. El componente ingenieril (la arquitectura ETL o "pipeline") es el motor interno del sistema, pero el producto final es este Sistema Predictivo Integral.

**Aporte Ingenieril:** Resolver desafíos computacionales severos (alta dimensionalidad, nulos, desbalance extremo) en bases de datos gubernamentales masivas, aportando rigor de Ingeniería de Sistemas frente al enfoque tradicional de salud pública.

- [Propuesta Ingenieril y Defensa Académica](file:///Users/abelguevarah/Desktop/invs/malnutrition-research/docs/docs/engineering_proposal.md)

## Fase 2: Comprensión de los Datos (Data Understanding)

**Estado Actual: COMPLETADO (Fase de variables base finalizada)**

*Exploración RAW (Limpieza Básica):*
- [x] `RECH6` -> `rech6` (Diagnóstico Clínico / Target).
- [x] `RECH1` -> `household_roster` (Demografía y Criterios de Inclusión).
- [x] `RECH0` -> `household_characteristics` (Datos de Entrevista).
- [x] `RECH23` -> `rech23` (Características del Hogar y Geografía).
- [ ] `REC0111` -> `mef` (Salud Materna y Antecedentes). *← PAUSADO por limitantes de tiempo. Queda como trabajo pendiente para agregarse a futuro.*

*Análisis Exploratorio Profundo (Interim EDA):*
- [x] **`RECH6` (Análisis del Target):** ¡COMPLETADO! 
  - Se validó `HC70` (Z-score Talla/Edad) como target.
  - Se identificó un salto masivo en el muestreo post-2015, exigiendo el uso de un **Time-Series Split**.
  - Se demostró la no-linealidad biológica de la caída nutricional, forzando algoritmos basados en árboles (RF, XGBoost).
  - La Anemia (`HC57`) fue coronada como *Super-Predictor*, mientras que Peso y Talla cruda fueron vetados (*Data Leakage*).
- [x] **`RECH0` y `RECH1` (Criterios Base):** COMPLETADOS. Filtros estructurales de participación y residentes habituales validados, listos para hacer los *joins* correctos.
- [x] **`RECH23` (Hogares y Geografía):** ¡COMPLETADO!
  - 93 variables auditadas y categorizadas.
  - Se identificaron dinámicas históricas críticas: el estancamiento de cocinar con leña (Humo) en un 25%, y cómo el celular ya no sirve para medir riqueza (96% cobertura) comparado con tener refrigeradora.
  - Se estableció la guillotina del 60% para los Valores Nulos en todos los módulos pasados.

## Fase 3: Preparación de Datos (Data Preparation)

**Estado Actual: SIGUIENTE PASO INMEDIATO**

- **Consolidación (Merge Final):** Unir todas las tablas limpias auditadas (`RECH6`, `RECH0`, `RECH1`, `RECH23`) mediante llaves foráneas (`HHID`, `HC0`, `HVIDX`, `HV112`).
- **Feature Engineering:** Imputación de nulos y codificación de categorías basándonos en la distribución real de los datos y en el análisis de Nulidad (eliminar ruido estadístico mayor a 60%).

## Fase 4: Modelado (Modeling)

**Estado Actual: PENDIENTE**
*Nota: La selección algorítmica dependerá estrictamente de los hallazgos en la Fase 3.*

- **Enfoque Propuesto:** Algoritmos basados en árboles (Tree-based como XGBoost o LightGBM).
- **Manejo de Desbalance:** Técnicas (e.g., SMOTE, Class Weights) a definir según la prevalencia final del target (`HC70`).

## Fase 5: Evaluación (Evaluation)

**Estado Actual: PENDIENTE**

- **Métricas a considerar:** PR-AUC, F1-Score (idóneas para clases desbalanceadas).
- **Interpretabilidad (XAI):** Técnicas (SHAP) para garantizar explicabilidad médica.

## Fase 6: Despliegue (Deployment)

**Estado Actual: PENDIENTE**

- Empaquetado de la arquitectura de extracción y el modelo de pronóstico.

---

### Próximo Paso Inmediato para la IA (Next Action)

- **Transición a Fase 3 (Preparación y Joins):** Dado que la auditoría de los datos (Fase 2) para el individuo (`RECH6`) y su entorno demográfico y estructural (`RECH0, 1, 23`) ha sido validada exhaustivamente, el siguiente hito clave es construir la **tabla maestra consolidada**. La IA deberá empezar a diseñar el script de `merge` para integrar los *dataframes* sin perder o duplicar filas, preparándolos para la inyección al algoritmo predictivo.