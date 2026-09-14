"""Regenera models/threshold_recall_curve.json para el modelo campeon vigente.

La curva alimenta el calibrador de umbral de la app Streamlit. Se calcula con
el mismo protocolo del benchmark (StratifiedKFold 5, semilla 42, pesos HV005
aplicados tanto al entrenamiento como a las metricas), de modo que el recall
que muestra la app coincida con el reportado en el manuscrito.
"""

import json

import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.metrics import precision_score, recall_score
from sklearn.model_selection import StratifiedKFold

from mnp.config import MODELS_DIR, PROCESSED_DATA_DIR


def main():
    meta = json.load(open(MODELS_DIR / "champion_metadata.json"))
    feats = meta["features"]

    df = pd.read_parquet(PROCESSED_DATA_DIR / "master_preprocessed_v2.parquet")
    y = df["TARGET_DESNUTRICION"]
    w = df["HV005"] / 1_000_000.0

    # mismo preprocesamiento que el benchmark: nombres aplanados y categoricas nativas
    import re
    import unicodedata

    from mnp.configs.column_labels import LABELS

    X = df.drop(columns=["TARGET_DESNUTRICION", "year", "SHREGION", "HV005", "HV024"], errors="ignore")
    X = X.rename(columns=LABELS)
    X.columns = [
        re.sub(r"[^a-zA-Z0-9]+", "_", unicodedata.normalize("NFKD", str(c)).encode("ASCII", "ignore").decode()).strip("_")
        for c in X.columns
    ]
    X = X[feats]
    for c in X.select_dtypes(include=["object", "category", "str"]).columns:
        X[c] = X[c].fillna("Desconocido").astype(str).astype("category")

    # probabilidades out-of-fold: cada nino se evalua con un modelo que no lo vio
    oof = np.zeros(len(y))
    kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    for tr, va in kf.split(X, y):
        clf = lgb.LGBMClassifier(class_weight="balanced", random_state=42, verbose=-1, n_estimators=300)
        clf.fit(X.iloc[tr], y.iloc[tr], sample_weight=w.iloc[tr])
        oof[va] = clf.predict_proba(X.iloc[va])[:, 1]

    curve = []
    for t in np.arange(0.05, 1.00, 0.01):
        pred = (oof >= t).astype(int)
        curve.append(
            {
                "threshold": round(float(t), 2),
                "recall": round(float(recall_score(y, pred, sample_weight=w, zero_division=0)), 4),
                "precision": round(float(precision_score(y, pred, sample_weight=w, zero_division=0)), 4),
            }
        )

    out = MODELS_DIR / "threshold_recall_curve.json"
    json.dump(curve, open(out, "w"))
    print(f"curva regenerada: {out} ({len(curve)} puntos)")

    ok = [r for r in curve if r["recall"] >= 0.80]
    if ok:
        b = max(ok, key=lambda r: r["threshold"])
        print(f"tau minimo para Recall>=80%: {b['threshold']} "
              f"(recall {b['recall']*100:.2f}%, precision {b['precision']*100:.2f}%)")


if __name__ == "__main__":
    main()
