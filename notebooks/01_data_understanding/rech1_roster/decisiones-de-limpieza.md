# Módulo RECH1: Roster del Hogar (Individuos)

> [!WARNING]
> Este módulo contiene a nivel granular a todas las personas que residen en la vivienda. Las decisiones tomadas aquí dictarán cómo se conectarán las características de la familia con el estado nutricional del niño objetivo.

## Mutación de 'variable labels' (Nombres de columnas)

- **Estrategia**: Se utilizará la etiqueta del último año (latest year label) como estándar. Tras analizar el reporte de 42 descripciones mutadas, se constata que los cambios corresponden a traducciones directas del inglés al español (ej. *Line number* a *Número de orden*) o ligeras reformulaciones de la pregunta (ej. *Relationship to head* a *Relación de parentesco con el jefe del hogar*). El significado y propósito de las variables se mantiene constante a lo largo de los 18 años.

## Mutación de 'value labels'

- Se analizaron las 52 columnas con mapeo de valores (11 estables y 41 mutadas). La conclusión es que **no existe "Value Drifting" semántico**. Las mutaciones son traducciones o ajustes lingüísticos (ej. `1.0 (Head) -> 1.0 (Jefe)`).
- **Códigos Omitidos:** En años recientes (ej. 2019-2024 en `HV101`), algunas etiquetas como `9.0 (Conviviente)` o `13.0 (Sobrino)` dejan de ser reportadas en el diccionario oficial. Sin embargo, los códigos base conservan el mismo significado numérico estricto.

> [!TIP]
> **DICCIONARIO MAESTRO COMPUESTO**: Para mapear estas variables, se tomará como base el último diccionario completo disponible (ej. 2017), dado que mantiene la granularidad histórica total. Esto previene la pérdida de etiquetas para los años antiguos.

- **Pérdida de granularidad (Ej. HV101 a partir de 2019)**: Se identificó que a partir del año 2019, el INEI dejó de recolectar sub-categorías específicas en variables de parentesco, agrupándolas en categorías más amplias. Esto no afecta el modelado ya que las categorías principales (`1.0` Jefe, `2.0` Pareja, `3.0` Hijo) mantienen su codificación y significado intacto.

## Tipos lógicos de variable

- Categóricos (con label a imputar): [Revisado]
- Numéricos (Pseudo-Categóricos): [Revisado]
- Numéricos (sin label): [Revisado]
- Identificadores: [Revisado]

---

## Categóricos de negocio

### Salud

| Variable          | Descripción                                       | Nulos (%) | Tipo Categórico | Acción |
| :---------------- | :------------------------------------------------- | :-------- | :--------------- | :------ |
| **QH13A1**  | Limitacion permanente para moverse                 | 72.0%     | Binaria (con NS) | DROP    |
| **QH13A2**  | Limitacion permanente para ver                     | 72.0%     | Binaria (con NS) | DROP    |
| **QH13A3**  | Limitacion permanente para oir                     | 72.0%     | Binaria (con NS) | DROP    |
| **QH13A4**  | Limitacion permanente para hablar                  | 72.0%     | Binaria (con NS) | DROP    |
| **QH13A5**  | Limitacion permanente para entender                | 72.0%     | Binaria (con NS) | DROP    |
| **QH13A6**  | Limitacion permanente para relacionarse            | 81.1%     | Binaria (con NS) | DROP    |
| **QH13A6A** | Otra Limitacion permanente para actividad diarias  | 90.9%     | Binaria (con NS) | DROP    |
| **QH13A6B** | Otra Limitación permanente para actividad diarias | 100.0%    | Binaria (con NS) | DROP    |
| **QH13A6C** | Otra Limitación permanente para actividad diarias | 100.0%    | Binaria (con NS) | DROP    |
| **QH13A6D** | Otra Limitación permanente para actividad diarias | 100.0%    | Binaria (con NS) | DROP    |
| **HV130**   | Member has been very sick for 3+ months last year  | 100.0%    | Binaria (con NS) | DROP    |
| **HV131**   | Mother has been very sick for 3+ months last year  | 100.0%    | Binaria (con NS) | DROP    |
| **HV132**   | Father has been very sick for 3+ months last year  | 100.0%    | Binaria (con NS) | DROP    |
| **HV133**   | Mother/father dead or been very sick for 3+ months | 100.0%    | Binaria          | DROP    |

**ACCIONES DE LIMPIEZA:**

1. **DROP DE TODAS**: Tienen entre 72% y 100% de nulos debido a que se evaluaron en un periodo corto (2013-2017) o fueron descartadas en la recolección. No aportan valor para un análisis longitudinal.

### Educacion

