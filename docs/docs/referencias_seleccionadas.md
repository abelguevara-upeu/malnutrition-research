# Referencias seleccionadas (12)

Selección sobre los 44 registros recuperados con Scopus AI (`leapspace/`). Todas verificadas con DOI
en el índice de Scopus. Se indica dónde va cada una en el manuscrito y qué afirmación sostiene.

---

## A. Trabajo relacionado — ML sobre datos DHS (4)

Estas cuatro sitúan tu aporte frente al estado del arte y, sobre todo, **dan el punto de comparación
de desempeño** que el jurado va a pedir.

| # | Referencia | Dónde va | Qué sostiene |
|---:|---|---|---|
| 1 | *Predicting stunting status among under-5 children in Rwanda using neural network model* (2025). **F1000Research**. `10.12688/f1000research.141458.2` | Trabajo relacionado · Discusión | **AUC 0.84 con DHS 2020 (Ruanda)**. Es el referente más cercano al tuyo: tu 0.8295 queda en el mismo rango, lo que respalda que tu resultado es competitivo. Además identifica **talla materna** como predictor principal — justifica pedirla en la sección 3.ter de la solicitud. |
| 2 | *Machine learning algorithms for predicting undernutrition among under-five children in Ethiopia* (2022). **Public Health Nutrition**. `10.1017/S1368980021004262` | Trabajo relacionado | Compara 5 algoritmos sobre DHS 2016 (n=9,471) y corona a **XGBoost**. Da precedente metodológico al benchmarking de 6 familias que hiciste, y coincide contigo en un predictor: *time to water source* (`HV204`). |
| 3 | *Machine learning algorithms for predicting malnutrition among under-five children in Bangladesh* (2020). **Nutrition**. `10.1016/j.nut.2020.110861` | Trabajo relacionado · Justificación de métrica | Random Forest con **sensibilidad 94.66% y κ=0.24**: un caso donde alto recall convive con bajo acuerdo. Sirve para argumentar por qué priorizas Recall y descartas accuracy. |
| 4 | *Performance of Machine Learning Classifiers in Classifying Stunting among Under-Five Children in Zambia* (2022). **Children**. `10.3390/children9071082` | Trabajo relacionado · Selección de variables | Random Forest **redujo de 58 a 13 variables** sin perder desempeño. Precedente directo de tu reducción algorítmica y de la ablación de la sección C.1. |

---

## B. Contexto peruano (3)

Sin estas, la discusión no aterriza en el país. Las tres usan ENDES o datos peruanos.

| # | Referencia | Dónde va | Qué sostiene |
|---:|---|---|---|
| 5 | *The double burden of malnutrition in Peru: an update with a focus on social inequities* (2021). **American Journal of Clinical Nutrition**. `10.1093/ajcn/nqaa387` | Introducción · Discusión | Serie 1992–2017: el stunting cae más rápido en lo urbano que en lo rural (AAPC −4.5% vs −2.6%). **Cuantifica la desigualdad territorial** que tu mapa por departamento visualiza, y es Q1. |
| 6 | *Age and altitude of residence determine anemia prevalence in Peruvian 6 to 35 months old children* (2020). **PLoS ONE**. `10.1371/journal.pone.0226846` | Metodología · Discusión | La hemoglobina varía con la altitud en niños peruanos. **Respalda dos de tus variables a la vez** (`HC56` ajustada por altitud y `HV040`) y explica por qué la altitud pesa distinto según región en tu análisis SHAP. |
| 7 | *Child malnutrition in children under 5 years of age in Peru: trends and determinants* (2014) | Introducción | Serie 2000–2011: desnutrición crónica de 31.6% a 19.6%. **Da la línea de base histórica** previa a tu ventana 2007–2025 y contextualiza la caída de prevalencia que observas. |

> *Nota:* la referencia 7 no trae DOI en el registro de Scopus. Conviene completarla desde la ficha
> del artículo antes de enviar el manuscrito.

---

## C. Marco conceptual (2)

