import pandas as pd
from IPython.display import display

def format_year_ranges(years):
    if not years: return ""
    years = sorted(years)
    ranges = []
    start = prev = years[0]
    for y in years[1:]:
        if y == prev + 1:
            prev = y
        else:
            ranges.append(str(start) if start == prev else f"{start}-{prev}")
            start = prev = y
    ranges.append(str(start) if start == prev else f"{start}-{prev}")
    return ", ".join(ranges)


def analyze_schema_drift(col_labels_hist):
    from collections import defaultdict
    all_cols = set()
    schema_drift_report = defaultdict(lambda: defaultdict(list))
    
    for year, cols_dict in col_labels_hist.items():
        for col_name, label in cols_dict.items():
            all_cols.add(col_name)
            normalized_label = " ".join(str(label).split())
            schema_drift_report[col_name][normalized_label].append(year)
            
    mutated_schema = {k: v for k, v in schema_drift_report.items() if len(v) > 1}
    stable_schema = {k: v for k, v in schema_drift_report.items() if len(v) == 1}
    
    return all_cols, stable_schema, mutated_schema

def print_schema_drift_report(all_cols, stable_schema, mutated_schema):
    print("\033[1;94mREPORTE GLOBAL DE MUTACIÓN DE DESCRIPCIONES DE COLUMNAS (COLUMN LABELS)\033[0m\n")
    print(f"\033[1;94mTotal de columnas detectadas: {len(all_cols)}\033[0m\n")
    
    all_versions = []
    for label_dict in [stable_schema, mutated_schema]:
        for versions in label_dict.values():
            all_versions.extend(versions.values())
    global_max_len = max([len(format_year_ranges(a)) for a in all_versions] + [0])
    
    for title, label_dict in [("Descripciones estables", stable_schema), ("Descripciones mutadas", mutated_schema)]:
        print(f"\033[1;94m{title}: {len(label_dict)}\033[0m")
        for var_name, versions in label_dict.items():
            print(f"\033[1;94m{var_name} (Apariciones: {sum(len(y) for y in versions.values())} años)\033[0m")
            for label, years_list in versions.items():
                years_str = format_year_ranges(years_list)
                print(f"  - Años {years_str:<{global_max_len}} : {label}")
        print("\n")

def analyze_val_drift(value_labels_history):
    from collections import defaultdict
    all_val_cols = set()
    val_drift_report = defaultdict(lambda: defaultdict(list))

    for year, year_labels in value_labels_history.items():
        for col_name, val_mapping in year_labels.items():
            if val_mapping:
                all_val_cols.add(col_name)
                try:
                    mapping_key = tuple(sorted((k, str(v).strip()) for k, v in val_mapping.items()))
                except TypeError:
                    mapping_key = tuple((k, str(v).strip()) for k, v in val_mapping.items())
                
                val_drift_report[col_name][mapping_key].append(year)

    mutated_val_labels = {k: v for k, v in val_drift_report.items() if len(v) > 1}
    stable_val_labels = {k: v for k, v in val_drift_report.items() if len(v) == 1}
    
    return all_val_cols, stable_val_labels, mutated_val_labels

