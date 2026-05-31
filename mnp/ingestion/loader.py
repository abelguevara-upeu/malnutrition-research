"""
Cargador inteligente de datos ENDES.

Reescritura en Python de src-r/core/utils.R.
Usa pyreadstat para leer archivos SPSS (.sav) directamente.
"""

import json
from pathlib import Path
import re
import unicodedata
from typing import Any, Tuple, Union

import pandas as pd
from loguru import logger
import pyreadstat

from mnp.config import RAW_DATA_DIR

# =============================================================================
# 1. CONSTANTES Y DICCIONARIOS DE NORMALIZACIÓN
# =============================================================================

# Mapeo de nombres de módulo (metadata.json) en español → alias estándar en inglés
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
    # Household
    "rech0": "household_characteristics",
    "rech1": "household_roster",
    "rech4": "rech4",
    "rech8": "rech8",
    "rech9": "rech9",
    "rechm": "rechm",
    "vivienda": "household_characteristics",
    "miembros_hogar": "household_roster",
    # Mortality_violence → rec84M
    "re848591": "rec84m",
    "rec84_91": "rec84m",
    "rec84_dv": "rec84m",
    "rec84dv": "rec84m",
    "rec84": "rec84m",
    "rec84m": "rec84m",
    # Social_programs
    "programas sociales x hogar": "ps_x_hogar",
    # Anthropometry / Peso y Talla / Anemia
    "rech6": "rech6",  # Niños: z-scores talla/peso, hemoglobina
    "rec44": "rec44",  # Datos individuales complementarios
    "rech5": "rech5",  # Mujeres: hemoglobina, anemia
}


# =============================================================================
# 2. FUNCIONES AUXILIARES (Helpers)
# Estas funciones se utilizan internamente para estandarizar textos, leer
# archivos base o procesar metadatos.
# =============================================================================


def _read_metadata(folder_path):
    """Lee y devuelve el metadata.json de una carpeta, o un dict vacío si falla."""
    meta_file = folder_path / "metadata.json"
    if meta_file.exists():
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def _normalize_module_name(name, year=None):
    """
    Normaliza el nombre del módulo para consistencia longitudinal.
    Convierte nombres en español o códigos numéricos a alias estándar en inglés.
    """
    if not name:
        return "unknown"

    name_str = str(name)

    # Si es un código numérico, buscamos su nombre real en los metadatos
    if name_str.isdigit():
        # Si no nos dan año, buscamos en el más reciente disponible hacia atrás
        if year is not None:
            years_to_search = [str(year)]
        else:
            years_to_search = [str(y) for y in get_available_years()]

        # Usamos una mini-función interna (closure) para evitar las banderas (flags)
        def _find_name_by_code():
            for y in years_to_search:
                base_path = RAW_DATA_DIR / y
                if not base_path.exists():
                    continue
                for folder in base_path.iterdir():
                    if not folder.is_dir():
                        continue

                    meta = _read_metadata(folder)
                    if str(meta.get("module_code")) == name_str:
                        # Al usar return, destruimos ambos bucles instantáneamente
                        return meta.get("module_name", name_str)
            return name_str  # Si no encuentra nada, devuelve el original

        name_str = _find_name_by_code()

    clean_name = name_str.lower().strip()
    clean_name = unicodedata.normalize("NFD", clean_name)
    clean_name = "".join(c for c in clean_name if unicodedata.category(c) != "Mn")
    clean_name = re.sub(r"[^a-z0-9]", "_", clean_name)
    clean_name = re.sub(r"_+", "_", clean_name)
    clean_name = clean_name.strip("_")
    # Idempotencia: Si ya es un alias estándar válido, lo devolvemos tal cual
    if clean_name in MODULE_ALIAS.values() or clean_name.startswith("new_"):
        return clean_name

    if clean_name not in MODULE_ALIAS:
        logger.warning(f"Modulo desconocido: Marcándolo como 'new_{clean_name}'")

    return MODULE_ALIAS.get(clean_name, f"new_{clean_name}")


def _normalize_record_name(name):
    """
    Normaliza el nombre de un registro (archivo .sav) a su alias estándar.
    """
    if not name or not isinstance(name, str):
        return "unknown"

    clean_name = re.sub(r"\.sav$", "", name, flags=re.IGNORECASE)
    clean_name = re.sub(r"_\d{4}$", "", clean_name)
    clean_name = clean_name.lower()
    # Idempotencia: Si ya es un alias estándar válido, lo devolvemos tal cual
    if clean_name in RECORD_ALIAS.values() or clean_name.startswith("new_"):
        return clean_name

    if clean_name not in RECORD_ALIAS:
        logger.warning(f"Registro desconocido: Marcándolo como 'new_{clean_name}'")

    return RECORD_ALIAS.get(clean_name, f"new_{clean_name}")


def get_available_years(base_dir=RAW_DATA_DIR):
    """
    Obtiene la lista de años disponibles en un directorio (por defecto data/raw).
    """
    base_dir = Path(base_dir)
    if not base_dir.exists():
        return []

    years = []
    for folder in base_dir.iterdir():
        if folder.is_dir():
            try:
                years.append(int(folder.name))
            except ValueError:
                continue

    return sorted(years, reverse=True)