| # | Referencia | Dónde va | Qué sostiene |
|---:|---|---|---|
| 8 | *Maternal and child undernutrition and overweight in low-income and middle-income countries* (2013). **The Lancet**, Serie de Nutrición. `10.1016/S0140-6736(13)60937-X` | Introducción · Marco teórico | El **marco de causas inmediatas, subyacentes y básicas** sobre el que organizaste la sección 3.ter. Es la referencia canónica del campo. |
| 9 | *Revisiting maternal and child undernutrition in low-income and middle-income countries: variable progress towards an unfinished agenda* (2021). **The Lancet**. `10.1016/S0140-6736(21)00394-9` | Introducción | Actualización 2021 de la serie anterior. **Evita que tu marco teórico parezca desactualizado** al apoyarse solo en 2013. |

---

## D. Método (3)

| # | Referencia | Dónde va | Qué sostiene |
|---:|---|---|---|
| 10 | Kaufman et al. (2011). *Leakage in data mining: formulation, detection, and avoidance*. **ACM TKDD**. `10.1145/2020408.2020496` | Metodología §B | **Sustenta la exclusión de `HC2`, `HC3` y los Z-scores derivados.** Es la decisión metodológica central de tu diseño y hasta ahora no tenía respaldo bibliográfico. |
| 11 | Collins et al. (2015). *Transparent reporting of a multivariable prediction model (TRIPOD)*. **Annals of Internal Medicine**. `10.7326/M14-0698` | Metodología · Protocolo de validación | Estándar internacional de reporte de modelos predictivos en salud. **Le da forma clínica reconocible a tu Eje 1** y es lo que un evaluador de salud pública espera ver. |
| 12 | *A comparative analysis of gradient boosting algorithms* (2021). **Artificial Intelligence Review**. `10.1007/s10462-020-09896-5` | Metodología §D | Compara LightGBM, XGBoost y CatBoost. **Justifica por qué evaluaste esas tres familias** y respalda el manejo nativo de categóricas que explica la ventaja de LightGBM en tu benchmark. |

---

## Cómo queda el conjunto

El archivo `docs/papers/referencias.bib` contiene **estas 12 y solo estas**, todas provenientes de la
búsqueda con Scopus AI. Las referencias metodológicas que figuraban en el Momento 6 (Aiken, Bangor,
Davis, DeLong, Efron & Tibshirani, Kohavi, Lipton, Wilkinson) quedan fuera del archivo.

### Autores pendientes

Ni los CSV ni los informes `.md` de LeapSpace exponen los autores: el propio informe los marca como
*"Not surfaced in excerpt"*. Los campos `author` quedan como `{COMPLETAR}` y deben rellenarse abriendo
cada EID en Scopus. Rellenarlos por aproximación produciría citas falsas que compilan sin error.

> **Un error detectado en el informe de LeapSpace.** Atribuye *Leakage in data mining* a Domingos y
> Pazzani, cuando el trabajo es de Kaufman, Rosset, Perlich y Stitelman. Conviene verificar cada
> autoría en la ficha original antes de compilar: la herramienta acierta en DOI y títulos, pero no es
> fiable en atribución.

## Descartadas y por qué

- **Estudios de violencia de pareja y desnutrición (2014, 2022):** temáticamente valiosos, pero la
  variable no está en tu modelo; citarlos abriría una discusión que no puedes sostener con tus datos.
- **Qali Warma (2021):** evalúa un programa de alimentación escolar en niños de 3–5 años; tu unidad de
  análisis es distinta.
- **Papers de WASH en Túnez, Camboya y Ghana:** el vínculo agua-nutrición ya queda cubierto por la
  serie de *The Lancet*, y son contextos lejanos al andino.
- **Malawi (2024) y Bangladesh (2021, 2025):** aportan lo mismo que las cuatro seleccionadas de la
  sección A, con AUC más bajos (0.64) o sin métrica comparable.
- **Egipto (2025):** reporta AUC 0.994 sobre *wasting*; una cifra tan alta sugiere fuga de información
  y citarla como comparación te perjudicaría.
- **SHAP → RGE (2025) y aplicación en cáncer de próstata (2020):** el primero es una revisión
  tangencial y el segundo un dominio ajeno. **Falta el paper original de SHAP (Lundberg & Lee, 2017)**,
  que no apareció en esta búsqueda y conviene recuperar aparte: es imprescindible para tu Fase 5.
