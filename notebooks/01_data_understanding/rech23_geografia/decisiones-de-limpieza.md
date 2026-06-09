# Módulo RECH23: Geografía y Características del Hogar

> [!WARNING]
> Este módulo contiene características extendidas de la vivienda y variables geográficas. A diferencia de RECH1, aquí encontraremos variables a nivel de hogar (repetidas para todos los miembros) y enfocadas fuertemente en determinantes básicos estructurales.

## Tipos lógicos de variable
- Categóricos (con label a imputar): [Pendiente]
- Numéricos (Pseudo-Categóricos): [Pendiente]
- Numéricos (sin label): [Pendiente]
- Identificadores: [Pendiente]

---

## Categóricos de negocio

### Agua y Saneamiento

| Variable | Descripción | Años Presentes | Nulos (%) | Tipo Categórico | Acción | Estado | Advertencia | Nota | Column Label (Latest) | Value Label (Latest) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SH2201** | Water to drink is available the one whole day | 2 años (2007-2008) | TBD | Binario (0/1) | Mantener (Directo a modelo) | KEEP | TBD | Valores Estables | English Meta Column (2007-2008) | English Meta Column (2007-2008) |
| **HV201** | Source of drinking water (Fuente principal) | 18 años (2007-2024) | TBD | Categórico Nominal con NS/NR | Mapear a Value Label -> Reemplazar texto Otro/NS por NaN -> Imputar -> One-Hot Encoding | KEEP | ¡Múltiples diccionarios! Cuidado al mapear. | Valores Mutados (4 bloques) | Construir Súper Diccionario | TBD |
| **HV202** | Source of non-drinking water (Fuente de agua no potable) | 18 años (2007-2024) | TBD | Categórico Nominal (Vacío Histórico) | Eliminar columna (90% de nulos desde 2009 hasta 2024) | DROP | ¡Peligro! Tiene ~90% de nulos desde 2009 al 2024. Inviable para imputación. | Valores Mutados (Vacío histórico) | No aplica (Eliminar) | TBD |
| **HV204** | Time to get to water source (Tiempo de viaje a fuente) | 18 años (2007-2024) | TBD | Numérico Pseudo-Categórico | Reemplazar 998.0 por NaN -> Reemplazar 996.0 por 0.0 -> Imputar | KEEP | ¡996.0 significa 0 minutos, 998.0 es faltante/NS! | Valores Estables (Mutación solo traducción) | No aplica (Recodificación manual) | TBD |
| **HV205** | Type of toilet facility (Tipo de servicio higiénico) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV225** | Share toilet with other households (Comparte servicio higiénico) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV235** | Location of source for water (Ubicación de la fuente de agua) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV236** | Person fetching water (Persona que recoge agua) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV237** | Anything done to water to make safe to drink (Tratamiento del agua) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV237A** | Water usually treated by: boil (Tratamiento de agua: hervir) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV237B** | Water usually treated by: add bleach/chlorine (Añadir lejía o cloro) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV237C** | Water usually treated by: strain through a cloth (Filtrar por paño) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV237D** | Water usually treated by: use water filter (Usar filtro de agua) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV237E** | Water usually treated by: solar disinfection (Desinfección solar) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV237F** | Water usually treated by: let it stand and settle (Dejar reposar) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Error de Traducción Histórico | Error INEI (2009-2018): Tradujeron 'settle' como 'revolver'. Corregido en 2019 a 'asentarse'. | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV237G** | Water usually treated by: CS - packed water (Agua embotellada) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV237H** | Water usually treated by: CS (Opciones Específicas del País) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV237I** | Water usually treated by: CS (Opciones Específicas del País) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV237J** | Water usually treated by: CS (Opciones Específicas del País) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV237K** | Water usually treated by: CS (Opciones Específicas del País) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV237X** | Water usually treated by: other (Tratamiento de agua: otros) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV237Z** | Water usually treated by: don't know (Tratamiento de agua: no sabe) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV238** | Number of households sharing toilet (Número de hogares compartiendo baño) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Posible Numérico | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **SH2202** | Last 2 weeks was water discontinued for a day or more | 2 años (2007-2008) | TBD | Binario (0/1) | Mantener (Directo a modelo) | KEEP | TBD | Valores Estables | English Meta Column (2007-2008) | English Meta Column (2007-2008) |
| **SH2203** | Other source of water when it wasn't availalble | 2 años (2007-2008) | TBD | Categórico Nominal | One-Hot Encoding | KEEP | TBD | Valores Estables | English Meta Column (2007-2008) | English Meta Column (2007-2008) |
| **SH2204** | Do you store the water to drink | 2 años (2007-2008) | TBD | Binario (0/1) | Mantener (Directo a modelo) | KEEP | TBD | Valores Estables | English Meta Column (2007-2008) | English Meta Column (2007-2008) |
| **SH2208** | Does household pays for water service | 2 años (2007-2008) | TBD | Binario con NS/NR (0/1/8) | Reemplazar 8 (DK) por NaN e imputar | KEEP | TBD | Valores Estables | English Meta Column (2007-2008) | English Meta Column (2007-2008) |
| **SH2209** | Agency that collects water fees | 2 años (2007-2008) | TBD | Categórico Nominal | One-Hot Encoding | KEEP | TBD | Valores Estables | English Meta Column (2007-2008) | English Meta Column (2007-2008) |
| **SH2210** | How often pays for water service | 2 años (2007-2008) | TBD | Categórico con NS/NR | Reemplazar 8 (DK) por NaN y One-Hot | KEEP | TBD | Valores Estables | English Meta Column (2007-2008) | English Meta Column (2007-2008) |
| **SH2212A** | Use water for cooking | 2 años (2007-2008) | TBD | Binario (0/1) | Mantener (Directo a modelo) | KEEP | TBD | Valores Estables | English Meta Column (2007-2008) | English Meta Column (2007-2008) |
| **SH2212B** | Use water to take a bath | 2 años (2007-2008) | TBD | Binario (0/1) | Mantener (Directo a modelo) | KEEP | TBD | Valores Estables | English Meta Column (2007-2008) | English Meta Column (2007-2008) |
| **SH2212C** | Use water to wash clothes | 2 años (2007-2008) | TBD | Binario (0/1) | Mantener (Directo a modelo) | KEEP | TBD | Valores Estables | English Meta Column (2007-2008) | English Meta Column (2007-2008) |
| **SH2212D** | Use water to sprinkle on floor to avoid dust | 2 años (2007-2008) | TBD | Binario (0/1) | Mantener (Directo a modelo) | KEEP | TBD | Valores Estables | English Meta Column (2007-2008) | English Meta Column (2007-2008) |
| **SH2212E** | Use water to water plants | 2 años (2007-2008) | TBD | Binario (0/1) | Mantener (Directo a modelo) | KEEP | TBD | Valores Estables | English Meta Column (2007-2008) | English Meta Column (2007-2008) |
|
| **SH2212F** | Use water to sprinkle outdoor floor to avoid dust | 2 años (2007-2008) | TBD | Binario (0/1) | Mantener (Directo a modelo) | KEEP | TBD | Valores Estables | English Meta Column (2007-2008) | English Meta Column (2007-2008) |
|
| **SH2213** | Do you store water used for shower, wash or sprinkle | 2 años (2007-2008) | TBD | Binario (0/1) | Mantener (Directo a modelo) | KEEP | TBD | Valores Estables | English Meta Column (2007-2008) | English Meta Column (2007-2008) |
|
| **SH2401** | Where is the bathroom or latrine located | 2 años (2007-2008) | TBD | Categórico Nominal | One-Hot Encoding | KEEP | TBD | Valores Estables | English Meta Column (2007-2008) | English Meta Column (2007-2008) |
|
| **SH2406** | How often is the bathroom or latrine cleaned | 2 años (2007-2008) | TBD | Categórico Ordinal con NS/NR | Reemplazar 8.0 por NaN e imputar | KEEP | TBD | Valores Estables | English Meta Column (2007-2008) | English Meta Column (2007-2008) |
|
| **SH2407** | Is there a place to wash hands near bathroom/letrine | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |
| **SH2408** | Does household pays to use bathroom or latrine | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |
| **SH2409** | Is the bathroom available for use the day and night | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |
| **SH2410** | Where does household members wash their hands | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |
| **SH2412** | Where does household throw away the garbage | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |
| **SH2413** | How often is garbage picked up | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |
| **SH2414** | Before disposing of garbage where it is stored | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |
| **SH32** | Agua potable esta disponible el día entero | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH2201 | Meta Column 2009 | TBD |
| **SH33** | En las 2 últimas semanas el agua fue suspendida por un día o más | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH2202 | Meta Column 2009 | TBD |
| **SH37** | Almacena el agua para beber | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH2204 | Meta Column 2009 | TBD |
| **SH39** | El hogar paga por el servicio de agua | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH2208 | Meta Column 2009 | TBD |
| **SH40** | Agencia que recibe los cobros por el agua | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH2209 | Meta Column 2009 | TBD |
| **SH41** | Con que frecuencia paga por el servicio de agua | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH2210 | Meta Column 2009 | TBD |
| **SH42** | Water to drink is available the one whole day (Agua disponible todo el día) | 16 años (2009-2024) | TBD | Especial (Columna Bipolar) | Dividir en 2 variables: SH42_Agua_Todo_El_Dia (2010+) y SH42_Recibo_Agua (2009) | SPLIT | ¡Columna reciclada! -> COMBINAR SH42_Recibo_Agua(2009) con SH52_Monto_Pago(2010). | Valores Mutados (Reciclaje de columna) | No aplica (División manual en Python) | TBD |
| **SH43** | Last 2 weeks was water discontinued for a day or more (Agua suspendida 2 últimas semanas) | 15 años (2010-2024) | TBD | Binario (0/1) | Mapear a Value Label -> Label Encoding | KEEP |   | Valores Estables (Mutación solo traducción) | Meta Column 2024 | TBD |
| **SH46** | Cada cuánto limpia el baño o letrina | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH2406 | Meta Column 2009 | TBD |
| **SH48** | Do you store the water to drink (Almacena el agua para beber) | 16 años (2009-2024) | TBD | Especial (Columna Bipolar) | Dividir en 2 variables: SH48_Conserva_Agua (2010+, Binaria) y SH48_Basura (2009, Categórica Nominal) | SPLIT | ¡Columna reciclada! -> COMBINAR SH48_Basura(2009) con SH58(2010+). COMBINAR SH48_Conserva_Agua(2010+) con SH49_Tiene_Envase(2010). | Valores Mutados (Reciclaje de columna) | No aplica (División manual en Python) | TBD |
| **SH49** | Has a container or packet (Tipo de envase o recipiente) | 16 años (2009-2024) | TBD | Especial (Columna Multipolar) | Dividir en 3: Frec_Basura(2009), Tiene_Envase(2010), Tipo_Envase(2011+) | SPLIT | ¡Columna reciclada! -> COMBINAR Frec_Basura(2009) con SH59(2010+). COMBINAR Tiene_Envase(2010) con SH48_Conserva_Agua(2010+). | Valores Mutados (Reciclaje masivo) | No aplica (División manual en Python) | TBD |
| **SH50** | Use lid (¿Lo usa con tapa?) | 16 años (2009-2024) | TBD | Especial (Columna Multipolar) | Dividir en 3: Tipo_Basurero(2009), Proveedor_Agua(2010), Tiene_Tapa(2011+) | SPLIT | ¡Columna reciclada! -> COMBINAR Tipo_Basurero(2009) con SH60(2010+). COMBINAR Proveedor_Agua(2010) con SH52_Institucion_Agua(2011+). | Valores Mutados (Reciclaje masivo) | No aplica (División manual en Python) | TBD |
| **SH51** | Do you payment for water (¿Pago por el agua?) | 15 años (2010-2024) | TBD | Especial (Columna Bipolar) | Dividir en 2: Frec_Pago_Agua(2010, Categórica) y Pago_Agua(2011+, Binaria) | SPLIT | ¡Peligro! Columna reciclada. | Valores Mutados (Reciclaje masivo) | No aplica (División manual en Python) | TBD |
| **SH52** | Institution for payment water (Institución de pago de agua) | 15 años (2010-2024) | TBD | Especial (Columna Bipolar) | Dividir en 2: Monto_Pago(2010, Numérica con top-coding 401.0) y Institucion_Agua(2011+, Categórica) | SPLIT | ¡Columna reciclada! -> COMBINAR Institucion_Agua(2011+) con SH50_Proveedor_Agua(2010). | Valores Mutados (Reciclaje masivo) | No aplica (División manual en Python) | TBD |
| **SH56** | How often is the bathroom or latrine cleaned (Con qué frecuencia se limpia el baño) | 16 años (2009-2024) | TBD | Especial (Columna Bipolar) | Dividir en 2: Limpió_Baño(2009, Binaria) y Frec_Limpieza(2010+, Categórica) | SPLIT | ¡Peligro extremo! Columna reciclada. INEI movió preguntas de un código a otro. | Valores Mutados (Reciclaje masivo) | No aplica (División manual en Python) | TBD |
| **SH58** | Where does household throw away the garbage (Dónde tira la basura) | 15 años (2010-2024) | TBD | Categórico Nominal con NS/NR | Reemplazar 98.0 por NaN -> Mapear a Value Label -> Imputar -> One-Hot Encoding | KEEP | ¡Pésima traducción en 2019+! Usar dict 2018. -> COMBINAR con SH48_Basura(2009). | Valores Mutados (Error tipográfico INEI) | Meta Column 2018 | TBD |
| **SH59** | How often is garbage picked up (Con qué frecuencia se recoge la basura) | 16 años (2009-2024) | TBD | Especial (Columna Bipolar) | Dividir en 2: Recogen_Basura(2009, Binaria) y Frec_Recojo(2010+, Categórica) | SPLIT | ¡Columna reciclada! -> COMBINAR Frec_Recojo(2010+) con SH49_Frec_Basura(2009). | Valores Mutados (Reciclaje masivo) | No aplica (División manual en Python) | TBD |
| **SH60** | Before disposing of garbage where it is stored (Antes de desechar la basura donde se almacena) | 16 años (2009-2024) | TBD | Especial (Columna Bipolar) | Dividir en 2: Fuente_Luz(2009, Categórica) y Tipo_Basurero(2010+, Categórica) | SPLIT | ¡Columna reciclada! -> COMBINAR Fuente_Luz(2009) con SH70_Fuente_Luz(2010+). COMBINAR Tipo_Basurero(2010+) con SH50_Tipo_Basurero(2009). | Valores Mutados (Reciclaje masivo) | No aplica (División manual en Python) | TBD |
| **SH110** | Test de cloro | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | TBD | Meta Column 2009 | TBD |
| **SH127** | Test de cloro | 1 año (2010) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH110 | Meta Column 2010 | TBD |
| **SH227** | Chlorine test (Prueba de cloro) | 14 años (2011-2024) | TBD | Categórico Mixto con NS/NR | Reemplazar 9.0 por NaN -> Recodificar 6.0 a 3.0 -> Mapear a Value Label -> One-Hot Encoding | KEEP | En 2024 agregaron el código 6.0 para 0.0 mg/lt (digital). Químicamente equivale a 3.0. Recodificarlos juntos para mantener el histórico intacto. | Valores Estables (Nueva variante en 2024) | Meta Column 2024 | TBD |
| **QH227A** | La muestra fue tomada por: | 7 años (2018-2024) | TBD | TBD | TBD | KEEP | TBD | Complementa a SH227 (Nueva desde 2018) | Meta Column 2024 | TBD |
| **QH227B** | La muestra del agua se extrajo del: | 7 años (2018-2024) | TBD | Categórico Nominal | Reemplazar texto Otro por NaN -> Mapear a Value Label -> Imputar -> One-Hot Encoding | KEEP |   | Valores Estables (Mutación solo traducción) | Meta Column 2024 | TBD |