def print_val_drift_report(all_val_cols, stable_val_labels, mutated_val_labels):
    print("\033[1;94mREPORTE GLOBAL DE MUTACIÓN DE ETIQUETAS DE VALORES (2007 - 2024)\033[0m\n")
    print(f"\033[1;94mTotal de columnas con mapeo de valores detectadas: {len(all_val_cols)}\033[0m\n")

    all_versions = []
    for label_dict in [stable_val_labels, mutated_val_labels]:
        for versions in label_dict.values():
            all_versions.extend(versions.values())
    global_max_len = max([len(format_year_ranges(a)) for a in all_versions] + [0])

    from collections import defaultdict
    for title, label_dict in [("Etiquetas de valores estables", stable_val_labels), ("Etiquetas de valores mutadas", mutated_val_labels)]:
        print(f"\033[1;94m{title}: {len(label_dict)}\033[0m")
        for var_name, versions in label_dict.items():
            print(f"\033[1;94m{var_name} (Apariciones: {sum(len(y) for y in versions.values())} años)\033[0m")
            
            col_max_lens = defaultdict(int)
            for mapping_str in versions.keys():
                if isinstance(mapping_str, tuple):
                    for i, (k, v) in enumerate(mapping_str):
                        text_len = len(f"{k} ({v})")
                        if text_len > col_max_lens[i]:
                            col_max_lens[i] = text_len
            
            for mapping_str, years_list in versions.items():
                years_str = format_year_ranges(years_list)
                prefix = f"  - Años {years_str:<{global_max_len}} : "
                
                if isinstance(mapping_str, tuple):
                    formatted_items = []
                    for i, (k, v) in enumerate(mapping_str):
                        text = f"{k} ({v})"
                        formatted_items.append(f"{text:<{col_max_lens[i]}}" if i < len(mapping_str) - 1 else text)
                    mapping_str_fmt = " | ".join(formatted_items)
                else:
                    mapping_str_fmt = mapping_str
                print(f"{prefix}{mapping_str_fmt}")
        print("\n")

def analyze_logical_types(df, all_cols, value_labels_history, col_labels_hist, forced_ids=None):
    if forced_ids is None:
        forced_ids = []
    forced_ids_upper = [str(x).upper() for x in forced_ids]
    
    logical_types = {
        "Identifier": [],
        "Categorical": [],
        "Numerical": []
    }
    
    df_years = {year: df[df["year"] == year] for year in col_labels_hist.keys()}
    
    for col in sorted(all_cols):
        if str(col).upper() in forced_ids_upper:
            logical_types["Identifier"].append(col)
            continue
            
        is_categorical = any(
            col in year_labels and bool(year_labels[col]) 
            for year_labels in value_labels_history.values()
        )
        
        if is_categorical:
            logical_types["Categorical"].append(col)
        else:
            years_present = [y for y, cols in col_labels_hist.items() if col in cols]
            latest_year_present = max(years_present) if years_present else None
            
            if latest_year_present:
                df_col = df_years[latest_year_present][col]
                is_text = False
                if hasattr(df_col, "dtype"):
                    is_text = pd.api.types.is_string_dtype(df_col) or pd.api.types.is_object_dtype(df_col)
                    
                valid_vals = df_col.dropna()
                is_primary_key = (len(valid_vals) > 0) and (valid_vals.nunique() == len(valid_vals)) and (len(valid_vals) == len(df_years[latest_year_present]))
                
                if is_text or is_primary_key:
                    logical_types["Identifier"].append(col)
                else:
                    logical_types["Numerical"].append(col)
            else:
                logical_types["Numerical"].append(col)
                
    return logical_types

def print_logical_types_report(logical_types, latest_year_labels, df, value_labels_history=None):
    print("\033[1;94mREPORTE GLOBAL DE TIPOS LÓGICOS DE VARIABLES\033[0m\n")
    
    rows = []
    df_dtypes = df.dtypes
    
    for type_name, cols in logical_types.items():
        print(f"\033[1;94m{type_name}: {len(cols)}\033[0m")
        for col in cols:
            desc = latest_year_labels.get(col, "Sin descripción")
            pd_type = str(df_dtypes[col]) if col in df_dtypes else "Desconocido"
            
            row = {
                "Variable": col,
                "Tipo Lógico": type_name,
                "Pandas Dtype": pd_type
            }
            
            if value_labels_history is not None:
                has_label = any(col in y_labels and bool(y_labels[col]) for y_labels in value_labels_history.values())
                row["Value Labels"] = "X" if has_label else ""
                
            row["Descripción"] = desc
            rows.append(row)
    print("\n")
    
    report_df = pd.DataFrame(rows)
    if not report_df.empty:
        report_df.set_index(["Tipo Lógico", "Variable"], inplace=True)
        display(report_df)
    else:
        print("No hay variables para mostrar.")

