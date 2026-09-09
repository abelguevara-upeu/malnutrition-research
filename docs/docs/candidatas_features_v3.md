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

# RESULTADO EXPERIMENTAL (ablación en `develop`)

Script: `mnp/evaluation/feature_ablation.py` · Resultados: `reports/feature_ablation_results.json`

Protocolo: replica EXACTA del notebook 03_model_benchmarking_extended (celda 11).
Incluye drop de metadatos pasivos (year, SHREGION, HV005, HV024), rename vía
`mnp.configs.column_labels.LABELS`, aplanado ASCII de nombres,
StratifiedKFold(5, shuffle, seed=42) y **ponderación HV005 tanto en el
entrenamiento como en el cálculo de métricas**.

| Experimento | Feats | AUC | Recall | Precision | dAUC |
|---|---:|---:|---:|---:|---:|
| BASELINE Top43 | 43 | 0.8308 | 76.49% | 36.89% | — |
| + WASH/vivienda | 50 | 0.8308 | 76.49% | 36.89% | +0.0000 |
| + territorio | 47 | 0.8308 | 76.51% | 36.90% | +0.0000 |
| + bloque A completo | 54 | 0.8308 | 76.51% | 36.90% | +0.0000 |

El baseline reproduce exactamente el AUC 0.8308 / Recall 76.49% del manuscrito.

**Conclusión: las candidatas NO aportan. Delta de AUC nulo.**

## Diagnóstico de por qué

1. Entrenando SOLO con las 7 candidatas WASH/vivienda: AUC 0.6733 — tienen
   señal real y sustancial.
2. Pero dentro del modelo completo reciben `feature_importance = 0`:
   LightGBM no hace ni un split con ellas.
3. No es redundancia con riqueza: eta^2 de HV271 explicado por cada candidata
   es sólo 0.04-0.10.
4. La causa es que el baseline YA cubre el constructo vivienda/agua/saneamiento
   con 19 de sus 43 features (HV237, HV237A, HV237G, HV204, HV225, HV242,
   HV216, SH42, SH48, SH49, SH63, SH70, SH71, SH76B/C/D, HV234, HV240, HV220).
   Las candidatas son información redundante ya capturada.

## Lección de reproducibilidad

El primer intento dio AUC 0.8206 en lugar de 0.8308. La causa NO era el
preprocesamiento sino que las métricas se calculaban sin ponderar: el notebook
pasa `sample_weight=w_val` también a `roc_auc_score` y `recall_score`. Sin esa
ponderación las métricas describen la muestra cruda (sesgada a lo urbano) y no
la población expandida. Documentado aquí porque afecta a cualquier script que
reproduzca métricas del manuscrito, incluido el Bootstrap del Eje 1.

## Hallazgo secundario (relevante para tuning)

Con la config por defecto, LightGBM usa 1 de 7 categóricas. Con
`cat_smooth=1, cat_l2=1` usa 2 y el AUC solo-WASH sube de 0.6733 a 0.7085.
La regularización de categóricas por defecto está suprimiendo variables con
señal. Esto sugiere que **Optuna sobre los hiperparámetros de categóricas
(`cat_smooth`, `cat_l2`, `min_data_per_group`, `max_cat_threshold`) es una
vía más prometedora que agregar features**, dado que 15 de las 43 del
campeón son categóricas.

## Umbral de decisión

Verificado contra `models/threshold_recall_curve.json`:
- tau = 0.35 → Recall 87.95%, Precision 29.36%
- tau = 0.46 → Recall 80.10%, Precision 34.33%  ← mínimo que cumple Recall >= 80%

Los documentos de expo/ (Sesión 1 y Momento 6) afirman tau ~ 0.35 para una meta
de 80%; el valor correcto es 0.46. Corregido en `metodologia_articulo.md`,
pendiente en `expo/semestre2/`.