### Posesiones e Infraestructura

| Variable | Descripción | Años Presentes | Nulos (%) | Tipo Categórico | Acción | Estado | Advertencia | Nota | Column Label (Latest) | Value Label (Latest) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SH25F** | Has a computer | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |
| **SH25H** | Has internet access at home | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |
| **SH26A** | Number of rooms in the household | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | Posible re-clasificación a Numérico Continuo | English Meta Column (2007-2008) | TBD |
| **SH2601** | Use other type of fuel for cooking | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |
| **SH2602** | Type of other fuel used for cooking | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |
| **SH2604** | Does household buys fuel for cooking | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |
| **SH2605** | A household member fetches the fuel | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |
| **SH2606** | How long does it take to go and come back to fetch fuel | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |
| **SH2607** | Frequency to fetch fuel | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |
| **SH2609** | Type of light used by household | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |
| **SH27CA** | Dwelling has windows | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |
| **SH27CB** | Windows with glass | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |
| **SH27CC** | Wood windows | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |
| **SH27CD** | Windows with screens | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |
| **SH27CE** | Windows with curtains/blinds | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |
| **SH2801** | Any household member rents land for agricultural use | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |
| **SH28D** | Any other transportation type (horses, peque-peque, etc) | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |
| **SH28EE** | Could you be evicted from dwelling | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |
| **SH51A** | Tiene sofá | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | TBD | Meta Column 2009 | TBD |
| **HV207** | Has radio (Tiene radio) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV208** | Has television (Tiene televisión) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV209** | Has refrigerator (Tiene refrigerador) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV210** | Has bicycle (Tiene bicicleta) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV211** | Has motorcycle/scooter (Tiene motocicleta) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV212** | Has car/truck (Tiene carro o camión) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV213** | Main floor material (Material predominante en el piso) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV214** | Main wall material (Material predominante en la pared) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV215** | Main roof material (Material predominante en el techo) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV216** | Rooms used for sleeping (Habitaciones para dormir) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Posible Numérico | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV221** | Has telephone (Tiene teléfono) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV226** | Type of cooking fuel (Tipo de combustible para cocinar) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV227** | Have bednet for sleeping (Tiene mosquitero para dormir) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV239** | Food cooked on stove or open fire (Lugar de preparación de alimentos) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV240** | Household has a chimney, hood or neither (Tiene chimenea o campana) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV241** | Food cooked in the house / in separate building / outdoors (Ubicación de cocina) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV242** | Household has separate room used as kitchen (Cuarto separado para cocinar) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV243A** | Has a mobile telephone (Tiene celular) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV243B** | Has a watch (Tiene reloj) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV243C** | Has an animal-drawn cart (Tiene carreta jalada por animales) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV243D** | Has a boat with a motor (Tiene bote a motor) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HML1** | Number of mosquito nets (Número de mosquiteros) | 18 años (2007-2024) | TBD | Metadato Administrativo/Vacío | Eliminar columna (100% de nulos en todos los años) | DROP | ¡Columna completamente vacía durante 18 años! 100% nulos. | Valores Estables (Vacío histórico) | No aplica (Eliminar) | TBD |
| **HML1A** | Number of mosquito nets with specific information (Número de mosquiteros con información específica) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Posible Numérico | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **SH51B** | Tiene vitrina/aparado | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | TBD | Meta Column 2009 | TBD |
| **SH51C** | Tiene repostero | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | TBD | Meta Column 2009 | TBD |
| **SH51D** | Tiene cómoda/ropero | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | TBD | Meta Column 2009 | TBD |
| **SH51E** | Tiene reloj de pared | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | TBD | Meta Column 2009 | TBD |
| **SH51J** | Tiene televisión por cable | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | TBD | Meta Column 2009 | TBD |
| **SH51K** | Tiene licuadora | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | TBD | Meta Column 2009 | TBD |
| **SH51L** | Tiene cocina a gas | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | TBD | Meta Column 2009 | TBD |
| **SH51M** | Tiene cocina a kerosene | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | TBD | Meta Column 2009 | TBD |
| **SH51N** | Tiene microondas | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | TBD | Meta Column 2009 | TBD |
| **SH51O** | Tiene lavadora | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | TBD | Meta Column 2009 | TBD |
| **SH51P** | Tiene computadora | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH25F | Meta Column 2009 | TBD |
| **SH51Q** | Tiene acceso a Internet en casa | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH25H | Meta Column 2009 | TBD |
| **SH51R** | Tiene bomba de agua | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | TBD | Meta Column 2009 | TBD |
| **SH51S** | Tiene generador de electricidad | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | TBD | Meta Column 2009 | TBD |
| **SH53** | Usa otro tipo de combustible para cocinar | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH2601 | Meta Column 2009 | TBD |
| **SH54** | Tipo de otro combustible usado para cocinar | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH2602 | Meta Column 2009 | TBD |
| **SH61** | Número de habitaciones en el hogar | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | Posible Numérico. Equivalente a SH26A | Meta Column 2009 | TBD |
| **SH61A** | Has a sofa (¿Tiene sofá?) | 15 años (2010-2024) | TBD | Binario (0/1) | Mapear a Value Label -> Label Encoding | KEEP |   | Valores Estables (Mutación solo traducción) | Meta Column 2024 | TBD |
| **SH61B** | Has a cabinet (¿Tiene vitrina/aparador?) | 15 años (2010-2024) | TBD | Binario (0/1) | Mapear a Value Label -> Label Encoding | KEEP |   | Valores Estables (Mutación solo traducción) | Meta Column 2024 | TBD |
| **SH61C** | Has a shelf (¿Tiene repostero?) | 15 años (2010-2024) | TBD | Binario (0/1) | Mapear a Value Label -> Label Encoding | KEEP |   | Valores Estables (Mutación solo traducción) | Meta Column 2024 | TBD |
| **SH61D** | Has a wardrobe (¿Tiene cómoda/ropero?) | 15 años (2010-2024) | TBD | Binario (0/1) | Mapear a Value Label -> Label Encoding | KEEP |   | Valores Estables (Mutación solo traducción) | Meta Column 2024 | TBD |
| **SH61E** | Has a wall's clock (¿Tiene reloj de pared?) | 15 años (2010-2024) | TBD | Binario (0/1) | Mapear a Value Label -> Label Encoding | KEEP |   | Valores Estables (Mutación solo traducción) | Meta Column 2024 | TBD |
| **SH61J** | Has a cable television (¿Tiene televisión por cable?) | 15 años (2010-2024) | TBD | Binario (0/1) | Mapear a Value Label -> Label Encoding | KEEP |   | Valores Estables (Mutación solo traducción) | Meta Column 2024 | TBD |
| **SH61K** | Has a blender (¿Tiene licuadora?) | 15 años (2010-2024) | TBD | Binario (0/1) | Mapear a Value Label -> Label Encoding | KEEP |   | Valores Estables (Mutación solo traducción) | Meta Column 2024 | TBD |
| **SH61L** | Has a gas cooker (¿Tiene cocina de gas?) | 15 años (2010-2024) | TBD | Binario (0/1) | Mapear a Value Label -> Label Encoding | KEEP |   | Valores Estables (Mutación solo traducción) | Meta Column 2024 | TBD |
| **SH61M** | Has a kerosen cooker (¿Tiene cocina de kerosene?) | 15 años (2010-2024) | TBD | Binario (0/1) | Mapear a Value Label -> Label Encoding | KEEP |   | Valores Estables (Mutación solo traducción) | Meta Column 2024 | TBD |
| **SH61N** | Has a microwave (¿Tiene microondas?) | 15 años (2010-2024) | TBD | Binario (0/1) | Mapear a Value Label -> Label Encoding | KEEP |   | Valores Estables (Mutación solo traducción) | Meta Column 2024 | TBD |
| **SH61O** | Has a washing machine (¿Tiene lavadora?) | 15 años (2010-2024) | TBD | Binario (0/1) | Mapear a Value Label -> Label Encoding | KEEP |   | Valores Estables (Mutación solo traducción) | Meta Column 2024 | TBD |
| **SH61P** | Has a computer (¿Tiene computadora?) | 15 años (2010-2024) | TBD | Binario (0/1) | Mapear a Value Label -> Label Encoding | KEEP |   | Valores Estables (Mutación solo traducción) | Meta Column 2024 | TBD |
| **SH61Q** | Has internet access at home (¿Tiene acceso a Internet en casa?) | 15 años (2010-2024) | TBD | Binario (0/1) | Mapear a Value Label -> Label Encoding | KEEP |   | Valores Estables (Mutación solo traducción) | Meta Column 2024 | TBD |
| **SH61R** | Has a water pump (¿Tiene bomba de agua?) | 15 años (2010-2024) | TBD | Binario (0/1) | Mapear a Value Label -> Label Encoding | KEEP |   | Valores Estables (Mutación solo traducción) | Meta Column 2024 | TBD |
| **SH61S** | Has a electricity generator (¿Tiene generador de electricidad?) | 15 años (2010-2024) | TBD | Binario (0/1) | Mapear a Value Label -> Label Encoding | KEEP |   | Valores Estables (Mutación solo traducción) | Meta Column 2024 | TBD |
| **SH62** | Número de habitaciones para dormir | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | Posible Numérico | Meta Column 2009 | TBD |
| **SH63** | Use other type of fuel for cooking (¿Utiliza otro tipo de combustible para cocinar?) | 16 años (2009-2024) | TBD | Binario (0/1) | Mapear a Value Label -> Label Encoding | KEEP |   | Valores Estables (Mutación solo traducción) | Meta Column 2024 | TBD |
| **SH64** | Type of other fuel used for cooking (Otro tipo de combustible utilizado para cocinar) | 15 años (2010-2024) | TBD | Categórico Nominal con NS/NR | Mapear a Value Label -> Reemplazar texto Otro por NaN -> Imputar -> One-Hot Encoding | KEEP | ¡Códigos 4.0 (Biogás) y 95.0 (No cocina) desaparecieron en 2019+! Riesgo de generar NaNs masivos. | Valores Mutados (Códigos eliminados) | Construir Súper Diccionario | TBD |
| **SH66** | Kitchen has a chimney (¿La cocina tiene una chimenea o un mecanismo para eliminar el humo?) | 15 años (2010-2024) | TBD | Binario con NS/NR (0/1/6) | Reemplazar 6.0 por NaN -> Mapear a Value Label -> Imputar -> Label Encoding | KEEP | Código 6.0 (Otro) desapareció en 2019+. Se vuelve NaN antes del mapeo. | Valores Mutados (Código eliminado) | Meta Column 2024 | TBD |
| **SH67A** | Vivienda tiene ventanas | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH27CA | Meta Column 2009 | TBD |
| **SH67B** | Ventanas con vidrios | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH27CB | Meta Column 2009 | TBD |
| **SH67C** | Ventanas de madera | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH27CC | Meta Column 2009 | TBD |
| **SH67D** | Ventanas mallas | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH27CD | Meta Column 2009 | TBD |
| **SH67E** | Ventanas con cortinas o persianas | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH27CE | Meta Column 2009 | TBD |
| **SH68F** | Otro medio de transporte (caballos, peque-peque, etc) | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH28D | Meta Column 2009 | TBD |
| **SH69** | Does household buys fuel for cooking (¿El hogar compra combustible para cocinar?) | 16 años (2009-2024) | TBD | Binario con NS/NR (0/1/8) | Reemplazar 8.0 por NaN -> Mapear a Value Label -> Imputar -> Label Encoding | KEEP |   | Valores Estables (Mutación solo traducción) | Meta Column 2024 | TBD |
| **SH70** | Type of light used by household (¿Qué tipo de alumbrado utiliza el hogar?) | 16 años (2009-2024) | TBD | Especial (Columna Bipolar) | Dividir en 2: Hectareas(2009, Numérico con top-coding 5010) y Fuente_Luz(2010+, Categórica) | SPLIT | ¡Columna reciclada! -> COMBINAR Fuente_Luz(2010+) con SH60_Fuente_Luz(2009). | Valores Mutados (Reciclaje de columna) | No aplica (División manual en Python) | TBD |
| **SH71** | Number of rooms in the household (Número de habitaciones en el hogar) | 15 años (2010-2024) | TBD | TBD | TBD | KEEP | TBD | Posible Numérico. Equivalente a SH61 (2009) / SH26A (2007-08). | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **SH72** | Number of rooms for sleeping (Número de habitaciones para dormir) | 15 años (2010-2024) | TBD | TBD | TBD | KEEP | TBD | Posible Numérico. Equivalente a SH62 (2009) / HV216. | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **SH73** | Tiene mosquitero para dormir | 1 año (2010) | TBD | TBD | TBD | KEEP | TBD | TBD | Meta Column 2010 | TBD |
| **SH76D** | Windows with screens (Ventanas con malla) | 14 años (2011-2024) | TBD | Binario (0/1) | Mapear a Value Label -> Label Encoding | KEEP |   | Valores Estables (Mutación solo traducción) | Meta Column 2024 | TBD |
| **SH76E** | Windows with curtains/blinds (Ventanas con cortinas/persianas) | 14 años (2011-2024) | TBD | Binario (0/1) | Mapear a Value Label -> Label Encoding | KEEP |   | Valores Estables (Mutación solo traducción) | Meta Column 2024 | TBD |
| **SH77A** | Vivienda tiene ventanas | 1 año (2010) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH67A / SH27CA | Meta Column 2010 | TBD |
| **SH77B** | Ventanas con vidrios | 1 año (2010) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH67B / SH27CB | Meta Column 2010 | TBD |
| **SH77C** | Ventanas de madera | 1 año (2010) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH67C / SH27CC | Meta Column 2010 | TBD |
| **SH77D** | Ventanas mallas | 1 año (2010) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH67D / SH27CD | Meta Column 2010 | TBD |
| **SH77E** | Ventanas con cortinas o persianas | 1 año (2010) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH67E / SH27CE | Meta Column 2010 | TBD |
| **SH77F** | Any other transportation type (Otro tipo de transporte: caballos, peque-peque, etc) | 14 años (2011-2024) | TBD | Binario (0/1) | Mapear a Value Label -> Label Encoding | KEEP |   | Valores Estables (Mutación solo traducción) | Meta Column 2024 | TBD |
| **SH78** | Any household member rents land for agricultural use (¿Miembro del hogar es dueño de tierras agrícolas?) | 14 años (2011-2024) | TBD | Binario con NS/NR (0/1/8) | Reemplazar 8.0 por NaN -> Mapear a Value Label -> Imputar -> Label Encoding | KEEP | ¡Pregunta duplicada! COMBINAR con HV244 (Dueño de tierras agrícolas). Códigos 8.0 son faltantes. | Valores Estables (Mutación solo traducción) | Meta Column 2024 | TBD |
| **SH78F** | Otro medio de transporte (caballos, peque-peque, etc) | 1 año (2010) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH68F / SH28D | Meta Column 2010 | TBD |

