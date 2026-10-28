# Búsquedas en LeapSpace

Cada búsqueda va en su propia carpeta con tres archivos:

- `informe.md` / `informe.pdf`: la respuesta de LeapSpace.
- `matriz.csv`: la tabla comparativa que exporta LeapSpace (botón *compare table*).

| Carpeta | Fecha | Uso |
| --- | --- | --- |
| `2026-09_busqueda_inicial/` | Septiembre 2026 | Primeras 5 búsquedas; de aquí salió `../articulo/referencias_seleccionadas.md`. Los prompts usados están en `prompts.txt` |
| `2026-10_citas_articulo/` | Octubre 2026 | Búsquedas para completar las citas del artículo, con los 11 prompts de `../articulo/prompts_leapspace.md` |

## Búsqueda inicial (2026-09)

| Carpeta | Tema | Registros en la matriz |
| --- | --- | --- |
| `01_ml_desnutricion_dhs` | Machine learning para desnutrición con datos DHS | 9 |
| `02_determinantes_peru` | Determinantes de la desnutrición crónica en Perú (ENDES) | 12 |
| `03_marco_unicef_lancet` | Marco conceptual de UNICEF y serie de *The Lancet* | 12 |
| `04_literatura_metodologica` | LightGBM, SHAP, TRIPOD y fuga de información | 5 |
| `05_ml_salud_publica` | Machine learning para focalizar intervenciones de salud pública | 6 |

## Citas del artículo (2026-10)

Guardar cada respuesta en `2026-10_citas_articulo/<número>_<tema>/`, con el número del prompt:

| Carpeta | Prompt |
| --- | --- |
| `01_revista_nutrition` | Artículos de la revista *Nutrition* |
| `02_carga_mundial` | Carga mundial de la desnutrición crónica |
| `03_peru_brecha` | Perú: estancamiento y brecha territorial |
| `04_ml_dhs` | Machine learning con datos DHS |
| `05_seleccion_variables` | Selección de variables y fuga de información |
| `06_pesos_de_clase` | Pesos de clase en lugar de SMOTE |
| `07_pesos_muestrales` | Pesos muestrales de la encuesta |
| `08_umbral_metricas` | Umbral de triaje y métricas |
| `09_shap_desnutricion` | SHAP en desnutrición infantil |
| `10_determinantes` | Peso al nacer, pobreza y altitud |
| `11_tam_salud` | Aceptación de herramientas de apoyo con TAM |
