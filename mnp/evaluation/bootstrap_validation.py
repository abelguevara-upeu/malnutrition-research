"""Eje 1 del plan de validacion: intervalos de confianza y significancia.

Produce las dos evidencias que el Momento 6 exige para la confiabilidad
estadistica del modelo campeon:

1. Bootstrap no parametrico (B=1000) sobre las probabilidades out-of-fold para
   estimar IC 95% de AUC-ROC, Recall, Precision y F1 (Efron & Tibshirani, 1994).
2. Test de DeLong de LightGBM contra XGBoost y Regresion Logistica sobre curvas
   ROC correlacionadas (DeLong et al., 1988).

Las metricas se ponderan con HV005 tanto en el entrenamiento como en la
evaluacion, igual que el benchmark: sin esa ponderacion describen la muestra
cruda (sesgada a lo urbano) y no la poblacion expandida, y el AUC cae de 0.8295
a ~0.8206.
"""

import json
import re
import unicodedata
import warnings

import lightgbm as lgb
import numpy as np
import pandas as pd
import xgboost as xgb
from scipy import stats
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from mnp.config import MODELS_DIR, PROCESSED_DATA_DIR, RANDOM_SEED, REPORTS_DIR
from mnp.configs.column_labels import LABELS

warnings.filterwarnings("ignore")

N_BOOTSTRAP = 1000
METADATA_COLS = ["year", "SHREGION", "HV005", "HV024"]


def flatten(col: str) -> str:
    s = unicodedata.normalize("NFKD", str(col)).encode("ASCII", "ignore").decode("utf-8")
    return re.sub(r"[^a-zA-Z0-9]+", "_", s).strip("_")


def load_xy():
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


def oof_probabilities(X, y, w):
    """Probabilidades out-of-fold de los tres modelos bajo la misma particion."""
    kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_SEED)
    oof = {m: np.zeros(len(y)) for m in ("LightGBM", "XGBoost", "LogReg")}

    num = X.select_dtypes(include=[np.number]).columns.tolist()
    cat = [c for c in X.columns if c not in num]
    pre = ColumnTransformer(
        [
            ("num", Pipeline([("i", SimpleImputer(strategy="median")), ("s", StandardScaler())]), num),
            ("cat", Pipeline([("i", SimpleImputer(strategy="constant", fill_value="MISSING")),
                              ("o", OneHotEncoder(handle_unknown="ignore", sparse_output=False))]), cat),
        ]
    )

    for i, (tr, va) in enumerate(kf.split(X, y), 1):
        ytr, wtr = y.iloc[tr], w.iloc[tr]

        m = lgb.LGBMClassifier(class_weight="balanced", random_state=RANDOM_SEED,
                               verbose=-1, n_estimators=300)
        m.fit(X.iloc[tr], ytr, sample_weight=wtr)
        oof["LightGBM"][va] = m.predict_proba(X.iloc[va])[:, 1]

        Xtr, Xva = pre.fit_transform(X.iloc[tr]), pre.transform(X.iloc[va])

        scale = (len(ytr) - ytr.sum()) / ytr.sum()
        m = xgb.XGBClassifier(scale_pos_weight=scale, min_child_weight=1e-7,
                              random_state=RANDOM_SEED, n_estimators=300)
        m.fit(Xtr, ytr, sample_weight=wtr, verbose=False)
        oof["XGBoost"][va] = m.predict_proba(Xva)[:, 1]

        m = LogisticRegression(class_weight="balanced", max_iter=500, random_state=RANDOM_SEED)
        m.fit(Xtr, ytr, sample_weight=wtr)
        oof["LogReg"][va] = m.predict_proba(Xva)[:, 1]

        print(f"  fold {i}/5 listo", flush=True)
    return oof


def bootstrap_ci(y, p, w, threshold, n=N_BOOTSTRAP, seed=RANDOM_SEED):
    """IC 95% por percentiles sobre remuestreo con reemplazo de los individuos."""
    rng = np.random.default_rng(seed)
    y, w = np.asarray(y), np.asarray(w)
    pred_full = (p >= threshold).astype(int)
    point = {
        "auc": roc_auc_score(y, p, sample_weight=w),
        "recall": recall_score(y, pred_full, sample_weight=w),
        "precision": precision_score(y, pred_full, sample_weight=w),
        "f1": f1_score(y, pred_full, sample_weight=w),
    }

    acc = {k: [] for k in point}
    idx = np.arange(len(y))
    for _ in range(n):
        b = rng.choice(idx, size=len(idx), replace=True)
        yb, pb, wb = y[b], p[b], w[b]
        if yb.sum() == 0 or yb.sum() == len(yb):
            continue
        predb = (pb >= threshold).astype(int)
        acc["auc"].append(roc_auc_score(yb, pb, sample_weight=wb))
        acc["recall"].append(recall_score(yb, predb, sample_weight=wb))
        acc["precision"].append(precision_score(yb, predb, sample_weight=wb, zero_division=0))
        acc["f1"].append(f1_score(yb, predb, sample_weight=wb, zero_division=0))

    return {
        k: {
            "point": float(point[k]),
            "ci_low": float(np.percentile(acc[k], 2.5)),
            "ci_high": float(np.percentile(acc[k], 97.5)),
            "std": float(np.std(acc[k])),
        }
        for k in point
    }


