"""Mide cuanto pierde el modelo si se retira la hemoglobina (HC56).

HC56 es la unica de las 45 variables que exige un procedimiento sobre el nino:
el resto se obtiene por entrevista. Saber cuanto aporta permite responder si el
sistema puede operar donde el tamizaje de anemia no esta disponible.

Protocolo identico al del benchmark (StratifiedKFold 5, semilla 42, pesos HV005
en entrenamiento y evaluacion), de modo que la unica fuente de variacion sea la
ausencia de la variable. Ademas del contraste puntual, remuestrea la diferencia
de AUC para comprobar si es distinguible del ruido.
"""

import json
import re
import unicodedata
import warnings

import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.metrics import precision_score, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold

from mnp.config import MODELS_DIR, PROCESSED_DATA_DIR, RANDOM_SEED, REPORTS_DIR
from mnp.configs.column_labels import LABELS

warnings.filterwarnings("ignore")

N_BOOTSTRAP = 1000
METADATA_COLS = ["year", "SHREGION", "HV005", "HV024"]


def flatten(col: str) -> str:
    s = unicodedata.normalize("NFKD", str(col)).encode("ASCII", "ignore").decode("utf-8")
    return re.sub(r"[^a-zA-Z0-9]+", "_", s).strip("_")


def load():
    meta = json.load(open(MODELS_DIR / "champion_metadata.json"))
    df = pd.read_parquet(PROCESSED_DATA_DIR / "master_preprocessed_v2.parquet")
    y = df["TARGET_DESNUTRICION"].reset_index(drop=True)
    w = (df["HV005"] / 1_000_000.0).reset_index(drop=True)
    X = df.drop(columns=["TARGET_DESNUTRICION", *METADATA_COLS], errors="ignore")
    X = X.rename(columns=LABELS)
    X.columns = [flatten(c) for c in X.columns]
    X = X[meta["features"]].reset_index(drop=True)
    for c in X.select_dtypes(include=["object", "category", "str"]).columns:
        X[c] = X[c].fillna("Desconocido").astype(str).astype("category")
    return X, y, w, meta


def oof_probabilities(X, y, w, cols):
    """Probabilidades out-of-fold bajo la particion compartida."""
    kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_SEED)
    oof = np.zeros(len(y))
    for tr, va in kf.split(X, y):
        m = lgb.LGBMClassifier(
            class_weight="balanced", random_state=RANDOM_SEED, verbose=-1, n_estimators=300
        )
        m.fit(X[cols].iloc[tr], y.iloc[tr], sample_weight=w.iloc[tr])
        oof[va] = m.predict_proba(X[cols].iloc[va])[:, 1]
    return oof


def metrics(y, p, w, threshold=0.5):
    pred = (p >= threshold).astype(int)
    return {
        "auc": float(roc_auc_score(y, p, sample_weight=w)),
        "recall": float(recall_score(y, pred, sample_weight=w)),
        "precision": float(precision_score(y, pred, sample_weight=w, zero_division=0)),
    }


def main():
    X, y, w, meta = load()
    hb = next(f for f in meta["features"] if f.split("_")[0] == "HC56")
    sin_hb = [f for f in meta["features"] if f != hb]

    print(f"variable retirada: {hb}")
    print(f"dataset={X.shape} | prevalencia={y.mean()*100:.2f}%\n")

    print("Entrenando ambas configuraciones...", flush=True)
    p_con = oof_probabilities(X, y, w, meta["features"])
    p_sin = oof_probabilities(X, y, w, sin_hb)

    m_con, m_sin = metrics(y, p_con, w), metrics(y, p_sin, w)
    print(f"\n{'configuracion':<26}{'AUC':>9}{'Recall':>10}{'Precision':>11}")
    print(f"{'con hemoglobina (45)':<26}{m_con['auc']:>9.4f}{m_con['recall']*100:>9.2f}%{m_con['precision']*100:>10.2f}%")
    print(f"{'sin hemoglobina (44)':<26}{m_sin['auc']:>9.4f}{m_sin['recall']*100:>9.2f}%{m_sin['precision']*100:>10.2f}%")
    print(f"{'diferencia':<26}{m_sin['auc']-m_con['auc']:>+9.4f}"
          f"{(m_sin['recall']-m_con['recall'])*100:>+9.2f}%{(m_sin['precision']-m_con['precision'])*100:>+10.2f}%")

    # La diferencia puntual no basta: se remuestrea para situarla frente al ruido.
    print(f"\nBootstrap de la diferencia (B={N_BOOTSTRAP})...", flush=True)
    rng = np.random.default_rng(RANDOM_SEED)
    ya, wa = np.asarray(y), np.asarray(w)
    idx = np.arange(len(ya))
    deltas = []
    for _ in range(N_BOOTSTRAP):
        b = rng.choice(idx, size=len(idx), replace=True)
        if ya[b].sum() in (0, len(b)):
            continue
        deltas.append(
            roc_auc_score(ya[b], p_sin[b], sample_weight=wa[b])
            - roc_auc_score(ya[b], p_con[b], sample_weight=wa[b])
        )
    lo, hi = np.percentile(deltas, [2.5, 97.5])
    print(f"delta AUC = {np.mean(deltas):+.4f}  IC 95% [{lo:+.4f}, {hi:+.4f}]")
    print("=> la diferencia " + ("NO es" if lo < 0 < hi else "ES") + " distinguible de cero")

    out = REPORTS_DIR / "ablation_hemoglobina.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    json.dump(
        {
            "variable": hb,
            "con_hemoglobina": m_con,
            "sin_hemoglobina": m_sin,
            "delta_auc": {"point": float(np.mean(deltas)), "ci_low": float(lo), "ci_high": float(hi)},
            "n_bootstrap": N_BOOTSTRAP,
        },
        open(out, "w"), indent=2,
    )
    print(f"\nguardado: {out}")


if __name__ == "__main__":
    main()
