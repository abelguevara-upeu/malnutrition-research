"""
Pipeline de limpieza: raw → interim/master_cleaned.csv

Reescritura en Python de src-r/pipeline/01_cleaning.R.
Carga datos raw de todos los años disponibles, integra las tablas jerárquicas
y genera el dataset maestro limpio.
"""

from loguru import logger

from mnp.config import INTERIM_DATA_DIR
from mnp.integration import consolidate_master_children
from mnp.loader import get_available_years


def main():
    """Ejecuta el pipeline de limpieza."""
    logger.info("🚀 [PIPELINE] Iniciando Construcción de Capa CLEANED...")

    # Asegurar carpeta de salida
    INTERIM_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Obtener años disponibles
    anios = get_available_years()
    logger.info(f"📅 Años disponibles: {len(anios)}")

    # 2. Consolidar Gran Tabla Maestra (Hogar + Vivienda + Miembros + Niños)
    master_cleaned = consolidate_master_children(anios)

    if master_cleaned is None or len(master_cleaned) == 0:
        logger.error("❌ No se pudo generar el dataset maestro.")
        return

    # 3. Guardar resultados
    output_path = INTERIM_DATA_DIR / "master_cleaned.csv"
    logger.info(f"💾 Guardando {output_path.name}...")
    master_cleaned.to_csv(output_path, index=False)

    logger.success("✨ Capa CLEANED finalizada con éxito!")
    logger.info(f"📊 Registros totales: {len(master_cleaned)}")
    logger.info(f"📐 Variables totales: {len(master_cleaned.columns)}")


if __name__ == "__main__":
    main()