def format_year_ranges(years):
    """
    Formatea un vector de años en rangos legibles (ej: 1996, 2005-2024).
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

    if start == prev:
        ranges.append(str(start))
    else:
        ranges.append(f"{start}-{prev}")

    return ", ".join(ranges)


def read_sav(filepath: Union[str, Path], **kwargs: Any) -> Tuple[pd.DataFrame, Any]:
    """
    Lee un archivo SPSS (.sav) de forma robusta.

    Args:
        filepath: Ruta al archivo `.sav`
        **kwargs: Argumentos nativos de `pyreadstat.read_sav()`. Los más útiles:
            - `usecols` (list): Lista de columnas a cargar. Ej: `usecols=["HHID", "HV001"]`
            - `row_limit` (int): Límite de filas a leer. Ej: `row_limit=100`
            - `apply_value_formats` (bool): Traduce números a texto original de SPSS (ej: `1` -> `"Sí"`).
            - `encoding` (str): Forzar codificación. Ej: `encoding="latin1"`

    Returns:
        tuple: (`pd.DataFrame`, Metadata de `pyreadstat`)
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {filepath}")

    df, meta = pyreadstat.read_sav(str(filepath), **kwargs)

    return df, meta


# =============================================================================
# 3. API PRINCIPAL DE CARGA (Core Loader)
# Funciones orquestadoras finales para uso en scripts principales o pipelines.
# =============================================================================


def _load_multiple_years(module, record=None, years=None, meta=False, **kwargs):
    """
    Función interna auxiliar para iterar la carga de datos sobre múltiples años.
    """
    if years is None:
        years = get_available_years()
        if not years:
            raise FileNotFoundError("No se encontraron carpetas de años en data/raw")
        logger.info(f"🔎 Detectada historia de {len(years)} años.")

    data_history = {}
    for y in years:
        try:
            result = load_endes(y, module, record=record, meta=meta, **kwargs)
            data_history[y] = result
        except Exception as e:
            logger.warning(f"⚠️ Nota: Año {y} no cargado ({e})")

    logger.success("✅ ¡Historia cargada y organizada por años!")
    return data_history


def _resolve_endes_paths(year, target_module_alias, target_record_alias=None):
    """
    Busca la ruta física de los archivos .sav correspondientes a un módulo y registro.
    Retorna:
        - paths_dict: Diccionario {alias_registro: Ruta_al_archivo}
        - folder_name: Nombre de la subcarpeta encontrada (ej: "1472-Modulo102")
    """
    base_path = RAW_DATA_DIR / str(year)
    if not base_path.exists():
        raise FileNotFoundError(f"No se encontró la carpeta para el año {year}: {base_path}")

    # Programación Funcional: Encontramos la carpeta del módulo usando 'next' (equivalente a find + lambda)
    target_folder = next(
        (
            f
            for f in sorted(base_path.iterdir())
            if f.is_dir()
            and _normalize_module_name(_read_metadata(f).get("module_name", ""))
            == target_module_alias
        ),
        None,
    )
    if not target_folder:
        raise FileNotFoundError(
            f"No se encontró el módulo '{target_module_alias}' para el año {year}."
        )

    sav_files = sorted(target_folder.glob("*.sav")) + sorted(target_folder.glob("*.SAV"))

    if target_record_alias is None:
        paths_dict = {_normalize_record_name(sav.name): sav for sav in sav_files}
        return paths_dict, target_folder.name

    # Programación Funcional: Encontramos el archivo .sav específico usando 'next'
    target_sav = next(
        (sav for sav in sav_files if _normalize_record_name(sav.name) == target_record_alias), None
    )
    if not target_sav:
        raise FileNotFoundError(
            f"Se encontró el módulo {target_module_alias} pero no el registro "
            f"'{target_record_alias}' para el año {year}."
        )

    return {target_record_alias: target_sav}, target_folder.name


def load_endes(year=None, module=None, record=None, meta=False, **kwargs):
    """
    Carga archivos ENDES de forma inteligente.
    Si year no se proporciona, iterará sobre múltiples años internamente.
    Si meta=True, devuelve (datos, metadata_de_pyreadstat).
    """
    if module is None:
        raise ValueError("Se requiere especificar un 'module' para cargar los datos.")

    # 1. Normalización Temprana y Global
    target_module_alias = _normalize_module_name(module, year)
    target_record_alias = _normalize_record_name(record) if record else None

    if year is None:
        return _load_multiple_years(target_module_alias, target_record_alias, meta=meta, **kwargs)

    if isinstance(year, (list, tuple, range)):
        return _load_multiple_years(
            target_module_alias, target_record_alias, years=list(year), meta=meta, **kwargs
        )

    # 2. Resolución de Rutas (Cálculo del GPS)
    paths_dict, folder_name = _resolve_endes_paths(year, target_module_alias, target_record_alias)

    # 3. Carga de Datos (Trabajo Físico con pyreadstat)
    if not target_record_alias:
        logger.info(f"📦 Cargando módulo completo: {target_module_alias} desde {folder_name}")
        dataframes = {}
        for alias, path in paths_dict.items():
            df, meta_data = read_sav(path, **kwargs)
            dataframes[alias] = (df, meta_data) if meta else df
        return dataframes

    # Si se pidió un registro específico, paths_dict solo tiene 1 elemento
    target_record_alias, path = list(paths_dict.items())[0]
    logger.info(
        f"✓ Cargando registro: {path.name} desde {folder_name} [Alias: {target_record_alias}]"
    )
    df, meta_data = read_sav(path, **kwargs)
    return (df, meta_data) if meta else df
