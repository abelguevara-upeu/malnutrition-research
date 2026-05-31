"""
Integración jerárquica de datos ENDES.

Reescritura en Python de src-r/core/integration.R.
Combina datos de Hogar, Vivienda, Miembros y Antropometría infantil.
"""

from loguru import logger
import pandas as pd

from mnp.loader import (
    get_available_years,
    load_endes,
    read_sav,
)


def integrate_child_data(year):
    """
    Integra la información de Niños, Miembros, Hogar y Vivienda para un año.

    Equivalente a integrate_child_data() de integration.R.

    Proceso de Join (Integración Jerárquica):
        A. Hogar (RECH0) + Vivienda (RECH23) → por HHID
        B. + Miembros (RECH1) → por HHID
        C. Antropometría (RECH6) + resultado B → por HHID + HC0=HVIDX

    Args:
        year: Año a procesar.

    Returns:
        DataFrame integrado o None si falla.
    """
    logger.info(f"🔗 Iniciando integración técnica para el año: {year}")

    try:
        # 1. Carga de componentes (sin etiquetas para mantener códigos puros)
        r0 = load_endes(year, "household", "rech0")
        r23 = load_endes(year, "housing", "rech23H")
        r1 = load_endes(year, "household", "rech1")
        r6 = load_endes(year, "anthropometry", "rech6")

        # 2. Normalización de nombres a minúsculas
        r0.columns = r0.columns.str.lower()
        r23.columns = r23.columns.str.lower()
        r1.columns = r1.columns.str.lower()
        r6.columns = r6.columns.str.lower()

        # Asegurar tipos string para llaves de join
        for df in [r0, r23, r1, r6]:
            for col in ["hhid", "hv001", "nconglome"]:
                if col in df.columns:
                    df[col] = df[col].astype(str)
            if "hvidx" in df.columns:
                df["hvidx"] = df["hvidx"].astype(str)
            if "hc0" in df.columns:
                df["hc0"] = df["hc0"].astype(str)

        # 3. Proceso de Join (Integración Jerárquica)
        # A. Hogar + Vivienda (Nivel Estructura)
        hogar_vivienda = r0.merge(r23, on="hhid", how="inner", suffixes=("", "_vivienda"))

        # B. + Miembros (Nivel Personas)
        hogar_miembros = hogar_vivienda.merge(
            r1, on="hhid", how="inner", suffixes=("", "_miembro")
        )

        # C. + Antropometría (Nivel Niños)
        # La llave crítica es hc0 = hvidx
        data_integrada = r6.merge(
            hogar_miembros,
            left_on=["hhid", "hc0"],
            right_on=["hhid", "hvidx"],
            how="inner",
            suffixes=("", "_hogar"),
        )

        data_integrada["year_survey"] = year

        # 4. Aplicar Labels a columnas que NO son llaves ni variables analíticas
        cols_no_label = {
            "hhid",
            "hc0",
            "hvidx",
            "hv001",
            "hv002",
            "nconglome",
            "hc70",
            "hc71",
            "hc72",
            "hv005",
            "hv005x",
            "hv270",
            "hv271",
            "year_survey",
        }

        # Intentamos aplicar etiquetas usando la metadata del archivo más relevante
        # Para esto, recargamos con metadata
        try:
            import json

            from mnp.config import RAW_DATA_DIR

            # Buscar el módulo de anthropometry para obtener metadata de labels
            for d in (RAW_DATA_DIR / str(year)).iterdir():
                meta_path = d / "metadata.json"
                if meta_path.exists():
                    with open(meta_path) as f:
                        mod_meta = json.load(f)
                    if "antropometri" in mod_meta.get("module_name", "").lower():
                        for sav_file in d.glob("*.sav"):
                            _, sav_meta = read_sav(sav_file)
                            for col in data_integrada.columns:
                                if (
                                    col not in cols_no_label
                                    and col in sav_meta.variable_value_labels
                                ):
                                    labels = sav_meta.variable_value_labels[col]
                                    if labels:
                                        data_integrada[col] = (
                                            data_integrada[col]
                                            .map(labels)
                                            .fillna(data_integrada[col])
                                        )
        except Exception:
            pass  # Si falla la aplicación de labels, continuamos sin ellas

        logger.success(f"✅ Integración exitosa. Columnas finales: {len(data_integrada.columns)}")
        return data_integrada

    except Exception as e:
        logger.error(f"❌ Error integrando año {year}: {e}")
        return None


def consolidate_master_children(years=None):
    """
    Genera el Dataset Maestro consolidado de varios años.

    Equivalente a consolidate_master_children() de integration.R.

    Args:
        years: Lista de años. None = todos los disponibles.

    Returns:
        DataFrame consolidado con todos los años.
    """
    if years is None:
        years = get_available_years()

    datasets = []
    for y in years:
        result = integrate_child_data(y)
        if result is not None:
            datasets.append(result)

    if not datasets:
        return None

    # Armonizar tipos entre años antes de apilar
    # Si una columna es numérica en un año pero object/string en otro,
    # convertirla a string en todos para evitar conflictos
    all_cols = set()
    for df in datasets:
        all_cols.update(df.columns)

    col_types = {}
    for col in all_cols:
        types = set()
        for df in datasets:
            if col in df.columns:
                types.add(str(df[col].dtype))
        col_types[col] = types

    # Columnas conflictivas: tienen más de un tipo entre años
    conflicting = [col for col, types in col_types.items() if len(types) > 1]

    if conflicting:
        logger.warning(
            f"⚠️ Armonizando {len(conflicting)} columnas con tipos inconsistentes entre años"
        )
        for df in datasets:
            for col in conflicting:
                if col in df.columns:
                    df[col] = df[col].astype(str)

    master = pd.concat(datasets, ignore_index=True)

    logger.success(
        f"📋 Dataset maestro consolidado: {len(master)} registros, {len(master.columns)} columnas"
    )

    return master