def report_nulls(df, latest_year_labels):
    nulls = df.isna().mean().sort_values(ascending=False) * 100
    df_nulls_global = nulls.to_frame(name="% Nulls").round(1)
    df_nulls_global.insert(0, "Label", df_nulls_global.index.map(lambda x: latest_year_labels.get(x, "No label")))
    print("\033[1;94mVARIABLES CON NULOS (>0%)\033[0m")
    display(df_nulls_global[df_nulls_global["% Nulls"] > 0])
    print("\n\033[1;94mVARIABLES COMPLETAS (0% Nulos)\033[0m")
    display(df_nulls_global[df_nulls_global["% Nulls"] == 0])

def centrar_notebook():
    from IPython.display import HTML, display
    display(HTML("""
    <style>
    .dataframe { margin-left: auto !important; margin-right: auto !important; }
    .output_png { display: table-cell; text-align: center; vertical-align: middle; }
    </style>
    """))

def report_historical_presence(col_labels_hist, latest_year_labels):
    from collections import defaultdict
    import pandas as pd
    from IPython.display import display
    
    presence = defaultdict(list)
    for year, cols_dict in col_labels_hist.items():
        for col in cols_dict.keys():
            presence[col].append(year)
            
    rows = []
    for col, years in presence.items():
        years_str = format_year_ranges(years)
        desc = latest_year_labels.get(col, "Sin descripción")
        rows.append({
            "Variable": col,
            "Años Presente": years_str,
            "Total Años": len(years),
            "Descripción": desc
        })
        
    df_presence = pd.DataFrame(rows)
    df_presence.sort_values(by=["Total Años", "Variable"], ascending=[True, True], inplace=True)
    df_presence.set_index("Variable", inplace=True)
    
    print("\033[1;94mREPORTE DE PRESENCIA HISTÓRICA DE VARIABLES\033[0m\n")
    display(df_presence)

def generate_master_profile(df, all_cols, value_labels_history, col_labels_hist, latest_year_labels, forced_ids=None):
    from collections import defaultdict
    import pandas as pd
    from IPython.display import display
    
    # 1. Logical Types & Value Labels
    logical_types = analyze_logical_types(df, all_cols, value_labels_history, col_labels_hist, forced_ids)
    df_dtypes = df.dtypes
    
    types_rows = []
    for type_name, cols in logical_types.items():
        for col in cols:
            has_label = any(col in y_labels and bool(y_labels[col]) for y_labels in value_labels_history.values())
            types_rows.append({
                "Variable": col,
                "Tipo Lógico": type_name,
                "Pandas Dtype": str(df_dtypes[col]) if col in df_dtypes else "Desconocido",
                "Value Labels": "X" if has_label else ""
            })
    df_types = pd.DataFrame(types_rows).set_index("Variable") if types_rows else pd.DataFrame()
    
    # 2. Historical Presence
    presence = defaultdict(list)
    for year, cols_dict in col_labels_hist.items():
        for col in cols_dict.keys():
            presence[col].append(year)
            
    presence_rows = []
    for col, years in presence.items():
        presence_rows.append({
            "Variable": col,
            "Años Presente": format_year_ranges(years),
            "Total Años": len(years)
        })
    df_presence = pd.DataFrame(presence_rows).set_index("Variable") if presence_rows else pd.DataFrame()
    
    # 3. Nulls
    nulls = df.isna().mean() * 100
    df_nulls = nulls.to_frame(name="% Nulos").round(1)
    df_nulls.index.name = "Variable"
    
    # 4. Merge Everything
    master_df = pd.DataFrame(index=sorted(list(all_cols)))
    master_df.index.name = "Variable"
    
    master_df.insert(0, "Descripción", master_df.index.map(lambda x: latest_year_labels.get(x, "Sin descripción")))
    
    if not df_types.empty: master_df = master_df.join(df_types)
    if not df_presence.empty: master_df = master_df.join(df_presence)
    if not df_nulls.empty: master_df = master_df.join(df_nulls)
    
    master_df["% Nulos"] = master_df["% Nulos"].fillna(100.0)
    master_df["Total Años"] = master_df["Total Años"].fillna(0).astype(int)
    
    # Multi-level sort: First by Logical Type, then by Nulls
    master_df.sort_values(by=["Tipo Lógico", "% Nulos"], ascending=[True, False], inplace=True)
    
    print("\033[1;94mREPORTE MAESTRO DE PERFILADO DE DATOS (DATA DICTIONARY)\033[0m\n")
    display(master_df)
    
    return master_df

