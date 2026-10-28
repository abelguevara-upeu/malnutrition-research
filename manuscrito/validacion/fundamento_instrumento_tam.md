# Fundamento del instrumento de validación (TAM2)

Nota para el asesor. Justifica la versión del Modelo de Aceptación Tecnológica adoptada en la ficha
de validación y cómo se analizarán las respuestas.

---

## 1. Qué versión se adoptó y por qué

La elección se hizo aplicando el marco de decisión de Britto (2026), que compara TAM, TAM2, TAM3,
UTAUT y UTAUT2 en cinco dimensiones:

| Dimensión | Este estudio | Modelo que corresponde |
|---|---------------------------------------------------------------------|---|
| D1. Contexto de aplicación | Organizacional: la herramienta apoya tareas del personal de salud | TAM2, TAM3, UTAUT |
| D2. Régimen de uso | Voluntario: es una propuesta, no un sistema impuesto | TAM2 |
| D3. Etapa de adopción | **Aceptación inicial**: primera exposición, antes de cualquier despliegue | TAM, **TAM2** |
| D4. Foco explicativo | Utilidad ampliada por factores del trabajo (relevancia, calidad y demostrabilidad del resultado) | **TAM2** |
| D5. Granularidad | **Intermedia**: un panel de cinco especialistas no sostiene un modelo de alta complejidad | **TAM2** |

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

| Constructo | Origen | Sección | Ítems en la fuente | Ítems en la ficha |
|--------------------------------------------------------|---|---|---|---------|
| Relevancia para el trabajo (*job relevance*) | TAM2 | III | 2 | R1–R2 |
| Calidad del resultado (*output quality*) | TAM2 | IV | 2 | C1–C2 |
| Demostrabilidad del resultado (*result demonstrability*) | TAM2 | V | 4 | D1–D2 |
| Utilidad percibida (*perceived usefulness*) | TAM | VI | 4 | U1–U3 |
| Facilidad de uso percibida (*perceived ease of use*) | TAM | VII | 4 | F1–F3 |
| Percepción de control externo (*perceptions of external control*) | TAM3 | VIII | — | K1–K3 |
| Norma subjetiva (*subjective norm*) | TAM2 | IX | 2 | S1–S2 |
| Intención de uso (*behavioral intention*) | TAM | X | 2 | I1–I2 |

**19 ítems** en escala de 1 a 5, más una valoración global de 1 a 10 y cuatro preguntas abiertas.

### Por qué hay menos ítems que en la fuente

Las escalas de Venkatesh y Davis (2000, Apéndice 1) repiten a propósito la misma idea con otras
palabras dentro de cada constructo (por ejemplo, *"usage of the system is important"* y *"… is
relevant"*), porque así estiman la consistencia interna con el alfa de Cronbach. Con cinco evaluadores
ese cálculo no se hace, de modo que esa redundancia no aporta información y alarga la ficha. Se
conservó en cada constructo solo lo que tiene contenido distinto, sin bajar de dos ítems: los propios
autores usan dos ítems en cuatro escalas y declaran alfas superiores a 0.80 (sección *Limitations*).

Se eliminaron además los ítems que repetían el contenido de **otro** constructo: priorizar aparecía en
calidad y en utilidad, y comprender el resultado aparecía en facilidad de uso y en demostrabilidad.

La escala original es de 7 puntos; la ficha usa 5, adaptación habitual que se declara en la
metodología. Los autores ajustaron la redacción de sus ítems con un grupo focal de cinco profesionales,
procedimiento equivalente al de este panel.

### De qué ítem original sale cada uno

| Ítem | Ítem original (Venkatesh y Davis, 2000, salvo indicación) |
|:--:|------------------------------------------------------------|
| R1 | *In my job, usage of the system is important.* |
| R2 | *In my job, usage of the system is relevant.* |
| C1 | *I have no problem with the quality of the system's output.* |
| C2 | *The quality of the output I get from the system is high.* |
| D1 | *The results of using the system are apparent to me.* Adaptado hacia la explicación del modelo (valores SHAP) |
| D2 | *I have no difficulty telling others about the results of using the system.* |
| U1 | *Using the system improves my performance in my job.* |
| U2 | *Using the system in my job increases my productivity.* |
| U3 | *Using the system enhances my effectiveness in my job.* |
| F1 | *I find it easy to get the system to do what I want it to do.* |
| F2 | *My interaction with the system is clear and understandable.* |
| F3 | Facilidad de aprendizaje, de Davis (1989); no figura en el apéndice de TAM2 |
| K1–K3 | Percepción de control externo, de Venkatesh y Bala (2008) |
| S1 | *People who influence my behavior think that I should use the system.* Referente concretado en los colegas |
| S2 | *People who are important to me think that I should use the system.* Referente concretado en las autoridades |
| I1 | *Assuming I have access to the system, I intend to use it.* |
| I2 | Adaptación propia (recomendación a colegas); no figura en TAM2 |

De TAM2 se omiten **imagen** (el prestigio que da usar la herramienta) y **voluntariedad**, que no
aplican a una evaluación por expertos que no serán usuarios obligados del sistema.

El ítem **K2** pregunta de forma expresa por la disponibilidad del dato de hemoglobina, la única de
las 45 variables del modelo que exige un procedimiento sobre el niño. Sus respuestas contrastan la
medición que muestra que el modelo pierde poco sin ella (`manuscrito/validacion/hallazgos_validacion.md`, §1).

## 3. Cómo se analizarán las respuestas

TAM2 es un modelo estructural: en su formulación original se valida estimando las relaciones entre
constructos con cientos de respuestas. **Con un panel de cinco especialistas esa estimación no es
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
