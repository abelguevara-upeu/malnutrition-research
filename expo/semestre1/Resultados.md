# RESULTADOS

---

### Diapositiva R: Resultados del Sistema Predictivo

**Contenido Visual:**

**Rendimiento del modelo campeón — LightGBM (Top 43 variables, 5-Fold CV):**

| Métrica | Valor | Interpretación |
|---|---|---|
| AUC-ROC | **0.8308** | El modelo ordena correctamente el 83% de los pares sano/desnutrido |
| Recall (Sensibilidad) | **76.49%** | 3 de cada 4 niños desnutridos son detectados |
| Precision | 37.05% | 1 de cada 3 alertas es un caso real |
| F1-Score | 0.4976 | Balance entre detección y precisión |
| Umbral de producción | 0.5 | Ajustable — bajar a ~0.35 aproxima el Recall al 80% objetivo |

**¿Qué significa en términos de política pública?**

> Con 285,284 niños en el dataset histórico y una prevalencia del 16%, hay ~45,000 niños desnutridos.
> El modelo detecta ~34,400 de ellos usando solo datos de encuesta de hogar —
> sin medición antropométrica, sin visita previa al domicilio.

**Los 5 factores de riesgo más determinantes (SHAP global):**

| # | Factor | Tipo |
|---|---|---|
| 1 | Índice de riqueza del hogar (`HV271`) | Socioeconómico |
| 2 | Peso al nacer (`m19`) | Biológico-prenatal |
| 3 | Altitud del conglomerado (`HV040`) | Geográfico-fisiológico |
| 4 | Edad del niño en meses (`HC1`) | Ventana crítica 1000 días |
| 5 | Hemoglobina ajustada (`HC56`) | Clínico-ambiental |

**Respuesta a la pregunta de investigación:**

> ¿Puede un modelo de Machine Learning identificar, con datos de encuesta de hogar, qué niños tienen mayor riesgo de desnutrición crónica antes de que un agente de salud llegue al hogar?

**Sí — con AUC 0.8308 y Recall 76.49% usando 18 años de la ENDES y 43 variables de perfil sociodemográfico.**

**Guion del Expositor:**

> "Los resultados consolidados del sistema son los siguientes. El modelo LightGBM entrenado con las Top 43 variables seleccionadas algorítmicamente alcanza un AUC de 0.8308 en validación cruzada ponderada de 5 folds. Eso significa que dado un niño sano y uno desnutrido al azar, el modelo los ordena correctamente el 83% de las veces. El Recall del 76.49% significa que de cada 4 niños con desnutrición crónica, el modelo detecta 3 usando únicamente datos de encuesta de hogar — sin necesitar que nadie haya ido a medirlos previamente. El objetivo de política pública era alcanzar el 80% de Recall. El modelo actual llega al 76.49% con el umbral de clasificación fijo en 0.5. Ese umbral no fue optimizado — es una deuda técnica documentada, y bajar el umbral a aproximadamente 0.35 alcanzaría el objetivo sin necesidad de reentrenar. En cuanto a los factores de riesgo, el análisis SHAP confirma que la desnutrición crónica en el Perú es principalmente un problema de pobreza estructural — el índice de riqueza del hogar es el predictor dominante. El peso al nacer es el segundo factor, lo que señala que las intervenciones prenatales tienen impacto directo y medible sobre el resultado nutricional del niño a los 5 años. Y la altitud confirma el componente geográfico: la Sierra requiere una estrategia de intervención distinta a la Costa y la Selva."