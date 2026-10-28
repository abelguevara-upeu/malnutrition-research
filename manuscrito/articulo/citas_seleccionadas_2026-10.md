# Citas seleccionadas de LeapSpace (octubre 2026)

De 101 registros en las 11 búsquedas (`manuscrito/leapspace/2026-10_citas_articulo/`) se seleccionaron 21. Sus DOI se comprobaron en doi.org y sus fichas BibTeX, tomadas de Crossref, se agregaron a `manuscrito/referencias/referencias.bib` con la clave indicada.

## Selección por búsqueda

| # | Búsqueda | Clave BibTeX | Referencia | Dónde va | Qué sostiene |
| --- | --- | --- | --- | --- | --- |
| 1 | Revista *Nutrition* | `siy2022philippines` | Siy Van et al., 2022, *Nutrition* | Introducción, Discusión | Random forest con 78.6 % de exactitud para desnutrición escolar en Filipinas |
| 1 | Revista *Nutrition* | `khan2023hybrid` | Khan y Yunus, 2023, *Nutrition* | Introducción, Discusión | Ensamble híbrido con 96 % de exactitud en 14 países de África subsahariana; datos DHS |
| 1 | Revista *Nutrition* | `hendy2025egypt` | Hendy et al., 2025, *Nutrition* | Introducción, Discusión | XGBoost con AUC 0.99 para emaciación en Egipto (DHS) |
| 1 | Revista *Nutrition* | `arya2025india` | Arya et al., 2025, *Nutrition* | Introducción, Discusión | Desnutrición crónica por hogar en India con datos satelitales; pobreza y educación como predictores |
| 2 | Carga mundial | `deonis2013who` | de Onis et al., 2013, *Maternal & Child Nutrition* | Introducción | Meta de la OMS de reducir 40 % la desnutrición crónica al 2025 |
| 2 | Carga mundial | `victora2008consequences` | Victora et al., 2008, *The Lancet* | Introducción | La desnutrición se asocia a menor talla adulta, escolaridad y productividad |
| 2 | Carga mundial | `sudfeld2015growth` | Sudfeld et al., 2015, *Pediatrics* | Introducción | Metaanálisis de 68 estudios: mejor talla para la edad, mejor desarrollo cognitivo |
| 2 | Carga mundial | `benjaminchung2023faltering` | Benjamin-Chung et al., 2023, *Nature* | Introducción, Discusión | El retraso empieza en los primeros meses y rara vez se revierte; respalda el peso al nacer como factor |
| 2 | Carga mundial | `bhutta2013interventions` | Bhutta et al., 2013, *The Lancet* | Introducción, Discusión | Diez intervenciones a gran escala reducirían 20 % la desnutrición crónica; respalda priorizar |
| 3 | Perú | `huicho2020peru` | Huicho et al., 2020, *Am J Clin Nutr* | Introducción, Discusión | Qué explicó la reducción en el Perú: educación, atención materna, migración urbana |
| 4 | ML con DHS | `rao2025metaanalysis` | Rao et al., 2025, *IJERPH* | Introducción, Discusión | Metaanálisis de 11 estudios con DHS: exactitud combinada de 68.9 % para desnutrición crónica |
| 7 | Pesos muestrales | `macnell2023weights` | MacNell et al., 2023, *PLOS ONE* | Metodología (Modelado) | Sin pesos muestrales, el desempeño se sobreestima (F1 de 81.9 % frente a 77.4 %) |
| 7 | Pesos muestrales | `wadekar2024survey` | Wadekar y Reiter, 2024, *Epidemiology* | Metodología (Evaluación) | Las métricas sin ponderar no representan a la población; las ponderadas sí |
| 7 | Pesos muestrales | `si2025sampling` | Si et al., 2025, *Annals of Epidemiology* | Discusión (limitaciones) | Contrapunto: en algunos casos el diseño muestral no cambia la predicción |
| 8 | Umbral y métricas | `deng2025highauc` | Deng et al., 2025, *Medical Decision Making* | Metodología, Discusión | Un AUC alto no basta: hay que elegir el umbral según el uso clínico |
| 9 | SHAP | `yehuala2026xai` | Yehuala et al., 2026, *Discover Artificial Intelligence* | Discusión | SHAP para desnutrición crónica en Etiopía; pobreza, edad y lugar del parto entre los factores |
| 9 | SHAP | `mgomezulu2025malawi` | Mgomezulu et al., 2025, *Human Nutrition and Metabolism* | Discusión | Exactitud cercana al 100 % con SMOTE en Malawi: ejemplo de resultados que conviene leer con cautela |
| 10 | Determinantes | `cardenas2022colombia` | Cárdenas et al., 2022, *Child Indicators Research* | Discusión | En Colombia la pobreza explica 54 % de la brecha rural-urbana |
| 10 | Determinantes | `martinez2019altitude` | Martínez et al., 2019, *Jornal de Pediatria* | Discusión | Más bajo peso y talla al nacer por encima de 2,000 m de altitud |
| 11 | TAM en salud | `chien2025tam` | Chien et al., 2025, *BMJ Health & Care Informatics* | Metodología (Despliegue) | TAM aplicado a alertas de apoyo a decisiones con médicos |
| 11 | TAM en salud | `herter2026cdss` | Herter et al., 2026, *JMIR Medical Informatics* | Resultados, Discusión | Herramienta de ML en atención primaria: 65 % la consideró útil y 67 % confió en ella |

## Búsquedas sin buenas citas

- **5. Selección de variables y fuga de información:** solo 2 registros, ninguno sobre datos de encuestas. Se mantiene `kaufman2011leakage`, que ya está en el `.bib`.
- **6. Pesos de clase en lugar de SMOTE:** los 9 registros tratan de otros temas (crédito, accidentes cerebrovasculares, hongos). Conviene repetir la búsqueda con este texto:

```
Cost-sensitive learning versus SMOTE for class imbalance in clinical prediction models: comparisons of calibration, sensitivity and precision. Return a matrix with: authors, year, journal, DOI, data, methods compared, and main conclusion. Limit to 2015-2026.
```

## Observaciones

- Los cuatro artículos de *Nutrition* coinciden con los artículos semilla del mapeo del asesor; además ya estaba `talukder2020bangladesh`.
- Las búsquedas 3 (Perú) traen dos artículos sin DOI (tendencias por región 2007–2018 y análisis espacial de 2017). No se usaron, pero podrían servir si se consigue el DOI.
- Varios estudios reportan exactitudes de 95 % a 100 %. Con clases desbalanceadas y sobremuestreo, esas cifras suelen estar infladas; la Discusión puede usarlos para explicar por qué este estudio reporta sensibilidad, precisión y F1.
