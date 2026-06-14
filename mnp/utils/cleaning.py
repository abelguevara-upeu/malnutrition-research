import pandas as pd
import numpy as np


import time

def run_phase1_engine(df, config, inplace=False):
    """Limpieza (Fase 1) para cualquier módulo de ENDES."""
    start_total = time.time()
    print("[Limpieza] Iniciando Motor Fase 1...")
    
    if inplace:
        print("[Limpieza] MODO IN-PLACE ACTIVO: Ahorro máximo de RAM (Se sobreescribirá el DF original)")
        df_out = df
    else:
        # 0. Drops (Optimización de memoria: Eliminar antes de cualquier otra cosa)
        if "cols_to_drop" in config:
            cols = [c for c in config["cols_to_drop"] if c in df.columns]
            if cols:
                print(f"[Limpieza] Eliminando {len(cols)} columnas (Optimización RAM)...")
                start_step = time.time()
                df_out = df.drop(columns=cols)
                print(f"[Limpieza] Drops iniciales completados en {time.time() - start_step:.2f}s")
            else:
                df_out = df.copy()
        else:
            df_out = df.copy()

    # Si estamos en inplace, hacemos los drops in-place
    if inplace and "cols_to_drop" in config:
        cols = [c for c in config["cols_to_drop"] if c in df_out.columns]
        if cols:
            print(f"[Limpieza] Eliminando {len(cols)} columnas in-place...")
            start_step = time.time()
            df_out.drop(columns=cols, inplace=True)
            print(f"[Limpieza] Drops completados en {time.time() - start_step:.2f}s")

    # 1. Casteo de llaves
    if "keys_to_cast" in config:
        print(f"[Limpieza] Casteando {len(config['keys_to_cast'])} columnas clave...")
        start_step = time.time()
        for col in config["keys_to_cast"]:
            if col in df_out.columns:
                s = df_out[col].astype(str).str.strip()
                # Al castear a string, los nulos se vuelven la cadena "nan".
                mask = s.str.endswith(".0").fillna(False)
                s_stripped = np.where(mask, s.str[:-2], s)
                # Reemplazamos la cadena "nan" por np.nan real muy rápido en C
                df_out[col] = np.where(s_stripped == "nan", np.nan, s_stripped)
        print(f"[Limpieza] Casteo completado en {time.time() - start_step:.2f}s")

    # 2. Reemplazo de Falsos Numéricos
    if "false_numerics" in config and config["false_numerics"]:
        print("[Limpieza] Limpiando falsos numéricos...")
        start_step = time.time()
        for col, bad_values in config["false_numerics"].items():
            if col in df_out.columns:
                df_out.loc[df_out[col].isin(bad_values), col] = np.nan
        print(f"[Limpieza] Falsos numéricos limpiados en {time.time() - start_step:.2f}s")

    # 2.5. Reemplazo Custom (Recodificaciones específicas como 996 -> 0)
    if "replace_values" in config and config["replace_values"]:
        print("[Limpieza] Aplicando reemplazos custom...")
        start_step = time.time()
        for col, mapping in config["replace_values"].items():
            if col in df_out.columns:
                df_out[col] = df_out[col].replace(mapping)
        print(f"[Limpieza] Reemplazos custom completados en {time.time() - start_step:.2f}s")


    # 3. Drops (Se movió al inicio para optimizar memoria)
    # 4. Escalamiento matemático (Divide by 10)
    if "divide_by_10" in config:
        print("[Limpieza] Escalamiento matemático (x/10)...")
        start_step = time.time()
        for col in config["divide_by_10"]:
            if col in df_out.columns:
                df_out[col] = df_out[col] / 10.0
        print(f"[Limpieza] Escalamiento /10 completado en {time.time() - start_step:.2f}s")

    # 5. Escalamiento matemático (Divide by 100)
    if "divide_by_100" in config:
        print("[Limpieza] Escalamiento matemático (x/100)...")
        start_step = time.time()
        for col in config["divide_by_100"]:
            if col in df_out.columns:
                df_out[col] = df_out[col] / 100.0
        print(f"[Limpieza] Escalamiento /100 completado en {time.time() - start_step:.2f}s")

    # 5.5. Escalamiento matemático (Divide by 1,000,000)
    if "divide_by_1000000" in config:
        print("[Limpieza] Escalamiento matemático (x/1,000,000)...")
        start_step = time.time()
        for col in config["divide_by_1000000"]:
            if col in df_out.columns:
                df_out[col] = df_out[col] / 1000000.0
        print(f"[Limpieza] Escalamiento /1M completado en {time.time() - start_step:.2f}s")

    # 5.6. Escalamiento matemático (Divide by 100,000)
    if "divide_by_100000" in config:
        print("[Limpieza] Escalamiento matemático (x/100,000)...")
        start_step = time.time()
        for col in config["divide_by_100000"]:
            if col in df_out.columns:
                df_out[col] = df_out[col] / 100000.0
        print(f"[Limpieza] Escalamiento /100k completado en {time.time() - start_step:.2f}s")

    # 6. Coalesce (Unificación de columnas mutadas)
    if "coalesce" in config:
        print("[Limpieza] Ejecutando Coalesce (Unificación de columnas)...")
        start_step = time.time()
        for target_col, source_cols in config["coalesce"].items():
            valid_cols = [c for c in source_cols if c in df_out.columns]
            if valid_cols:
                # Optimized Coalesce: chained fillna is 100x faster than bfill(axis=1)
                res = df_out[valid_cols[0]]
                for col in valid_cols[1:]:
                    res = res.fillna(df_out[col])
                df_out[target_col] = res
                
                # Auto-drop absorbed source columns
                cols_to_remove = [c for c in valid_cols if c != target_col]
                if cols_to_remove:
                    df_out.drop(columns=cols_to_remove, inplace=True)
                    
        print(f"[Limpieza] Coalesce completado en {time.time() - start_step:.2f}s")

    print(f"[Limpieza] Motor Fase 1 finalizado. Tiempo total: {time.time() - start_total:.2f}s")
    return df_out

def apply_standard_labels(df, val_labels_hist, mapping_config, phase1_config=None):
    """
    Fase 3: Mapeo Categórico Estandarizado.
    Aplica las etiquetas de texto usando el diccionario de un año específico (Ej: 2024)
    definido en la configuración (mapping_config) para estandarizar la historia.
    """
    df_out = df.copy()
    
    for col, dict_year in mapping_config.items():
        if col not in df_out.columns:
            continue
            
        # Extraer el diccionario del año elegido
        if dict_year in val_labels_hist:
            mapping_dict = val_labels_hist[dict_year].get(col)
            
            # Si no está por el nombre exacto, buscamos en sus nombres origen (Coalesce)
            if mapping_dict is None and phase1_config and "coalesce" in phase1_config:
                if col in phase1_config["coalesce"]:
                    for source_col in phase1_config["coalesce"][col]:
                        mapping_dict = val_labels_hist[dict_year].get(source_col)
                        if mapping_dict is not None:
                            break
                
            if mapping_dict:
                # Mapeamos TODA la historia usando este único diccionario estándar
                df_out[col] = df_out[col].map(mapping_dict)
                
    return df_out
