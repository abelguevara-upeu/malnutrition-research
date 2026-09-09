from datetime import date
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file if it exists
load_dotenv()

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[1]
logger.info(f"PROJ_ROOT path is: {PROJ_ROOT}")

DATA_DIR = PROJ_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

MODELS_DIR = PROJ_ROOT / "models"

REPORTS_DIR = PROJ_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# --- ENDES Configuration ---
INEI_BASE_URL = "https://proyectos.inei.gob.pe"
ENDES_SURVEY_NAME = "Encuesta Demográfica y de Salud Familiar - ENDES"

# Rango histórico de datos disponibles.
# El tope se calcula con el año actual para que la ingesta descubra por sí sola
# los años nuevos que publique el INEI, sin tener que editar esta constante.
# El INEI publica la ENDES del año N durante N+1, así que el año en curso suele
# estar vacío todavía: get_module_links() devuelve [] y la ingesta lo omite.
ENDES_YEAR_START = 1996
ENDES_YEAR_END = date.today().year

# Rango analítico del estudio. Arranca en 2007 porque es desde ese año que la
# ENDES es continua y comparable; el tope se descubre solo (ver ENDES_YEAR_END),
# de modo que los scripts recogen cada año nuevo sin editar el rango a mano.
# Uso: load_endes(year=ANALYSIS_YEARS, ...)
ANALYSIS_YEAR_START = 2007


def analysis_years() -> range:
    """Años 2007..N con datos ENDES efectivamente descargados en data/raw.

    Se cierra sobre lo que hay en disco y no sobre el año del reloj: el INEI
    publica la ENDES del año N durante N+1, asi que el año en curso suele estar
    vacio todavia. Devolver un rango que incluya años inexistentes haria que
    cada script arrastrase avisos de módulo no encontrado.
    """
    years = [
        int(d.name)
        for d in RAW_DATA_DIR.iterdir()
        if d.is_dir() and d.name.isdigit() and int(d.name) >= ANALYSIS_YEAR_START
    ]
    return range(ANALYSIS_YEAR_START, (max(years) if years else ANALYSIS_YEAR_START) + 1)

# --- Global Data Science Settings ---
RANDOM_SEED = 42
TEST_SIZE = 0.2  # Proporción estándar para división de train/test (80/20)

# --- Logging a Archivo ---
LOGS_DIR = PROJ_ROOT / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)  # Crea la carpeta /logs si no existe
logger.add(
    LOGS_DIR / "pipeline.log",
    rotation="10 MB",  # Crea un archivo nuevo al llegar a 10MB
    retention="10 days",  # Conserva logs de los últimos 10 días
    level="INFO",
    encoding="utf-8",
)

# If tqdm is installed, configure loguru with tqdm.write
# https://github.com/Delgan/loguru/issues/135
try:
    from tqdm import tqdm

    logger.remove(0)
    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
except ModuleNotFoundError:
    pass
