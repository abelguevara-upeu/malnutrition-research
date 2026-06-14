from typing import Dict, Any, List

# ===================================================================
# CONFIGURACIÓN DE LIMPIEZA - MÓDULO RECH0 (HOGAR)
# ===================================================================

config_f1: Dict[str, Any] = {
    # 1. CASTEO DE DTYPES
    # Se fuerza a string para no perder los ceros a la izquierda en los códigos geográficos.
    "keys_to_cast": [
        "HHID",
        "HV001",
        "HV002",
        "HV002A",
        "HV021",
        "UBIGEO",
        "ubigeo",
        "NCONGLOME1",
        "NCONGLOME",
        "nconglome",
        "CODCCPP",
        "codccpp",
        "NOMCCPP",
        "nomccpp",
    ],
    # Falsos numéricos a limpiar (Códigos 8, 9, 99 que signifiquen No Sabe/Falta)
    "false_numerics": {},
    # 2. ELIMINACIÓN DE RUIDO (DROPS)
    # Según la auditoría de decisiones-de-limpieza.md
    "cols_to_drop": [
        "HV000",
        "HV003",  # Linea del encuestado (Irrelevante)
        "HV011",  # Hombres elegibles (Irrelevante)
        "HV041",  # Mujeres medidas (Drift severo y redundante)
        "HV005A",
        "HV005X",
        "HV023",  # Variables aisladas y colineales
        "HV020",
        "HV027",
        "HV042",
        "HV043",
        "HV044",  # Flags de submuestra
        "HV006",
        "HV007",
        "HV016",  # Fechas que mueren en 2017 (nos quedamos con HV008 CMC)
        "HV017",
        "HV018",
        "HV019",
        "HV030",
        "HV031",
        "HV032",  # Metadatos de operarios de campo
        "HV028",
        "HV033",  # Submuestras y ponderadores alternos
    ],
    # 3. DIVISIONES / ESCALAMIENTOS
    # Tradicionalmente DHS almacena los pesos multiplicados por 1,000,000
    "divide_by_1000000": ["HV005", "hv005"],
    # 4. FUSIÓN DE CADENAS ROTAS (COALESCE)
    "coalesce": {
        "HV022": ["HV022", "hv022"],  # Estrato
        "HV005": ["HV005", "hv005"],  # Factor de ponderación
        "UBIGEO": ["UBIGEO", "ubigeo"],  # Código UBIGEO
        "NCONGLOME": ["NCONGLOME1", "NCONGLOME", "nconglome"],  # Número de conglomerado
        "CODCCPP": ["CODCCPP", "codccpp"],  # Código de centro poblado
        "NOMCCPP": ["NOMCCPP", "nomccpp"],  # Nombre de centro poblado
        "LONGITUDX": ["LONGITUDX", "longitudx", "long_ccpp"],  # Longitud GPS
        "LATITUDY": ["LATITUDY", "latitudy", "lat_ccpp"],  # Latitud GPS
    },
    # 5. FILTRADO DE FILAS (Eliminar registros inválidos/vacíos)
    "rows_to_keep": {
        "HV015": [1.0],  # 1.0 = Entrevista Completada (Elimina Rechazos, Ausentes, etc)
    },
}

# Configuración Fase 3: Estandarización de Etiquetas (Labels)
# Define qué año de diccionario usar como "Estándar" para aplicar a TODA la historia
# Extraido de decisiones-de-limpieza-not-drops.md
config_f3 = {
    "HV024": 2024,  # Región
    "HV025": 2024,  # Área de residencia
    "HV026": 2024,  # Lugar de residencia
    "HV015": 2024,  # Resultado de la entrevista
}
