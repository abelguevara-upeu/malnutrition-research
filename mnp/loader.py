"""
Cargador inteligente de datos ENDES.

Reescritura en Python de src-r/core/utils.R.
Usa pyreadstat para leer archivos SPSS (.sav) directamente.
"""

import json
from pathlib import Path

from loguru import logger
import pyreadstat

from mnp.config import RAW_DATA_DIR

# =============================================================================
# Diccionarios de Normalización (Consistencia Longitudinal)
# =============================================================================

# Mapeo de nombres de módulo en español → alias estándar en inglés
MODULE_ALIAS = {
    "caracteristicas_del_hogar": "household",
    "caracteristicas_de_la_vivienda": "housing",
    "salud": "health",
    "individual": "individual",
    "partos": "births",
    "parejas": "couples",
    "ninos": "children",
    "antropometria": "anthropometry",
    "peso_y_talla_anemia": "anthropometry",
    "conocimiento_de_sida_y_uso_del_condon": "hiv_aids",
    "conocimiento_de_sida_y_uso_del_cond_on": "hiv_aids",
    "datos_basicos_de_mef": "mef_basics",
    "disciplina_infantil": "discipline",
    "embarazo_parto_puerperio_y_lactancia": "maternal_health",
    "encuesta_de_salud": "health_survey",
    "historia_de_nacimiento_tabla_de_conocimiento_de_metodo": "birth_history",
    "inmunizacion_y_salud": "health_immunization",
    "inmunizaci_on_y_salud": "health_immunization",
    "mortalidad_materna_violencia_familiar": "mortality_violence",
    "nupcialidad_fecundidad_conyugue_y_mujer": "fertility_nuptiality",
    "nupcialidad_fecundidad_c_onyugue_y_mujer": "fertility_nuptiality",
    "programas_sociales": "social_programs",
    "programas_sociales_programas_sociales_x_hogar": "social_programs",
}

# Mapeo de nombres de registro (.sav) → alias estándar
RECORD_ALIAS = {
    # Birth History → rec22B
    "re223132": "rec22b",
    "re212232": "rec22b",
    "rec22312": "rec22b",
    "rec223132": "rec22b",
    "rec22b": "rec22b",
    # Discipline
    "rec93dv disciplina": "rec93d",
    "rec93dvdisciplina": "rec93d",
    "rec93d": "rec93d",
    # Fertility_nuptiality
    "re516171": "rec51f",
    "rec516171": "rec51f",
    "rec567_1": "rec51f",
    "rec51f": "rec51f",
    # HIV_aids
    "re758081": "rec75i",
    "rec7581": "rec75i",
    "rec75_81": "rec75i",
    "rec75i": "rec75i",
    # Housing
    "rech23": "rech23h",
    "rech2_h3": "rech23h",
    "rech2_3": "rech23h",
    "rech23h": "rech23h",
    # MEF_basics
    "rec0111": "rec0111m",
    "rec01_11": "rec0111m",
    "rec0111m": "rec0111m",
    # Mortality_violence → rec84M
    "re848591": "rec84m",
    "rec84_91": "rec84m",
    "rec84_dv": "rec84m",
    "rec84dv": "rec84m",
    "rec84": "rec84m",
    "rec84m": "rec84m",
    # Social_programs
    "programas sociales x hogar": "ps_x_hogar",
}


def normalize_module_name(name):
    """
    Normaliza el nombre del módulo para consistencia longitudinal.

    Convierte nombres en español a alias estándar en inglés.
    """
    if not name or not isinstance(name, str):
        return "unknown"

    # Convertir a snake_case limpio (quitar tildes y caracteres especiales)
    import re
    import unicodedata

    clean = name.lower().strip()
    # Quitar tildes: é → e
    clean = unicodedata.normalize("NFD", clean)
    clean = "".join(c for c in clean if unicodedata.category(c) != "Mn")
    # Todo lo no alfanumérico a _
    clean = re.sub(r"[^a-z0-9]", "_", clean)
    clean = re.sub(r"_+", "_", clean)  # Colapsar guiones bajos
    clean = clean.strip("_")

    return MODULE_ALIAS.get(clean, clean)


def normalize_record_name(record_name):
    """
    Normaliza el nombre de un registro (archivo .sav) a su alias estándar.
    """
    import re

    # Quitar extensión y sufijos de año
    name = re.sub(r"\.sav$", "", record_name, flags=re.IGNORECASE)
    name = re.sub(r"_\d{4}$", "", name)
    name = name.lower()

    return RECORD_ALIAS.get(name, name)


def get_available_years():
    """
    Obtiene la lista de años disponibles en data/raw.

    Returns:
        Lista de años (int) ordenados de forma descendente.
    """
    if not RAW_DATA_DIR.exists():
        return []

    years = []
    for d in RAW_DATA_DIR.iterdir():
        if d.is_dir():
            try:
                years.append(int(d.name))
            except ValueError:
                continue

    return sorted(years, reverse=True)


