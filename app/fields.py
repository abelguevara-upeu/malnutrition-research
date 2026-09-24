"""Definición única de los 45 campos del modelo.

El formulario individual y la carga en lote traducen las respuestas al modelo
a través de esta tabla, de modo que ambos envían exactamente los mismos valores
y en la misma escala con que se entrenó `champion_lightgbm.pkl`.
"""
import math

import numpy as np
import pandas as pd

# Medianas de cada quintil de HV271 en ENDES 2018-2025. El índice de riqueza
# quedó en escalas distintas según el año de la encuesta; se usa la escala de
# los años recientes, que es la que corresponde a un niño evaluado hoy.
WEALTH_QUINTILES = [
    ("Quintil 1 (más pobre)", -1.23084311e-05),
    ("Quintil 2", -5.61556531e-06),
    ("Quintil 3 (medio)", 7.38259882e-07),
    ("Quintil 4", 6.76427840e-06),
    ("Quintil 5 (más rico)", 1.38836538e-05),
]

SI_NO = [("Sí", 1), ("No", 0)]


def _si(level):
    """Opciones Sí/No para una categoría cuyo nivel afirmativo es `level` ('Si' o 'Sí')."""
    return [("Sí", level), ("No", "No")]


# kind: "num" (número libre) · "opt" (opciones con valor numérico) · "cat" (categoría del modelo)
FIELDS = [
    # ── Niño ──
    dict(key="sexo", feature="HC27_Sexo", label="Sexo del niño", kind="cat",
         options=[("Masculino", "Hombre"), ("Femenino", "Mujer")], group="Niño"),
    dict(key="edad", feature="HC1_Edad_en_meses", label="Edad (meses)", kind="num",
         min=0, max=59, step=1, group="Niño", help="El riesgo es mayor entre los 6 y 20 meses."),
    dict(key="peso_nacer", feature="m19_Peso_al_nacer_kg", label="Peso al nacer (kg)", kind="num",
         min=0.5, max=6.0, step=0.1, group="Niño", help="Menos de 2.5 kg es bajo peso al nacer."),
    dict(key="tamano_nacer", feature="M18_Tamano_al_nacer", label="Tamaño al nacer (según la madre)", kind="opt",
         options=[("Muy grande", 1), ("Grande", 2), ("Mediano (normal)", 3), ("Pequeño", 4), ("Muy pequeño", 5)],
         group="Niño", help="Percepción de la madre, tal como la registra la ENDES. No es una medición."),
    dict(key="hemoglobina", feature="HC56_Nivel_de_hemoglobina_ajustado_por_altitud",
         label="Hemoglobina ajustada por altitud (g/dL)", kind="num", min=4.0, max=20.0, step=0.1,
         group="Niño", help="Normal en niños de 6 a 59 meses: 11.0 g/dL o más."),
    dict(key="intervalo", feature="HC63_Intervalo_de_nacimientos_anteriores_al_nino",
         label="Meses desde el nacimiento del hermano anterior", kind="num", min=7, max=400, step=1,
         group="Niño", help="Déjelo vacío si es el primer hijo."),
    dict(key="residente", feature="HV102_Residente_habitual", label="¿Reside habitualmente en el hogar?",
         kind="cat", options=_si("Sí"), group="Niño"),
    # ── Madre, embarazo y parto ──
    dict(key="educ_madre", feature="HC62_Ano_mas_alto_de_educacion_de_la_madre",
         label="Último año aprobado por la madre en su nivel más alto", kind="num", min=0, max=9, step=1,
         group="Madre", help="Como lo registra la ENDES: el año dentro del nivel. "
                             "Ej.: secundaria completa = 5; primaria completa = 6."),
    dict(key="visitas_prenatales", feature="M14_Numero_de_visitas_prenatales", label="Controles prenatales",
         kind="num", min=0, max=20, step=1, group="Madre", help="La OMS recomienda al menos 8."),
    dict(key="mes_primer_control", feature="M13_Mes_de_gestacion_en_el_1er_control",
         label="Mes de gestación del primer control", kind="num", min=0, max=9, step=1, group="Madre"),
    dict(key="dias_hierro", feature="M46_Dias_que_tomo_hierro", label="Días que tomó hierro en el embarazo",
         kind="num", min=0, max=364, step=1, group="Madre"),
    dict(key="antiparasitarios", feature="M60_Tomo_antiparasitarios_en_el_embarazo",
         label="¿Tomó antiparasitarios en el embarazo?", kind="opt", options=SI_NO, group="Madre"),
    dict(key="lugar_parto", feature="m15_Lugar_del_parto_agrupado", label="Lugar del parto", kind="cat",
         options=[("Establecimiento de salud", "Institucional"), ("Domicilio", "Domiciliario")], group="Madre"),
    dict(key="cesarea", feature="M17_Parto_por_cesarea", label="¿Parto por cesárea?", kind="opt",
         options=SI_NO, group="Madre"),
    dict(key="vitamina_a", feature="M54_Vitamina_A_primeros_2_meses_post_parto",
         label="¿Recibió vitamina A en los 2 meses después del parto?", kind="opt", options=SI_NO, group="Madre"),
    dict(key="horas_lactancia", feature="m34_Horas_hasta_inicio_de_lactancia",
         label="Horas hasta el inicio de la lactancia", kind="num", min=0, max=2400, step=1,
         group="Madre", help="0 si fue inmediatamente después del parto."),
    dict(key="formula", feature="M55G_Liquidos_primeros_3_dias_Formula_para_bebes",
         label="¿Recibió fórmula en los primeros 3 días?", kind="opt", options=SI_NO, group="Madre"),
    dict(key="lactancia", feature="M4_Duracion_de_la_lactancia", label="Duración de la lactancia (meses)",
         kind="num", min=0, max=59, step=1, group="Madre"),
    # ── Hogar y territorio ──
    dict(key="riqueza", feature="HV271_Factor_de_puntuacion_del_indice_de_riqueza",
         label="Nivel socioeconómico del hogar", kind="opt", options=WEALTH_QUINTILES, group="Hogar",
         help="Quintil de riqueza de la ENDES, calculado con los bienes y servicios de la vivienda."),
    dict(key="area", feature="HV025_Area_de_residencia", label="Área de residencia", kind="cat",
         options=[("Urbana", "Urbano"), ("Rural", "Rural")], group="Hogar"),
    dict(key="altitud", feature="HV040_Altitud_del_conglomerado_en_metros", label="Altitud (m s. n. m.)",
         kind="num", min=0, max=5100, step=10, group="Hogar"),
    dict(key="miembros", feature="HV012_Miembros_habituales_De_jure", label="Personas que viven en el hogar",
         kind="num", min=1, max=30, step=1, group="Hogar"),
    dict(key="ninos_menores5", feature="HV014_Ninos_menores_de_5_anos", label="Niños menores de 5 años en el hogar",
         kind="num", min=0, max=10, step=1, group="Hogar"),
    dict(key="edad_jefe", feature="HV220_Edad_del_jefe_del_hogar", label="Edad del jefe del hogar",
         kind="num", min=12, max=99, step=1, group="Hogar"),
    dict(key="sexo_jefe", feature="HV219_Sexo_del_jefe_del_hogar", label="Sexo del jefe del hogar", kind="cat",
         options=[("Masculino", "Masculino"), ("Femenino", "Femenino")], group="Hogar"),
    dict(key="transporte_rural", feature="SH77F_Otro_tipo_de_transporte_caballos_peque_peque_etc",
         label="¿El hogar usa caballo o peque-peque como transporte?", kind="cat",
         options=_si("Si"), group="Hogar"),
    # ── Agua y saneamiento ──
    dict(key="agua_continua", feature="SH42_Agua_Todo_El_Dia", label="¿Tiene agua para beber todo el día?",
         kind="cat", options=_si("Sí"), group="Agua"),
    dict(key="tiempo_fuente", feature="HV204_Tiempo_de_viaje_a_fuente",
         label="Minutos para ir por agua y volver", kind="num", min=0, max=600, step=1, group="Agua",
         help="0 si el agua está en la vivienda."),
    dict(key="trata_agua", feature="HV237_Tratamiento_del_agua", label="¿Trata el agua antes de beberla?",
         kind="cat", options=_si("Si"), group="Agua"),
    dict(key="hierve_agua", feature="HV237A_Tratamiento_de_agua_hervir", label="¿Hierve el agua?", kind="cat",
         options=_si("Si"), group="Agua"),
    dict(key="agua_botella", feature="HV237G_Agua_embotellada", label="¿Toma agua embotellada?", kind="cat",
         options=_si("Si"), group="Agua"),
    dict(key="conserva_agua", feature="SH48_Conserva_Agua", label="¿Guarda el agua para beber en un recipiente?",
         kind="cat", options=_si("Sí"), group="Agua"),
    dict(key="recipiente", feature="SH49_Tipo_de_envase_o_recipiente", label="Tipo de recipiente", kind="opt",
         options=[("Olla o tetera", 1), ("Balde", 2), ("Jarra", 3), ("Bidón", 4), ("Otro", 96)], group="Agua"),
    dict(key="tapa", feature="SH50_Lo_usa_con_tapa", label="¿El recipiente tiene tapa?", kind="opt",
         options=SI_NO, group="Agua"),
    dict(key="comparte_bano", feature="HV225_Comparte_servicio_higienico", label="¿Comparte el servicio higiénico?",
         kind="cat", options=_si("Si"), group="Agua"),
    dict(key="yodo", feature="HV234_Prueba_de_yodo_para_sal", label="Yodo en la sal (resultado del kit)",
         kind="opt", options=[("0 ppm (sin yodo)", 0), ("7 ppm", 7), ("15 ppm", 15), ("30 ppm", 30),
                              ("No se hizo la prueba", 994), ("No hay sal en el hogar", 995)], group="Agua"),
    # ── Vivienda ──
    dict(key="habitaciones", feature="SH71_Numero_de_habitaciones_en_el_hogar", label="Habitaciones en total",
         kind="num", min=1, max=15, step=1, group="Vivienda"),
    dict(key="dormitorios", feature="HV216_Habitaciones_para_dormir", label="Habitaciones para dormir",
         kind="num", min=0, max=10, step=1, group="Vivienda"),
    dict(key="alumbrado", feature="SH70_Fuente_Luz", label="Alumbrado del hogar", kind="opt",
         options=[("Electricidad", 1), ("GLP", 2), ("Gas natural", 3), ("Kerosene", 4), ("Velas", 5),
                  ("Batería", 6), ("Otro", 96)], group="Vivienda"),
    dict(key="chimenea", feature="HV240_Tiene_chimenea_o_campana", label="Salida de humo de la cocina", kind="opt",
         options=[("Ni chimenea ni campana", 0), ("Chimenea", 1), ("Campana", 2)], group="Vivienda"),
    dict(key="cocina_separada", feature="HV242_Cuarto_separado_para_cocinar", label="¿Cocina en un cuarto separado?",
         kind="cat", options=_si("Si"), group="Vivienda"),
    dict(key="otro_combustible", feature="SH63_Utiliza_otro_tipo_de_combustible_para_cocinar",
         label="¿Usa otro combustible para cocinar?", kind="cat", options=_si("Si"), group="Vivienda"),
    dict(key="ventana_cristal", feature="SH76B_Ventanas_con_cristal", label="¿Ventanas con vidrio?", kind="cat",
         options=_si("Si"), group="Vivienda"),
    dict(key="ventana_madera", feature="SH76C_Ventanas_de_madera", label="¿Ventanas de madera?", kind="cat",
         options=_si("Si"), group="Vivienda"),
    dict(key="ventana_malla", feature="SH76D_Ventanas_con_malla", label="¿Ventanas con malla?", kind="cat",
         options=_si("Si"), group="Vivienda"),
]