# --- Test de DeLong (implementacion de Sun & Xu, 2014) ------------------------

def _midrank(x):
    J = np.argsort(x)
    z = x[J]
    n = len(x)
    t = np.zeros(n, dtype=float)
    i = 0
    while i < n:
        j = i
        while j < n and z[j] == z[i]:
            j += 1
        t[i:j] = 0.5 * (i + j - 1) + 1
        i = j
    out = np.empty(n, dtype=float)
    out[J] = t
    return out


def _fast_delong(preds_sorted, m):
    """Covarianza de los AUC via componentes de varianza de DeLong."""
    n = preds_sorted.shape[1] - m
    k = preds_sorted.shape[0]
    tx = np.array([_midrank(preds_sorted[r, :m]) for r in range(k)])
    ty = np.array([_midrank(preds_sorted[r, m:]) for r in range(k)])
    tz = np.array([_midrank(preds_sorted[r, :]) for r in range(k)])
    aucs = (tz[:, :m].sum(axis=1) / m - (m + 1) / 2) / n
    v01 = (tz[:, :m] - tx) / n
    v10 = 1 - (tz[:, m:] - ty) / m
    sx = np.cov(v01)
    sy = np.cov(v10)
    return aucs, sx.reshape(k, k) / m + sy.reshape(k, k) / n


def delong_test(y, p1, p2):
    """p-valor bilateral para H0: AUC(p1) == AUC(p2) sobre las mismas muestras.

    El estadistico de DeLong se define sobre rangos y no admite pesos muestrales,
    asi que los AUC que devuelve son SIN ponderar por HV005 y quedan ~0.010 por
    debajo de los ponderados que reporta el bootstrap. La comparacion sigue
    siendo valida porque los tres modelos se miden sobre los mismos individuos
    y el contraste es entre curvas, no sobre el nivel absoluto del AUC.
    """
    y = np.asarray(y)
    order = (-y).argsort(kind="mergesort")
    m = int(y.sum())
    preds = np.vstack([np.asarray(p1)[order], np.asarray(p2)[order]])
    aucs, cov = _fast_delong(preds, m)
    var = cov[0, 0] + cov[1, 1] - 2 * cov[0, 1]
    if var <= 0:
        # Varianza nula: los dos vectores ordenan identicamente, de modo que no
        # hay diferencia que contrastar (p = 1), no una diferencia infinita.
        return float(aucs[0]), float(aucs[1]), 1.0, 0.0
    z = (aucs[0] - aucs[1]) / np.sqrt(var)
    return float(aucs[0]), float(aucs[1]), float(2 * stats.norm.sf(abs(z))), float(z)


def main():
    X, y, w, meta = load_xy()
    tau = meta["optimal_threshold"]
    print(f"dataset={X.shape} | prevalencia={y.mean()*100:.2f}% | tau={tau}\n")

    print("Calculando probabilidades out-of-fold (3 modelos x 5 folds)...")
    oof = oof_probabilities(X, y, w)

    print(f"\nBootstrap no parametrico (B={N_BOOTSTRAP})...")
    ci = bootstrap_ci(y, oof["LightGBM"], w, tau)
    print(f"\n{'metrica':<12}{'estimacion':>12}{'IC 95%':>26}")
    for k, v in ci.items():
        lo, hi = v["ci_low"], v["ci_high"]
        if k == "auc":
            print(f"{k:<12}{v['point']:>12.4f}   [{lo:.4f}, {hi:.4f}]")
        else:
            print(f"{k:<12}{v['point']*100:>11.2f}%   [{lo*100:.2f}%, {hi*100:.2f}%]")

    print("\nTest de DeLong (LightGBM vs. baselines) -- AUC sin ponderar:")
    delong = {}
    for rival in ("XGBoost", "LogReg"):
        a1, a2, p, z = delong_test(y, oof["LightGBM"], oof[rival])
        delong[rival] = {"auc_lightgbm": a1, "auc_rival": a2, "z": z, "p_value": p}
        ptxt = "< 1e-300" if p == 0 else f"{p:.3e}"
        print(f"  vs {rival:<9} AUC {a1:.4f} vs {a2:.4f} | z={z:8.2f} | p={ptxt}")

    out = REPORTS_DIR / "eje1_confiabilidad.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    json.dump(
        {"n_samples": int(len(y)), "n_bootstrap": N_BOOTSTRAP, "threshold": tau,
         "bootstrap_ci": ci, "delong": delong},
        open(out, "w"), indent=2,
    )
    print(f"\nguardado: {out}")


if __name__ == "__main__":
    main()