### Salud y Nutrición en el Hogar

| Variable | Descripción | Años Presentes | Nulos (%) | Tipo Categórico | Acción | Estado | Advertencia | Nota | Column Label (Latest) | Value Label (Latest) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SH107** | Prueba de Yodo | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | TBD | Meta Column 2009 | TBD |
| **SH108U** | Visualización de la bolsa de sal | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | TBD | Meta Column 2009 | TBD |
| **SH108** | Marca de sal usada por el hogar | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | TBD | Meta Column 2009 | TBD |
| **SH124** | Prueba de Yodo | 1 año (2010) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH107 | Meta Column 2010 | TBD |
| **SH125U** | Visualización de la bolsa de sal | 1 año (2010) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH108U | Meta Column 2010 | TBD |
| **SH125** | Marca de sal usada por el hogar | 1 año (2010) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH108 | Meta Column 2010 | TBD |
| **SH224** | Test of Iodine (Prueba de Yodo) | 14 años (2011-2024) | TBD | Especial (Columna Bipolar) | Recodificar numéricamente (1->0, 2->7, 3->15, 4->30) y COMBINAR con HV234 | SPLIT | ¡Diccionario 2019-2022 destrozado! Mezclaron los códigos categóricos con los numéricos. | Valores Mutados (Diccionario corrupto) | No aplica (Recodificación manual) | TBD |
| **SH225U** | Visualización de la bolsa de sal | 14 años (2011-2024) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH125U / SH108U | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **SH225** | Salt brand used by household (Marca de sal usada por el hogar) | 14 años (2011-2024) | TBD | Categórico Nominal | Eliminar columna (Exceso de dimensionalidad y redundante con la prueba de Yodo real) | DROP | ¡Peligro de colisión! El código 1.0 significa marcas totalmente distintas según el año. Generaría ruido en el modelo. | Valores Mutados (Diccionario superpuesto) | No aplica (Eliminar) | TBD |
| **HV228** | Children under 5 slept under bednet last night (Niños bajo mosquitero) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV234** | Test salt for Iodine (Prueba de yodo para sal) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV248** | Number of sick people 18-59 (Número de personas enfermas 18-59) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Posible Numérico | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV249** | Member of the HH died last 12 months (Miembro del hogar fallecido) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | CORE - Error de Traducción Histórico | Tradujeron Household dejándolo como 'HH' en 2018-2024 ('Miembro de la HH'). | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV250** | Number of members who died last 12 months (Número de miembros fallecidos) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Posible Numérico | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV251** | Number of orphans and vulnerable children (Número de huérfanos) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Posible Numérico | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HML2** | Number of children under bednet previous night (Niños bajo mosquitero) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | CORE - Error de Traducción Histórico | Error INEI (2019-2024): Omitieron 'mosquitero' en el label ('niños en la noche anterior'). | Meta Column 2024 y English Meta Column (~2017) | TBD |