GROUPS = {
    "Niño": "Datos del niño",
    "Madre": "Embarazo, parto y lactancia",
    "Hogar": "Hogar y territorio",
    "Agua": "Agua y saneamiento",
    "Vivienda": "Vivienda",
}

BY_KEY = {f["key"]: f for f in FIELDS}
BY_FEATURE = {f["feature"]: f for f in FIELDS}
LABEL_BY_FEATURE = {f["feature"]: f["label"] for f in FIELDS}

# Datos con mayor peso en el modelo (importancia SHAP global). Si faltan, el
# resultado es menos confiable y la app lo advierte.
KEY_FIELDS = ["riqueza", "peso_nacer", "altitud", "edad", "hemoglobina"]


def is_missing(v):
    return v is None or (isinstance(v, float) and math.isnan(v)) or (isinstance(v, str) and v.strip() == "")


def label_to_value(field, label):
    """Traduce la etiqueta visible de una opción al valor del modelo; None si no la reconoce."""
    for lab, val in field["options"]:
        if str(label).strip().lower() == lab.lower():
            return val
    return None


def value_to_label(field, value):
    if is_missing(value):
        return "Sin dato"
    if field["kind"] == "num":
        return f"{value:g}"
    for lab, val in field["options"]:
        if val == value:
            return lab
    return str(value)


