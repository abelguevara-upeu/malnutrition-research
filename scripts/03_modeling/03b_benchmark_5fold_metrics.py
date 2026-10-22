"""Repite el benchmark de 03_model_benchmarking_extended (mismos datos, pliegues e
hiperparámetros) y guarda las métricas de los cinco pliegues, incluidas la
especificidad y el AUC-PR, sin generar figuras ni tocar el modelo campeón."""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

print("Cargando el dataset maestro...")
# Ajusta el path relativo según la ubicación de tu entorno
from mnp.config import MODELS_DIR, PROCESSED_DATA_DIR
df = pd.read_parquet(PROCESSED_DATA_DIR / 'master_preprocessed_v2.parquet')
print(f"Dimensiones de la base de datos: {df.shape}")

# 1. ELIMINAR GEOVARIABLES INNECESARIAS (Ruido para el modelo)
cols_to_drop = [c for c in ['UBIGEO', 'LATITUDY', 'LONGITUDX'] if c in df.columns]
df = df.drop(columns=cols_to_drop)

# 2. IDENTIFICAR Y SEPARAR METADATOS PASIVOS
metadata_cols = ['year', 'SHREGION', 'HV005', 'HV024']
cols_to_extract = [c for c in metadata_cols if c in df.columns]

metadata = df[cols_to_extract].copy()
y = df['TARGET_DESNUTRICION']
X = df.drop(columns=['TARGET_DESNUTRICION'] + cols_to_extract)

# 3. CALCULAR PESO MUESTRAL ENDES
if 'HV005' in metadata.columns:
    sample_weight = metadata['HV005'] / 1000000.0
else:
    sample_weight = pd.Series(np.ones(len(metadata)))

# 4. APLANAR NOMBRES DE COLUMNAS (Para evitar errores en LightGBM/XGBoost)
import sys
import unicodedata
import re

try:
    from mnp.configs.column_labels import LABELS
    X = X.rename(columns=LABELS)
except ImportError:
    pass

clean_cols = []
for col in X.columns:
    col_str = unicodedata.normalize('NFKD', str(col)).encode('ASCII', 'ignore').decode('utf-8')
    col_str = re.sub(r'[^a-zA-Z0-9]+', '_', col_str).strip('_')
    clean_cols.append(col_str)
X.columns = clean_cols

print("OK: Dataset preprocesado. Nombres aplanados y pesos muestrales calculados.")


# %%

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

# Separación de variables por tipo
cat_features = X.select_dtypes(include=['object', 'category']).columns.tolist()
num_features = X.select_dtypes(include=[np.number]).columns.tolist()

# Convertir Nulos Categóricos a texto 'Desconocido' (Requisito estricto de CatBoost)
for col in cat_features:
    X[col] = X[col].fillna('Desconocido').astype(str)

# 1. Pipeline para Modelos Clásicos (Regresión Logística, Árboles, Redes Neuronales)
num_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

cat_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='MISSING')),
    ('ohe', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', num_pipeline, num_features),
        ('cat', cat_pipeline, cat_features)
    ])

# 2. Formato Nativo optimizado para Modelos Basados en Árboles (XGBoost / LightGBM)
X_boosters = X.copy()
for col in cat_features:
    X_boosters[col] = X_boosters[col].astype('category')
    
print(f"OK: Variables Categóricas: {len(cat_features)}")
print(f"OK: Variables Numéricas: {len(num_features)}")


# %%

from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import average_precision_score, roc_auc_score, recall_score, precision_score, f1_score
import xgboost as xgb
import lightgbm as lgb
import catboost as cb

import time
kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

results = {'LogReg': {'auc': [], 'recall': [], 'precision': [], 'f1': [], 'time': []},
           'LightGBM': {'auc': [], 'recall': [], 'precision': [], 'f1': [], 'time': []},
           'XGBoost': {'auc': [], 'recall': [], 'precision': [], 'f1': [], 'time': []},
           'CatBoost': {'auc': [], 'recall': [], 'precision': [], 'f1': [], 'time': []},
           'DecisionTree': {'auc': [], 'recall': [], 'precision': [], 'f1': [], 'time': []},
           'NeuralNet': {'auc': [], 'recall': [], 'precision': [], 'f1': [], 'time': []}}

fold5_data = {} # Diccionario crítico para guardar la data del último fold y graficarla sin re-entrenar

print("\nINICIANDO EVALUACIÓN DE MODELOS (5-Fold CV)...")
start_time_global = time.time()

