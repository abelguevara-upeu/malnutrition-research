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

**Estado Actual: COMPLETADO (Fase de variables base finalizada)**

*Exploración RAW (Limpieza Básica):*
- [x] `RECH6` -> `rech6` (Diagnóstico Clínico / Target).
- [x] `RECH1` -> `household_roster` (Demografía y Criterios de Inclusión).
- [x] `RECH0` -> `household_characteristics` (Datos de Entrevista).
- [x] `RECH23` -> `rech23` (Características del Hogar y Geografía).
- [ ] `REC41` -> `rec41_salud_materna` (Embarazo, Parto, Lactancia y Peso al nacer). *← EN PROGRESO: Integración crítica para aportar peso biológico al modelo.*

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

**Estado Actual: COMPLETADO (Fase Base) / EN PROGRESO (Inyección REC41)**

- **Consolidación (Merge Final):** Unir todas las tablas limpias auditadas (`RECH6`, `RECH0`, `RECH1`, `RECH23` y el nuevo `REC41`).
- **Feature Selection Matemática:** Eliminación de colinealidad y variables de ruido estadístico (P-Values > 0.05).

## Fase 4: Modelado (Modeling)

**Estado Actual: COMPLETADO AL 100%**

- **Enfoque Implementado:** Benchmarking riguroso de 4 algoritmos (Logistic Regression, XGBoost, LightGBM, CatBoost) usando 5-Fold Cross Validation Estratificado.
- **Manejo de Desbalance:** Se usó la ponderación demográfica real de la ENDES (`HV005`), eliminando la necesidad de balanceo físico.
- **Resultado Científico:** LightGBM fue coronado como el Campeón Absoluto (AUC: 0.83), demostrando que procesar variables categóricas de forma nativa supera al clásico One-Hot Encoding de XGBoost/LogReg.
- **Guardado:** Modelo de producción (`champion_lightgbm.pkl`) exportado con su Umbral Óptimo de 0.4511 (80% Recall).

## Fase 5: Evaluación y Explicabilidad (SHAP)

**Estado Actual: EN PROGRESO (Próximo paso)**

- **Interpretabilidad (XAI):** Extraer el ADN de la desnutrición utilizando SHAP Values globales.
- **Evaluación Regional (Perfiles Geográficos):** Aplicar Análisis Geográfico de Importancia Local (SHAP por Región) para demostrar cómo el perfil de riesgo muta drásticamente según el departamento geográfico (Costa vs. Sierra vs. Selva).

## Fase 6: Despliegue (Deployment en Streamlit)

**Estado Actual: PENDIENTE**

- Construcción de un **Sistema Web Interactivo en Streamlit**.
- La aplicación permitirá a los tomadores de decisiones del Estado simular perfiles demográficos e identificar visualmente los factores de riesgo geográficos extraídos en la Fase 5.

---

### Próximo Paso Inmediato para la IA (Next Action)

- **Fase 5 (Explicabilidad SHAP):** Crear el notebook `03_model_explainability.ipynb`, cargar el modelo campeón `champion_lightgbm.pkl` e inyectarle la librería SHAP para extraer los perfiles de riesgo globales y geográficos.