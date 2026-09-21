::: slide
# Sistema Predictivo de Riesgo de Desnutrición Crónica Infantil

### Una herramienta de apoyo a la focalización en salud pública

**Universidad Peruana Unión** — EP Ingeniería de Sistemas\
Abel Guevara Huasco · Verónica Vergara Rojas · Pamela Vallejos Cotrina\
Asesor: Mg. Nemias Saboya Rios

*Sesión de validación con panel de especialistas · 23 de septiembre de 2026*
:::

::: slide
## 1. El problema

En el Perú, **1 de cada 6 niños** menores de cinco años presenta desnutrición crónica.
No se distribuye de forma pareja: se concentra en zonas rurales, en la sierra y en los hogares
más pobres.

**El cuello de botella no es el diagnóstico. Es la focalización.**

> Cuando el presupuesto no alcanza para visitar a todos los hogares,
> ¿a cuáles se llega primero?

Hoy esa decisión se toma con criterios generales de territorio. La pregunta que motiva este trabajo es
si los datos que el Estado ya recoge permiten priorizar mejor.
:::

::: slide
## 2. Qué hace el sistema

Estima la **probabilidad de que un niño presente desnutrición crónica** a partir del perfil de su hogar
y de la historia materna, **sin medir al niño**.

| | |
|---|---|
| **Entrega** | Un nivel de riesgo por niño y un mapa de factores predominantes por departamento |
| **Requiere** | Datos de encuesta: condiciones de la vivienda, agua y saneamiento, historia del embarazo y parto |
| **No requiere** | Peso ni talla actuales del niño |

**Por qué no usa peso ni talla:** esas dos mediciones *definen* el diagnóstico. Si el sistema las
conociera, no estaría prediciendo nada. El modelo aprende de las señales que rodean al problema, no de
su resultado.

*La única variable que exige laboratorio es la hemoglobina, habitualmente disponible en el tamizaje de
anemia de los controles CRED.*
:::

::: slide
## 3. Con qué datos se construyó

**ENDES** — Encuesta Demográfica y de Salud Familiar del INEI. Datos públicos.

| | |
|---|---|
| Periodo | **2007 – 2025** (19 años) |
| Niños analizados | **304,271** menores de 5 años con antropometría válida |
| Casos con desnutrición crónica | 48,094 (15.8%) |
| Variables utilizadas | **45**, seleccionadas estadísticamente entre más de 180 |
| Criterio diagnóstico | Talla para la edad < −2 DE (estándar OMS, KPI 4 del INEI) |

**Los factores más determinantes según el modelo:**

1. Índice de riqueza del hogar
2. Peso al nacer
3. Altitud de residencia
4. Edad del niño en meses
5. Hemoglobina ajustada por altitud
:::

::: slide
## 4. Qué tan bien funciona

| Métrica | Valor | Qué significa en la práctica |
|---|:---:|---|
| Discriminación | **0.83** | Entre un niño con desnutrición y otro sin ella, el sistema asigna mayor riesgo al primero en **83 de cada 100 casos** |
| Cobertura | **76%** | De cada 100 niños que sí tienen desnutrición crónica, el sistema señala a **76** |
| No detectados | 24% | **24 de cada 100** pasarían inadvertidos con el punto de corte actual |
| Confirmación | 36% | De cada 100 niños señalados, **36 lo confirman**; el resto requiere verificación |

**El punto de corte es ajustable.** Puede elevarse la cobertura por encima del 80%, a costa de más
alertas que no se confirman. Se priorizó la cobertura de forma deliberada: no detectar a un niño
afectado es más costoso que una visita de verificación innecesaria.

*Estimaciones verificadas con 1,000 remuestreos; el margen de error es inferior a medio punto.*
:::

::: slide
## 5. Qué **no** hace el sistema

| No es | Sí es |
|---|---|
| Un diagnóstico clínico | Una estimación de probabilidad |
| Un reemplazo del profesional de salud | Un apoyo para decidir a quién evaluar primero |
| Una certeza sobre un niño concreto | Una orientación sobre dónde concentrar recursos |

**Un niño señalado como riesgo alto no está diagnosticado.** Está priorizado para evaluación.
La confirmación sigue siendo clínica y corresponde al profesional.

El sistema se encuentra en **versión preliminar** y esta sesión busca precisamente identificar sus
limitaciones antes de cualquier uso real.
:::

::: slide
## 6. Demostración

**A. Mapa de riesgo territorial**
Cómo cambian los factores predominantes según el departamento: lo que pesa en Puno no es lo mismo que
pesa en Ica.

**B. Predictor individual**
Ingreso de un perfil y estimación del nivel de riesgo, con los factores que más contribuyen en ese
caso concreto.

---

### Qué les pedimos

Tras la demostración, completar una **ficha de validación** de unos 10 minutos sobre:

- La **utilidad** de la herramienta para el trabajo en salud pública
- Su **facilidad de uso** e interpretación
- Las **variables o información** que consideran que falta
- Las **limitaciones** que identifican desde su experiencia

Su valoración se incorporará al artículo de investigación y orientará la siguiente versión del sistema.
:::

::: slide
## Gracias

**Equipo de investigación**

Abel Guevara Huasco · abelguevara@upeu.edu.pe\
Verónica Vergara Rojas · veronica.vergara@upeu.edu.pe\
Pamela Vallejos Cotrina · zulin.vallejos@upeu.edu.pe

EP Ingeniería de Sistemas — Universidad Peruana Unión\
Asesor: Mg. Nemias Saboya Rios

*Agradecemos el tiempo y la experiencia que aportan a esta validación.*
:::
