import streamlit as st
import pandas as pd
import joblib
import json
import os
import plotly.express as px

st.set_page_config(page_title="Sistema de Alerta de Desnutrición", layout="wide")

# CSS Premium y Clínico
st.markdown(
    """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3 {
        font-family: 'Inter', 'Helvetica Neue', sans-serif;
        color: #1e293b;
    }
    .stButton>button {
        background-color: #0f172a;
        color: white;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #334155;
        color: white;
    }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
</style>
""",
    unsafe_allow_html=True,
)


# 1. CARGA DE RECURSOS
@st.cache_resource
def load_assets():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(BASE_DIR, "../models/champion_lightgbm.pkl")
    meta_path = os.path.join(BASE_DIR, "../models/champion_metadata.json")
    shap_data_path = os.path.join(BASE_DIR, "../data/processed/shap_dept_impact.csv")
    geojson_path = os.path.join(BASE_DIR, "peru_departamentos.geojson")

    model = joblib.load(model_path)
    with open(meta_path, "r") as f:
        metadata = json.load(f)

    try:
        df_shap = pd.read_csv(shap_data_path, index_col=0)
        with open(geojson_path, "r") as f:
            peru_geojson = json.load(f)
    except FileNotFoundError:
        df_shap = None
        peru_geojson = None

    return model, metadata, df_shap, peru_geojson


model, metadata, df_shap, peru_geojson = load_assets()
threshold = metadata["optimal_threshold"]

# INTERFAZ PRINCIPAL
st.title("Sistema de Predicción de Perfil de Riesgo Geográfico")
st.markdown(
    "Herramienta de análisis estructural basada en Inteligencia Artificial (LightGBM). Entrenada con datos históricos de la ENDES (2007-2024)."
)

tab1, tab2 = st.tabs(["Mapa Interactivo", "Predictor"])

# ==========================================
# TAB 1: PERFILADOR GEOGRÁFICO Y MAPA
# ==========================================
with tab1:
    st.markdown("### Centro de Comando: Perfilador Geográfico")
    st.write(
        "Vista de Dashboard: Mapa Nacional Interactivo (Izquierda) y Radiografía Departamental (Derecha)."
    )

    if df_shap is not None and peru_geojson is not None:
        # Mapeo de columnas técnicas a nombres legibles
        column_mapping = {
            "HV271_Factor_de_puntuacion_del_indice_de_riqueza": "Pobreza Económica Extrema",
            "m19_Peso_al_nacer_kg": "Bajo Peso al Nacer",
            "HV040_Altitud_del_conglomerado_en_metros": "Altitud Geográfica",
            "M18_Tamano_al_nacer": "Tamaño Pequeño al Nacer",
            "HC1_Edad_en_meses": "Edad Crítica",
            "HC56_Nivel_de_hemoglobina_ajustado_por_altitud": "Prevalencia de Anemia",
            "HC63_Intervalo_de_nacimientos_anteriores_al_nino": "Embarazos sin descanso",
            "HV240_Tiene_chimenea_o_campana": "Cocinas a Leña (Sin extracción de Humo)",
            "HV012_Miembros_habituales_De_jure": "Hacinamiento Familiar",
            "M4_Duracion_de_la_lactancia": "Falta de Lactancia Materna",
        }

        # Crear copia y renombrar columnas
        df_map = df_shap.rename(columns=column_mapping)
        df_map["NOMBDEP"] = (
            df_map.index.str.upper()
            .str.replace("Á", "A")
            .str.replace("É", "E")
            .str.replace("Í", "I")
            .str.replace("Ó", "O")
            .str.replace("Ú", "U")
        )

        available_factors = [col for col in df_map.columns if col != "NOMBDEP"]
        departamentos_list = df_map.index.tolist()

        # DIVIDIR LA PANTALLA EN 2 PANELES
        col_mapa, col_grafico = st.columns([2, 1])

        with col_mapa:
            st.markdown("#### 🗺️ Visión Nacional (Macro)")
            selected_factor = st.selectbox(
                "1. Pinte el Mapa por Factor de Riesgo:", options=available_factors
            )

            # Renderizar el Mapa Coroplético con Plotly
            fig = px.choropleth_mapbox(
                df_map,
                geojson=peru_geojson,
                featureidkey="properties.NOMBDEP",
                locations="NOMBDEP",
                color=selected_factor,
                color_continuous_scale="Reds",
                range_color=(0, 1),
                mapbox_style="carto-positron",
                zoom=4.2,
                center={"lat": -9.19, "lon": -75.01},
                opacity=0.7,
                labels={selected_factor: "Impacto Relativo"},
            )
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
            st.plotly_chart(fig, use_container_width=True)

        with col_grafico:
            st.markdown("#### 📊 Radiografía Local (Micro)")
            selected_dept = st.selectbox(
                "2. Auditar Departamento Específico:",
                options=departamentos_list,
                index=departamentos_list.index("Puno") if "Puno" in departamentos_list else 0,
            )

            st.markdown(f"**Top 5 Problemas en {selected_dept}**")

            # Extraer data del departamento y ordenar
            dept_data = (
                df_map.loc[selected_dept].drop("NOMBDEP").sort_values(ascending=False).head(5)
            )

            chart_data = pd.DataFrame(
                {"Intensidad": dept_data.values, "Factor": dept_data.index}
            ).set_index("Factor")

            # Dibujar gráfico de barras en Streamlit
            st.bar_chart(chart_data, color="#ff4b4b", height=380)

            st.caption(
                f"Si el Estado invierte en {selected_dept}, la Inteligencia Artificial sugiere mitigar prioritariamente la barra más alta."
            )

    else:
        st.warning("Calculando el Motor Geográfico... Por favor espere y recargue.")


