# malnutrition-research

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Repositorio principal para la investigación de desnutrición crónica infantil usando datos ENDES (Encuesta Demográfica y de Salud Familiar) del INEI, Perú.

## Inicio Rápido

```bash
# 1. Crear entorno virtual
make create_environment
source .venv/bin/activate

# 2. Instalar dependencias
make requirements

# 3. Extraer datos ENDES del INEI (descarga a data/raw/)
python -m mnp.dataset extract --year 2024

# 4. Ejecutar pipeline completo (raw → interim)
make pipeline
```

## Comandos del Pipeline

| Comando | Descripción |
|---|---|
| `make extract` | Descarga datos raw desde INEI |
| `make clean_data` | Integra y limpia datos (raw → interim/master_cleaned.csv) |
| `make validate_data` | Aplica filtros de calidad (interim → master_validated.csv) |
| `make pipeline` | Ejecuta todo el pipeline: extract → clean → validate |

## CLI de Extracción

```bash
# Extraer un año específico
python -m mnp.dataset extract --year 2024

# Extraer rango de años
python -m mnp.dataset extract --year 1996-2024

# Solo verificar integridad (sin descargar)
python -m mnp.dataset extract --year 2024 --check --verbose

# Auditoría detallada
python -m mnp.dataset audit --year 2024
```

## Uso como Módulo Python

```python
from mnp.loader import load_endes

# Cargar un registro específico de un año
df = load_endes(2024, module="anthropometry", record="rech6")

# Cargar módulo completo (dict de DataFrames)
tablas = load_endes(2024, module="household")

# Cargar historia longitudinal
historia = load_endes(module="anthropometry", record="rech6", years=range(2010, 2025))

# Calcular indicador de desnutrición crónica
from mnp.utils.indicators import calculate_chronic_malnutrition
resultado = calculate_chronic_malnutrition(2024)
```

## Project Organization

```
├── LICENSE            ← Open-source license
├── Makefile           ← Makefile with convenience commands
├── README.md          ← This file
├── data
│   ├── external       ← Data from third party sources
│   ├── interim        ← Intermediate data (master_cleaned.csv, master_validated.csv)
│   ├── processed      ← Final, canonical data sets for modeling
│   └── raw            ← Original ENDES data from INEI (.sav files)
│       ├── 1996/      ← Datos por año
│       │   ├── Modulo.../
│       │   │   ├── *.sav         ← Archivos SPSS originales
│       │   │   ├── *.pdf         ← Diccionarios y fichas técnicas
│       │   │   └── metadata.json ← Metadata de descarga
│       ├── ...
│       └── 2024/
│
├── docs               ← MkDocs project documentation
├── models             ← Trained models and predictions
├── notebooks          ← Jupyter notebooks and exploration files
├── pyproject.toml     ← Project configuration and dependencies
├── references         ← Data dictionaries, manuals, ENDES documentation
├── reports            ← Generated analysis as HTML, PDF, etc.
│   └── figures
│
├── mnp   ← Source code
│   ├── __init__.py
│   ├── config.py           ← Paths and ENDES configuration
│   ├── dataset.py          ← CLI: extract/audit data from INEI
│   ├── features.py         ← Feature engineering (placeholder)
│   ├── integration.py      ← Hierarchical data integration
│   ├── loader.py           ← Smart ENDES data loader (pyreadstat)
│   ├── modeling/
│   │   ├── predict.py
│   │   └── train.py
│   ├── pipeline/
│   │   ├── cleaning.py     ← raw → interim/master_cleaned.csv
│   │   └── validation.py   ← cleaned → interim/master_validated.csv
│   ├── plots.py            ← Visualization code
│   └── utils/
│       ├── __init__.py
│       ├── console.py      ← Rich console UI for extraction
│       ├── extractor.py    ← INEI web scraper and downloader
│       └── indicators.py   ← Malnutrition indicator calculations
│
└── tests
```

## Estructura de Datos ENDES

Los datos se organizan por año y módulo. Cada módulo contiene archivos SPSS (.sav):

| Módulo | Contenido |
|---|---|
| Modulo 1629 | Características del Hogar (RECH0, RECH1) |
| Modulo 1630 | Características de la Vivienda (RECH23) |
| Modulo 1638 | Antropometría - Peso y Talla (RECH5, RECH6) |
| Modulo 1641 | Programas Sociales |

Ver [references/endes_relaciones.md](references/endes_relaciones.md) para el diagrama completo de relaciones entre tablas.

## Tecnologías

- **Python 3.12** — Lenguaje único del proyecto
- **pyreadstat** — Lectura de archivos SPSS (.sav), reemplaza haven de R
- **pandas** — Manipulación de datos, reemplaza dplyr/tidyr de R
- **Rich** — UI de consola para extracción
- **Cookiecutter Data Science** — Estructura de proyecto estándar

--------