fold = 1
for train_idx, val_idx in kf.split(X, y):
    print(f"\n--- Procesando Fold {fold}/5 ---")
    
    y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
    w_train, w_val = sample_weight.iloc[train_idx], sample_weight.iloc[val_idx]
    
    # Transformaciones para modelos clásicos
    X_train_lr = preprocessor.fit_transform(X.iloc[train_idx])
    X_val_lr = preprocessor.transform(X.iloc[val_idx])
    
    # Transformaciones para ensambles de árboles
    X_train_b, X_val_b = X_boosters.iloc[train_idx], X_boosters.iloc[val_idx]
    
    # --- 1. Regresión Logística ---
    lr = LogisticRegression(class_weight='balanced', max_iter=500, random_state=42)
    start_lr = time.time()
    lr.fit(X_train_lr, y_train, sample_weight=w_train)
    lr_probs = lr.predict_proba(X_val_lr)[:, 1]
    time_lr = time.time() - start_lr
    
    # --- 2. LightGBM ---
    lgbm = lgb.LGBMClassifier(class_weight='balanced', random_state=42, verbose=-1, n_estimators=300)
    start_lgb = time.time()
    lgbm.fit(X_train_b, y_train, sample_weight=w_train)
    lgb_probs = lgbm.predict_proba(X_val_b)[:, 1]
    time_lgb = time.time() - start_lgb
    
    # --- 3. XGBoost ---
    scale_pos = (len(y_train) - y_train.sum()) / y_train.sum()
    xg = xgb.XGBClassifier(scale_pos_weight=scale_pos, min_child_weight=1e-7, random_state=42, n_estimators=300)
    start_xgb = time.time()
    xg.fit(X_train_lr, y_train, sample_weight=w_train, verbose=False)
    xgb_probs = xg.predict_proba(X_val_lr)[:, 1]
    time_xgb = time.time() - start_xgb
    
    # --- 4. CatBoost ---
    cat = cb.CatBoostClassifier(auto_class_weights='Balanced', cat_features=cat_features, random_state=42, iterations=300, verbose=False)
    start_cat = time.time()
    cat.fit(X.iloc[train_idx], y_train, sample_weight=w_train, verbose=False)
    cat_probs = cat.predict_proba(X.iloc[val_idx])[:, 1]
    time_cat = time.time() - start_cat
    
    # --- 5. Decision Tree (Nueva Exigencia) ---
    dt = DecisionTreeClassifier(max_depth=5, class_weight='balanced', random_state=42)
    start_dt = time.time()
    dt.fit(X_train_lr, y_train, sample_weight=w_train)
    dt_probs = dt.predict_proba(X_val_lr)[:, 1]
    time_dt = time.time() - start_dt
    
    # --- 6. Neural Network (Nueva Exigencia) ---
    # Nota: Scikit-learn MLPClassifier no soporta sample_weight ni class_weight nativo.
    mlp = MLPClassifier(hidden_layer_sizes=(200, 200, 200), max_iter=50, random_state=42, early_stopping=True)
    start_mlp = time.time()
    mlp.fit(X_train_lr, y_train)
    mlp_probs = mlp.predict_proba(X_val_lr)[:, 1]
    time_mlp = time.time() - start_mlp
    
    # --- Evaluación de Probabilidades ---
    models_probs = {
        'LogReg': lr_probs, 'LightGBM': lgb_probs, 'XGBoost': xgb_probs, 
        'CatBoost': cat_probs, 'DecisionTree': dt_probs, 'NeuralNet': mlp_probs
    }
    
    for name, probs in models_probs.items():
        auc_score = roc_auc_score(y_val, probs, sample_weight=w_val)
        recall = recall_score(y_val, (probs >= 0.5).astype(int), sample_weight=w_val)
        precision = precision_score(y_val, (probs >= 0.5).astype(int), sample_weight=w_val, zero_division=0)
        f1 = f1_score(y_val, (probs >= 0.5).astype(int), sample_weight=w_val, zero_division=0)
        
        results[name]['auc'].append(auc_score)
        results[name]['recall'].append(recall)
        results[name]['precision'].append(precision)
        results[name]['f1'].append(f1)
        pred=(probs >= 0.5).astype(int)
        results[name].setdefault('spec',[]).append(recall_score(1-y_val, 1-pred, sample_weight=w_val))
        results[name].setdefault('auc_pr',[]).append(average_precision_score(y_val, probs, sample_weight=w_val))
        time_dict = {'LogReg': time_lr, 'LightGBM': time_lgb, 'XGBoost': time_xgb, 'CatBoost': time_cat, 'DecisionTree': time_dt, 'NeuralNet': time_mlp}
        results[name]['time'].append(time_dict[name])
        print(f"  - {name.ljust(15)}: AUC = {auc_score:.4f} | Recall = {recall:.4f} | Prec = {precision:.4f} | F1 = {f1:.4f} | Tiempo = {time_dict[name]:.2f}s")
        
    # Guardamos los resultados del último ciclo para poder graficarlos después
    if fold == 5:
        fold5_data = {'y_val': y_val, 'w_val': w_val, 'probs': models_probs}
        
    fold += 1


import json
out={n:{k:[float(x) for x in v] for k,v in m.items()} for n,m in results.items()}
json.dump(out,open("reports/benchmark/benchmark_5fold_metrics.json","w"),indent=1)
rows=[]
for n,m in out.items():
    r={"modelo":n}
    for k in ["auc","auc_pr","recall","precision","spec","f1"]: r[k+"_media"]=np.mean(m[k]); r[k+"_de"]=np.std(m[k])
    rows.append(r)
pd.DataFrame(rows).sort_values("auc_media",ascending=False).to_csv("reports/benchmark/benchmark_5fold_resumen.csv",index=False)
print(pd.DataFrame(rows).round(4).to_string())
