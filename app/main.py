import json
import os
import sys

import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fields import (BY_FEATURE, BY_KEY, EXAMPLES, FIELDS, GROUPS, KEY_FIELDS, LABEL_BY_FEATURE,
                    build_model_frame, is_missing, label_to_value, parse_upload, read_table, template_frame,
                    value_to_label)

st.set_page_config(page_title="Sistema de Alerta de Desnutrición", layout="wide")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1, h2, h3 { font-family: 'Inter', 'Helvetica Neue', sans-serif; color: #1e293b; }
    .result-box { padding: 16px 18px; border-radius: 10px; margin-top: 6px; }
</style>
""", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
N_FIELDS = len(FIELDS)


@st.cache_resource
def load_assets():
    model = joblib.load(os.path.join(BASE_DIR, "../models/champion_lightgbm.pkl"))
    with open(os.path.join(BASE_DIR, "../models/champion_metadata.json")) as f:
        metadata = json.load(f)
    with open(os.path.join(BASE_DIR, "../models/threshold_recall_curve.json")) as f:
        recall_curve = json.load(f)
    booster = model.booster_
    features = booster.feature_name()
    cat_feats = [f for f in features if f in metadata["cat_features"]]
    categories = dict(zip(cat_feats, booster.pandas_categorical))
    try:
        df_shap = pd.read_csv(os.path.join(BASE_DIR, "../data/processed/shap_dept_impact.csv"), index_col=0)
        with open(os.path.join(BASE_DIR, "peru_departamentos.geojson")) as f:
            peru_geojson = json.load(f)
    except FileNotFoundError:
        df_shap, peru_geojson = None, None
    return model, features, categories, recall_curve, df_shap, peru_geojson


def threshold_for_recall(recall_curve, target_recall_pct):
    target = target_recall_pct / 100
    candidates = [r for r in recall_curve if r["recall"] >= target]
    best = max(candidates, key=lambda r: r["threshold"]) if candidates else recall_curve[-1]
    return best["threshold"], round(best["recall"] * 100, 1), round(best["precision"] * 100, 1)


def score(answers):
    """Puntaje (0-1) y contribuciones por variable para una lista de respuestas {feature: valor}."""
    X = build_model_frame(answers, FEATURES, CATEGORIES)
    probs = MODEL.predict_proba(X)[:, 1]
    contrib = MODEL.predict(X, pred_contrib=True)[:, :-1]
    return probs, pd.DataFrame(contrib, columns=FEATURES)


def n_answered(answer):
    return sum(not is_missing(answer.get(f["feature"])) for f in FIELDS)


def top_factors(contrib_row, answer, k=3):
    s = contrib_row[contrib_row > 0].sort_values(ascending=False).head(k)
    return "; ".join(f"{LABEL_BY_FEATURE[f]} ({value_to_label(BY_FEATURE[f], answer.get(f))})" for f in s.index)


MODEL, FEATURES, CATEGORIES, RECALL_CURVE, DF_SHAP, PERU_GEOJSON = load_assets()

st.title("Sistema Predictivo de Riesgo de Desnutrición Crónica")
st.markdown("Herramienta de apoyo a la focalización basada en Machine Learning (LightGBM · AUC 0.83). "
            "Entrenada con 304,271 niños — ENDES 2007–2025.")

# ── Sensibilidad del triaje: común a la evaluación individual y por grupo ──
with st.sidebar:
    st.markdown("### Sensibilidad del triaje")
    target_recall = st.slider("¿Qué % de niños con desnutrición crónica quiero detectar?",
                              min_value=50, max_value=99, value=80, step=1, key="recall",
                              help="Detectar más casos exige revisar a más niños que finalmente no la tienen.")
    THRESHOLD, REAL_RECALL, REAL_PRECISION = threshold_for_recall(RECALL_CURVE, target_recall)
    st.markdown(f"Umbral de prioridad: **{THRESHOLD * 100:.0f}** de 100")
    st.caption(f"En la validación, este umbral detectó al {REAL_RECALL}% de los niños con desnutrición "
               f"crónica; de los señalados como prioridad alta, el {REAL_PRECISION}% la tenía.")

tab_map, tab_one, tab_batch = st.tabs(["Mapa de riesgo territorial", "Evaluar un niño", "Evaluar un grupo"])

# ──────────────────────────────────────────────
# MAPA
# ──────────────────────────────────────────────
with tab_map:
    st.markdown("### Qué factores pesan más en cada departamento")
    st.caption("Para cada factor, el mapa compara cuánto influye en las predicciones del modelo para los niños de "
               "cada departamento (0 = el departamento donde menos influye, 1 = donde más). Indica peso, no si el "
               "factor sube o baja el riesgo. Fuente: valores SHAP del modelo sobre 10,000 niños.")

    if DF_SHAP is not None and PERU_GEOJSON is not None:
        df_map = DF_SHAP.copy()
        df_map.columns = [LABEL_BY_FEATURE.get(c, c) for c in df_map.columns]
        df_map["NOMBDEP"] = (df_map.index.str.upper().str.replace("Á", "A").str.replace("É", "E")
                             .str.replace("Í", "I").str.replace("Ó", "O").str.replace("Ú", "U"))
        available_factors = [c for c in df_map.columns if c != "NOMBDEP"]
        departamentos_list = df_map.index.tolist()

        col_mapa, col_grafico = st.columns([2, 1])
        with col_mapa:
            selected_factor = st.selectbox("Factor:", options=available_factors, key="map_factor")
            df_map["Peso relativo"] = (df_map[selected_factor] * 100).round(1).astype(str) + "% del máximo"
            fig = px.choropleth_map(
                df_map, geojson=PERU_GEOJSON, featureidkey="properties.NOMBDEP", locations="NOMBDEP",
                color=selected_factor, color_continuous_scale="Reds", range_color=(0, 1),
                map_style="carto-positron", zoom=4.2, center={"lat": -9.19, "lon": -75.01}, opacity=0.75,
                hover_name="NOMBDEP", hover_data={"NOMBDEP": False, selected_factor: False, "Peso relativo": True},
            )
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                              coloraxis_colorbar=dict(title="Peso", tickformat=".0%"))
            st.plotly_chart(fig, width="stretch")

            top5 = df_map.nlargest(5, selected_factor)[[selected_factor]].copy()
            top5.columns = ["Peso relativo"]
            top5["Peso relativo"] = (top5["Peso relativo"] * 100).round(1).astype(str) + "%"
            st.markdown(f"**Departamentos donde más pesa «{selected_factor}»:**")
            st.dataframe(top5, width="stretch")

        with col_grafico:
            selected_dept = st.selectbox(
                "Departamento:", options=departamentos_list, key="map_dept",
                index=departamentos_list.index("Puno") if "Puno" in departamentos_list else 0)
            top_n = st.slider("Factores a mostrar:", min_value=3, max_value=15, value=8, key="map_topn")
            dept_data = (df_map.loc[selected_dept, available_factors].astype(float)
                         .sort_values(ascending=True).tail(top_n).round(2))
            fig_bar = px.bar(x=dept_data.values, y=dept_data.index, orientation="h", text=dept_data.values,
                             labels={"x": "Peso relativo", "y": ""})
            fig_bar.update_traces(marker_color="#b91c1c", textposition="outside", texttemplate="%{text:.2f}")
            fig_bar.update_layout(margin={"r": 10, "t": 10, "l": 0, "b": 0}, xaxis_range=[0, 1.15])
            st.plotly_chart(fig_bar, width="stretch")
            st.info(f"En **{selected_dept}**, estos son los factores que más pesan en las predicciones del modelo, "
                    "comparado con el resto del país.")
    else:
        st.warning("No se encontraron los archivos del mapa (shap_dept_impact.csv y peru_departamentos.geojson).")


# ──────────────────────────────────────────────
# EVALUAR UN NIÑO
# ──────────────────────────────────────────────
def load_example(name):
    for f in FIELDS:
        st.session_state["f_" + f["key"]] = EXAMPLES.get(name, {}).get(f["key"])


def render_field(f):
    wkey = "f_" + f["key"]
    st.session_state.setdefault(wkey, None)
    if f["kind"] == "num":
        is_int = float(f["step"]).is_integer()
        cast = int if is_int else float
        st.number_input(f["label"], min_value=cast(f["min"]), max_value=cast(f["max"]), step=cast(f["step"]),
                        key=wkey, placeholder="Sin dato", help=f.get("help"))
    else:
        st.selectbox(f["label"], options=[lab for lab, _ in f["options"]], key=wkey,
                     index=None, placeholder="Sin dato", help=f.get("help"))


def answer_from_state():
    answer = {}
    for f in FIELDS:
        raw = st.session_state.get("f_" + f["key"])
        if is_missing(raw):
            answer[f["feature"]] = None
        elif f["kind"] == "num":
            answer[f["feature"]] = float(raw)
        else:
            answer[f["feature"]] = label_to_value(f, raw)
    return answer


with tab_one:
    st.markdown("### Evaluar a un niño")
    st.caption("Complete los datos que conozca. Los campos que deje en **Sin dato** se envían al modelo como "
               "dato faltante, sin inventar un valor.")

    b1, b2, b3, _ = st.columns([1.2, 1.2, 1, 3])
    b1.button("Ejemplo: prioridad alta", on_click=load_example, args=("alto",), width="stretch")
    b2.button("Ejemplo: prioridad regular", on_click=load_example, args=("bajo",), width="stretch")
    b3.button("Limpiar", on_click=load_example, args=("",), width="stretch")

    form_col, result_col = st.columns([2, 1])
    with form_col:
        cols = st.columns(3)
        for col, group in zip(cols, ["Niño", "Madre", "Hogar"]):
            with col:
                st.markdown(f"##### {GROUPS[group]}")
                for f in FIELDS:
                    if f["group"] == group:
                        render_field(f)
        with st.expander("Agua, saneamiento y vivienda"):
            cols = st.columns(2)
            for col, group in zip(cols, ["Agua", "Vivienda"]):
                with col:
                    st.markdown(f"##### {GROUPS[group]}")
                    for f in FIELDS:
                        if f["group"] == group:
                            render_field(f)

    with result_col:
        answer = answer_from_state()
        n = n_answered(answer)
        missing_key = [BY_KEY[k]["label"] for k in KEY_FIELDS if is_missing(answer[BY_KEY[k]["feature"]])]

        st.markdown("##### Resultado")
        st.progress(n / N_FIELDS, text=f"Datos ingresados: {n} de {N_FIELDS}")

        if n == 0:
            st.info("Ingrese los datos del niño o cargue un ejemplo para ver el resultado.")
        else:
            probs, contrib = score([answer])
            prob = float(probs[0])
            if missing_key:
                st.warning("Faltan datos de mucho peso en el modelo: " + ", ".join(missing_key) +
                           ". El resultado es menos confiable.")

            high = prob >= THRESHOLD
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number", value=prob * 100, number={"font": {"size": 40}, "valueformat": ".0f"},
                gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#b91c1c" if high else "#15803d"},
                       "steps": [{"range": [0, THRESHOLD * 100], "color": "#dcfce7"},
                                 {"range": [THRESHOLD * 100, 100], "color": "#fee2e2"}],
                       "threshold": {"line": {"color": "#7f1d1d", "width": 3}, "thickness": 0.75,
                                     "value": THRESHOLD * 100}},
                title={"text": "Puntaje de riesgo (0–100)", "font": {"size": 13}},
            ))
            fig_gauge.update_layout(margin=dict(t=50, b=10, l=10, r=10), height=230)
            st.plotly_chart(fig_gauge, width="stretch")

            if high:
                st.markdown(f"""<div class="result-box" style="background:#fef2f2;border:2px solid #f87171;">
                    <strong style="color:#b91c1c;">Prioridad alta</strong><br>
                    <span style="color:#7f1d1d;font-size:0.9rem;">El puntaje ({prob*100:.0f}) supera el umbral
                    ({THRESHOLD*100:.0f}). Se sugiere priorizar su evaluación antropométrica.</span></div>""",
                            unsafe_allow_html=True)
            else:
                st.markdown(f"""<div class="result-box" style="background:#f0fdf4;border:2px solid #4ade80;">
                    <strong style="color:#15803d;">Prioridad regular</strong><br>
                    <span style="color:#166534;font-size:0.9rem;">El puntaje ({prob*100:.0f}) está por debajo del
                    umbral ({THRESHOLD*100:.0f}). Mantener el control regular.</span></div>""",
                            unsafe_allow_html=True)
            st.caption("El puntaje sirve para ordenar a los niños según su riesgo; no es la probabilidad de que el "
                       "niño tenga desnutrición crónica. El diagnóstico requiere medir talla y edad.")

    if n > 0:
        st.markdown("#### Por qué obtuvo este puntaje")
        st.caption("Cuánto sube (rojo) o baja (verde) el puntaje cada dato de este niño según el modelo (valores "
                   "SHAP). Es una asociación aprendida de la ENDES, no una causa. Los datos en «Sin dato» también "
                   "influyen, porque el modelo aprendió qué suele pasar cuando falta ese dato.")
        c = contrib.iloc[0]
        top = c.reindex(c.abs().sort_values(ascending=False).index).head(10)[::-1]
        labels = [f"{LABEL_BY_FEATURE[f]}: {value_to_label(BY_FEATURE[f], answer.get(f))}" for f in top.index]
        fig_c = go.Figure(go.Bar(x=top.values, y=labels, orientation="h",
                                 marker_color=["#b91c1c" if v > 0 else "#15803d" for v in top.values]))
        fig_c.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=380,
                            xaxis_title="Efecto sobre el puntaje (escala log-odds)")
        st.plotly_chart(fig_c, width="stretch")


# ──────────────────────────────────────────────
# EVALUAR UN GRUPO
# ──────────────────────────────────────────────
with tab_batch:
    st.markdown("### Evaluar a un grupo de niños")
    st.caption("Suba un archivo con un niño por fila (por ejemplo, el padrón de un establecimiento) y obtenga la "
               "lista ordenada por puntaje de riesgo. Las celdas vacías se tratan como dato faltante.")

    c1, c2 = st.columns([1, 2])
    with c1:
        st.download_button("Descargar plantilla (CSV)", data=template_frame().to_csv(index=False).encode("utf-8-sig"),
                           file_name="plantilla_evaluacion_grupo.csv", mime="text/csv", width="stretch")
        with st.expander("Valores aceptados en las columnas de opciones"):
            for f in FIELDS:
                if f["kind"] != "num":
                    st.markdown(f"**{f['label']}:** " + " · ".join(lab for lab, _ in f["options"]))
    with c2:
        upload = st.file_uploader("Archivo CSV o Excel", type=["csv", "xlsx"], key="batch_file")

    if upload is not None:
        try:
            df_up = read_table(upload.getvalue(), upload.name)
        except Exception as e:
            st.error(f"No se pudo leer el archivo: {e}. Use la plantilla en CSV o Excel.")
            df_up = None

        if df_up is not None and len(df_up):
            answers, matched, problems = parse_upload(df_up)
            if not matched:
                st.error("Ninguna columna coincide con la plantilla. Descargue la plantilla y use sus encabezados.")
            else:
                probs, contrib = score(answers)
                id_col = next((c for c in df_up.columns if str(c).strip().lower() == "id"), None)
                ids = df_up[id_col].astype(str) if id_col else pd.Series(range(1, len(df_up) + 1)).astype(str)
                out = pd.DataFrame({
                    "id": ids.values,
                    "Puntaje": (probs * 100).round(0).astype(int),
                    "Prioridad": np.where(probs >= THRESHOLD, "Alta", "Regular"),
                    "Datos ingresados": [f"{n_answered(a)} de {N_FIELDS}" for a in answers],
                    "Principales factores que suben el puntaje": [
                        top_factors(contrib.iloc[i], answers[i]) for i in range(len(answers))],
                }).sort_values("Puntaje", ascending=False).reset_index(drop=True)
                out.index = out.index + 1

                n_high = int((out["Prioridad"] == "Alta").sum())
                m1, m2, m3 = st.columns(3)
                m1.metric("Niños evaluados", len(out))
                m2.metric("Prioridad alta", n_high)
                m3.metric("Columnas reconocidas", f"{len(matched)} de {N_FIELDS}")

                if len(matched) < N_FIELDS:
                    faltan = [f["label"] for f in FIELDS if f not in matched.values()]
                    st.info("Columnas no incluidas en el archivo (se tratan como dato faltante): " + ", ".join(faltan))
                if problems:
                    st.warning("Algunos valores no se reconocieron y se trataron como dato faltante: " + "; ".join(
                        f"{k}: {', '.join(sorted(v)[:4])}" for k, v in problems.items()))

                st.dataframe(out, width="stretch",
                             column_config={"Puntaje": st.column_config.ProgressColumn(
                                 "Puntaje", min_value=0, max_value=100, format="%d")})
                st.download_button("Descargar lista priorizada (CSV)",
                                   data=out.to_csv(index_label="orden").encode("utf-8-sig"),
                                   file_name="lista_priorizada.csv", mime="text/csv")
                st.caption("El puntaje ordena a los niños según su riesgo; no es la probabilidad de desnutrición "
                           "crónica. La lista sirve para decidir a quién evaluar primero, no reemplaza la medición.")
        elif df_up is not None:
            st.warning("El archivo no tiene filas.")
