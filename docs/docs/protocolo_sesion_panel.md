# Protocolo de la sesión con el panel de especialistas

Guía interna del equipo para conducir la sesión de validación de pertinencia (tercer eje de la
metodología). Fija el orden, los tiempos y las reglas que aseguran que las respuestas del panel sean
comparables entre sí.

**Fecha:** miércoles 23 de septiembre de 2026, 7:45 p. m. · **Duración prevista:** 60 minutos
**Participantes:** cinco especialistas (dos nutricionistas, un médico y dos enfermeros), el equipo de
investigación y, si asiste, el docente asesor.

---

## 1. Antes de la sesión

| Tarea | Responsable | Hecho |
|---|---|:--:|
| Probar el enlace de la videollamada y compartir pantalla | | ☐ |
| Levantar la aplicación (`streamlit run app/main.py`) y probar un perfil completo | | ☐ |
| Abrir la presentación en PDF (`presentacion_panel_expertos.pdf`) | | ☐ |
| Tener a mano el enlace del formulario de Google y el PDF de la ficha como respaldo | | ☐ |
| Enviar el consentimiento informado (o confirmar que está en el formulario) | | ☐ |
| Preparar dos perfiles de ejemplo para la demostración: uno de riesgo alto y uno de riesgo bajo | | ☐ |
| Definir quién toma notas de las preguntas y comentarios | | ☐ |

## 2. Roles

| Rol | Tarea | Responsable |
|---|---|---|
| Moderación | Abre, controla los tiempos y conduce la ronda de preguntas | |
| Exposición | Presenta las diapositivas | |
| Demostración | Opera la aplicación en pantalla compartida | |
| Registro | Anota preguntas, dudas y comentarios literales del panel | |

Una misma persona puede cubrir dos roles, salvo **registro**, que debe estar libre para anotar.

## 3. Desarrollo

| Min. | Bloque | Qué se hace | Material |
|:--:|---|---|---|
| 0–5 | Bienvenida | Presentación del equipo y del objetivo de la sesión. Lectura breve del consentimiento y consulta sobre la grabación | Consentimiento |
| 5–20 | Exposición | Diapositivas 1 a 6: problema, qué hace el sistema, datos, lo que aprendió el modelo, desempeño y límites | Presentación |
| 20–32 | Demostración | Mapa de riesgo territorial y predictor individual con los dos perfiles de ejemplo | Aplicación |
| 32–45 | Preguntas | Ronda abierta de aclaraciones. Se responde qué hace el sistema, no se opina sobre qué tan bueno es | — |
| 45–57 | Ficha | Envío del enlace por el chat. El equipo permanece conectado para resolver dudas de llenado | Formulario |
| 57–60 | Cierre | Agradecimiento y aviso de cómo se usarán los resultados | — |

## 4. Reglas para no sesgar las respuestas

- **No anticipar la valoración.** Evitar frases como "es muy útil" o "es fácil de usar". Describir lo
  que hace el sistema y dejar que el panel juzgue.
- **Responder dudas, no argumentar.** Si un especialista objeta una limitación, se anota tal cual y
  no se discute; es un dato para las preguntas abiertas.
- **Mismas explicaciones para todos.** Si surge una aclaración importante durante la ficha, se
  comparte con todo el panel, no solo con quien preguntó.
- **Hemoglobina.** Si preguntan, informar lo medido: sin ese dato el modelo pasa de un AUC de 0.8295 a
  0.8281 y la sensibilidad de 76.44% a 76.30%. No sugerir cómo responder el ítem K2.
- **Tiempo de la ficha.** No presionar; si alguien no termina en la sesión, puede completarla después
  con el mismo enlace.

## 5. Preguntas previsibles y respuesta sugerida

| Pregunta | Respuesta |
|---|---|
| ¿El sistema diagnostica desnutrición? | No. Estima el riesgo para priorizar a quién evaluar primero; el diagnóstico sigue siendo antropométrico y clínico |
| ¿De dónde salen los datos? | De la ENDES (INEI), 2007–2025: 304,271 registros de niños menores de cinco años |
| ¿Qué tan confiable es? | AUC-ROC de 0.83 con intervalo de confianza al 95% de [0.827, 0.832]. Con el umbral de triaje identifica a ocho de cada diez niños con desnutrición crónica |
| ¿Por qué pide peso o talla si no mide al niño? | Aclarar qué variables son del hogar y la madre, y cuáles requieren medir al niño (solo la hemoglobina exige un procedimiento) |
| ¿Se puede usar ya en un establecimiento? | Es una propuesta académica; su valoración sirve precisamente para decidir qué falta antes de una prueba piloto |

## 6. Después de la sesión

- Pasar en limpio las notas de registro el mismo día, separando preguntas, objeciones y sugerencias.
- Verificar en la hoja de respuestas que hay cinco filas completas y borrar las filas de prueba.
- Descargar la hoja como CSV para el análisis: mediana y rango intercuartílico por constructo,
  porcentaje de acuerdo por ítem y análisis de contenido de las preguntas abiertas.
- Enviar un mensaje de agradecimiento a cada especialista.
