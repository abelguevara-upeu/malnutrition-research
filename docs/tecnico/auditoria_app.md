# Auditoría de la aplicación frente a la ficha, la presentación y el modelo

Revisión de `app/main.py` contra lo que prometen la ficha TAM2, la presentación al panel y el modelo
entrenado (`models/champion_lightgbm.pkl`). Cada hallazgo indica dónde está, qué afirmación afecta y
qué se propone.

**Criterio:** la app debe cumplir cada aspecto que evalúa la ficha, y ningún texto de la app, la
presentación o la ficha debe prometer más de lo que la app hace.

## Estado actual (rama `develop/app-audit-fixes`)

| Hallazgo | Estado | Cómo se resolvió |
|---|:--:|---|
| 1.1 Escala de riqueza | ⚠️ mitigado | La app envía la mediana de cada quintil de riqueza de ENDES 2018–2025, la escala de los años recientes. El modelo responde de forma coherente (puntaje de 34 en el quintil 1 a 17 en el 5, con el resto sin dato). La corrección de fondo sigue pendiente: estandarizar `HV271` por año y reentrenar |
| 1.2, 1.3, 1.5 Valores que el modelo no reconocía | ✅ | Las categorías se toman de las opciones que aprendió el modelo, el yodo usa ppm y lo no respondido va como faltante |
| 1.4 Variables sin campo | ✅ | La app pide las 45. Estaban en el modelo desde el principio; la app no las pedía |
| 1.6 Educación materna e intervalo genésico (nuevo) | ✅ | `HC62` es el año aprobado dentro del nivel (0–9), no los años totales; la app lo pregunta así. En el intervalo genésico, el primer hijo se envía como faltante, como en el entrenamiento, y no como 0 |
| 2.3, 2.4 Explicación del caso concreto | ✅ | Gráfico con los 10 datos que más suben o bajan el puntaje de ese niño (valores SHAP del propio modelo) |
| 2.5 Datos faltantes | ✅ | Todo campo puede quedar en «Sin dato» |
| 2.6 Priorizar a muchos niños | ✅ | Pestaña «Evaluar un grupo»: plantilla, carga de CSV o Excel y lista ordenada descargable |
| 2.7, 3.1 Códigos ENDES | ✅ | Todas las opciones se muestran en texto (alumbrado, recipiente, yodo, sí/no) |
| 2.8 Probabilidad inflada | ⚠️ parcial | Se muestra como «puntaje de riesgo» y «prioridad alta/regular», con la aclaración de que no es una probabilidad. Calibrar el modelo sigue pendiente |
| 3.3 Completitud | ✅ | Contador «Datos ingresados: n de 45» y advertencia si falta un dato de mucho peso |
| 3.4 Mapa ambiguo | ✅ | Las etiquetas son neutras y el texto explica que el mapa indica peso, no dirección |

**Pendiente:** reentrenar con `HV271` estandarizado por año (1.1) y calibrar las probabilidades (2.8).

**Estados:** 🔴 da resultados incorrectos · 🟠 contradice lo que se promete · 🟡 usabilidad

---

## 1. La app envía al modelo datos que no reconoce

| # | Hallazgo | Dónde | Estado |
|---|---|---|:--:|
| 1.1 | **Índice de riqueza con escala mezclada.** En los datos de entrenamiento `HV271` tiene la mediana cerca de 0 (±0.00002) pero extremos de ±200,000: los años 2015–2016 quedaron sin dividir. La app envía −150,000 a 150,000, que solo corresponde a esos años. El estrato "Medio" (0) sí cae en la masa central; los demás caen en los valores extremos. Es el problema de `HV271` ya documentado, pendiente de regenerar y reentrenar | `riqueza_map`, l. 229 | 🔴 |
| 1.2 | **Categorías con tilde que el modelo no conoce.** El modelo aprendió `Si` para cocina separada (`HV242`) y otro combustible (`SH63`); la app envía `Sí`. Una categoría desconocida se trata como dato faltante, así que esas dos respuestas **se ignoran en silencio** | l. 303–304 | 🔴 |
| 1.3 | **Sal con yodo con otra escala.** El modelo se entrenó con partes por millón (0, 7, 15, 30); la app envía 0 o 1 | l. 297 | 🔴 |
| 1.4 | **Dos variables añadidas con ENDES 2025:** sexo del jefe del hogar (`HV219`) y otro tipo de transporte (`SH77F`). Ya incorporadas a los formularios | `c3`, `e2` | ✅ |
| 1.5 | **Lo que no se llena va como 0, no como faltante.** Las variables numéricas sin campo reciben 0, que el modelo interpreta como un valor real | l. 347 | 🔴 |

