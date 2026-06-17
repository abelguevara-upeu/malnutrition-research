# config_rec41.py

# Configuración DEFINITIVA para la limpieza de REC41 (Salud Materna)
# Todas las reglas aquí mapeadas provienen directamente del archivo decisiones-de-limpieza.md
# y de la verificación de etiquetas en value_label.txt

config_f1 = {
    # 1. Llaves maestras que deben castearse a string de forma segura
    "keys_to_cast": ["CASEID", "MIDX"],
    
    # 2. Valores falsos numéricos reportados por el INEI/SPSS que deben ser NaN
    "false_numerics": {
        # ---- Lote 1 ----
        "M13": [98, 98.0, 99, 99.0],  # Mes del 1er control prenatal (No sabe)
        "M14": [98, 98.0, 99, 99.0],  # Número de visitas prenatales (No sabe)
        
        # ---- Lote 2 (Nuevos agregados según value_label.txt) ----
        "M15": [98, 98.0],            # Lugar de parto (No sabe). Mantenemos 96 (Otro).
        "M18": [8, 8.0],              # Tamaño del niño al nacer (No sabe)
        "M19": [9996, 9996.0, 9997, 9997.0, 9998, 9998.0], # Peso (No se pesó / No sabe)
        "M45": [8, 8.0],              # Tomó hierro (No sabe)
        "M46": [998, 998.0, 999, 999.0], # Días tomó hierro (No sabe)
        "M4":  [97, 97.0, 98, 98.0], # Duración lactancia (Inconsistente / No sabe)
        "M5":  [97, 97.0, 98, 98.0],  # Meses de lactancia (Inconsistente / No sabe)
        
        # ---- Lote 3 (El lote final de variables M55, M60, M70) ----
        "M60": [8, 8.0],              # Antiparasitarios embarazo (No sabe)
        "M70": [8, 8.0],              # Chequeo médico bebé 1er mes (No sabe)
        "M55A": [8, 8.0],
        "M55B": [8, 8.0],
        "M55C": [8, 8.0],
        "M55E": [8, 8.0],
        "M55F": [8, 8.0],
        "M55G": [8, 8.0],
        "M55H": [8, 8.0],
        "M55I": [8, 8.0],
        "M55X": [8, 8.0],
        "M55Z": [8, 8.0],
    },
    
    # 2.5 Reemplazos Matemáticos Custom (Ej. Nunca amamantó 94 -> 0)
    "replace_values": {
        "M4": {94: 0.0, 94.0: 0.0},
        "M5": {94: 0.0, 94.0: 0.0},
    },
    
    # 3. Columnas basura a eliminar (ej. ID1)
    "cols_to_drop": [
        "ID1",
    ],
}

# Configuración Fase 3: Estandarización de Etiquetas (Labels)
# Define qué año de diccionario usar como "Estándar" para aplicar las etiquetas de texto
# SOLO a las variables Categóricas Nominales. Las numéricas y binarias conservan sus números.
config_f3 = {
    "M15": 2024,  # Lugar del parto (Nominal: Necesitamos saber si fue MINSA, Clínica, Casa)
}
