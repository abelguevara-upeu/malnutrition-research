# FASE 6: DESPLIEGUE

---

### Diapositiva 6.1: Sistema Web de Triaje Nutricional

**Contenido Visual:**

> `[INSERTAR: captura de pantalla del Tab 1 "Mapa de Riesgo Territorial" de la app Streamlit. Mostrar el mapa coroplético de Perú con un factor de riesgo seleccionado (sugerido: "Pobreza económica extrema") y el gráfico de barras departamental a la derecha. Captura en pantalla completa, layout wide.]`

> `[INSERTAR: captura de pantalla del Tab 2 "Predictor Individual" de la app Streamlit. Mostrar el formulario de 3 columnas con valores ingresados y el panel derecho con el gauge de probabilidad y el slider de sensibilidad. Captura en pantalla completa, layout wide.]`

**Características del sistema desplegado:**

| Componente | Descripción |
|---|---|
| Stack | Python · Streamlit · Plotly · LightGBM |
| Tab 1 | Mapa coroplético interactivo por los 25 departamentos del Perú — SHAP geográfico normalizado |
| Tab 2 | Predictor individual: 17 variables principales + 26 complementarias — resultado en tiempo real |
| Umbral adaptable | El operador define el % de detección objetivo → el sistema calcula el umbral automáticamente |
| Tiempo de respuesta | < 1 segundo por predicción |
| Modelo en producción | LightGBM · Top 43 variables · 285,284 niños de entrenamiento · ENDES 2007–2024 |

**Guion del Expositor:**

> "El modelo no quedó en un notebook. Lo desplegamos como una aplicación web operativa con dos módulos. El primer módulo es el mapa de riesgo territorial: un tomador de decisiones a nivel regional puede seleccionar cualquiera de los 43 factores de riesgo del modelo y ver inmediatamente qué departamentos están más afectados por ese factor específico — no como una estadística general, sino como el impacto real que ese factor tiene sobre las predicciones del modelo. El segundo módulo es el predictor individual: dado el perfil de un niño —socioeconómico, biológico, materno— el sistema calcula en menos de un segundo la probabilidad de desnutrición crónica. Y hay un detalle que cambia completamente cómo se usa este sistema: el operador no ajusta un umbral técnico. Le dice al sistema cuántos niños desnutridos quiere detectar — por ejemplo el 80% — y el sistema encuentra automáticamente el punto de corte que logra esa cobertura, mostrando el costo en términos de visitas preventivas adicionales. Eso convierte una decisión técnica de Machine Learning en una decisión de política pública que cualquier gestor puede tomar."
