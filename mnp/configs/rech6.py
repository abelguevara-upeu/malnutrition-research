# config_rech6.py

# Configuración DEFINITIVA para la limpieza de RECH6 (Antropometría)
# Todas las reglas aquí mapeadas provienen directamente del archivo decisiones-de-limpieza.md

config_f1 = {
    # 1. Llaves maestras que deben castearse a string de forma segura
    "keys_to_cast": ["HHID", "HC0", "HC51", "HC60"],
    # 2. Valores falsos numéricos reportados por el INEI/SPSS que deben ser NaN
    # Se reemplazan ANTES de hacer cualquier cálculo matemático.
    "false_numerics": {
        "HC51": ["0", "0.0"],  # No en el hogar
        "HC60": [
            "993",
            "993.0",
            "994",
            "994.0",
            "995",
            "995.0",
        ],  # Madre no de facto, no en hogar, etc.
        "HC61": [8, 8.0],  # Educación de la madre: 8 = "No sabe"
        "HC30": [97, 97.0, 98, 98.0],  # Mes Inconsistente / No sabe
        "HC31": [9997, 9997.0, 9998, 9998.0],  # Año Inconsistente / No sabe
        # Falsos numéricos en biometría (Pesos, Tallas y Z-scores)
        "HC2": [999, 999.0, 9999, 9999.0],
        "HC3": [999, 999.0, 9999, 9999.0],
        "HC4": [9998, 9998.0],
        "HC5": [9998, 9998.0],
        "HC7": [9998, 9998.0],
        "HC8": [9998, 9998.0],
        "HC10": [9998, 9998.0],
        "HC11": [9998, 9998.0],
        "HC6": [99998, 99998.0, 9998, 9998.0],
        "HC9": [99998, 99998.0, 9998, 9998.0],
        "HC12": [99998, 99998.0, 9998, 9998.0],
        # Nuevos estándares OMS para Z-Scores
        "HC70": [9996, 9996.0, 9997, 9997.0, 9998, 9998.0],
        "HC71": [9996, 9996.0, 9997, 9997.0, 9998, 9998.0],
        "HC72": [9996, 9996.0, 9997, 9997.0, 9998, 9998.0],
        "HC73": [9996, 9996.0, 9997, 9997.0, 9998, 9998.0],
    },
    # 3. Unificación de columnas (Schema Drift) por directriz MINSA 2024
    "coalesce": {"HC56": ["HC56A", "HC56"], "HC57": ["HC57A", "HC57"]},
    # 4. Variables que requieren recuperar 1 decimal (división entre 10)
    "divide_by_10": ["HC2", "HC3", "HC53", "HC56", "HC56A"],
    # 5. Z-scores que requieren recuperar 2 decimales (división entre 100)
    "divide_by_100": ["HC5", "HC8", "HC11", "HC70", "HC71", "HC72", "HC73"],
    # 6. Columnas basura a eliminar (incluyendo las ya unificadas/coalescidas)
    "cols_to_drop": [
        "f",
        "ID1",
        "HV005A",
        "HC17",
        "HC18",
        "HC52",
        "HC58",
        "HC68",
    ],
}

# Configuración Fase 3: Estandarización de Etiquetas (Labels)
# Define qué año de diccionario usar como "Estándar" para aplicar a TODA la historia
config_f3 = {
    "HC27": 2024,  # Sexo
    "HC33": 2024,  # Control de fecha (resuelve inestabilidad histórica)
    "HC55": 2024,  # Resultado medir hemoglobina
    #'HC57': 2024, # Nivel de anemia
    #'HC61': 2024, # Nivel educativo madre
    "HC13": 2024,  # Razón de no medición
    "HC15": 2024,  # Acostado o de pie
}