def read_sav(filepath, n_max=None):
    """
    Lee un archivo SPSS (.sav) usando pyreadstat.

    Args:
        filepath: Ruta al archivo .sav
        n_max: Número máximo de filas a leer (None = todas)

    Returns:
        Tupla (DataFrame, metadata) donde metadata contiene labels y formatos.
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {filepath}")

    if n_max is not None and n_max < float("inf"):
        df, meta = pyreadstat.read_sav(str(filepath), row_limit=int(n_max))
    else:
        df, meta = pyreadstat.read_sav(str(filepath))

    return df, meta


def apply_labels(df, meta):
    """
    Aplica etiquetas de valor SPSS a las columnas del DataFrame.

    Equivalente a haven::as_factor() en R.

    Args:
        df: DataFrame con datos
        meta: Metadata de pyreadstat

    Returns:
        DataFrame con columnas categóricas donde hay etiquetas.
    """
    for col in df.columns:
        if col in meta.variable_value_labels:
            labels = meta.variable_value_labels[col]
            if labels:
                df[col] = df[col].map(labels).fillna(df[col])
    return df


def load_endes(year=None, module=None, record=None, clean=False, n_max=None):
    """
    Carga archivos ENDES de forma inteligente.

    Equivalente a load_endes() de utils.R.

    Args:
        year: Año (int) o None para cargar toda la historia.
        module: Alias o nombre del módulo (ej: "household", "anthropometry").
        record: Prefijo del registro (ej: "RECH0", "RECH6"). None = módulo completo.
        clean: Si True, aplica etiquetas de valor SPSS.
        n_max: Número máximo de filas por archivo.

    Returns:
        DataFrame (si es un registro) o dict de DataFrames (si es módulo completo).
    """
    # Si no se especifica año, carga historia completa
    if year is None:
        return load_endes_history(module, record, clean=clean, n_max=n_max)

    # Si se pasan múltiples años como lista
    if isinstance(year, (list, tuple, range)):
        return load_endes_history(module, record, years=list(year), clean=clean, n_max=n_max)

    base_path = RAW_DATA_DIR / str(year)
    if not base_path.exists():
        raise FileNotFoundError(f"No se encontró la carpeta para el año {year}: {base_path}")

    # Normalizar input
    target_module_alias = normalize_module_name(module)
    target_record_alias = normalize_record_name(record) if record else None

    # Buscar en los subdirectorios de ese año
    module_found = False
    for d in sorted(base_path.iterdir()):
        if not d.is_dir():
            continue

        meta_file = d / "metadata.json"
        if meta_file.exists():
            try:
                with open(meta_file, "r", encoding="utf-8") as f:
                    meta = json.load(f)
            except Exception:
                continue

            # Verificar si el alias del módulo coincide
            if normalize_module_name(meta.get("module_name", "")) == target_module_alias:
                module_found = True

                # Listar archivos .sav
                sav_files = sorted(d.glob("*.sav")) + sorted(d.glob("*.SAV"))
                if not sav_files:
                    continue

                # Caso 1: Módulo completo
                if record is None:
                    logger.info(
                        f"📦 Cargando módulo completo: {target_module_alias} desde {d.name}"
                    )
                    tablas = {}
                    for sav in sav_files:
                        df, sav_meta = read_sav(sav, n_max=n_max)
                        alias = normalize_record_name(sav.name)
                        if clean:
                            df = apply_labels(df, sav_meta)
                        tablas[alias] = df
                    return tablas

                # Caso 2: Registro específico
                for sav in sav_files:
                    if normalize_record_name(sav.name) == target_record_alias:
                        logger.info(
                            f"✓ Cargando registro: {sav.name} desde {d.name} "
                            f"[Alias: {target_record_alias}]"
                        )
                        df, sav_meta = read_sav(sav, n_max=n_max)
                        if clean:
                            df = apply_labels(df, sav_meta)
                        return df

    # Error handling descriptivo
    if not module_found:
        raise FileNotFoundError(
            f"No se encontró el módulo {module} (alias: {target_module_alias}) para el año {year}"
        )
    else:
        raise FileNotFoundError(
            f"Se encontró el módulo {target_module_alias} pero no el registro "
            f"{record} (alias: {target_record_alias}) para el año {year}"
        )


def load_endes_history(module, record=None, years=None, clean=True, n_max=None):
    """
    Carga la historia completa o un rango de años de un módulo/registro.

    Equivalente a load_endes_history() de utils.R.

    Args:
        module: Alias del módulo.
        record: Prefijo del registro (ej: "RECH6"). None = módulo completo.
        years: Lista de años. None = todos los disponibles.
        clean: Si True, aplica etiquetas.
        n_max: Número máximo de filas por archivo.

    Returns:
        Dict {año: DataFrame} con los datos cargados.
    """
    if years is None:
        years = get_available_years()
        if not years:
            raise FileNotFoundError("No se encontraron carpetas de años en data/raw")
        logger.info(f"🔎 Detectada historia de {len(years)} años.")

    data_history = {}
    for y in years:
        try:
            result = load_endes(y, module, record=record, clean=clean, n_max=n_max)
            data_history[y] = result
        except Exception as e:
            logger.warning(f"⚠️ Nota: Año {y} no cargado ({e})")

    logger.success("✅ ¡Historia cargada y organizada por años!")
    return data_history


def format_year_ranges(years):
    """
    Formatea un vector de años en rangos legibles (ej: 1996, 2005-2024).

    Args:
        years: Lista de años numéricos.

    Returns:
        String con rangos formateados.
    """
    if not years:
        return ""

    years = sorted(set(int(y) for y in years))
    if len(years) == 1:
        return str(years[0])

    ranges = []
    start = years[0]
    prev = years[0]

    for y in years[1:]:
        if y != prev + 1:
            if start == prev:
                ranges.append(str(start))
            else:
                ranges.append(f"{start}-{prev}")
            start = y
        prev = y

    # Último rango
    if start == prev:
        ranges.append(str(start))
    else:
        ranges.append(f"{start}-{prev}")

    return ", ".join(ranges)
