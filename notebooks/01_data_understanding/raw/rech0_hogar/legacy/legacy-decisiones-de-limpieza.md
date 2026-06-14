## Mutación de 'variable labels'
- **Estrategia**: Se utilizará la etiqueta del último año (latest year label) como estándar. No se detectaron variables donde el significado conceptual haya cambiado drásticamente a lo largo de los años evaluados.

## Mutación de 'value labels'
- Se observó consistencia en las etiquetas de valores. Las variaciones detectadas corresponden a versiones semánticamente equivalentes, sin alteraciones drásticas en su significado lógico.

## Tipos lógicos de variable
- Categóricos (con label a imputar): 11
- Identificadores: 14
- Numéricos: 36

---

## Categóricos de negocio (Categorias Lógicas)
De los 11 labels evaluados:

### Socio demográficos

| Variable | Descripción |
| :--- | :--- |
| **HV023** (Dominio) | 25 dominios geográficos. |
| **HV024** (Región) | 25 regiones geográficas equivalentes al dominio. |
| **HV025** (Área de residencia) | Subdivisión en Urbano / Rural. Variable estructurante para el modelado poblacional. |
| **HV026** (Lugar de residencia) | Subdivisión detallada del nivel de urbanización (Capital, Ciudad, Pueblo, Campo). |
| **HV022 / hv022** (Estrato) | Subdivisión administrativa (Sede Capital, Resto Urbano, Rural). |

**ACCIONES DE LIMPIEZA:**
1. **DROP `HV023`**: Presenta colinealidad perfecta con Región (0% nulos históricos).
2. **COALESCE `HV022` y `hv022`**: `HV022` (mayúscula) tiene 0% nulos en todos los años excepto en 2016 (100% nulos), donde se empleó `hv022` (minúscula) con 0% nulos. Se requiere una fusión (coalesce) para obtener la columna consolidada.
3. **KEEP `HV024`, `HV025`**: Muestran consistencia total (0% nulos).
4. **KEEP `HV026`**: Presenta 10.1% de nulos únicamente en el año 2008. Se requiere imputación condicional basada en su correlación con `HV025` (Área de residencia) para preservar los registros de dicho año.

   > [!WARNING]
   > En modelos estadísticos o de regresión, la inclusión simultánea de `HV025` (Área) y `HV026` (Lugar de residencia) requiere evaluación previa debido a posible inflación de varianza (multicolinealidad).

### Metadatos de Encuesta (Flags)

| Variable | Descripción |
| :--- | :--- |
| **HV015** (Resultado de la entrevista) | Resultado de la encuesta en la vivienda (Completa, Ausente, Rechazada, etc.). |
| **HV020** (Criterio de elegibilidad) | Define el universo de mujeres encuestadas. |
| **HV027** (Selección hombre/esposo) | Indicador de aplicación de cuestionario masculino. |
| **HV042** (Selección medición hemoglobina) | Indicador de selección para prueba de sangre. |
| **HV043** (Módulo mujeres estado) | Indicador administrativo de submuestra. |
| **HV044** (Módulo violencia familiar) | Indicador administrativo de submuestra. |

**ACCIONES DE LIMPIEZA:**
1. **FILTER `HV015`**: Presenta 0% de nulos. Se debe aplicar un filtrado estricto conservando únicamente el código `1.0` (Entrevista Completa). Códigos alternativos representan hogares sin datos efectivos.
2. **DROP RESTANTES** (`HV020`, `HV027`, `HV042`, `HV043`, `HV044`): Variables operativas sin relevancia directa para el modelado poblacional subyacente. Nota: `HV042` podría requerirse si se parametriza específicamente el análisis de anemia en futuras fases.

   > [!WARNING]
   > El filtro por `HV015` debe ejecutarse con prioridad alta en el pipeline antes de descartar registros, a fin de aislar apropiadamente las encuestas finalizadas con éxito.

---

## Numéricos (sin label)
De los 36 numéricos evaluados:

### 1. Pesos Muestrales y Probabilidades (Sample Weights)

| Variable | Descripción |
| :--- | :--- |
| **HV005** (Factor de ponderación) | Peso estadístico base de diseño. |
| **hv005** (Factor ponderación minúscula) | Complemento temporal de HV005. |
| **HV005A** (Peso Departamental) | Factor de expansión departamental. |
| **HV005X** (Peso niño <5 años) | Factor de expansión infantil específico. |
| **HV004** (Unidad última de muestreo) | Componente del diseño de la muestra. |
| **HV033** (Probabilidad de selección de área) | Probabilidad poblacional base. |