def build_model_frame(answers, model_features, categories):
    """answers: lista de dicts {feature: valor del modelo o None}. Devuelve el DataFrame que espera el modelo."""
    rows = [{f: (np.nan if is_missing(a.get(f)) else a.get(f)) for f in model_features} for a in answers]
    X = pd.DataFrame(rows, columns=model_features)
    for feat, levels in categories.items():
        X[feat] = pd.Categorical(X[feat].where(X[feat].notna(), None), categories=levels)
    for feat in model_features:
        if feat not in categories:
            X[feat] = pd.to_numeric(X[feat], errors="coerce").astype(float)
    return X


# Perfiles de ejemplo para la demostración y la plantilla de carga en lote.
EXAMPLES = {
    "alto": dict(sexo="Masculino", edad=18, peso_nacer=2.4, tamano_nacer="Pequeño", hemoglobina=9.6,
                 intervalo=18, residente="Sí", educ_madre=3, visitas_prenatales=4, mes_primer_control=5,
                 dias_hierro=20, antiparasitarios="No", lugar_parto="Domicilio", cesarea="No", vitamina_a="No",
                 horas_lactancia=3, formula="No", lactancia=17, riqueza="Quintil 1 (más pobre)", area="Rural",
                 altitud=3850, miembros=7, ninos_menores5=3, edad_jefe=29, sexo_jefe="Masculino",
                 agua_continua="No", tiempo_fuente=25, trata_agua="No", hierve_agua="No", agua_botella="No",
                 comparte_bano="Sí", yodo="No se hizo la prueba", habitaciones=2, dormitorios=1,
                 alumbrado="Electricidad", chimenea="Ni chimenea ni campana", cocina_separada="No",
                 otro_combustible="Sí", ventana_cristal="No", ventana_madera="Sí", ventana_malla="No"),
    "bajo": dict(sexo="Femenino", edad=40, peso_nacer=3.4, tamano_nacer="Mediano (normal)", hemoglobina=12.4,
                 residente="Sí", educ_madre=5, visitas_prenatales=10, mes_primer_control=2, dias_hierro=180,
                 antiparasitarios="No", lugar_parto="Establecimiento de salud", cesarea="No", vitamina_a="Sí",
                 horas_lactancia=1, formula="No", lactancia=14, riqueza="Quintil 5 (más rico)", area="Urbana",
                 altitud=150, miembros=4, ninos_menores5=1, edad_jefe=38, sexo_jefe="Masculino",
                 agua_continua="Sí", tiempo_fuente=0, trata_agua="Sí", hierve_agua="Sí", agua_botella="No",
                 comparte_bano="No", yodo="30 ppm", habitaciones=5, dormitorios=3, alumbrado="Electricidad",
                 chimenea="Ni chimenea ni campana", cocina_separada="Sí", otro_combustible="No",
                 ventana_cristal="Sí", ventana_madera="No", ventana_malla="No"),
}


