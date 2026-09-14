# Candidatas para ampliar X (objetivo: subir AUC → mejorar Precision y Recall)

Fuente: `data/processed/master_preprocessed_v2.parquet` (285,284 × 79).
Modelo actual: 43 features · AUC 0.8308 · Recall 76.49% · Precision 37.05%.
Prevalencia del target: 16.07%.

Señal medida como: categóricas = spread en puntos porcentuales de tasa de
desnutrición entre categorías (n>=500); numéricas = |AUC-0.5| x 200.

## Bloque A — Alta señal, incorporar (marco UNICEF: causas subyacentes/básicas)

| Var | Señal | Contenido | Nivel UNICEF | Rango observado |
|---|---:|---|---|---|
| HV214 | 41.2 | Material de paredes | Subyacente (vivienda) | 48.7% sin paredes → 7.6% ladrillo |
| HV213 | 39.5 | Material del piso | Subyacente (WASH/vivienda) | 28.0% tierra → 4.8% losetas |
| HV215 | 36.3 | Material del techo | Subyacente (vivienda) | 42.4% paja → 6.1% concreto |
| HV201 | 34.5 | Fuente de agua | Subyacente (WASH) | 41.5% manantial → 7.0% embotellada |
| HV024 | 33.0 | Departamento | Básica (territorio) | 35.7% Huancavelica → 2.8% Tacna |
| SH227 | 30.2 | Cloro residual en agua | Subyacente (WASH) | 36.8% agua sin tratar → 6.6% >=0.5mg/L |
| HV226 | 27.3 | Combustible de cocina | Subyacente (humo intradomiciliario) | 31.8% paja/leña → 4.5% gas natural |
| HV205 | 23.0 | Tipo de servicio higiénico | Subyacente (saneamiento) | 31.5% sin servicio → 8.6% dentro |
| HV026 | 22.8 | Tipo de residencia (urbano/rural detallado) | Básica | — |
| SH77F | 19.4 | (verificar etiqueta) | — | — |
| SHREGION | 18.9 | Región natural | Básica (territorio) | — |

Notas:
- Ninguna es leakage: todas describen el hogar, no la antropometría del niño.
- Todas son observables SIN visita domiciliaria → válidas para triaje.
- HV213/214/215 + HV201/HV205/SH227 forman el bloque WASH+vivienda que la
  literatura DHS reporta consistentemente y que el modelo actual sólo cubre
  de forma parcial e indirecta.

## Bloque B — Señal media, evaluar

| Var | Señal | Observación |
|---|---:|---|
| year | 18.5 | Capturaría el target drift (30% en 2007 → 11% en 2024). CUIDADO: usarla mejora métricas retrospectivas pero degrada el uso prospectivo. Decidir con criterio, no por AUC. |
| QH227B | 11.9 | Sólo 41.4% de cobertura. |
| HV237F / HV237B / HV237D | 8-11 | Tratamiento del agua (complementan HV237/HV237A ya incluidas). |

## Bloque C — Descartar

- `HV103` es CONSTANTE (nuniq=1) — sin varianza, igual que el caso conocido
  de `kpi5_lactancia_exclusiva`.
- `HV237C` señal 0.00.
- `M55B/C/E/H/X`, `HV124`, `HV128`, `SHTOTH` — señal < 1.5.
- `HV005` es el factor de expansión muestral: NO es feature, es peso.

## Riesgo a controlar

HV213/214/215 + HV226 + HV201/HV205 son proxies de riqueza y probablemente
colineales con HV271 (índice de riqueza, factor #1 en SHAP). LightGBM tolera
colinealidad, pero el aporte marginal al AUC puede ser menor que la señal
individual sugiere. Medir el delta de AUC, no asumirlo.

---

# RESULTADO EXPERIMENTAL (19 años, ENDES 2007-2025)

Script: `mnp/evaluation/feature_ablation.py` · Resultados: `reports/feature_ablation_results.json`
Dataset: 304,271 x 79 · prevalencia 15.81% · campeon de 45 variables.

| Experimento | Feats | AUC | Recall | Precision | dAUC |
|---|---:|---:|---:|---:|---:|
| BASELINE Top45 | 45 | 0.8295 | 76.44% | 36.36% | — |
| + WASH/vivienda | 52 | 0.8295 | 76.44% | 36.36% | +0.0000 |
| + territorio | 48 | 0.8295 | 76.44% | 36.36% | +0.0000 |
| + bloque A completo | 55 | 0.8295 | 76.44% | 36.36% | +0.0000 |

El baseline reproduce exactamente el AUC 0.8295 / Recall 76.44% del modelo
reentrenado. **Las candidatas no aportan: delta nulo hasta la cuarta decimal.**

## El resultado se sostiene al pasar de 18 a 19 años

La ablacion con 18 años dio identico delta nulo sobre un baseline de 43
variables y AUC 0.8308. Repetirla sobre un dataset 6.7% mayor y un campeon
distinto devuelve la misma conclusion, lo que descarta que fuera un artefacto
de la muestra.

Dos de las candidatas de la corrida anterior ya no lo son: **HV219** (sexo del
jefe del hogar) y **SH77F** (otro tipo de transporte) cruzaron el umbral de
importancia >= 10 al entrenar con 19 años y entraron al modelo por merito
propio. Las candidatas bajan de 35 a 33 y el campeon sube de 43 a 45.

Esto refuerza el argumento de suficiencia: cuando una variable descartada tiene
señal real, el propio criterio de importancia la recupera al haber mas datos —
no hace falta reinyectarla a mano.

## Diagnostico (recalculado sobre 19 años)

1. Entrenando SOLO con las 7 candidatas WASH/vivienda: AUC 0.6895 — tienen
   señal real y sustancial.
2. Pero dentro del modelo completo reciben `feature_importance = 0`.
3. No es redundancia lineal con riqueza: eta^2 de HV271 explicado por cada
   candidata va de 0.038 a 0.098.
4. La causa es que el baseline ya cubre el constructo vivienda/agua/saneamiento
   con 19 atributos correlacionados (HV237, HV237A, HV237G, HV204, HV225,
   HV242, HV216, SH42, SH48, SH49, SH63, SH70, SH71, SH76B/C/D, HV234, HV240,
   HV220). Las candidatas aportan informacion ya capturada.

## Leccion de reproducibilidad

El primer intento dio AUC 0.8206 en lugar de 0.8308. La causa NO era el
preprocesamiento sino que las metricas se calculaban sin ponderar: el notebook
pasa `sample_weight=w_val` tambien a `roc_auc_score` y `recall_score`. Sin esa
ponderacion las metricas describen la muestra cruda (sesgada a lo urbano) y no
la poblacion expandida. Afecta a cualquier script que reproduzca metricas del
manuscrito, incluido el Bootstrap del Eje 1.

## Hallazgo secundario (vigente)

Con la config por defecto LightGBM usa 1 de 7 categoricas; con
`cat_smooth=1, cat_l2=1` usa 2. La regularizacion de categoricas por defecto
suprime variables con señal, y 15 de las 45 del campeon son categoricas: Optuna
sobre esos hiperparametros sigue siendo la via mas prometedora para subir AUC.

## Umbral de decision

Recalculado con el modelo de 19 años (`mnp/evaluation/threshold_curve.py`):
**tau = 0.45 -> Recall 80.46%, Precision 34.04%** (antes 0.46 con 18 años).
Corregido en `metodologia_articulo.md`; pendiente en `expo/semestre2/`, que
ademas arrastra el valor incorrecto 0.35.
