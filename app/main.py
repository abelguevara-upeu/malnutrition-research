import streamlit as st
import pandas as pd
import joblib
import json
import os
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Sistema de Alerta de Desnutrición", layout="wide")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1, h2, h3 { font-family: 'Inter', 'Helvetica Neue', sans-serif; color: #1e293b; }
    .stButton>button {
        background-color: #0f172a; color: white;
        border-radius: 6px; padding: 0.5rem 1rem; font-weight: 600;
    }
    .stButton>button:hover { background-color: #334155; color: white; }
    .result-box { padding: 20px; border-radius: 10px; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_assets():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    model = joblib.load(os.path.join(BASE_DIR, "../models/champion_lightgbm.pkl"))
    with open(os.path.join(BASE_DIR, "../models/champion_metadata.json")) as f:
        metadata = json.load(f)
    with open(os.path.join(BASE_DIR, "../models/threshold_recall_curve.json")) as f:
        recall_curve = json.load(f)
    try:
        df_shap = pd.read_csv(os.path.join(BASE_DIR, "../data/processed/shap_dept_impact.csv"), index_col=0)
        with open(os.path.join(BASE_DIR, "peru_departamentos.geojson")) as f:
            peru_geojson = json.load(f)
    except FileNotFoundError:
        df_shap = None
        peru_geojson = None
    return model, metadata, recall_curve, df_shap, peru_geojson


def threshold_for_recall(recall_curve, target_recall_pct):
    target = target_recall_pct / 100
    candidates = [r for r in recall_curve if r["recall"] >= target]
    if not candidates:
        best = recall_curve[-1]
    else:
        best = max(candidates, key=lambda r: r["threshold"])
    return best["threshold"], round(best["recall"] * 100, 1), round(best["precision"] * 100, 1)


model, metadata, recall_curve, df_shap, peru_geojson = load_assets()

st.title("Sistema Predictivo de Riesgo de Desnutrición Crónica")
st.markdown("Herramienta de triaje basada en Machine Learning (LightGBM · AUC 0.83 · Recall 76%). Entrenada con 285,284 niños — ENDES 2007–2024.")

tab1, tab2 = st.tabs(["Mapa de Riesgo Territorial", "Predictor Individual"])

# ──────────────────────────────────────────────
# TAB 1: MAPA INTERACTIVO
# ──────────────────────────────────────────────
with tab1:
    st.markdown("### Distribución Geográfica del Riesgo")
    st.caption("Intensidad relativa de cada factor de riesgo por departamento (escala 0–1 normalizada). Fuente: SHAP values del modelo campeón sobre 10,000 niños.")

    # Nombres legibles para las 43 variables SHAP
    FACTOR_NAMES = {
        "HV271_Factor_de_puntuacion_del_indice_de_riqueza": "Pobreza económica extrema",
        "m19_Peso_al_nacer_kg": "Bajo peso al nacer",
        "HV040_Altitud_del_conglomerado_en_metros": "Altitud geográfica",
        "HC1_Edad_en_meses": "Edad crítica (ventana 1000 días)",
        "HC56_Nivel_de_hemoglobina_ajustado_por_altitud": "Anemia (hemoglobina baja)",
        "HC63_Intervalo_de_nacimientos_anteriores_al_nino": "Embarazos muy seguidos",
        "M4_Duracion_de_la_lactancia": "Lactancia materna insuficiente",
        "HV220_Edad_del_jefe_del_hogar": "Jefe del hogar joven o mayor",
        "M46_Dias_que_tomo_hierro": "Falta de hierro gestacional",
        "M18_Tamano_al_nacer": "Talla pequeña al nacer",
        "m34_Horas_hasta_inicio_de_lactancia": "Inicio tardío de lactancia",
        "M14_Numero_de_visitas_prenatales": "Controles prenatales insuficientes",
        "HC62_Ano_mas_alto_de_educacion_de_la_madre": "Educación materna baja",
        "HC27_Sexo": "Sexo del niño",
        "HV012_Miembros_habituales_De_jure": "Hacinamiento familiar",
        "SH49_Tipo_de_envase_o_recipiente": "Tipo de recipiente de agua",
        "M13_Mes_de_gestacion_en_el_1er_control": "Inicio tardío de controles prenatales",
        "HV234_Prueba_de_yodo_para_sal": "Sal sin yodo",
        "SH42_Agua_Todo_El_Dia": "Sin acceso a agua continua",
        "HV240_Tiene_chimenea_o_campana": "Cocina a leña sin extracción de humo",
        "SH71_Numero_de_habitaciones_en_el_hogar": "Vivienda pequeña",
        "M55G_Liquidos_primeros_3_dias_Formula_para_bebes": "Fórmula artificial primeros días",
        "SH76B_Ventanas_con_cristal": "Sin ventanas de cristal",
        "SH70_Fuente_Luz": "Fuente de luz precaria",
        "HV014_Ninos_menores_de_5_anos": "Más niños < 5 años en el hogar",
        "SH50_Lo_usa_con_tapa": "Recipiente sin tapa",
        "SH63_Utiliza_otro_tipo_de_combustible_para_cocinar": "Uso de combustible adicional",
        "HV216_Habitaciones_para_dormir": "Pocas habitaciones para dormir",
        "HV242_Cuarto_separado_para_cocinar": "Sin cocina separada",
        "HV204_Tiempo_de_viaje_a_fuente": "Lejos de fuente de agua",
        "HV225_Comparte_servicio_higienico": "Comparte servicio higiénico",
        "HV237G_Agua_embotellada": "Usa agua embotellada",
        "HV025_Area_de_residencia": "Zona rural",
        "SH76D_Ventanas_con_malla": "Sin ventanas con malla",
        "m15_Lugar_del_parto_agrupado": "Parto domiciliario",
        "M17_Parto_por_cesarea": "Parto sin cesárea (cuando indicada)",
        "M54_Vitamina_A_primeros_2_meses_post_parto": "Sin vitamina A post-parto",
        "SH76C_Ventanas_de_madera": "Ventanas de madera",
        "M60_Tomo_antiparasitarios_en_el_embarazo": "Sin antiparasitarios en gestación",
        "SH48_Conserva_Agua": "No conserva agua",
        "HV237A_Tratamiento_de_agua_hervir": "Hierve el agua",
        "HV102_Residente_habitual": "Residente no habitual",
        "HV237_Tratamiento_del_agua": "Trata el agua",
    }

    if df_shap is not None and peru_geojson is not None:
        df_map = df_shap.copy()
        df_map.columns = [FACTOR_NAMES.get(c, c.split("_", 1)[-1].replace("_", " ").capitalize()) for c in df_map.columns]
        df_map["NOMBDEP"] = (
            df_map.index.str.upper()
            .str.replace("Á", "A").str.replace("É", "E")
            .str.replace("Í", "I").str.replace("Ó", "O").str.replace("Ú", "U")
        )

        available_factors = [c for c in df_map.columns if c != "NOMBDEP"]
        departamentos_list = df_map.index.tolist()

        col_mapa, col_grafico = st.columns([2, 1])

        with col_mapa:
            st.markdown("#### Mapa Nacional por Factor de Riesgo")
            selected_factor = st.selectbox("Factor de riesgo a visualizar:", options=available_factors)

            df_map["Intensidad"] = (df_map[selected_factor] * 100).round(1).astype(str) + "% del máximo nacional"

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
                opacity=0.75,
                hover_name="NOMBDEP",
                hover_data={"NOMBDEP": False, selected_factor: False, "Intensidad": True},
            )
            fig.update_traces(
                hovertemplate="<b>%{hovertext}</b><br>Intensidad relativa: %{customdata[2]}<extra></extra>"
            )
            fig.update_layout(
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                coloraxis_colorbar=dict(title="Intensidad", tickformat=".0%"),
            )
            st.plotly_chart(fig, use_container_width=True)

            # Top 5 departamentos más afectados por el factor seleccionado
            top5 = df_map.nlargest(5, selected_factor)[["NOMBDEP", selected_factor]].copy()
            top5.columns = ["Departamento", "Intensidad relativa"]
            top5["Intensidad relativa"] = (top5["Intensidad relativa"] * 100).round(1).astype(str) + "%"
            top5.index = range(1, 6)
            st.markdown(f"**Top 5 departamentos con mayor '{selected_factor}':**")
            st.dataframe(top5, use_container_width=True)

        with col_grafico:
            st.markdown("#### Perfil de Riesgo Departamental")
            selected_dept = st.selectbox(
                "Departamento:",
                options=departamentos_list,
                index=departamentos_list.index("Puno") if "Puno" in departamentos_list else 0,
            )
            top_n = st.slider("Variables a mostrar:", min_value=3, max_value=15, value=8)

            dept_data = (
                df_map.loc[selected_dept, available_factors]
                .sort_values(ascending=True)
                .tail(top_n)
                .astype(float)
                .round(3)
            )

            chart_data = pd.DataFrame({
                "Intensidad de riesgo": dept_data.values,
                "Factor": dept_data.index,
            })

            fig_bar = px.bar(
                chart_data,
                x="Intensidad de riesgo",
                y="Factor",
                orientation="h",
                color="Intensidad de riesgo",
                color_continuous_scale="Reds",
                text="Intensidad de riesgo",
            )
            fig_bar.update_traces(textposition="outside", texttemplate="%{text:.2f}")
            fig_bar.update_layout(
                margin={"r": 10, "t": 10, "l": 0, "b": 0},
                xaxis_range=[0, 1.15],
                coloraxis_showscale=False,
                yaxis=dict(tickfont=dict(size=11)),
            )
            st.plotly_chart(fig_bar, use_container_width=True)

            st.info(
                f"**Lectura del perfil en {selected_dept}:**\n\n"
                "Los factores con barra más larga son los que más impulsan el riesgo de desnutrición "
                "en este departamento comparado con el resto del país (escala relativa 0–1)."
            )
    else:
        st.warning("Archivos de datos geográficos no encontrados. Verifique shap_dept_impact.csv y peru_departamentos.geojson.")


# ──────────────────────────────────────────────
# TAB 2: PREDICTOR INDIVIDUAL
# ──────────────────────────────────────────────
with tab2:
    st.markdown("### Evaluación de Riesgo Individual")
    st.caption("Variables ordenadas por importancia predictiva (SHAP global). Top 43 del modelo campeón.")

    tamano_map = {"Muy grande": 1, "Más grande que el promedio": 2, "Promedio": 3,
                  "Más pequeño que el promedio": 4, "Muy pequeño": 5}
    riqueza_map = {"Pobreza Extrema": -150000, "Pobre": -50000, "Medio": 0, "Rico": 50000, "Muy Rico": 150000}


    # Layout: formulario (izquierda amplia) | panel de resultado (derecha fija)
    form_col, result_col = st.columns([2, 1])

    with form_col:
        # ── Formulario principal en 3 columnas ──
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown("##### Datos del Niño")
            sexo_ui = st.selectbox("Género", options=["Masculino", "Femenino"])
            sexo_str = "Hombre" if sexo_ui == "Masculino" else "Mujer"
            edad = st.number_input("Edad (meses)", min_value=0, max_value=59, value=24,
                help="Riesgo máximo meses 6–20.")
            peso_nacer = st.number_input("Peso al nacer (kg)", min_value=0.5, max_value=6.0,
                value=3.2, step=0.1, help="< 2.5 kg = bajo peso al nacer.")
            tamano_nacer_text = st.selectbox("Talla al nacer",
                options=["Muy grande", "Más grande que el promedio", "Promedio",
                         "Más pequeño que el promedio", "Muy pequeño"], index=2)
            hemo = st.number_input("Hemoglobina ajustada (g/dL)", min_value=1.0,
                max_value=20.0, value=11.3, step=0.1, help="Normal en niños: > 11.0 g/dL.")
            intervalo_nac = st.number_input(
                "Meses desde el nacimiento anterior",
                min_value=0, max_value=200, value=24,
                help="¿Cuántos meses pasaron entre el hijo anterior y este niño? "
                     "Si es el primer hijo, ingrese 0. "
                     "OMS recomienda mínimo 24 meses.")

        with c2:
            st.markdown("##### Historia Materna")
            lactancia = st.number_input("Duración de la lactancia (meses)", min_value=0, max_value=36, value=6)
            dias_hierro = st.number_input("Días de hierro en el embarazo", min_value=0, max_value=300, value=90)
            visitas_prenatales = st.number_input("Visitas prenatales", min_value=0, max_value=20, value=6,
                help="OMS recomienda mínimo 8.")
            educ_madre = st.number_input("Años de educación de la madre",
                min_value=0, max_value=20, value=8,
                help="0 = sin educación · 6 = primaria · 11 = secundaria · 16+ = superior")
            lugar_parto_str = st.selectbox("Lugar del parto",
                options=["Institucional", "Domiciliario"], index=0)

        with c3:
            st.markdown("##### Entorno del Hogar")
            riqueza_text = st.select_slider("Estrato socioeconómico",
                options=["Pobreza Extrema", "Pobre", "Medio", "Rico", "Muy Rico"], value="Medio")
            area_str = st.radio("Área de residencia", options=["Urbano", "Rural"], horizontal=True)
            altitud = st.number_input("Altitud (m s.n.m.)", min_value=0, max_value=5000, value=150,
                help="> 2,500 m: riesgo por hipoxia.")
            miembros = st.number_input("Personas en el hogar", min_value=1, max_value=20, value=4)
            edad_jefe = st.number_input("Edad del jefe del hogar", min_value=15, max_value=99, value=35)
            chimenea_str = st.radio("¿Cocina con extracción de humo?",
                options=["Sí", "No"], index=1, horizontal=True)

        # ── Expander: 26 variables adicionales en 3 columnas temáticas ──
        with st.expander("Parámetros adicionales (26 variables complementarias)"):
            st.caption("Defaults razonables precargados. El modelo maneja datos faltantes internamente.")

            e1, e2, e3 = st.columns(3)

            with e1:
                st.markdown("**Agua y Saneamiento**")
                comparte_sanitario = st.selectbox("¿Comparte servicio higiénico?", ["Si", "No"], index=1, key="hv225")
                trata_agua        = st.selectbox("¿Trata el agua?",          ["Si", "No"], index=1, key="hv237")
                hierve_agua       = st.selectbox("¿Hierve el agua?",         ["Si", "No"], index=0, key="hv237a")
                agua_botella      = st.selectbox("¿Agua embotellada?",       ["Si", "No"], index=1, key="hv237g")
                agua_continua     = st.selectbox("¿Agua todo el día?",       ["Sí", "No"], index=0, key="sh42")
                conserva_agua     = st.selectbox("¿Conserva agua?",          ["Sí", "No"], index=0, key="sh48")
                tiempo_fuente     = st.number_input("Tiempo a fuente de agua (min)", min_value=0, max_value=999, value=0, key="hv204")
                prueba_yodo       = st.number_input("Sal con yodo (0=No, 1=Sí)", min_value=0, max_value=1, value=1, key="hv234")
                tipo_recipiente   = st.number_input("Tipo recipiente de agua (código)", min_value=0, max_value=20, value=0, key="sh49")
                usa_tapa          = st.number_input("¿Recipiente con tapa? (0=No, 1=Sí)", min_value=0, max_value=1, value=1, key="sh50")

            with e2:
                st.markdown("**Vivienda**")
                cuarto_cocina     = st.selectbox("¿Cocina en cuarto separado?",        ["Sí", "No"], index=0, key="hv242")
                otro_combustible  = st.selectbox("¿Usa otro combustible?",             ["Sí", "No"], index=1, key="sh63")
                ventana_cristal   = st.selectbox("¿Ventanas con cristal?",             ["Si", "No"], index=0, key="sh76b")
                ventana_madera    = st.selectbox("¿Ventanas de madera?",               ["Si", "No"], index=1, key="sh76c")
                ventana_malla     = st.selectbox("¿Ventanas con malla?",               ["Si", "No"], index=0, key="sh76d")
                fuente_luz        = st.number_input("Fuente de luz (código)", min_value=0, max_value=20, value=1, key="sh70")
                habitaciones_total= st.number_input("Total habitaciones", min_value=1, max_value=15, value=3, key="sh71")
                habitaciones_dormir=st.number_input("Habitaciones para dormir", min_value=1, max_value=10, value=2, key="hv216")

            with e3:
                st.markdown("**Prenatal / Clínico**")
                ninos_menores5    = st.number_input("Niños < 5 años en el hogar", min_value=1, max_value=10, value=1, key="hv014")
                residente_hab     = st.selectbox("¿Residente habitual?", ["Sí", "No"], index=0, key="hv102")
                mes_primer_control= st.number_input("Mes gestación 1er control", min_value=0, max_value=10, value=3, key="m13")
                cesarea           = st.number_input("¿Cesárea? (0=No, 1=Sí)", min_value=0, max_value=1, value=0, key="m17")
                vitamina_a        = st.number_input("¿Vitamina A post-parto? (0=No, 1=Sí)", min_value=0, max_value=1, value=0, key="m54")
                formula_bebe      = st.number_input("¿Fórmula primeros 3 días? (0=No, 1=Sí)", min_value=0, max_value=1, value=0, key="m55g")
                antiparasitarios  = st.number_input("¿Antiparasitarios gestación? (0=No, 1=Sí)", min_value=0, max_value=1, value=0, key="m60")
                horas_lactancia   = st.number_input("Horas hasta inicio de lactancia", min_value=0, max_value=72, value=0, key="m34")

    # ── Panel de resultado (columna derecha, siempre visible) ──
    with result_col:
        st.markdown("##### Sensibilidad del Triaje")

        target_recall = st.slider(
            "¿Qué % de niños desnutridos quiero detectar?",
            min_value=50, max_value=99, value=80, step=1,
            help="Aumentar la detección reduce la precisión — se generan más visitas preventivas."
        )

        threshold_used, real_recall, real_precision = threshold_for_recall(recall_curve, target_recall)

        st.markdown(
            f"Umbral automático: **{threshold_used:.2f}** → "
            f"Recall real **{real_recall}%** · Precisión **{real_precision}%**"
        )
        st.caption("A mayor recall: más casos detectados, más visitas preventivas necesarias.")
        st.markdown("---")

        calcular = st.button("Calcular Riesgo", use_container_width=True)

        if calcular:
            input_dict = {}
            for feat in metadata["features"]:
                input_dict[feat] = None if feat in metadata["cat_features"] else 0

            # Formulario principal
            input_dict["HC27_Sexo"] = sexo_str
            input_dict["HC1_Edad_en_meses"] = edad
            input_dict["m19_Peso_al_nacer_kg"] = peso_nacer
            input_dict["M18_Tamano_al_nacer"] = tamano_map[tamano_nacer_text]
            input_dict["HC56_Nivel_de_hemoglobina_ajustado_por_altitud"] = hemo
            input_dict["HC63_Intervalo_de_nacimientos_anteriores_al_nino"] = intervalo_nac
            input_dict["M4_Duracion_de_la_lactancia"] = lactancia
            input_dict["M46_Dias_que_tomo_hierro"] = dias_hierro
            input_dict["M14_Numero_de_visitas_prenatales"] = visitas_prenatales
            input_dict["HC62_Ano_mas_alto_de_educacion_de_la_madre"] = educ_madre
            input_dict["m15_Lugar_del_parto_agrupado"] = lugar_parto_str
            input_dict["HV271_Factor_de_puntuacion_del_indice_de_riqueza"] = riqueza_map[riqueza_text]
            input_dict["HV025_Area_de_residencia"] = area_str
            input_dict["HV040_Altitud_del_conglomerado_en_metros"] = altitud
            input_dict["HV012_Miembros_habituales_De_jure"] = miembros
            input_dict["HV220_Edad_del_jefe_del_hogar"] = edad_jefe
            input_dict["HV240_Tiene_chimenea_o_campana"] = 1 if chimenea_str == "Sí" else 0

            # Expander — agua y saneamiento
            input_dict["HV225_Comparte_servicio_higienico"] = comparte_sanitario
            input_dict["HV237_Tratamiento_del_agua"] = trata_agua
            input_dict["HV237A_Tratamiento_de_agua_hervir"] = hierve_agua
            input_dict["HV237G_Agua_embotellada"] = agua_botella
            input_dict["SH42_Agua_Todo_El_Dia"] = agua_continua
            input_dict["SH48_Conserva_Agua"] = conserva_agua
            input_dict["HV204_Tiempo_de_viaje_a_fuente"] = tiempo_fuente
            input_dict["HV234_Prueba_de_yodo_para_sal"] = prueba_yodo
            input_dict["SH49_Tipo_de_envase_o_recipiente"] = tipo_recipiente
            input_dict["SH50_Lo_usa_con_tapa"] = usa_tapa

            # Expander — vivienda
            input_dict["HV242_Cuarto_separado_para_cocinar"] = cuarto_cocina
            input_dict["SH63_Utiliza_otro_tipo_de_combustible_para_cocinar"] = otro_combustible
            input_dict["SH76B_Ventanas_con_cristal"] = ventana_cristal
            input_dict["SH76C_Ventanas_de_madera"] = ventana_madera
            input_dict["SH76D_Ventanas_con_malla"] = ventana_malla
            input_dict["SH70_Fuente_Luz"] = fuente_luz
            input_dict["SH71_Numero_de_habitaciones_en_el_hogar"] = habitaciones_total
            input_dict["HV216_Habitaciones_para_dormir"] = habitaciones_dormir

            # Expander — prenatal/clínico
            input_dict["HV014_Ninos_menores_de_5_anos"] = ninos_menores5
            input_dict["HV102_Residente_habitual"] = residente_hab
            input_dict["M13_Mes_de_gestacion_en_el_1er_control"] = mes_primer_control
            input_dict["M17_Parto_por_cesarea"] = cesarea
            input_dict["M54_Vitamina_A_primeros_2_meses_post_parto"] = vitamina_a
            input_dict["M55G_Liquidos_primeros_3_dias_Formula_para_bebes"] = formula_bebe
            input_dict["M60_Tomo_antiparasitarios_en_el_embarazo"] = antiparasitarios
            input_dict["m34_Horas_hasta_inicio_de_lactancia"] = horas_lactancia

            df_input = pd.DataFrame([input_dict])
            for feat in metadata["cat_features"]:
                df_input[feat] = df_input[feat].astype("category")

            prob = model.predict_proba(df_input)[0][1]
            prob_pct = prob * 100

            # Gauge
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob_pct,
                number={"suffix": "%", "font": {"size": 40}},
                gauge={
                    "axis": {"range": [0, 100], "tickwidth": 1},
                    "bar": {"color": "#b91c1c" if prob >= threshold_used else "#15803d"},
                    "steps": [
                        {"range": [0, threshold_used * 100], "color": "#dcfce7"},
                        {"range": [threshold_used * 100, 100], "color": "#fee2e2"},
                    ],
                    "threshold": {
                        "line": {"color": "#7f1d1d", "width": 3},
                        "thickness": 0.75,
                        "value": threshold_used * 100,
                    },
                },
                title={"text": "Probabilidad estimada", "font": {"size": 13}},
            ))
            fig_gauge.update_layout(margin=dict(t=50, b=10, l=10, r=10), height=250)
            st.plotly_chart(fig_gauge, use_container_width=True)

            # Veredicto
            if prob >= threshold_used:
                st.markdown(f"""<div class="result-box" style="background-color:#fef2f2;border:2px solid #f87171;">
                    <strong style="color:#b91c1c;">ALERTA — Riesgo Alto ({prob_pct:.1f}%)</strong><br>
                    <span style="color:#7f1d1d;font-size:0.9rem;">Perfil coincide con casos históricos de desnutrición crónica. Priorizar visita domiciliaria.</span>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div class="result-box" style="background-color:#f0fdf4;border:2px solid #4ade80;">
                    <strong style="color:#15803d;">Riesgo Bajo ({prob_pct:.1f}%)</strong><br>
                    <span style="color:#166534;font-size:0.9rem;">Factores protectores suficientes. Mantener vigilancia regular.</span>
                </div>""", unsafe_allow_html=True)

            # Factores de riesgo detectados
            alertas = []
            if riqueza_map[riqueza_text] < -50000: alertas.append("Pobreza económica severa")
            if peso_nacer < 2.5:                   alertas.append(f"Bajo peso al nacer ({peso_nacer} kg)")
            if hemo < 11.0:                        alertas.append(f"Anemia (Hb {hemo:.1f} g/dL)")
            if visitas_prenatales < 6:             alertas.append(f"Controles prenatales insuficientes ({visitas_prenatales})")
            if dias_hierro < 60:                   alertas.append(f"Hierro gestacional bajo ({dias_hierro} días)")
            if altitud > 2500:                     alertas.append(f"Altitud elevada ({altitud} m)")
            if lugar_parto_str == "Domiciliario":  alertas.append("Parto domiciliario")
            if area_str == "Rural":                alertas.append("Zona rural")
            if lactancia < 3:                      alertas.append(f"Lactancia breve ({lactancia} meses)")

            if alertas:
                st.markdown("**Factores detectados:**")
                for a in alertas:
                    st.markdown(f"- {a}")
        else:
            st.info("Complete el formulario y presione **Calcular Riesgo**.")