# Fundamento del instrumento de validación (TAM2)

Nota para el asesor. Justifica la versión del Modelo de Aceptación Tecnológica adoptada en la ficha
de validación y cómo se analizarán las respuestas.

---

## 1. Qué versión se adoptó y por qué

La elección se hizo aplicando el marco de decisión de Britto (2026), que compara TAM, TAM2, TAM3,
UTAUT y UTAUT2 en cinco dimensiones:

| Dimensión | Este estudio | Modelo que corresponde |
|---|---|---|---|
| D1. Contexto de aplicación | Organizacional: la herramienta apoya tareas del personal de salud | TAM2, TAM3, UTAUT |
| D2. Régimen de uso | Voluntario: es una propuesta, no un sistema impuesto | TAM2 |
| D3. Etapa de adopción | **Aceptación inicial**: primera exposición, antes de cualquier despliegue | TAM, **TAM2** |
| D4. Foco explicativo | Utilidad ampliada por factores del trabajo (relevancia, calidad y demostrabilidad del resultado) | **TAM2** |
| D5. Granularidad | **Intermedia**: un panel de seis especialistas no sostiene un modelo de alta complejidad | **TAM2** |

**Se adopta TAM2** (Venkatesh y Davis, 2000), que coincide con el estudio en las cinco dimensiones.

Se descartan las demás por motivos concretos:

- **TAM** (Davis, 1989): se queda corto; mide utilidad y facilidad de uso, pero no por qué la
  herramienta resulta útil, que es lo que interesa preguntar a un panel clínico.
- **TAM3** (Venkatesh y Bala, 2008): orientado a cómo cambian las percepciones con la experiencia de
  uso a lo largo del tiempo, y de granularidad alta. Lo que añade sobre TAM2 son antecedentes de la
  facilidad de uso (autoeficacia, ansiedad, disfrute) que no aplican a una evaluación tras una única
  demostración. Se toma de él un solo constructo: la **percepción de control externo**, para preguntar
  si los datos que pide el sistema están disponibles en la práctica.
- **UTAUT y UTAUT2**: granularidad alta; UTAUT2 además está pensado para consumo individual.
- **TAM Plus** y **TAM 5**, sugeridos por la búsqueda en LeapSpace: el primero es la denominación que
  un meta-análisis da al TAM extendido y no define un instrumento; el segundo mide desarrollo ágil y
  trabajo híbrido en la industria de software, fuera del dominio.
- **TAM3 + Warm-Glow**: añade el bienestar emocional de "hacer el bien" como antecedente de la
  utilidad percibida; pensado para tecnología de consumo/filantropía, no para personal clínico
  evaluando una herramienta de trabajo.
- **TAM3 en contextos educativos** (meta-análisis con 12 estudios, n=3874): encuentra que TAM3 puede
  no ajustar bien fuera de su dominio organizacional original, lo que refuerza no forzarlo aquí.

Matemba et al. (2020), tras revisar 166 estudios sobre TAM, plantean como hipótesis que el estado de
salud modera la fuerza de las relaciones entre sus constructos. No se aplica un modelo distinto por
eso, pero sí respalda **adaptar los enunciados al contexto sanitario** en vez de traducir los ítems
originales de forma literal.

## 2. Correspondencia entre constructos e ítems

| Constructo | Origen | Sección | Ítems |
|---|---|---|
| Relevancia para el trabajo (*job relevance*) | TAM2 | III | R1–R3 |
| Calidad del resultado (*output quality*) | TAM2 | IV | C1–C3 |
| Demostrabilidad del resultado (*result demonstrability*) | TAM2 | V | D1–D2 |
| Utilidad percibida (*perceived usefulness*) | TAM | VI | U1–U4 |
| Facilidad de uso percibida (*perceived ease of use*) | TAM | VII | F1–F4 |
| Percepción de control externo (*perceptions of external control*) | TAM3 | VIII | K1–K3 |
| Norma subjetiva (*subjective norm*) | TAM2 | IX | S1–S2 |
| Intención de uso (*behavioral intention*) | TAM | X | I1–I3 |

**24 ítems** en escala de 1 a 5, más una valoración global de 1 a 10 y cuatro preguntas abiertas.

De TAM2 se omiten **imagen** (el prestigio que da usar la herramienta) y **voluntariedad**, que no
aplican a una evaluación por expertos que no serán usuarios obligados del sistema.

El ítem **K2** pregunta de forma expresa por la disponibilidad del dato de hemoglobina, la única de
las 45 variables del modelo que exige un procedimiento sobre el niño. Sus respuestas contrastan la
medición que muestra que el modelo pierde poco sin ella (`docs/docs/hallazgos_validacion.md`, §1).

## 3. Cómo se analizarán las respuestas

TAM2 es un modelo estructural: en su formulación original se valida estimando las relaciones entre
constructos con cientos de respuestas. **Con un panel de seis especialistas esa estimación no es
posible ni se pretende.** Los constructos se usan como **dimensiones de evaluación**, y el análisis es
descriptivo:

- Mediana y rango intercuartílico por dimensión, que son los estadísticos adecuados para una escala
  ordinal con pocos evaluadores.
- Porcentaje de acuerdo por ítem (respuestas 4 y 5).
- Análisis de contenido de las preguntas abiertas, agrupando las variables faltantes y las
  limitaciones señaladas.

Se considerará una dimensión **favorablemente valorada** cuando su mediana sea igual o superior a 4.

## 4. Dónde están los ítems originales

Los enunciados de la ficha son adaptaciones al contexto sanitario. Los ítems originales, en inglés,
están en los propios artículos fuente:

- **TAM2**: Venkatesh y Davis (2000), *Management Science*, 46(2), 186–204.
  DOI 10.1287/mnsc.46.2.186.11926
- **Percepción de control externo (TAM3)**: Venkatesh y Bala (2008), *Decision Sciences*, 39(2),
  273–315. DOI 10.1111/j.1540-5915.2008.00192.x

Ambos son de pago; se acceden desde las bases suscritas por la biblioteca de la UPeU (INFORMS y Wiley)
o desde la copia que los autores suelen subir a ResearchGate.

Conviene cotejar cada ítem adaptado con su original y, si existe, preferir una **versión en español ya
validada** en población sanitaria. Búsqueda sugerida en LeapSpace/Scopus:

> *Spanish validated questionnaire Technology Acceptance Model 2 health professionals clinical
> decision support. Matrix with: authors, year, country, sample, constructs, reliability
> (Cronbach's alpha).*
