"""Ablacion de features: mide el delta de AUC al ampliar X con las candidatas.

Replica EXACTAMENTE el preprocesamiento del notebook
03_model_benchmarking_extended.ipynb para que el baseline reproduzca el
AUC 0.8308 reportado en el manuscrito:
  - drop de metadatos pasivos (year, SHREGION, HV005, HV024)
  - rename via mnp.configs.column_labels.LABELS
  - aplanado ASCII de nombres de columna
  - categoricas: fillna('Desconocido') -> astype(str) -> astype('category')
  - StratifiedKFold(5, shuffle=True, random_state=42), pesos HV005/1e6
  - LGBMClassifier(class_weight='balanced', n_estimators=300, random_state=42)
  - metricas ponderadas con HV005 tambien en evaluacion (sample_weight=w_val)
"""

import json
import re
import unicodedata
import warnings

import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold

from mnp.configs.column_labels import LABELS

warnings.filterwarnings("ignore")

DATA = "data/processed/master_preprocessed_v2.parquet"
META = "models/champion_metadata.json"

# Metadatos pasivos que el notebook excluye del espacio de atributos.
METADATA_COLS = ["year", "SHREGION", "HV005", "HV024"]

# Candidatas del Bloque A (codigos crudos del parquet).
WASH_VIVIENDA = ["HV213", "HV214", "HV215", "HV201", "HV205", "SH227", "HV226"]
# HV024 y SHREGION son metadatos pasivos en el notebook; se reinyectan aqui
# de forma deliberada para medir su aporte como atributo territorial.
TERRITORIO = ["HV024", "HV026", "SHREGION", "SH77F"]


def flatten(col: str) -> str:
    s = unicodedata.normalize("NFKD", str(col)).encode("ASCII", "ignore").decode("utf-8")
    return re.sub(r"[^a-zA-Z0-9]+", "_", s).strip("_")


def load():
    df = pd.read_parquet(DATA)
    df = df.drop(columns=[c for c in ["UBIGEO", "LATITUDY", "LONGITUDX"] if c in df.columns])
    y = df["TARGET_DESNUTRICION"]
    w = df["HV005"] / 1_000_000.0
    return df, y, w


def build(df, extra=()):
    """Espacio de atributos del notebook, opcionalmente ampliado con `extra`."""
    drop = ["TARGET_DESNUTRICION"] + [c for c in METADATA_COLS if c not in extra]
    X = df.drop(columns=[c for c in drop if c in df.columns])
    X = X.rename(columns=LABELS)
    X.columns = [flatten(c) for c in X.columns]
    for c in X.select_dtypes(include=["object", "category", "str"]).columns:
        X[c] = X[c].fillna("Desconocido").astype(str).astype("category")
    return X


def run_cv(X, y, w, label):
    kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    m = {"auc": [], "recall": [], "precision": [], "f1": []}
    for tr, va in kf.split(X, y):
        clf = lgb.LGBMClassifier(
            class_weight="balanced", random_state=42, verbose=-1, n_estimators=300
        )
        clf.fit(X.iloc[tr], y.iloc[tr], sample_weight=w.iloc[tr])
        p = clf.predict_proba(X.iloc[va])[:, 1]
        pred = (p >= 0.5).astype(int)
        yv, wv = y.iloc[va], w.iloc[va]
        # las metricas se ponderan con HV005 igual que en el notebook (celda 11),
        # de modo que reflejen la poblacion expandida y no la muestra cruda.
        m["auc"].append(roc_auc_score(yv, p, sample_weight=wv))
        m["recall"].append(recall_score(yv, pred, sample_weight=wv))
        m["precision"].append(precision_score(yv, pred, sample_weight=wv))
        m["f1"].append(f1_score(yv, pred, sample_weight=wv))
    out = {k: float(np.mean(v)) for k, v in m.items()}
    out["n_features"] = int(X.shape[1])
    print(
        f"{label:<44} n={out['n_features']:<3} AUC={out['auc']:.4f}  "
        f"Rec={out['recall']*100:5.2f}%  Prec={out['precision']*100:5.2f}%  "
        f"F1={out['f1']:.4f}",
        flush=True,
    )
    return out


def main():
    df, y, w = load()
    meta = json.load(open(META))
    top43 = meta["features"]

    # Espacio completo del notebook (74 vars) y subconjunto campeon (43).
    X_full = build(df)
    missing = [f for f in top43 if f not in X_full.columns]
    if missing:
        raise ValueError(f"features del campeon ausentes tras el preprocesamiento: {missing}")
    print(f"dataset={df.shape}  espacio_notebook={X_full.shape[1]}  campeon={len(top43)}")
    print(f"prevalencia={y.mean()*100:.2f}%\n")

    results = {}
    results["BASELINE Top43"] = run_cv(X_full[top43], y, w, "BASELINE Top43 (manuscrito)")

    for label, extra in [
        ("+ WASH/vivienda", WASH_VIVIENDA),
        ("+ territorio", TERRITORIO),
        ("+ bloque A completo", WASH_VIVIENDA + TERRITORIO),
    ]:
        Xe = build(df, extra=extra)
        cols = top43 + [c for c in (flatten(LABELS.get(k, k)) for k in extra) if c in Xe.columns]
        cols = list(dict.fromkeys(cols))
        results[label] = run_cv(Xe[cols], y, w, label)

    b = results["BASELINE Top43"]
    print("\n--- DELTA vs BASELINE ---")
    for label, r in results.items():
        if label == "BASELINE Top43":
            continue
        print(
            f"{label:<24} dAUC={r['auc']-b['auc']:+.4f}  "
            f"dRecall={(r['recall']-b['recall'])*100:+.2f}pts  "
            f"dPrecision={(r['precision']-b['precision'])*100:+.2f}pts"
        )
    json.dump(results, open("reports/feature_ablation_results.json", "w"), indent=2)
    print("\nguardado: reports/feature_ablation_results.json")


if __name__ == "__main__":
    main()