### Programas Sociales

| Variable | Descripción | Años Presentes | Nulos (%) | Tipo Categórico | Acción | Estado | Advertencia | Nota | Column Label (Latest) | Value Label (Latest) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **QH90** | Algún miembro beneficiario de Prog. Juntos? | 1 año (2013) | TBD | TBD | TBD | KEEP | TBD | TBD | Meta Column 2013 | TBD |
| **QH90A** | Nº orden de la persona | 1 año (2013) | TBD | TBD | TBD | KEEP | TBD | Relacionado a QH90 | Meta Column 2013 | TBD |
| **QH91D** | Día de acuerdo de compromiso | 1 año (2013) | TBD | TBD | TBD | KEEP | TBD | Relacionado a QH90 | Meta Column 2013 | TBD |
| **QH91M** | Mes de acuerdo de compromiso | 1 año (2013) | TBD | TBD | TBD | KEEP | TBD | Relacionado a QH90 | Meta Column 2013 | TBD |
| **QH91Y** | Año de acuerdo de compromiso | 1 año (2013) | TBD | TBD | TBD | KEEP | TBD | Relacionado a QH90 | Meta Column 2013 | TBD |
| **QH93** | Algún miembro beneficiario de pensión 65 | 1 año (2013) | TBD | TBD | TBD | KEEP | TBD | TBD | Meta Column 2013 | TBD |
| **QH94A** | Pensión 65 persona 1 | 1 año (2013) | TBD | TBD | TBD | KEEP | TBD | Relacionado a QH93 | Meta Column 2013 | TBD |
| **QH94AB** | Alguien más? | 1 año (2013) | TBD | TBD | TBD | KEEP | TBD | Relacionado a QH93 | Meta Column 2013 | TBD |
| **QH94B** | Pensión 65 persona 2 | 1 año (2013) | TBD | TBD | TBD | KEEP | TBD | Relacionado a QH93 | Meta Column 2013 | TBD |
| **QH94BB** | Alguien más? | 1 año (2013) | TBD | TBD | TBD | KEEP | TBD | Relacionado a QH93 | Meta Column 2013 | TBD |
| **QH94C** | Pensión 65 persona 3 | 1 año (2013) | TBD | TBD | TBD | KEEP | TBD | Relacionado a QH93 | Meta Column 2013 | TBD |
| **QH94CB** | Alguien más? | 1 año (2013) | TBD | TBD | TBD | KEEP | TBD | Relacionado a QH93 | Meta Column 2013 | TBD |
| **QH94D** | Pensión 65 persona 4 | 1 año (2013) | TBD | TBD | TBD | KEEP | TBD | Relacionado a QH93 | Meta Column 2013 | TBD |

