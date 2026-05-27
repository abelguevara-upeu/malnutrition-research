"""
Pipeline de validación: interim/master_cleaned.csv → interim/master_validated.csv

Reescritura en Python de src-r/pipeline/02_validation.R.
Toma la data cleaned y aplica filtros de calidad y validación científica.
"""

from loguru import logger
import pandas as pd

from mnp.config import INTERIM_DATA_DIR


def main():
    """Ejecuta el pipeline de validación."""
    logger.info("🚀 [PIPELINE] Iniciando Construcción de Capa VALIDATED...")

    # 1. Cargar la data Cleaned
    input_path = INTERIM_DATA_DIR / "master_cleaned.csv"
    if not input_path.exists():
        logger.error(
            f"❌ No se encontró la data Cleaned en {input_path}. "
            "Ejecuta primero el pipeline de cleaning."
        )
        return

    master = pd.read_csv(input_path)
    inicial = len(master)

    logger.info("🔍 Aplicando filtros de validación...")

    # 2. Aplicar lógica de validación (Criterios de inclusión/exclusión)

    # Filtro A: Miembros que durmieron en el hogar (HV103)
    hv103_col = "hv103" if "hv103" in master.columns else None
    if hv103_col:
        master[hv103_col] = master[hv103_col].astype(str)
        master = master[master[hv103_col].isin(["1", "1.0", "Sí", "Yes", "si"])]

    # Filtro B: Casos con medición de talla válida (HC70)
    # hc70 debe estar entre -600 y 600 (códigos especiales fuera de este rango)
    hc70_col = "hc70" if "hc70" in master.columns else None
    if hc70_col:
        master["hc70_num"] = pd.to_numeric(master[hc70_col], errors="coerce")
        master = master[
            master["hc70_num"].notna() & (master["hc70_num"] >= -600) & (master["hc70_num"] <= 600)
        ]

    # Filtro C: Ponderación válida (HV005)
    hv005_col = "hv005" if "hv005" in master.columns else None
    if hv005_col:
        master[hv005_col] = pd.to_numeric(master[hv005_col], errors="coerce")
        master = master[master[hv005_col].notna() & (master[hv005_col] > 0)]

    # 3. Reporte de limpieza
    final = len(master)
    eliminados = inicial - final
    rendimiento = round((final / inicial) * 100, 2) if inicial > 0 else 0

    logger.info("📊 REPORTE DE VALIDACIÓN:")
    logger.info(f"   - Registros iniciales (Cleaned): {inicial}")
    logger.info(f"   - Registros eliminados por calidad: {eliminados}")
    logger.info(f"   - Registros finales (Validated): {final}")
    logger.info(f"   - Rendimiento: {rendimiento}%")

    # 4. Guardar resultados
    output_path = INTERIM_DATA_DIR / "master_validated.csv"
    logger.info(f"💾 Guardando {output_path.name}...")
    master.to_csv(output_path, index=False)

    logger.success("✨ Capa VALIDATED finalizada con éxito!")


if __name__ == "__main__":
    main()
