# Prompts de LeapSpace para las citas del artículo

Revista destino: *Nutrition* (Elsevier). Pegar cada prompt por separado y guardar la respuesta en `leapspace/`.
Cada prompt pide una matriz con DOI para poder verificar cada cita antes de usarla.

| # | Sección del artículo | Qué debe sostener la cita |
| --- | --- | --- |
| 1 | Introducción, Discusión | Estudios de *Nutrition* sobre predicción de desnutrición (la revista destino) |
| 2 | Introducción | Carga mundial y consecuencias de la desnutrición crónica |
| 3 | Introducción, Discusión | Perú: estancamiento desde 2018 y brecha territorial |
| 4 | Introducción, Discusión | Machine learning con datos DHS para predecir desnutrición |
| 5 | Metodología (Preparación) | Selección de variables y fuga de información |
| 6 | Metodología (Modelado) | Pesos de clase en lugar de SMOTE |
| 7 | Metodología (Modelado y Evaluación) | Pesos muestrales de la encuesta en machine learning |
| 8 | Metodología y Resultados (Evaluación) | Umbral de decisión orientado al triaje y métricas para clases desbalanceadas |
| 9 | Metodología y Resultados (Explicabilidad) | SHAP en desnutrición infantil |
| 10 | Discusión | Peso al nacer, pobreza y altitud como determinantes |
| 11 | Metodología y Resultados (Despliegue) | Aceptación de herramientas de apoyo con TAM |

## 1. Artículos de la revista Nutrition

```
Machine learning or predictive modeling studies on child malnutrition, stunting or undernutrition published in the journal Nutrition (Elsevier). Return a matrix with: authors, year, DOI, country, data source, sample size, algorithms compared, best AUC/accuracy, and key predictors. Limit to 2019-2026.
```

## 2. Carga mundial de la desnutrición crónica

```
Global burden and long-term consequences of child stunting: prevalence estimates, effects on cognitive development, schooling, adult productivity and Sustainable Development Goal 2 targets. Return a matrix with: authors, year, journal, DOI, type of study, population, main estimate or finding. Limit to 2013-2026.
```

## 3. Perú: estancamiento y brecha territorial

```
Chronic child malnutrition (stunting) trends and regional inequalities in Peru after 2015, including stagnation of national prevalence and rural-urban or department-level gaps. Return a matrix with: authors, year, journal, DOI, data source (ENDES or other), period, prevalence reported, and main determinants. Limit to 2016-2026.
```

## 4. Machine learning con datos DHS

```
Machine learning models predicting child stunting or chronic malnutrition using Demographic and Health Survey (DHS) data, including gradient boosting (LightGBM, XGBoost, CatBoost). Return a matrix with: authors, year, journal, DOI, country, sample size, algorithms compared, validation strategy, best AUC/sensitivity/F1, and key predictors. Limit to 2019-2026.
```

## 5. Selección de variables y fuga de información

```
Feature selection and data leakage prevention in clinical or public health prediction models using survey data: multicollinearity (VIF), statistical filtering and model-based importance. Return a matrix with: authors, year, journal, DOI, data type, selection methods used, and effect on model performance. Limit to 2015-2026.
```

## 6. Pesos de clase en lugar de SMOTE

```
Studies comparing cost-sensitive learning or class weights against SMOTE or oversampling for imbalanced health or survey data. Return a matrix with: authors, year, journal, DOI, data type, imbalance ratio, methods compared, metric used, and main conclusion. Limit to 2018-2026.
```

## 7. Pesos muestrales de la encuesta

```
Use of survey sampling weights in machine learning models trained on Demographic and Health Surveys or national household surveys. Return a matrix with: authors, year, journal, DOI, survey, how weights were used (training, evaluation or both), and effect on results. Limit to 2015-2026.
```

## 8. Umbral de triaje y métricas para clases desbalanceadas

```
Decision threshold selection for screening or triage prediction models in health, and evaluation metrics for imbalanced outcomes (sensitivity, precision, F1, precision-recall AUC) instead of accuracy. Return a matrix with: authors, year, journal, DOI, clinical context, threshold criterion, metrics recommended, and main conclusion. Limit to 2015-2026.
```

## 9. SHAP en desnutrición infantil

```
Studies applying SHAP or other explainable AI methods to child stunting or undernutrition prediction. Return a matrix with: authors, year, journal, DOI, country, data source, best model, top predictors identified by SHAP, and whether local or regional explanations were reported. Limit to 2020-2026.
```

## 10. Peso al nacer, pobreza y altitud

```
Evidence on low birth weight, small size at birth, household wealth and altitude of residence as determinants of child stunting in Latin America or Andean populations. Return a matrix with: authors, year, journal, DOI, country, design, sample size, determinant studied, and effect size. Limit to 2015-2026.
```

## 11. Aceptación de herramientas de apoyo con TAM

```
Studies evaluating clinical decision support or machine learning tools with health professionals using TAM, TAM2 or UTAUT. Return a matrix with: authors, year, journal, DOI, tool evaluated, participants, model used, constructs measured, and main findings. Limit to 2018-2026.
```

## Después de correrlos

1. Guardar cada respuesta en `leapspace/` con el número del prompt en el nombre.
2. Elegir de 1 a 3 referencias por prompt, priorizando las de *Nutrition* y las de Q1.
3. Verificar cada DOI en doi.org antes de citarlo; descartar las filas con "Not surfaced in excerpt" en datos clave.
4. Pasar las elegidas al `.bib` y reemplazar las citas manuales [1], [2]… de la Introducción por `\cite{}`.