---

## Infraestructura y Socioeconomía (CORE)

| Variable | Descripción | Años Presentes | Nulos (%) | Tipo | Acción | Estado | Advertencia | Nota | Column Label (Latest) | Value Label (Latest) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SHWLTHI2** | Wealth Index -2000 | 1 año (2010) | TBD | TBD | TBD | KEEP | TBD | Índice de Riqueza base 2000. Complementa a HV270. | Meta Column 2010 | TBD |
| **SHWLTHF2** | Wealth Index Score - 2000 | 1 año (2010) | TBD | TBD | TBD | KEEP | TBD | Score de Riqueza base 2000. Complementa a HV271. | Meta Column 2010 | TBD |
| **hv270** | Wealth index | 1 año (2016) | TBD | TBD | TBD | KEEP | CORE - Reemplaza a HV270 en 2016 | Quintil de Riqueza CORE | English Meta Column (~2017) | TBD |
| **hv271** | Wealth index factor score (5 decimals) | 2 años (2015-2016) | TBD | TBD | TBD | KEEP | CORE - Reemplaza a HV271 en 2015-2016 | Score de Riqueza Numérico Continuo | English Meta Column (~2017) | TBD |
| **HV206** | Has electricity (Tiene electricidad) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV217** | Relationship structure (Estructura de relación) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV219** | Sex of head of household (Sexo del jefe del hogar) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV220** | Age of head of household (Edad del jefe del hogar) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Posible Numérico | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **SHTOTH** | Households in dwelling (Hogares en la vivienda) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Posible Numérico | Meta Column 2024 y English Meta Column (~2017) | TBD |