**ACCIONES DE LIMPIEZA:**
1. **COALESCE `HV005` y `hv005`**: Fusión requerida para cubrir los años 2014 y 2016 donde la notación varió de mayúscula a minúscula.
2. **EVALUAR `HV005A` y `HV005X`**: Activación limitada a años específicos (2008 y 2015 respectivamente). 
3. **KEEP `HV004`**: Muestra 0% de nulos y es requerida si se implementa modelado multinivel de recolección.
4. **DROP `HV033`**: Muestra 89.1% de nulos históricos globales.

   > [!TIP]
   > Las variables sensibles a mayúsculas deben procesarse de forma explícita mediante un método unificado (coalesce) debido al tratamiento de case-sensitivity en DataFrames.

### 2. Geolocalización

| Variable | Descripción |
| :--- | :--- |
| **latitudy / longitudx** | Coordenadas geoespaciales formato 1. |
| **lat_ccpp / long_ccpp** | Coordenadas geoespaciales formato 2. |
| **LATITUDY / LONGITUDX** | Coordenadas geoespaciales formato 3. |

**ACCIONES DE LIMPIEZA:**
1. **COALESCE**: Las diferentes variantes nominales deben consolidarse en dos columnas únicas (`Latitud_final`, `Longitud_final`) para evitar pérdida de datos por exclusión simple.

### 3. Metadatos Temporales

| Variable | Descripción |
| :--- | :--- |
| **ID1** (Año) | Año de la recolección. |
| **HV007** (Año de entrevista) | Año de la recolección. |

**ACCIONES DE LIMPIEZA:**
1. **COALESCE `ID1` y `HV007`**: Fusión obligatoria debido a que ID1 presenta 27.6% de nulos y HV007 presenta 6.2%. 
2. **IMPUTAR AÑO 2018**: Ambas variables registran 100% de nulos en la edición 2018. El valor numérico del año debe calcularse algebraicamente mediante la variable Century Month Code (`HV008`): `Año = 1900 + (HV008 - 1) // 12`.

### 4. Metadatos Operativos / Administrativos

| Variable | Descripción |
| :--- | :--- |
| **HV031** (Editor de campo) | Identificador administrativo. |
| **HV019** (Identificador del digitador) | Identificador administrativo. |
| **HV006** (Mes de la entrevista) | Variable operativa temporal. |
| **HV016** (Día de la entrevista) | Variable operativa temporal. |
| **HV018** (Identificador del entrevistador) | Identificador administrativo. |
| **HV017** (Número de visitas al hogar) | Conteo operativo. |

**ACCIONES DE LIMPIEZA:**
1. **DROP TODAS**: Exclusión por constituir ruido operativo administrativo sin injerencia analítica en los modelos predictivos del núcleo familiar.

### 5. Características Demográficas Estructurales

| Variable | Descripción |
| :--- | :--- |
| **HV009** (Total de personas en el hogar) | Tamaño bruto de la unidad familiar residente. |
| **HV012** (Miembros de jure / residentes habituales) | Población permanente. Denominador oficial para índices de ocupación y hacinamiento. |
| **HV013** (Miembros de facto / durmieron anoche) | Población transitoria de la noche previa. |
| **HV014** (Número de niños menores de 5 años) | Población objetivo principal dentro de la estructura poblacional. |
| **HV010** (Número de mujeres elegibles) | Población femenina en edad fértil potencial. |
| **HV011** (Número de hombres elegibles) | Población masculina elegible de la vivienda. |
| **HV035** (Niños elegibles para altura y peso) | Volumetría operativa de niños derivados a antropometría. |
| **HV041** (Mujeres con medición de peso y talla) | Volumetría operativa de mujeres en antropometría. |

**ACCIONES DE LIMPIEZA:**
1. **KEEP TODAS** (0% nulos históricos): Constituyen el bloque numérico base sociodemográfico a nivel vivienda.
2. **FEATURE ENGINEERING**: Se parametrizará el cálculo de variables derivadas (ej. tasa de hacinamiento familiar) tomando como base estable `HV012`, en preferencia frente a la medición transitoria `HV013`.
3. **FILTRO ANTROPOMÉTRICO**: La variable `HV035` debe utilizarse como control cruzado (> 0) para determinar viabilidad de los bloques de estudio de la fase biométrica.

