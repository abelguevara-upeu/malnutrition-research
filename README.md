# malnutrition-research

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Repositorio principal para la investigación de desnutrición crónica infantil usando datos ENDES (Encuesta Demográfica y de Salud Familiar) del INEI, Perú.

---

## 🛠️ Cómo Ejecutar el Proyecto (Mac / Linux / Windows)

Para garantizar la reproducibilidad científica y evitar conflictos de software, tienes dos formas de ejecutar este proyecto: **usando Docker** (altamente recomendado, funciona igual en cualquier sistema operativo) o **de forma nativa**.

### Opción A: Usando Docker (Recomendado)
*Esta opción no requiere instalar Python ni configurar entornos virtuales locales. Todo corre dentro de un contenedor aislado con soporte completo para exportación de gráficos y PDFs con LaTeX.*

#### Requisitos Previos:
* Instalar [Docker Desktop](https://www.docker.com/products/docker-desktop/) en tu computadora.

#### Instrucciones por Sistema Operativo:

##### **macOS y Linux:**
1. Abre tu terminal en la carpeta raíz del proyecto.
2. Inicia el contenedor en segundo plano:
   ```bash
   make docker-up
   ```
3. Accede a Jupyter Lab en tu navegador: **[http://localhost:8888](http://localhost:8888)**
4. Si necesitas entrar a la terminal interna de Docker para correr scripts o comandos:
   ```bash
   make docker-shell
   ```
5. Para apagar el contenedor al terminar:
   ```bash
   make docker-down
   ```

##### **Windows (usando Git Bash, WSL o PowerShell):**
*Si usas Git Bash o WSL, puedes usar los mismos comandos de `make` que en macOS/Linux. Si usas PowerShell o CMD, ejecuta los comandos directos de Docker:*
1. Abre tu terminal de Windows en la carpeta del proyecto.
2. Inicia el contenedor en segundo plano:
   ```powershell
   docker compose up -d
   ```
3. Accede a Jupyter Lab en tu navegador: **[http://localhost:8888](http://localhost:8888)**
4. Si necesitas entrar al shell interactivo del contenedor:
   ```powershell
   docker compose exec malnutrition-research-workspace bash
   ```
5. Para apagar el contenedor:
   ```powershell
   docker compose down
   ```

---

### Opción B: Instalación Nativa (Local)
*Requiere instalar Python 3.12 y herramientas de compilación en tu máquina.*

#### **macOS y Linux:**
1. Crear el entorno virtual con pyenv/venv:
   ```bash
   make create_environment
   source .venv/bin/activate
   ```
2. Instalar dependencias del proyecto:
   ```bash
   make requirements
   ```
3. Ejecutar el pipeline completo:
   ```bash
   make pipeline
   ```

#### **Windows (Nativo):**
1. Asegúrate de tener Python 3.12 instalado localmente.
2. Abre la terminal (PowerShell) en la carpeta raíz:
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
3. Instalar dependencias:
   ```powershell
   pip install -e .
   ```
4. Ejecutar la extracción manual:
   ```powershell
   python -m mnp.dataset extract --year 2024
   ```

---

## 📅 Comandos del Pipeline (Dentro del Contenedor / Nativo)

| Comando | Descripción |
|---|---|
| `make extract` | Descarga datos raw desde INEI |
| `make clean_data` | Integra y limpia datos (raw → interim/master_cleaned.csv) |
| `make validate_data` | Aplica filtros de calidad (interim → master_validated.csv) |
| `make pipeline` | Ejecuta todo el pipeline secuencialmente |
| `make clean` | Limpia archivos cache de Python y archivos auxiliares de LaTeX |

---

## 📁 Organización del Proyecto (Directory Structure)

```
├── LICENSE            ← Licencia Open-Source
├── Makefile           ← Comandos automatizados para reproducibilidad
├── README.md          ← Este archivo
├── docker-compose.yml ← Configuración de servicios de desarrollo de Docker
├── Dockerfile         ← Receta de Docker para levantar el entorno científico
├── pyproject.toml     ← Configuración del proyecto y dependencias de Python
│
├── data/
│   ├── external/      ← Datos de terceras fuentes externas
│   ├── interim/       ← Datos intermedios de limpieza (master_cleaned, master_validated)
│   ├── processed/     ← Datos finales procesados listos para modelamiento estadístico
│   └── raw/           ← Datos ENDES originales comprimidos/extraídos desde INEI (.sav)
│
├── docs/              ← Carpeta principal de documentación y artículos
│   ├── mkdocs.yml     ← Configuración del sitio web de MkDocs
│   ├── docs/          ← Wiki/Documentación técnica en Markdown (MkDocs)
│   │   ├── index.md
│   │   └── getting-started.md
│   └── papers/        ← Artículos académicos, propuestas y manuscritos (en LaTeX)
│       ├── graduation-profile/  ← Propuesta de perfil de egreso en LaTeX
│       └── malnutrition-paper/  ← Artículo de investigación de desnutrición
│
├── mnp/               ← Código fuente de Python (Módulos de datos)
│   ├── __init__.py
│   ├── config.py      ← Rutas base y configuraciones de módulos ENDES
│   ├── dataset.py     ← CLI para interactuar con los datos (extract/audit)
│   ├── loader.py      ← Lector inteligente de archivos SPSS (.sav)
│   ├── pipeline/
│   │   ├── cleaning.py   ← Proceso de extracción a base limpia unificada
│   │   └── validation.py ← Filtros de calidad y consistencia lógica
│   └── utils/
│       ├── extractor.py  ← Web scraper automatizado del portal de INEI
│       └── indicators.py ← Cálculos de indicadores biométricos de desnutrición
│
├── notebooks/         ← Jupyter Notebooks de exploración y análisis visual
├── models/            ← Modelos predictivos entrenados y checkpoints
├── references/        ← Diccionarios de datos, manuales oficiales y guías ENDES
├── reports/           ← Reportes generados (Figuras PNG/PDF, HTML, etc.)
└── tests/             ← Pruebas unitarias para validar la integridad del código
```

---

## 📊 Estructura de Datos ENDES

Los datos descargados automáticamente por el scraper se organizan por año y por el código de módulo oficial del INEI:

| Módulo | Contenido Principal |
|---|---|
| Modulo 1629 | Características del Hogar (RECH0, RECH1) |
| Modulo 1630 | Características de la Vivienda (RECH23) |
| Modulo 1638 | Antropometría - Peso y Talla infantil (RECH5, RECH6) |
| Modulo 1641 | Programas Sociales y coberturas alimentarias |

*Ver [references/endes_relaciones.md](references/endes_relaciones.md) para el esquema detallado del modelo relacional de las tablas ENDES.*

---

## 💻 Tecnologías Utilizadas

* **Docker & Docker Compose** — Entornos científicos reproducibles.
* **Python 3.12** — Lenguaje núcleo del proyecto.
* **pyreadstat** — Lector optimizado de formatos de datos estadísticos (.sav / SPSS).
* **pandas** — Análisis y estructuración de sets de datos.
* **Jupyter Lab** — Entorno interactivo de análisis científico.
* **LaTeX** — Composición tipográfica de alta calidad para artículos y reportes.