| Variable        | Descripción                                                   | Nulos (%) | Tipo Categórico | Acción     |
| :-------------- | :------------------------------------------------------------- | :-------- | :--------------- | :---------- |
| **HV106** | ¿Cuál fue el nivel de estudios más alto que aprobó?        | 0.0%      | Ordinal (con NS) | KEEP (CORE) |
| **HV109** | Nivel educativo alcanzado                                      | 0.0%      | Ordinal (con NS) | KEEP        |
| **HV110** | Actualmente ¿Asiste a una escuela o colegio?                  | 0.0%      | Binaria          | KEEP        |
| **HV121** | ¿Asistió a escuela en algún momento durante el año actual? | 0.0%      | Nominal          | KEEP        |
| **HV122** | ¿A qué nivel asiste o se matriculó?                         | 0.0%      | Ordinal (con NS) | KEEP        |
| **HV125** | ¿Estuvo matriculado el año pasado?                           | 0.0%      | Binaria          | KEEP        |
| **HV126** | ¿A qué nivel se matriculó el año pasado?                   | 0.0%      | Ordinal (con NS) | KEEP        |
| **HV129** | Condición de asistencia escolar                               | 63.8%     | Nominal (con NS) | DROP        |
| **QH21A** | ¿Estudia en una escuela o colegio estatal?                    | 92.0%     | Binaria          | DROP        |
| **QH21B** | Recibe en escuela desayuno almuerzo Qali Warma?                | 99.4%     | Binaria (con NS) | DROP        |

**ACCIONES DE LIMPIEZA:**

1. **KEEP `HV106`, `HV109` (CORE)**: Cuentan con 0.0% de nulos. `HV106` permite medir de forma estructurada el nivel de escolaridad de cada individuo.
   > [!TIP]
   > **Tratamiento de variables Ordinales con código "No sabe" (`HV106`, `HV109`)**: Estas variables cuentan con un estado operativo (`8.0` No sabe / NS / DK). Para que el modelado ordinal se mantenga lineal y no se vea distorsionado por un valor numéricamente extremo, este código `8.0` debe ser mapeado obligatoriamente a nulo (`np.nan`).
   >
2. **KEEP `HV110` y bloque `HV121`-`HV128`**: Presentan 0.0% de nulos, indicando que las categorías de exclusión fueron codificadas correctamente.
   > [!WARNING]
   > **Mutación de Valores en `HV121`**: Hasta el 2018, esta variable manejaba 3 categorías (`0.0` No, `1.0` Asiste actualmente, `2.0` Asistió algunas veces). A partir de 2019, la categoría `2.0` desaparece por completo, convirtiéndose funcionalmente en binaria. Se debe emplear un diccionario maestro que contemple la categoría `2.0` para los datos históricos.
   >
3. **DROP RESTANTES (`QH21B`, `HV123`, `HV127`, `HV129`, etc.)**: Descartadas por presentar más de 60% de nulos. Por ejemplo, `HV129` (Condición de asistencia escolar) tiene 63.8% de nulos porque es una pregunta condicionada exclusivamente a la población en edad escolar, dejando vacíos al resto del hogar. Imputar este volumen distorsionaría el modelo, por lo que su eliminación es correcta.

### Demografia

| Variable        | Descripción                                     | Nulos (%) | Tipo Categórico | Acción          |
| :-------------- | :----------------------------------------------- | :-------- | :--------------- | :--------------- |
| **HV134** | Both parents alive                               | 100.0%    | Binaria          | DROP             |
| **HV111** | ¿Está viva la madre natural?                   | 65.4%     | Binaria (con NS) | KEEP (A EVALUAR) |
| **HV113** | ¿Está vivo el padre natural?                   | 65.4%     | Binaria (con NS) | KEEP (A EVALUAR) |
| **HV104** | Sexo del miembro del hogar                       | 0.0%      | Nominal          | KEEP (CORE)      |
| **HV102** | Residente habitual / ¿Vive habitualmente aquí? | 0.0%      | Binaria          | KEEP (CORE)      |
| **HV103** | ¿Durmió aquí anoche?                          | 0.0%      | Binaria          | KEEP (CORE)      |
| **HV101** | Relación de parentesco con el jefe del hogar    | 0.0%      | Nominal (con NS) | KEEP (CORE)      |
| **HV115** | ¿Cúal es su estado civil o conyugal?           | 31.3%     | Nominal          | KEEP             |
| **HV116** | Acutalmente, anteriormente o nunca unida         | 31.3%     | Nominal          | DROP             |

**ACCIONES DE LIMPIEZA:**

