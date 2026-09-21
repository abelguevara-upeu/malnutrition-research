"""Figuras pensadas para audiencias no tecnicas.

Las que generan los notebooks rotulan los ejes con el nombre de la variable
ENDES (HV271_Factor_de_puntuacion_del_indice_de_riqueza), ilegible para quien no
conoce el diccionario. Aqui se reetiquetan en lenguaje natural y se recorta el
numero de columnas para que la figura se lea proyectada.
"""

import json

import joblib
import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from mnp.config import FIGURES_DIR, MODELS_DIR, PROCESSED_DATA_DIR

# Etiquetas en el vocabulario del personal de salud, no en el del dataset.
ETIQUETAS = {
    "HV271": "Pobreza del hogar",
    "m19": "Bajo peso al nacer",
    "HV040": "Altitud de residencia",
    "HC1": "Edad del niño",
    "HC56": "Anemia (hemoglobina)",
    "HC63": "Intervalo entre partos",
    "M4": "Duración de la lactancia",
    "HV220": "Edad del jefe del hogar",
    "M46": "Hierro en el embarazo",
    "M18": "Tamaño al nacer",
    "m34": "Inicio tardío de lactancia",
    "M14": "Controles prenatales",
    "HC62": "Educación de la madre",
    "HV025": "Residencia rural",
    "HV012": "Personas en el hogar",
    "HV204": "Distancia a fuente de agua",
    "HV216": "Hacinamiento",
    "HV014": "Otros menores de 5 años",
    "HC27": "Sexo del niño",
    "SH42": "Agua todo el día",
    "HV237": "Trata el agua",
    "HV226": "Combustible de cocina",
    "m15": "Parto institucional",
    "M17": "Parto por cesárea",
    "HV242": "Cocina separada",
    "HV225": "Servicio higiénico compartido",
}

# Regiones naturales, para agrupar los departamentos por franja.
REGION = {
    "Tumbes": "Costa", "Piura": "Costa", "Lambayeque": "Costa", "La Libertad": "Costa",
    "Ancash": "Costa", "Lima": "Costa", "Ica": "Costa", "Arequipa": "Costa",
    "Moquegua": "Costa", "Tacna": "Costa", "Callao": "Costa",
    "Cajamarca": "Sierra", "Huanuco": "Sierra", "Pasco": "Sierra", "Junin": "Sierra",
    "Huancavelica": "Sierra", "Ayacucho": "Sierra", "Apurimac": "Sierra",
    "Cusco": "Sierra", "Puno": "Sierra",
    "Amazonas": "Selva", "San Martin": "Selva", "Loreto": "Selva",
    "Ucayali": "Selva", "Madre de Dios": "Selva",
}


def mapa_riesgo_departamental(n_factores: int = 10):
    """Heatmap de factores por departamento, ordenado por region natural."""
    shap = pd.read_csv(PROCESSED_DATA_DIR / "shap_dept_impact.csv", index_col=0)
    meta = json.load(open(MODELS_DIR / "champion_metadata.json"))
    modelo = joblib.load(MODELS_DIR / "champion_lightgbm.pkl")

    # Las columnas se eligen por importancia en el modelo, no por su media en el
    # csv: los valores vienen normalizados por departamento y la media no separa.
    importancia = pd.Series(modelo.feature_importances_, index=meta["features"])
    cols = [c for c in importancia.sort_values(ascending=False).index if c in shap.columns]
    cols = cols[:n_factores]

    d = shap[cols].copy()
    d.columns = [ETIQUETAS.get(c.split("_")[0], c.split("_")[0]) for c in cols]

    d["__region"] = [REGION.get(i, "Otro") for i in d.index]
    orden = {"Costa": 0, "Sierra": 1, "Selva": 2, "Otro": 3}
    d = d.sort_values("__region", key=lambda s: s.map(orden)).drop(columns="__region")

    fig, ax = plt.subplots(figsize=(15, 7.6))
    sns.heatmap(
        d, cmap="YlOrRd", vmin=0, vmax=1, linewidths=0.6, linecolor="white",
        cbar_kws={"label": "Intensidad relativa del factor", "shrink": 0.7}, ax=ax,
    )
    ax.set_title(
        "Qué factor pesa más en cada departamento",
        fontsize=17, fontweight="bold", pad=14,
    )
    ax.set_xlabel("")
    ax.set_ylabel("")
    plt.setp(ax.get_xticklabels(), rotation=38, ha="right", fontsize=11.5)
    plt.setp(ax.get_yticklabels(), rotation=0, fontsize=11)

    # Separadores entre regiones naturales.
    regiones = [REGION.get(i, "Otro") for i in d.index]
    for i in range(1, len(regiones)):
        if regiones[i] != regiones[i - 1]:
            ax.axhline(i, color="#003366", linewidth=2.2)

    fig.text(0.5, 0.015,
             "Cuanto más intenso el color, mayor es el peso de ese factor en ese departamento.  "
             "Franjas separadas por región natural: costa, sierra y selva.",
             ha="center", fontsize=11, color="#55606b")
    plt.tight_layout(rect=(0, 0.035, 1, 1))

    out = FIGURES_DIR / "panel"
    out.mkdir(parents=True, exist_ok=True)
    path = out / "mapa_riesgo_departamental.png"
    fig.savefig(path, dpi=190, bbox_inches="tight")
    plt.close(fig)
    print(f"guardado: {path}")
    return path


if __name__ == "__main__":
    mapa_riesgo_departamental()