# --- Functional EDA Profiling Builder ---

def metric_latest_label(col, latest_year_labels):
    return latest_year_labels.get(col, "Sin etiqueta")

def metric_pandas_dtype(col, df_dtypes):
    return str(df_dtypes[col]) if col in df_dtypes else "Desconocido"

def metric_logical_type(col, logical_types_dict):
    for t_name, cols in logical_types_dict.items():
        if col in cols: return t_name
    return "Desconocido"

def metric_has_value_labels(col, value_labels_history):
    has_label = any(col in y_labels and bool(y_labels[col]) for y_labels in value_labels_history.values())
    return "X" if has_label else ""

def metric_nulls(col, df):
    if col in df.columns:
        return round(df[col].isna().mean() * 100, 1)
    return 100.0

def metric_years_present(col, col_labels_hist):
    years = [y for y, cols in col_labels_hist.items() if col in cols]
    return format_year_ranges(years)

def metric_total_years(col, col_labels_hist):
    return sum(1 for cols in col_labels_hist.values() if col in cols)

def analyze_nulls_evolution(df, cols, group_name="Grupo", latest_year_labels=None, cmap='Oranges_r', figsize=(14, 8)):
    """
    Analiza la evolución del % de nulos por año para un grupo de variables (ej. por tipo lógico).
    Equivalente a analizar_categoria pero dinámico y no acoplado a un módulo específico.
    """
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    from IPython.display import display
    
    vars_cat = [v for v in cols if v in df.columns]
    
    if not vars_cat:
        print(f"No se encontraron columnas válidas en el df para el grupo '{group_name}'.")
        return
        
    if 'year' not in df.columns:
        print("El DataFrame no contiene la columna 'year'.")
        return
        
    df_nulos = df.groupby('year')[vars_cat].apply(lambda x: x.isna().mean() * 100)
    
    matriz_imprimir = df_nulos.T.copy()
    if latest_year_labels is None:
        latest_year_labels = {}
    matriz_imprimir.insert(0, 'Etiqueta', matriz_imprimir.index.map(lambda x: latest_year_labels.get(x, 'Sin etiqueta')))
    
    pd.set_option('display.max_colwidth', None)
    print(f"\n{'='*60}")
    print(f"ANÁLISIS DE EVOLUCIÓN DE NULOS: {group_name.upper()}")
    print(f"{'='*60}")
    display(matriz_imprimir)
    
    # Ajuste automático del figsize si son muchas variables para que no se apriete el texto
    adjusted_height = max(figsize[1], len(vars_cat) * 0.4)
    
    plt.figure(figsize=(figsize[0], adjusted_height))
    sns.heatmap(df_nulos.T, annot=True, fmt=".0f", cmap=cmap, vmin=0, vmax=100, cbar_kws={'label': '% de Nulos'})
    plt.title(f"Evolución de Nulos por Año: {group_name}", pad=20, fontsize=14)
    plt.xlabel("Año", fontsize=12)
    plt.ylabel("Variables", fontsize=12)
    plt.tight_layout()
    plt.show()