1. **KEEP `HV101`, `HV102`, `HV103`, `HV104` (CORE)**: Conforman el bloque base sociodemográfico con 0.0% de nulos. Permiten establecer la estructura del hogar, confirmar residencia y sexo.
   > !WARNING
   > **Mutación y Valores de `HV101`**: A partir de 2019, se dejó de recolectar subcategorías específicas (ej. `9.0`, `13.0`, `14.0`). Los números base (`1.0` Jefe, `2.0` Esposa, `3.0` Hijo) mantienen su significado estricto. Se requiere emplear un Diccionario Maestro Compuesto (basado en el año 2017) durante la transformación. Adicionalmente, cuenta con el código `98.0 (NS)`, el cual debe mapearse a nulo (`np.nan`).
   >
2. **KEEP `HV111`, `HV113` (A EVALUAR)**: Variables requeridas para evaluar la supervivencia parental. Presentan 65.4% de nulos, pero **no son datos perdidos**. Son "Nulos por diseño" (Skip Logic): la pregunta se salta para adultos o cuando el padre/madre ya figura como residente en el hogar (`HV112`/`HV114`). Este 65.4% de vacíos es estructural y completamente lógico.
   > !TIP
   > **Tratamiento de variables Binarias con código "No sabe" (`HV111`, `HV113`)**: Aunque se catalogan lógicamente como binarias (`0.0` No, `1.0` Sí), incluyen un tercer estado operativo (`8.0` No sabe / NS / DK). Para garantizar la integridad del modelado matemático (e.g. regresiones logísticas), este tercer estado debe mapearse obligatoriamente a nulo (`np.nan`).
   >
3. **KEEP `HV115`**: Se conserva por su valor predictivo en los padres.
4. **DROP (`HV134`, `HV116`)**: Descartadas por alta redundancia o nulos totales.

### Posesiones

| Variable        | Descripción                  | Nulos (%) | Tipo Categórico | Acción |
| :-------------- | :---------------------------- | :-------- | :--------------- | :------ |
| **HV137** | Member has a blanket          | 100.0%    | Binaria (con NS) | DROP    |
| **HV138** | Member has a pair of shoes    | 100.0%    | Binaria (con NS) | DROP    |
| **HV139** | Member has 2+ sets of clothes | 100.0%    | Binaria (con NS) | DROP    |

**ACCIONES DE LIMPIEZA:**

1. **DROP DE TODAS**: Total de nulos históricos de 100%.

### Metadatos

| Variable        | Descripción                                                  | Nulos (%) | Tipo Categórico | Acción     |
| :-------------- | :------------------------------------------------------------ | :-------- | :--------------- | :---------- |
| **HV120** | Menores de 5 años para medición de peso/talla y hemoglobina | 0.0%      | Binaria          | KEEP (CORE) |
| **HV117** | Elegibilidad para entrevista individual de mujeres            | 0.0%      | Binaria          | KEEP        |
| **QH25B** | Vive permanentemente en el Perú                              | 100.0%    | Binaria          | DROP        |
| **HV135** | Has brothers/sisters under 18 of the same father and mother   | 100.0%    | Binaria (con NS) | DROP        |
| **HV136** | Brothers/sisters under 18 that don't live in household        | 100.0%    | Binaria          | DROP        |
| **HV140** | Member has a birth certificate                                | 95.6%     | Nominal (con NS) | DROP        |
| **HV118** | Elegibilidad para entrevista de hombres                       | 100.0%    | Binaria          | DROP        |

**ACCIONES DE LIMPIEZA:**

1. **KEEP `HV120` (CORE ABSOLUTO)**: Esta variable cuenta con 0.0% de nulos e indica explícitamente si el individuo en el roster es un niño menor de 5 años elegible para las mediciones biomédicas. Se utilizará como variable de filtrado para la tabla poblacional final.
2. **KEEP `HV117`**: Utilizada para identificar transversalmente si la mujer completó el cuestionario individual.
3. **DROP RESTANTES**: Descartadas por presentar entre 95% y 100% de nulos.

---

## Numéricos (Pseudo-Categóricos)

Las siguientes variables fueron catalogadas inicialmente como categóricas por contar con un diccionario parcial para códigos especiales (ej. `98.0 (NS)`), pero lógicamente representan variables continuas.

### Educacion (Numérico)

| Variable        | Descripción                                            | Nulos (%) | Acción |
| :-------------- | :------------------------------------------------------ | :-------- | :------ |
| **HV108** | Número de años de estudio                             | 0.0%      | KEEP    |
| **HV107** | ¿Cuál fue el año o grado más alto que aprobó?      | 22.0%     | KEEP    |
| **HV124** | Número de años de estudio matriculado año actual     | 0.0%      | KEEP    |
| **HV128** | Número de años de estudio matriculado año pasado     | 0.0%      | KEEP    |
| **HV127** | Año o grado que asistió o se matriculó (año pasado) | 76.0%     | DROP    |
| **HV123** | Año o grado que asiste o se matriculó                 | 77.1%     | DROP    |

