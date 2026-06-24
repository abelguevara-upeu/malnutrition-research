# FASE 1: COMPRENSIÓN DEL NEGOCIO

---

### Diapositiva 1.1: El Problema de Política Pública

**Contenido Visual:**

**La brecha: la cobertura sanitaria no llega a todos**

- La desnutrición crónica infantil en el Perú es estructuralmente desigual: se concentra en zonas rurales, sierra y quintiles de mayor pobreza.
- Los recursos de intervención en salud pública son finitos.
- Las visitas de supervisión nutricional se ejecutan de forma reactiva o ciega — sin criterio de priorización basado en datos.

**Pregunta central de investigación:**

> ¿Puede un modelo de Machine Learning identificar, con datos de encuesta de hogar, qué niños tienen mayor riesgo de desnutrición crónica *antes* de que un agente de salud llegue al hogar?

**Guion del Expositor:**

> "Antes de hablar de cualquier algoritmo, hay que entender el problema real. La desnutrición crónica en el Perú no es un problema médico individual — es un problema estructural de asignación de recursos en salud pública. El cuello de botella no está en el diagnóstico clínico. Está en la focalización: ¿qué hogares se priorizan primero cuando el presupuesto no alcanza para todos? Esa es la pregunta que este proyecto intenta responder con Machine Learning."

---

### Diapositiva 1.2: El Objetivo Analítico — Triaje, No Diagnóstico

**Contenido Visual:**

| Enfoque Tradicional | Este Sistema |
|---|---|
| Diagnóstico clínico individual | Perfil de riesgo sociodemográfico |
| Requiere medición antropométrica directa | Opera con datos de encuesta de hogar |
| Reemplaza al profesional de salud | Orienta al tomador de decisiones |
| Maximiza Precisión | Maximiza Recall (Sensibilidad) |

**Objetivo formal:**

> Predecir el perfil de riesgo de desnutrición crónica infantil utilizando 18 años de datos de la ENDES, para orientar la focalización de recursos en salud pública.

**Métrica de éxito primaria: Recall >= 80%**

> En triaje de política pública, el costo de un falso negativo supera al de un falso positivo.

**Guion del Expositor:**

> "Este sistema no reemplaza a ningún médico ni a ninguna medición antropométrica. Su función es actuar como un radar previo: dado un perfil de hogar conocido, ¿cuál es la probabilidad de que el niño esté desnutrido? Ese radar permite priorizar qué hogares visitar primero, detectando una proporción alta de casos invirtiendo solo una fracción del presupuesto total. Y en ese contexto, la métrica que importa es el Recall — la Sensibilidad. Un niño desnutrido que el modelo no detecta es un caso que el sistema no alcanza. Ese es el error que tenemos que minimizar, no los falsos positivos."

---

### Diapositiva 1.3: Definición del Target Clínico

**Contenido Visual:**

**¿Qué es un Z-score?**

Un Z-score expresa cuántas desviaciones estándar se aleja un valor de la mediana de una población de referencia.

```
Z = 0       →  Talla exactamente en la mediana mundial (niño de referencia OMS)
Z = -1      →  1 desviación estándar por debajo
Z = -2      →  Umbral clínico de Desnutrición Crónica
Z < -3      →  Desnutrición crónica severa
```

**Estándar oficial: KPI 4 — INEI / OMS**

| Campo | Valor |
|---|---|
| Variable ENDES | `HC70` — Z-score Talla/Edad (calculado por el INEI según metodología OMS) |
| Almacenamiento SPSS crudo | `HC70 = -200` equivale a -2.0 DS (el INEI guarda el valor × 100) |
| Umbral de clasificación | `HC70 < -2.0` desviaciones estándar (post-normalización) |
| Resultado | Variable binaria de clasificación |

```python
TARGET_DESNUTRICION = (HC70 < -2.0).astype(int)
# 0 → Talla adecuada para la edad
# 1 → Desnutrición Crónica
```

**Variables descartadas por Data Leakage:**

- `HC2` Peso crudo, `HC3` Talla cruda, `HC71/72/73` Z-scores derivados — si se conoce la talla del niño, el diagnóstico es trivial.

**Guion del Expositor:**

> "Antes de hablar del umbral, hay que entender qué es un Z-score. Es simplemente una forma de medir cuán lejos está la talla de un niño respecto a la mediana de la población de referencia de la OMS, expresado en unidades de desviación estándar. Un Z-score de cero significa que el niño tiene exactamente la talla esperada. Un Z-score de -2 significa que está 2 desviaciones estándar por debajo — ese es el umbral internacional de desnutrición crónica, establecido por la OMS y adoptado formalmente por el INEI como KPI 4 del sistema de Programas Presupuestales. Un detalle técnico importante: en los archivos SPSS originales de la ENDES, este valor se almacena multiplicado por 100, entonces un -200 equivale a -2.0. Nuestro pipeline normaliza ese valor antes de cualquier procesamiento. Y tomamos una decisión crítica: descartamos el peso y la talla crudos del modelo. Si le damos al algoritmo la talla del niño, ya sabe el diagnóstico — eso no es predicción, es fuga de datos."

---

### Diapositiva 1.4: La Fuente de Datos y los Módulos Seleccionados

**Contenido Visual:**

**ENDES — Encuesta Demográfica y de Salud Familiar (INEI)**

- Cobertura: 24 departamentos, zonas urbanas y rurales, todos los estratos socioeconómicos.
- Horizonte temporal del proyecto: **2007 – 2024 (18 años)**
- Universo analizable: **294,109 niños menores de 5 años** con antropometría válida
- Formato de origen: archivos SPSS (`.sav`) con etiquetas de valor variables por año

**4 módulos ENDES seleccionados — 5 registros activos:**

| Módulo ENDES | Registros | Contenido | Rol en el Modelo |
|---|---|---|---|
| Peso y Talla - Anemia | RECH6 | Biometría infantil y hemoglobina | Target + predictor clínico (Anemia) |
| Características del Hogar | RECH0, RECH1 | Composición familiar, demografía y servicios básicos | Perfil familiar y criterios de inclusión |
| Características de la Vivienda | RECH23 | Infraestructura del hogar, altitud y entorno regional | Determinantes ambientales y socioeconómicos |
| Embarazo, Parto, Puerperio y Lactancia | REC41 | Prenatal, parto, lactancia y peso al nacer | Determinantes biológicos del primer año |

**Guion del Expositor:**

> "La ENDES es la encuesta de salud más completa del Perú y la fuente oficial del INEI. Trabajar con 18 años de datos en formato SPSS implica un desafío de ingeniería concreto: los nombres de columnas y las etiquetas de valores cambian entre ediciones de la encuesta — no se puede simplemente concatenar archivos. Fue necesario auditar registro por registro, año por año, cómo evolucionó la estructura del dato antes de poder procesarlo. De los 13 módulos disponibles en la ENDES, seleccionamos estratégicamente 4, de los cuales extrajimos 5 registros activos: RECH0 y RECH1 comparten módulo pero capturan niveles distintos — uno el hogar como unidad y otro cada miembro de forma individual. La selección cubre los cuatro determinantes clave del ecosistema materno-infantil: la biometría del niño, el entorno del hogar, el contexto territorial y la historia clínica de la madre."