---

## Numéricos (sin label)

### Economía y Gastos

| Variable | Descripción | Años Presentes | Nulos (%) | Tipo | Acción | Estado | Advertencia | Nota | Column Label (Latest) | Value Label (Latest) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SH2211** | Water bill average (1 decimal) | 2 años (2007-2008) | TBD | Numérico Pseudo-Categórico | Dividir entre 10, tratar 401.0 como techo (401+), reemplazar 999.6/999.8 por NaN | SPLIT | ¡Top-coding (4010=401+) y 1 decimal implícito! | Valores Estables | English Meta Column (2007-2008) | English Meta Column (2007-2008) |
| **SH28BB** | Hectares owned by household members (1 decimal) | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |
| **SH79** | Hectares owned by household members (Cuantas hectareas) | 15 años (2010-2024) | TBD | Especial (Columna Bipolar) | Dividir en 2: Pregunta_Binaria(2010, Categórica) y Hectareas(2011+, Numérica con top-coding 5010) | SPLIT | ¡Columna reciclada! -> COMBINAR Hectareas(2011+) con SH70_Hectareas(2009). | Valores Mutados (Reciclaje de columna) | No aplica (División manual en Python) | TBD |
| **SH80** | Hectáreas de propiedad de miembros del hogar (1 decimal) | 1 año (2010) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH28BB | Meta Column 2010 | TBD |
| **HV244** | Own land usable for agriculture (Dueño de tierras agrícolas) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV245** | Hectares for agricultural land (Hectáreas de tierras agrícolas) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Posible Numérico / Equivalente madre de SH80 y SH28BB | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV246** | Livestock, herds or farm animals (Dueño de ganado/animales) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV246A** | Cattle own (Cantidad de ganado) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Posible Numérico | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV246B** | Cows, bulls own (Cantidad de vacas, toros) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Posible Numérico | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV246C** | Horses, donkeys, mules own (Cantidad de caballos, burros, mulas) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Posible Numérico | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV246D** | Goats own (Cantidad de cabras) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Posible Numérico | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV246E** | Sheep own (Cantidad de ovejas) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Posible Numérico | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV246F** | Chickens own (Cantidad de pollos) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Posible Numérico | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV246G** | Poultry own (Cantidad de aves de corral) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Posible Numérico | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV246H** | Cuyes/rabits own (Cantidad de cuyes/conejos) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Posible Numérico | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV246I** | Pigs own (Cantidad de cerdos) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Posible Numérico | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV246J** | Other own (Cantidad de otros animales) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Posible Numérico | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV246K** | CS own (Cantidad de animal CS) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Posible Numérico | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV247** | Owns a bank account (Posee una cuenta bancaria) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV270** | Wealth index (Índice de riqueza) | 17 años (2007-2015, 2017-2024) | TBD | TBD | TBD | KEEP | CORE - Variable Crítica / Falta 2016 | En 2016 usar 'hv270'. | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV271** | Wealth index factor score (5 decimals) (Factor de puntuación del índice de riqueza) | 16 años (2007-2014, 2017-2024) | TBD | TBD | TBD | KEEP | CORE - Numérico Crítico / Faltan 2015 y 2016 | En 2015 y 2016 usar 'hv271'. | Meta Column 2024 y English Meta Column (~2017) | TBD |