**ACCIONES DE LIMPIEZA:**

1. **DROP `HV123`, `HV127`**: A pesar de estar presentes los 18 años, alcanzan ~77% de nulos porque son **nulos condicionados**: solo se pregunta el grado a quienes asisten actualmente o asistieron. Imputar el 77% sesgaría el modelo. Las variables `HV106` y `HV109` (0% nulos) ya cubren la escolaridad máxima alcanzada de manera global.

### Demografia (Numérico)

| Variable        | Descripción                 | Nulos (%) | Acción         |
| :-------------- | :--------------------------- | :-------- | :-------------- |
| **HV105** | Edad del miembro del hogar   | 0.0%      | KEEP (CORE)     |
| **HV112** | Número de orden de la madre | 65.4%     | KEEP (CRÍTICA) |
| **HV114** | Número de orden del padre   | 65.4%     | KEEP (CRÍTICA) |

**ACCIONES DE LIMPIEZA:**

1. **Tratamiento de Valores Especiales**: Los valores `97.0` (Inconsistente / Mayores de 96) y `98.0` (No Sabe) fungen como identificadores de valores atípicos. Durante el procesamiento, estos códigos deben ser reemplazados explícitamente por `np.nan` para que las columnas puedan ser tratadas como variables numéricas continuas sin distorsionar su distribución media.
2. **KEEP `HV105`**: Representa la edad continua del miembro del hogar.
3. **KEEP `HV108`, `HV107`**: Proveen el grado específico y los años de educación completados. Es importante notar que `HV107` presenta un 22.0% de nulos por ser **"Nulo por diseño" (Skip Logic)**: esta pregunta se salta automáticamente para las personas (bebés o adultos) que nunca asistieron a la escuela. Dado que aporta información continua vital para los que sí asistieron, conservarla (KEEP) es indispensable.
4. **Tratamiento Relacional (`HV112`, `HV114`)**: Representan el número de línea (ID) del padre o la madre. Presentan un 65.4% de nulos porque son **"Nulos por diseño" (Skip Logic)**: esta pregunta solo aplica a menores de edad y se salta para los adultos del hogar. Adicionalmente, el valor especial `0.0 (Madre/Padre no en HH)` debe convertirse obligatoriamente a nulo (`np.nan`) para evitar cruces erróneos con la línea cero durante las operaciones de *merge* intrahogar.

---

## Numéricos (sin label)

### Metadatos y Extranjería

| Variable         | Tipo    | Nulos (%) | Descripción                                      |
| :--------------- | :------ | :-------- | :------------------------------------------------ |
| **QH25CA** | float64 | 99.6%     | Desde qué año vive en el Perú (Solo 2018-2024) |
| **QH25CM** | float64 | 99.6%     | Desde qué mes vive en el Perú (Solo 2018-2024)  |
| **ID1**    | float64 | 63.5%     | Año de la encuesta (Solo 2019-2024)              |

**ACCIONES DE LIMPIEZA:**

1. **DROP `QH25CA` y `QH25CM`**: Al tener 99.6% de nulos históricos, no poseen varianza estadística significativa.
2. **DROP `ID1`**: Presenta 63.5% de nulos. El metadato temporal real ("Año de la Encuesta") debe ser rescatado desde el módulo RECH0 mediante la imputación generada previamente.

---

## Identificadores

### Llaves Primarias y Extranjeras

| Variable        | Tipo    | Nulos (%) | Descripción                                                                  |
| :-------------- | :------ | :-------- | :---------------------------------------------------------------------------- |
| **HHID**  | str     | 0.0%      | Identificación Cuestionario del Hogar. Llave extranjera para unir con RECH0. |
| **HVIDX** | float64 | 0.0%      | Número de orden del individuo. Llave primaria a nivel de persona.            |
| **QH25A** | str     | 57.0%     | ¿Cuál es su nacionalidad? (Solo presente 2018-2024).                        |

**ACCIONES DE LIMPIEZA:**

1. **KEEP `HHID` y `HVIDX` (CORE ABSOLUTO)**: Constituyen el núcleo relacional de la tabla. `HHID` permite la unión con los datos del hogar (RECH0), y `HVIDX` funge como llave primaria a nivel de individuo. Ambas poseen 0.0% de nulos inquebrantable.
2. **DROP `QH25A`**: Al tener 100% de datos nulos durante los primeros 11 años del estudio (2007-2017), insertaría un sesgo temporal masivo en el modelo longitudinal. Se elimina de tajo.

