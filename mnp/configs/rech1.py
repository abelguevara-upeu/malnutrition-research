from typing import Dict, Any

# ===================================================================
# CONFIGURACIÓN DE LIMPIEZA - MÓDULO RECH1 (ROSTER DE HOGAR)
# ===================================================================

config_f1: Dict[str, Any] = {
    # 1. CASTEO DE DTYPES
    # Llaves primarias y foráneas siempre deben ser str para no perder integridad
    "keys_to_cast": [
        "HHID",
        "HVIDX",
    ],
    
    # Falsos numéricos a limpiar (Códigos de "No Sabe" o consistencias lógicas)
    # Extraído directamente de la matriz de decisiones para convertirlos a np.nan
    "false_numerics": {
        "HV101": [98.0],                # Parentesco
        "HV105": [97.0, 98.0],          # Edad
        "HV106": [8.0],                 # Nivel estudios
        "HV107": [98.0],                # Año aprobado
        "HV108": [97.0, 98.0],          # Años estudio
        "HV109": [8.0],                 # Nivel educativo
        "HV111": [8.0],                 # Madre viva
        "HV112": [0.0],                 # ID madre (0 no en HH)
        "HV113": [8.0],                 # Padre vivo
        "HV114": [0.0],                 # ID padre (0 no en HH)
        "HV124": [97.0, 98.0],          # Años estudio actual
        "HV128": [97.0, 98.0],          # Años estudio pasado
    },
    
    # 2. ELIMINACIÓN DE RUIDO (DROPS)
    "cols_to_drop": [
        # Módulos muertos y variables con demasiada pérdida (>70%)
        "QH13A1", "QH13A2", "QH13A3", "QH13A4", "QH13A5", "QH13A6", "QH13A7", "QH13A8", "QH13A",
        "HV130", "HV131", "HV132", "HV133",  # Enfermedades padres (100% nulos)
        "HV123", "HV127", "HV129",           # Educación redundante
        "QH21A", "QH21B",                    # Estatal / Qali Warma
        "HV116", "HV134",                    # Demografía redundante
        "HV137", "HV138", "HV139",           # Posesiones (100% nulos)
        "QH25A", "QH25B",                    # Extranjería (Introduce sesgo temporal pre-2018)
        "QH25CA", "QH25CM",                  # Extranjería tiempos (100% nulos)
        "HV135", "HV136", "HV140",           # Hermanos / Partida nac. (Alta pérdida)
        "ID1",                               # Año (se cruza desde RECH0)
    ],
    
    # 3. DIVISIONES / ESCALAMIENTOS
    # En RECH1 (Roster) no hay factores de ponderación con 6 ceros. 
    "divide_by_1000000": [],
    
    # 4. FUSIÓN DE CADENAS ROTAS (COALESCE)
    # RECH1 no tiene variables rotas identificadas en la auditoría.
    "coalesce": {},
}

# Configuración Fase 3: Estandarización de Etiquetas (Labels)
config_f3 = {
    # Todas las variables categóricas nominales, ordinales y binarias a estandarizar
    "HV101": 2024,  # Parentesco con jefe
    "HV102": 2024,  # Residente habitual
    "HV103": 2024,  # Durmió aquí anoche
    "HV104": 2024,  # Sexo
    # "HV106": 2024,  # Nivel de estudios más alto (Ordinal)
    # "HV109": 2024,  # Nivel educativo (Ordinal)
    "HV110": 2024,  # Asiste escuela
    "HV111": 2024,  # Madre viva
    "HV113": 2024,  # Padre vivo
    "HV115": 2024,  # Estado civil
    "HV120": 2024,  # Niños elegibles
    "HV121": 2024,  # Asistió escuela este año
    # "HV122": 2024,  # Nivel asiste/matriculado (Ordinal)
    "HV125": 2024,  # Matriculado año pasado
    # "HV126": 2024,  # Nivel matriculado año pasado (Ordinal)
}
