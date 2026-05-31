"""
Cálculo de indicadores de desnutrición crónica infantil.

Reescritura en Python de src-r/core/indicators.R.
Implementa el cálculo según el Patrón OMS usando datos ENDES.
"""

from loguru import logger
import numpy as np
import pandas as pd

from mnp.loader import load_endes


def calculate_chronic_malnutrition(year):
    """
    Calcula la Desnutrición Crónica Infantil (Patrón OMS) para un año dado.

    Lógica equivalente a calculate_chronic_malnutrition() de indicators.R.

    Proceso:
        1. Carga RECH6 (antropometría niños), RECH1 (miembros), RECH0 (hogar)
        2. Join: RECH6 + RECH1 (por HHID + HC0=HVIDX) + RECH0 (por HHID)
        3. Filtro: Solo miembros que durmieron en el hogar (HV103=1)
        4. Ponderación: Factor de expansión HV005 / 1,000,000
        5. Clasificación: HC70 < -200 = desnutrido (Patrón OMS)

    Args:
        year: Año a calcular.

    Returns:
        DataFrame con columnas: Anio, Casos_Muestra, Porcentaje_DC
    """
    logger.info(f"🚀 Calculando Desnutrición Crónica para el año {year}...")

    # 1. Cargar registros necesarios (sin etiquetas para mantener códigos numéricos)
    r6 = load_endes(year, module="anthropometry", record="rech6")
    r1 = load_endes(year, module="household", record="rech1")
    r0 = load_endes(year, module="household", record="rech0")

    # 2. Normalizar nombres de columnas a minúsculas
    r6.columns = r6.columns.str.lower()
    r1.columns = r1.columns.str.lower()
    r0.columns = r0.columns.str.lower()

    # Seleccionar columnas relevantes
    r6_cols = [c for c in ["hhid", "hc0", "hc70"] if c in r6.columns]
    r1_cols = [c for c in ["hhid", "hvidx", "hv103"] if c in r1.columns]
    r0_cols = [c for c in ["hhid", "hv005", "hv007", "hv005x"] if c in r0.columns]

    r6 = r6[r6_cols]
    r1 = r1[r1_cols]
    r0 = r0[r0_cols]

    # 3. Join de las tablas (HC0 = HVIDX)
    data = r6.merge(r1, left_on=["hhid", "hc0"], right_on=["hhid", "hvidx"], how="inner")
    data = data.merge(r0, on="hhid", how="inner")

    # 4. Filtro: Durmió en el hogar
    data = data[data["hv103"] == 1].copy()

    # 5. Ponderación (Factor de expansión)
    # Lógica especial para 2015 que usa hv005x
    if "hv005x" in data.columns and data["hv005x"].notna().any():
        unique_year = data["hv007"].unique()
        if len(unique_year) == 1 and unique_year[0] == 2015:
            data["factor_val"] = data["hv005x"]
        else:
            data["factor_val"] = data["hv005"]
    else:
        data["factor_val"] = data["hv005"]

    data["peso"] = data["factor_val"] / 1_000_000

    # 6. Clasificación de desnutrición (Patrón OMS: hc70 < -200)
    data["hc70"] = pd.to_numeric(data["hc70"], errors="coerce")
    data["desnutrido"] = np.where(
        data["hc70"] < -200,
        1,
        np.where((data["hc70"] >= -200) & (data["hc70"] < 601), 0, np.nan),
    )

    # Eliminar registros sin medición válida
    data = data.dropna(subset=["desnutrido"])

    # 7. Cálculo del Indicador (Media Ponderada)
    if len(data) == 0:
        logger.warning(f"⚠️ No hay datos válidos para el año {year}")
        return pd.DataFrame({"Anio": [year], "Casos_Muestra": [0], "Porcentaje_DC": [0.0]})

    porcentaje = np.average(data["desnutrido"], weights=data["peso"]) * 100

    resultado = pd.DataFrame(
        {
            "Anio": [year],
            "Casos_Muestra": [len(data)],
            "Porcentaje_DC": [round(porcentaje, 2)],
        }
    )

    return resultado
