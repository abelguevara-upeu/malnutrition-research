import pandas as pd
import numpy as np


def run_phase1_engine(df, config):
    """Limpieza (Fase 1) para cualquier módulo de ENDES."""
    # Usamos .copy() para evitar fragmentación de memoria (el problema de lentitud que tuviste)
    df_out = df.copy()

    # 1. Casteo de llaves
    if "keys_to_cast" in config:
        for col in config["keys_to_cast"]:
            if col in df_out.columns:
                df_out[col] = (
                    df_out[col]
                    .astype(str)
                    .str.replace(r"\.0$", "", regex=True)
                    .str.strip()
                    .replace("nan", np.nan)
                )

    # 2. Reemplazo de Falsos Numéricos (Ultrarrápido)
    if "false_numerics" in config:
        for col, bad_values in config["false_numerics"].items():
            if col in df_out.columns:
                df_out.loc[df_out[col].isin(bad_values), col] = np.nan

    # 3. Drops
    if "cols_to_drop" in config:
        cols = [c for c in config["cols_to_drop"] if c in df_out.columns]
        df_out = df_out.drop(columns=cols)

    # 4. Escalamiento matemático (Divide by 10)
    if "divide_by_10" in config:
        for col in config["divide_by_10"]:
            if col in df_out.columns:
                df_out[col] = df_out[col] / 10.0

    # 5. Escalamiento matemático (Divide by 100)
    if "divide_by_100" in config:
        for col in config["divide_by_100"]:
            if col in df_out.columns:
                df_out[col] = df_out[col] / 100.0

    # 6. Coalesce (Unificación de columnas mutadas)
    if "coalesce" in config:
        for target_col, source_cols in config["coalesce"].items():
            valid_cols = [c for c in source_cols if c in df_out.columns]
            if valid_cols:
                # bfill a través de las columnas de la lista y nos quedamos con la primera
                df_out[target_col] = df_out[valid_cols].bfill(axis=1).iloc[:, 0]

    return df_out
