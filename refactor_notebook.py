import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

nb = new_notebook()

nb.cells.append(new_markdown_cell("# 01 - Modelado Avanzado: La Santa Trinidad del Boosting\n\nEste notebook usa el dataset limpio de la Fase 2 (74 columnas puras) y entrena a los 3 gigantes del Machine Learning (XGBoost, LightGBM, CatBoost) para predecir la desnutrición crónica."))

cell_1 = """import pandas as pd
import numpy as np
import re
import warnings
warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', None)

# 1. Cargar datos preprocesados de oro
# Ya no necesitamos hacer limpieza aquí, la Fase 2 entregó 74 columnas puras.
master = pd.read_parquet('../../data/processed/master_preprocessed.parquet')

print(f"Dataset de élite cargado. Filas: {len(master)} | Columnas: {master.shape[1]}")"""
nb.cells.append(new_code_cell(cell_1))

cell_2 = """# 2. Separar Features y Target
features = master.drop(columns=['TARGET_DESNUTRICION'])
target = master['TARGET_DESNUTRICION']

# Tipado Nativo para Árboles Modernos
for col in features.columns:
    if not pd.api.types.is_numeric_dtype(features[col]):
        # Rellenar vacíos explícitamente para CatBoost (solo en categóricas)
        features[col] = features[col].fillna('Desconocido')
        features[col] = features[col].astype(str).astype('category')"""
nb.cells.append(new_code_cell(cell_2))

cell_3 = """import sys
import os
import unicodedata

sys.path.append(os.path.abspath('../../')) 
from mnp.configs.column_labels import LABELS

# 3. Renombrar y Aplanar Columnas para LightGBM y XGBoost
features = features.rename(columns=LABELS)

clean_cols = []
for col in features.columns:
    col_str = unicodedata.normalize('NFKD', str(col)).encode('ASCII', 'ignore').decode('utf-8')
    col_str = re.sub(r'[^a-zA-Z0-9]+', '_', col_str).strip('_')
    clean_cols.append(col_str)
features.columns = clean_cols

print("Columnas renombradas y aplanadas. Ejemplo:")
print(features.columns[:5].tolist())"""
nb.cells.append(new_code_cell(cell_3))

cell_4 = """from sklearn.model_selection import train_test_split

# 4. División Estratificada Train/Test
# Como eliminamos 'year' en Fase 2 para evitar fugas, haremos un split 80/20 
# estratificando por el Target para mantener la proporción exacta de desnutridos.
X_train, X_test, y_train, y_test = train_test_split(
    features, target, test_size=0.20, random_state=42, stratify=target
)

print(f"Train: {X_train.shape}")
print(f"Test: {X_test.shape}")"""
nb.cells.append(new_code_cell(cell_4))

cell_5 = """# 5. BALANCEO FÍSICO DE DATOS (Undersampling)
from imblearn.under_sampling import RandomUnderSampler
import matplotlib.pyplot as plt
import seaborn as sns

print("Aplicando Undersampling solo a los datos de Train...")
rus = RandomUnderSampler(random_state=42)

X_train_resampled, y_train_resampled = rus.fit_resample(X_train, y_train)

print(f"Train Original (Desbalanceado): {X_train.shape}")
print(f"Train Nuevo (Balanceado 50/50): {X_train_resampled.shape}")

# Visualizamos el nuevo balance
plt.figure(figsize=(7, 4))
ax = sns.countplot(x=y_train_resampled, palette='Set2')
plt.title('Nueva Distribución del Target en TRAIN (Físicamente Balanceado)')
plt.xticks([0, 1], ['Sanos', 'Desnutridos'])
plt.ylabel('Cantidad de Niños')
plt.show()"""
nb.cells.append(new_code_cell(cell_5))

