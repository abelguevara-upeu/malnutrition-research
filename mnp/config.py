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

# Rango histórico de datos disponibles
ENDES_YEAR_START = 1996
ENDES_YEAR_END = 2024

# --- Global Data Science Settings ---
RANDOM_SEED = 42
TEST_SIZE = 0.2  # Proporción estándar para división de train/test (80/20)

# --- Logging a Archivo ---
LOGS_DIR = PROJ_ROOT / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)  # Crea la carpeta /logs si no existe
logger.add(
    LOGS_DIR / "pipeline.log", 
    rotation="10 MB",       # Crea un archivo nuevo al llegar a 10MB
    retention="10 days",    # Conserva logs de los últimos 10 días
    level="INFO",
    encoding="utf-8"
)

# If tqdm is installed, configure loguru with tqdm.write
# https://github.com/Delgan/loguru/issues/135
try:
    from tqdm import tqdm

    logger.remove(0)
    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
except ModuleNotFoundError:
    pass