TEMPLATE_COLUMNS = ["id"] + [f["label"] for f in FIELDS]


def template_frame():
    rows = []
    for name, ex in EXAMPLES.items():
        row = {"id": f"EJEMPLO-{name.upper()}"}
        row.update({f["label"]: ex.get(f["key"], "") for f in FIELDS})
        rows.append(row)
    return pd.DataFrame(rows, columns=TEMPLATE_COLUMNS)


def parse_upload(df):
    """Traduce cada fila del archivo a respuestas del modelo. Devuelve respuestas y valores no reconocidos."""
    by_header = {}
    for f in FIELDS:
        by_header[f["label"].strip().lower()] = f
        by_header[f["key"].lower()] = f
    matched = {c: by_header[str(c).strip().lower()] for c in df.columns if str(c).strip().lower() in by_header}
    answers, problems = [], {}
    for _, row in df.iterrows():
        answer = {f["feature"]: None for f in FIELDS}
        for col, f in matched.items():
            raw = row[col]
            if is_missing(raw) or (isinstance(raw, str) and raw.strip().lower() == "sin dato"):
                continue
            if f["kind"] == "num":
                val = pd.to_numeric(str(raw).replace(",", "."), errors="coerce")
                ok = not pd.isna(val) and f["min"] <= val <= f["max"]
                val = float(val) if ok else None
            else:
                val = label_to_value(f, raw)
                ok = val is not None
            if ok:
                answer[f["feature"]] = val
            else:
                problems.setdefault(f["label"], set()).add(str(raw))
        answers.append(answer)
    return answers, matched, problems


def read_table(data, filename):
    """Lee el archivo subido. Excel en español guarda los CSV con punto y coma: el separador se toma de la cabecera."""
    import io
    if filename.lower().endswith(".xlsx"):
        return pd.read_excel(io.BytesIO(data))
    text = data.decode("utf-8-sig", errors="replace")
    header = text.splitlines()[0] if text else ""
    sep = ";" if header.count(";") > header.count(",") else ","
    return pd.read_csv(io.StringIO(text), sep=sep)
