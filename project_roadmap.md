# Hoja de Ruta del Proyecto (AI Context & CRISP-DM Roadmap)

> [!WARNING]
> **Documento Vivo y Adaptable (Living Document):** Este roadmap NO es rígido. Es un documento sujeto a modificaciones continuas a medida que avancemos empíricamente en el Análisis Exploratorio de Datos (EDA), comprendamos la verdadera naturaleza y calidad de la base de datos, y afinemos el objetivo final del modelo predictivo. No debemos dar por sentadas técnicas avanzadas (como SHAP, SMOTE o algoritmos específicos) ni cerrarnos a un único enfoque hasta que los datos mismos nos lo dicten.
> 
> **Regla de Oro del Desarrollo (Cero Suposiciones):** La IA tiene terminantemente PROHIBIDO autorrellenar celdas de código, armar lógicas de filtrado o tomar decisiones analíticas sin antes haber corrido y validado los resultados previos paso a paso *junto con el usuario*. Todo avance debe ser estrictamente iterativo y basado en la salida empírica de la ejecución, asegurando que nunca se avance a ciegas en ninguna fase del proyecto.

Este documento sirve como el **punto de anclaje (Master Context)** para el asistente de Inteligencia Artificial en futuras conversaciones, y está estructurado rigurosamente bajo el método científico de **CRISP-DM**.

## Fase 1: Comprensión del Negocio (Business Understanding)
**Objetivo:** Desarrollar un **Sistema Predictivo Sociodemográfico y Estructural** (Machine Learning) para pronosticar la Desnutrición Crónica Infantil en el Perú utilizando datos de la ENDES.
*Nota conceptual:* Se evita el término estricto "Geográfico" para no limitarnos a modelos de coordenadas (Lat/Lon) y se prefiere "Estructural/Sociodemográfico" para englobar de manera más realista las variables de vivienda, saneamiento e identidad que provee la encuesta. El componente ingenieril (la arquitectura ETL o "pipeline") es el motor interno del sistema, pero el producto final es este Sistema Predictivo Integral.

**Aporte Ingenieril:** Resolver desafíos computacionales severos (alta dimensionalidad, nulos, desbalance extremo) en bases de datos gubernamentales masivas, aportando rigor de Ingeniería de Sistemas frente al enfoque tradicional de salud pública.
- [Propuesta Ingenieril y Defensa Académica](file:///Users/abelguevarah/Desktop/invs/malnutrition-research/docs/docs/engineering_proposal.md)

## Fase 2: Comprensión de los Datos (Data Understanding)
**Estado Actual: EN PROGRESO**
Estandarización de la ingesta dinámica de datos a través de diccionarios semánticos (`loader.py`), mapeando archivos históricos cambiantes a alias canónicos técnicos para facilitar el EDA.

*Exploración de Módulos:*
- [x] `RECH6` $\rightarrow$ `rech6` (Diagnóstico Clínico / Target).
- [x] `RECH1` $\rightarrow$ `household_roster` (Demografía y Criterios de Inclusión).
- [ ] `RECH0` $\rightarrow$ `household_characteristics` (Infraestructura). *← Próximo paso.*
- [ ] `REC0111` $\rightarrow$ `mef` (Salud Materna y Antecedentes). *← Pendiente.*

**Documentos de Apoyo Generados en esta Fase:**
- [Diccionario y Justificación de Variables](file:///Users/abelguevarah/Desktop/invs/malnutrition-research/docs/docs/variable_justifications.md)
- [Esquema Entidad-Relación (ERD)](file:///Users/abelguevarah/Desktop/invs/malnutrition-research/docs/docs/database_schema.md)

## Fase 3: Preparación de Datos (Data Preparation)
**Estado Actual: PENDIENTE**
- **Consolidación (Merge Final):** Unir todas las tablas limpias mediante llaves foráneas (`HHID`, `HC0`, `HVIDX`, `HV112`).
- **Feature Engineering:** Imputación de nulos y codificación de categorías (Las estrategias exactas se definirán al terminar la Fase 2, basándonos en la distribución real de los datos).

## Fase 4: Modelado (Modeling)
**Estado Actual: PENDIENTE**
*Nota: La selección algorítmica dependerá estrictamente de los hallazgos en la Fase 3.*
- **Enfoque Propuesto:** Algoritmos basados en árboles (Tree-based como XGBoost o LightGBM) debido a la naturaleza tabular heterogénea de la ENDES.
- **Manejo de Desbalance:** Técnicas (e.g., SMOTE, Class Weights) a definir según la tasa de prevalencia final del target (`HC70`).

## Fase 5: Evaluación (Evaluation)
**Estado Actual: PENDIENTE**
- **Métricas a considerar:** PR-AUC, F1-Score (idóneas para clases desbalanceadas).
- **Interpretabilidad (XAI):** Exploración de técnicas (como SHAP) para garantizar que las predicciones sean explicables al dominio médico.

## Fase 6: Despliegue (Deployment)
**Estado Actual: PENDIENTE**
- Empaquetado de la arquitectura de extracción y el modelo de pronóstico, consolidando el Sistema Predictivo Sociodemográfico para una posible integración en dashboards o reportes dinámicos.

---

### Próximo Paso Inmediato para la IA (Next Action)
- Iniciar el **EDA del módulo de Vivienda (`01_eda_raw_rech0.ipynb`)** bajo el alias `household_characteristics`. El objetivo es entender empíricamente qué variables de saneamiento e infraestructura son rescatables y coherentes antes de tomar cualquier decisión de modelado.