## 2. Contradicciones con lo que se promete

| # | Afirmación | Dónde se promete | Qué hace la app | Estado |
|---|---|---|---|:--:|
| 2.1 | Datos de 304,271 niños, ENDES 2007–2025 | PPT, metodología | El encabezado dice 285,284 niños, 2007–2024 | 🟠 |
| 2.2 | 45 variables | Metodología, solicitud | El texto dice "Top 43" | 🟠 |
| 2.3 | "Los factores que más contribuyen **en ese caso concreto**" | PPT, diapositiva 7 | La lista "Factores detectados" son 9 reglas fijas (por ejemplo, Hb < 11), no la contribución del modelo para ese niño | 🟠 |
| 2.4 | D1: "comprendo por qué asigna un nivel de riesgo a un niño concreto" | Ficha | Igual que 2.3: no hay explicación individual (SHAP) | 🟠 |
| 2.5 | "El modelo maneja datos faltantes internamente" | Texto del expander | Ningún campo puede dejarse vacío; todos traen un valor por defecto | 🟠 |
| 2.6 | U1: "priorizar qué niños atender primero" | Ficha | Solo se evalúa un niño a la vez; no hay lista ordenada | 🟠 |
| 2.8 | "Probabilidad estimada" de 45.8% | Indicador de la app | El modelo se entrenó con `class_weight='balanced'`, que infla las probabilidades: el perfil por defecto (urbano, estrato medio, 150 m) ya sale en riesgo alto. El número sirve para ordenar niños, no como probabilidad real (prevalencia nacional: 15.8%) | 🟠 |
| 2.7 | F1: "ingresar los datos es sencillo" | Ficha | 43 campos a mano, varios como códigos ENDES | 🟡 |

## 3. Usabilidad

| # | Hallazgo | Estado |
|---|---|:--:|
| 3.1 | Campos que piden códigos: "Fuente de luz (código)", "Tipo recipiente de agua (código)" y los 0/1 de cesárea, vitamina A, fórmula y antiparasitarios | 🟡 |
| 3.2 | Sin opción "No sabe"; el usuario no distingue un valor real de un valor por defecto | 🟡 |
| 3.3 | No se informa cuántos datos se usaron ni cuán confiable es el resultado cuando faltan datos clave | 🟡 |
| 3.4 | Etiquetas del mapa ambiguas: "Usa agua embotellada" o "Hierve el agua" aparecen como factores de riesgo | 🟡 |

## 4. Lo que falta

1. **Evaluación en lote.** Subir un CSV o Excel (por ejemplo, un padrón) y descargar la lista ordenada por riesgo. Es lo que responde a U1 y reduce el ingreso manual.
2. **Explicación individual.** Mostrar los factores que más suben o bajan el riesgo de ese niño con valores SHAP, en lugar de reglas fijas.
3. **Datos faltantes honestos.** Opción "No sabe" en cada campo, enviada como faltante, y un aviso del tipo "se usaron 38 de 45 datos".
4. **Calibrar o renombrar el puntaje (2.8).** Calibrar las probabilidades (por ejemplo, con regresión isotónica sobre las predicciones *out-of-fold*) o mostrarlo como "puntaje de riesgo" en vez de probabilidad.
5. **Medición de la pérdida por datos faltantes**, como se hizo con la hemoglobina, para declarar en la metodología cuánto empeora el modelo.

## 5. Orden propuesto

| Paso | Qué | Por qué primero |
|:--:|---|---|
| 1 | Corregir 1.2, 1.3, 1.5 y los textos 2.1, 2.2, 2.5 | Son errores de la app, rápidos de corregir y no requieren reentrenar |
| 2 | Regenerar datos con la corrección de `HV271` y reentrenar (1.1) | Cambia las métricas; hay que actualizar documentos |
| 3 | Opción "No sabe" y aviso de completitud (3.2, 3.3) | Hace honesto el resultado |
| 4 | Explicación individual con SHAP (2.3, 2.4) | Cumple lo prometido en la presentación y en D1 |
| 5 | Evaluación en lote (2.6) | Mayor cambio; da sentido a la focalización |

## 6. Para la demostración de hoy

- No usar el perfil por defecto como ejemplo de riesgo bajo: sale en riesgo alto. Preparar los dos perfiles de antemano.
- Decir "puntaje de riesgo" y no "probabilidad" al leer el indicador.
- Usar el estrato **"Medio"**, que es el único que no cae en valores extremos de riqueza.
- No presentar la lista "Factores detectados" como explicación del modelo; decir que son alertas clínicas de referencia.
- Si preguntan por muchos niños o por datos que no se tienen, responder que la evaluación en lote y el manejo de datos faltantes son las siguientes mejoras.