cell_6 = """import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostClassifier
import time

# 6. ENTRENAMIENTO DE LA SANTA TRINIDAD
cat_features = X_train_resampled.select_dtypes(include=['category']).columns.tolist()

models = {
    'XGBoost': xgb.XGBClassifier(
        random_state=42, 
        eval_metric='logloss', 
        enable_categorical=True
    ),
    'LightGBM': lgb.LGBMClassifier(
        random_state=42, 
        verbose=-1
    ),
    'CatBoost': CatBoostClassifier(
        random_state=42, 
        verbose=0
    )
}

trained_models = {}

for name, model in models.items():
    print(f"Entrenando {name} con datos 50/50...")
    start_time = time.time()
    
    if name == 'CatBoost':
        model.fit(X_train_resampled, y_train_resampled, cat_features=cat_features)
    else:
        model.fit(X_train_resampled, y_train_resampled)
        
    trained_models[name] = model
    print(f"[{name}] Completado en {time.time() - start_time:.2f} segundos.\\n")"""
nb.cells.append(new_code_cell(cell_6))

cell_7 = """from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

print("--- MÉTRICAS CON CLASES BALANCEADAS ---")

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for i, (name, model) in enumerate(trained_models.items()):
    print(f"\\n==================== {name} ====================")
    
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    auc = roc_auc_score(y_test, y_proba)
    print(f"➜ AUC-ROC Score: {auc:.4f}")
    print(classification_report(y_test, y_pred, target_names=['Sanos (0)', 'Desnutridos (1)']))
    
    # Matriz de Confusión
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Sano', 'Desnutrido'])
    disp.plot(ax=axes[i], cmap='Blues', values_format='d')
    axes[i].set_title(f"Matriz Confusión - {name}")

plt.tight_layout()
plt.show()"""
nb.cells.append(new_code_cell(cell_7))

cell_8 = """# 7. OPTIMIZACIÓN DEL UMBRAL (Threshold Tuning)
from sklearn.metrics import precision_recall_curve
import numpy as np

cb_model = trained_models['CatBoost']
y_probs = cb_model.predict_proba(X_test)[:, 1]
precisions, recalls, thresholds = precision_recall_curve(y_test, y_probs)

plt.figure(figsize=(10, 6))
plt.plot(thresholds, precisions[:-1], 'b--', label='Precisión (Falsos Positivos)')
plt.plot(thresholds, recalls[:-1], 'g-', label='Recall (Desnutridos Atrapados)')
f1_scores = 2 * (precisions[:-1] * recalls[:-1]) / (precisions[:-1] + recalls[:-1] + 1e-10)
plt.plot(thresholds, f1_scores, 'k-', linewidth=2, label='F1-Score (Promedio Armónico)')
plt.xlabel('Umbral Matemático (Threshold)')
plt.ylabel('Puntuación (0 a 1)')
plt.title('Curva Precision-Recall (Elige tu Umbral)')
plt.legend()
plt.axvline(x=0.5, color='r', linestyle=':', label='Umbral Fijo Actual (0.5)')
plt.grid(True)
plt.show()"""
nb.cells.append(new_code_cell(cell_8))

cell_9 = """# 8. IMPORTANCIA DE VARIABLES (Insights Médicos/Sociales)
import seaborn as sns

print("Extrayendo Importancia de Variables del Mejor Modelo (CatBoost)")
cb_model = trained_models['CatBoost']

importances = cb_model.get_feature_importance()
feat_imp_df = pd.DataFrame({
    'Feature': X_train_resampled.columns,
    'Importance': importances
}).sort_values('Importance', ascending=False).head(20)

plt.figure(figsize=(10, 8))
sns.barplot(x='Importance', y='Feature', data=feat_imp_df, palette='viridis')
plt.title('Top 20 Variables más Importantes Predictoras de Desnutrición Crónica')
plt.tight_layout()
plt.show()"""
nb.cells.append(new_code_cell(cell_9))

with open('/Users/abelguevarah/Desktop/invs/malnutrition-research/notebooks/03_modeling/01_advanced_boosters_v2.ipynb', 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)