### 6. Cronología Calculable (Century Month Code)

| Variable | Descripción |
| :--- | :--- |
| **HV008** (Fecha de entrevista meses - CMC) | Formato estandarizado de tiempo continuo en base mensual. |

**ACCIONES DE LIMPIEZA:**
1. **KEEP `HV008`**: 0% de nulos. Variable requerida para cálculos precisos de series de tiempo e imputaciones temporales.

   > [!TIP]
   > El uso de mediciones temporales CMC (Century Month Code) es mandatario en análisis poblacionales para el cálculo preciso de edades expresadas en meses, un estándar metodológico para el contraste con tablas biométricas internacionales (ej. OMS).

### 7. Características Geofísicas

| Variable | Descripción |
| :--- | :--- |
| **HV040** (Altitud del conglomerado en metros) | Medición altitudinal del estrato geográfico sobre el nivel del mar. |

**ACCIONES DE LIMPIEZA:**
1. **KEEP `HV040`**: 0% de nulos. Se conserva como variable biológica e infraestructural de peso analítico.

---

## Identificadores
De los 14 identificadores evaluados:

### 1. Llaves Primarias (Primary Keys)

| Variable | Descripción |
| :--- | :--- |
| **HHID** (Identificación Cuestionario del Hogar) | Identificador compuesto a nivel vivienda oficializado por la encuesta. |
| **HV001** (Conglomerado) | Primary Sampling Unit. |
| **HV002** (Vivienda) | Identificador de estructura habitacional. |
| **HV002A** (Hogar) | Identificador del núcleo familiar dentro de la estructura habitacional. |
| **HV021** (Unidad de muestreo primario - conglomerado) | Variable homóloga redundante respecto a HV001. |

**ACCIONES DE LIMPIEZA:**
1. **KEEP `HHID`**: (0% nulos). Variable relacional consolidada para el mapeo transversal del data mart a nivel vivienda.
2. **KEEP `HV001`, `HV002` y `HV002A`**: Representan la trazabilidad jerárquica histórica.
3. **DROP `HV021`**: Se excluye por colinealidad nominal con `HV001`.

   > [!WARNING]
   > `HV002A` registra 100% de nulos en las ediciones 2007-2011, introduciéndose metodológicamente a partir de 2012 para capturar viviendas con hogares múltiples. Se debe aplicar un tratamiento condicional de los componentes si se implementan operaciones de *join* que abarquen el panel 2007-2011. En caso contrario, utilizar exclusivamente `HHID` previene fragmentación de cruces.

### 2. Identificadores Geográficos Nominales

| Variable | Descripción |
| :--- | :--- |
| **NCONGLOME / NCONGLOME1 / nconglome** | Nomenclatura del muestreo primario administrativo. |
| **UBIGEO / ubigeo** | Codificación del sistema nacional de ubicación. |
| **CODCCPP / codccpp** (Código Centro Poblado) | Codificación distrital submunicipal. |
| **NOMCCPP / nomccpp** (Nombre Centro Poblado) | Nomenclatura distrital submunicipal. |

**ACCIONES DE LIMPIEZA:**
1. **COALESCE `UBIGEO`, `CODCCPP` y `NOMCCPP`**: Debido a discrepancias tipográficas a lo largo de las ediciones (mayúsculas frente a minúsculas), presentan fragmentación que oscila entre el 56% y 93%. Se aplicará consolidación programática.
2. **DROP `NCONGLOME*`**: Presentan alta tasa de nulos (69% a 94%) por fragmentación extrema y son conceptualmente dependientes de la llave primaria `HV001`.

### 3. Identificadores Operativos Constantes

| Variable | Descripción |
| :--- | :--- |
| **HV000** (Código del país) | Codificación nacional de origen (DHS). |
| **HV003** (N° orden informante) | Apuntador individual de informante matriz. |
| **HV030** (Supervisor de campo) | ID administrativo. |
| **HV032** (Editor de la oficina) | ID administrativo. |

**ACCIONES DE LIMPIEZA:**
1. **DROP TODAS**: Variables exclusivas de la cadena de supervisión, con nula o escasa varianza transversal analítica.