# ==========================================
# TAB 1: SIMULADOR CLÍNICO
# ==========================================
with tab2:
    st.markdown("### Evaluación de Riesgo Estructural Individual")

    # Diseño sin formulario cuadrado, usando columnas directas
    col1, padding, col2 = st.columns([1, 0.1, 1])

    with col1:
        st.markdown("#### Historial Biológico")
        edad = st.number_input(
            "Edad actual del niño/a (meses)",
            min_value=0,
            max_value=59,
            value=24,
            help="La desnutrición es acumulativa y se agrava después del primer año de vida.",
        )

        peso_nacer = st.number_input(
            "Peso al nacer (Kilogramos)",
            min_value=1.0,
            max_value=6.0,
            value=3.2,
            step=0.1,
            help="Menos de 2.5kg se considera Bajo Peso al Nacer.",
        )

        hemo = st.number_input(
            "Resultado de Hemoglobina (g/dL multiplicado por 10)",
            min_value=50,
            max_value=200,
            value=110,
            help="Ejemplo: Si tiene 11.0 g/dL, ingrese 110. Valores por debajo de 110 indican Anemia.",
        )

        lactancia = st.number_input(
            "Duración de la Lactancia Materna (meses)",
            min_value=0,
            max_value=36,
            value=6,
            help="Factor protector inmunológico primario.",
        )

    with col2:
        st.markdown("#### Entorno Socio-Geográfico")
        altitud = st.number_input(
            "Altitud de la residencia (Metros s.n.m.)",
            min_value=0,
            max_value=5000,
            value=150,
            help="Zonas por encima de 2500m presentan riesgos por hipoxia y seguridad alimentaria.",
        )

        riqueza_text = st.select_slider(
            "Estrato socioeconómico del hogar",
            options=["Pobreza Extrema", "Pobre", "Medio", "Rico", "Muy Rico"],
            value="Medio",
        )
        riqueza_map = {
            "Pobreza Extrema": -150000,
            "Pobre": -50000,
            "Medio": 0,
            "Rico": 50000,
            "Muy Rico": 150000,
        }
        riqueza_val = riqueza_map[riqueza_text]

        miembros = st.number_input(
            "Personas que habitan en el hogar",
            min_value=2,
            max_value=20,
            value=4,
            help="Indicador de hacinamiento y competencia de recursos.",
        )

        chimenea_str = st.radio(
            "¿La cocina cuenta con extracción de humo (chimenea)?",
            options=["Sí, tiene extracción", "No, el humo se encierra"],
            help="La exposición crónica al humo de leña causa infecciones respiratorias que consumen la energía de crecimiento del niño.",
        )
        chimenea_val = 1 if chimenea_str == "Sí, tiene extracción" else 0

    st.markdown("<br>", unsafe_allow_html=True)

    # Botón principal
    if st.button("Ejecutar Diagnóstico Estructural"):
        input_dict = {col: 0 for col in metadata["features"]}
        input_dict["HC1_Edad_en_meses"] = edad
        input_dict["m19_Peso_al_nacer_kg"] = peso_nacer
        input_dict["HC56_Nivel_de_hemoglobina_ajustado_por_altitud"] = hemo
        input_dict["HV040_Altitud_del_conglomerado_en_metros"] = altitud
        input_dict["HV271_Factor_de_puntuacion_del_indice_de_riqueza"] = riqueza_val
        input_dict["HV012_Miembros_habituales_De_jure"] = miembros
        input_dict["HV240_Tiene_chimenea_o_campana"] = chimenea_val
        input_dict["M4_Duracion_de_la_lactancia"] = lactancia

        df_input = pd.DataFrame([input_dict])
        for col in metadata["cat_features"]:
            df_input[col] = df_input[col].astype("category")

        prob = model.predict_proba(df_input)[0][1]

        if prob >= threshold:
            st.markdown(
                f"""
            <div class="result-box" style="background-color: #fef2f2; border: 1px solid #f87171;">
                <h3 style="color: #b91c1c;">Alerta: Riesgo Estructural Alto ({prob * 100:.1f}%)</h3>
                <p style="color: #7f1d1d;">El análisis longitudinal de 18 años indica que los pacientes con este perfil exacto desarrollaron desnutrición crónica (talla baja para la edad). Se recomienda intervención nutricional y monitoreo constante.</p>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
            <div class="result-box" style="background-color: #f0fdf4; border: 1px solid #4ade80;">
                <h3 style="color: #15803d;">Diagnóstico: Riesgo Bajo ({prob * 100:.1f}%)</h3>
                <p style="color: #166534;">El paciente cuenta con factores protectores suficientes. Se mantiene la vigilancia de control regular.</p>
            </div>
            """,
                unsafe_allow_html=True,
            )