---

## Geografía y Ubicación

| Variable | Descripción | Años Presentes | Nulos (%) | Tipo | Acción | Estado | Advertencia | Nota | Column Label (Latest) | Value Label (Latest) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **HV026** | Place of residence (Lugar de residencia) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV040** | Cluster altitude in meters (Altitud del conglomerado en metros) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Numérico | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **SHREGION** | Región natural | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE Geografía Local | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **SHPROVIN** | Province (Provincia) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE Geografía Local | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **SHDISTRI** | District (Distrito) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE Geografía Local | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **UBIGEO** | Ubigeo (Código de Ubicación Geográfica) | 5 años (2020-2024) | TBD | TBD | TBD | KEEP | TBD | Variable Nacional Geográfica | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **SH2802** | Household would remain in dwelling for 5 or more years | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |
| **SH2803** | How long is household planning to move | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |

---

## Identificadores

### Llaves Primarias y Extranjeras

| Variable | Descripción | Años Presentes | Nulos (%) | Tipo | Acción | Estado | Advertencia | Nota | Column Label (Latest) | Value Label (Latest) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ID1** | Año | 6 años (2019-2024) | TBD | TBD | TBD | KEEP | Identificador | CORE - Año de recolección | Meta Column 2024 | TBD |
| **HHID** | Case Identification (Identificación del Hogar) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | Llave Primaria - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |

---

## Metadatos

### Contexto de la Encuesta

| Variable | Descripción | Años Presentes | Nulos (%) | Tipo | Acción | Estado | Advertencia | Nota | Column Label (Latest) | Value Label (Latest) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SHVER** | Version of questionnaire (Versión del cuestionario) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE Local | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **SHTRIMES** | Data collection round number | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |
| **SH31H** | Time HH interview ends (hour) | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |
| **SH31M** | Time HH interview ends (minutes) | 2 años (2007-2008) | TBD | TBD | TBD | KEEP | TBD | TBD | English Meta Column (2007-2008) | TBD |
| **SH81H** | Hora que termino la entrevista en el hogar (horas) | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH31H | Meta Column 2009 | TBD |
| **SH81M** | Hora que termino la entrevista en el hogar(minutos) | 1 año (2009) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH31M | Meta Column 2009 | TBD |
| **SH90H** | Hora que termino la entrevista en el hogar (horas) | 1 año (2010) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH81H / SH31H | Meta Column 2010 | TBD |
| **SH90M** | Hora que termino la entrevista en el hogar(minutos) | 1 año (2010) | TBD | TBD | TBD | KEEP | TBD | Equivalente a SH81M / SH31M | Meta Column 2010 | TBD |
| **SH82H** | Time HH interview ends (hour) (Hora que termino la entrevista en el hogar - horas) | 7 años (2011-2017) | TBD | TBD | TBD | KEEP | Variable de Auditoría / Falta desde 2018 | Equivalente a SH90H (2010) / SH81H (2009) / SH31H (2007-08). | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **SH82M** | Time HH interview ends (minutes) (Hora que termino la entrevista en el hogar - minutos) | 7 años (2011-2017) | TBD | TBD | TBD | KEEP | Variable de Auditoría / Falta desde 2018 | Equivalente a SH90M (2010) / SH81M (2009) / SH31M (2007-08). | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **HV218** | Line number of head of househ. (Número de línea del jefe de hogar) | 18 años (2007-2024) | TBD | TBD | TBD | KEEP | TBD | CORE - Mutación de label | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **SHEQUIPO** | Field work team (Equipo de trabajo de campo) | 16 años (2007-2022) | TBD | Metadato Administrativo | Eliminar columna (Exceso de dimensionalidad y no aporta valor predictivo) | DROP | Identificador del grupo de encuestadores del INEI. Genera ruido. | Valores Estables (Aumento de equipos por año) | No aplica (Eliminar) | TBD |
| **SH01H** | Time HH interview begins (hour) (Hora que comenzó la entrevista en el hogar - horas) | 11 años (2007-2017) | TBD | TBD | TBD | KEEP | TBD | Variable de Auditoría / Falta desde 2018 | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **SH01M** | Time HH interview begins (minutes) (Hora que comenzó la entrevista en el hogar - minutos) | 11 años (2007-2017) | TBD | TBD | TBD | KEEP | TBD | Variable de Auditoría / Falta desde 2018 | Meta Column 2024 y English Meta Column (~2017) | TBD |
| **SHSEMES** | Data collection round number / Semestre | 16 años (2009-2024) | TBD | TBD | TBD | KEEP | CORE Local de Recolección | Complementa y continúa a SHTRIMES (2007-2008). | Meta Column 2024 y English Meta Column (~2017) | TBD |

| **SXH73** | TBD | TBD | TBD | Binario (0/1) | Mapear a Value Label -> Label Encoding | KEEP |   | Valores Estables (Mutación solo traducción) | TBD | Meta Column 2024 |
| **SH76A** | TBD | TBD | TBD | Binario con NS/NR (0/1/8) | Reemplazar 8.0 por NaN -> Mapear a Value Label -> Imputar -> Label Encoding | KEEP | Códigos 8.0 son faltantes (NS). | Valores Estables (Mutación solo traducción) | TBD | Meta Column 2024 |
| **SH76B** | TBD | TBD | TBD | Binario (0/1) | Mapear a Value Label -> Label Encoding | KEEP |   | Valores Estables (Mutación solo traducción) | TBD | Meta Column 2024 |
| **SH76C** | TBD | TBD | TBD | Binario (0/1) | Mapear a Value Label -> Label Encoding | KEEP |   | Valores Estables (Mutación solo traducción) | TBD | Meta Column 2024 |
