# Decisiones de Limpieza - RECH0 (Características del Hogar)

Este documento centraliza todas las decisiones de limpieza, estandarización e imputación para las variables del módulo RECH0 a lo largo de los 18 años (2007-2024), aplicando estrictamente el Protocolo de Auditoría Longitudinal ENDES.

## Matriz de Auditoría y Decisiones

| Variable | Categoría Temática | Descripción | Años Presentes | Nulos (%) | Tipo | Acción | Estado | Advertencia | Nota | Column Label (Latest) | Value Label (Latest) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `HV005A` | Diseño Muestral / Ponderación | Factor de expansión departamental | 2008 (1 año) | - | - | - | - | `Aislada` | - | Sample weight Departamental (2008) | - |
| `ID1` | Metadato Administrativo | Año de la encuesta | 2010-2016, 2019-2024 (13 años) | - | - | - | - | `Valores Estables` | - | Año (2024) | - |
| `HV005X` | Diseño Muestral / Ponderación | Factor de ponderación niño menor de 5 años | 2015 (1 año) | - | - | - | - | `Aislada` | - | Factor de ponderación niño menor de 5 años 2015 (2015) | - |
| `hv022` | Diseño Muestral / Estrato | Estrato de muestreo | 2016 (1 año) | - | - | - | - | `Error INEI` | Posible error tipográfico de la minúscula de `HV022`. | Estrato (2016) | - |
| `codccpp` | Geografía / Ubicación | Código de centro poblado | 2016-2017 (2 años) | - | - | - | - | `Aislada` | - | Codigo de centro poblado (2017) | - |
| `nomccpp` | Geografía / Ubicación | Nombre de centro poblado | 2016-2017 (2 años) | - | - | - | - | `Aislada` | - | Nombre de centro poblado (2017) | - |
| `long_ccpp` | Geografía / Coordenadas | Longitud geográfica | 2017 (1 año) | - | - | - | - | `Aislada` | - | Longitud (2017) | - |
| `lat_ccpp` | Geografía / Coordenadas | Latitud geográfica | 2017 (1 año) | - | - | - | - | `Aislada` | - | Latitud (2017) | - |
| `HV023` | Sociodemográfico | Dominio | 2007-2024 | 0.0% | Categórico Nominal | **DROP** | Colinealidad perfecta con Región (`HV024`). Redundante. | `Valores Estables` | Descartar tras asegurar que Región está limpia. | Dominio | N/A |
| `HV024` | Sociodemográfico | Región | 2007-2024 | 0.0% | Categórico Nominal | **KEEP** | Región geográfica fundamental. | `CORE ESTRUCTURAL` | Identificador base geográfico. | Región | N/A |
| `HV025` | Sociodemográfico | Área de residencia | 2007-2024 | 0.0% | Categórico Nominal | **KEEP** | Subdivisión Urbano/Rural. | `CORE ESTRUCTURAL` | Clave para estratificación. | Tipo de lugar de residencia | 1.0 (Urbano), 2.0 (Rural) |
| `HV026` | Sociodemográfico | Lugar de residencia | 2007-2024 | 0.0% - 10.1% (2008) | Categórico Nominal | **KEEP** | Subdivisión detallada de urbanización. | `Valores Estables` | **Falsos Numéricos/Nulos:** Tiene 10% nulos solo en 2008. Imputar condicionalmente basándose en `HV025`. | Lugar de residencia | N/A |
| `HV022` | Sociodemográfico | Estrato | 2007-2024 | 0.0% | Categórico Nominal | **COALESCE** | Subdivisión administrativa. Sufrió Schema Drift en 2016 (`hv022`). | `CORE ESTRUCTURAL` | Fusionar con `hv022` para garantizar cobertura de 18 años. | Estrato | N/A |
| `HV015` | Control de Calidad | Resultado de la entrevista | 2007-2024 | 0.0% | Categórico Nominal | **KEEP** / **FILTER** | Código de status de la encuesta. | `CORE` | **Filtro vital:** Filtrar para conservar SOLO el código 1.0 (Completa). | Resultado de la entrevista | 1.0 (Completa) |
| `HV020` | Control de Calidad | Criterio de elegibilidad | 2007-2024 | 0.0% | Categórico Nominal | **DROP** | Metadato administrativo. | `Valores Estables` | Ruido operativo, eliminar. | N/A | N/A |
| `HV027` | Control de Calidad | Selección hombre/esposo | 2007-2024 | 0.0% | Categórico Nominal | **DROP** | Flag de submuestra. | `Valores Estables` | Ruido operativo. | N/A | N/A |
| `HV042` | Control de Calidad | Selección medición hemoglobina | 2007-2024 | 0.0% | Categórico Nominal | **DROP** | Flag de submuestra. | `Valores Estables` | Ruido operativo. | N/A | N/A |
| `HV043` | Control de Calidad | Módulo mujeres estado | 2007-2024 | 0.0% | Categórico Nominal | **DROP** | Flag de submuestra. | `Valores Estables` | Ruido operativo. | N/A | N/A |
| `HV044` | Control de Calidad | Módulo violencia familiar | 2007-2024 | 0.0% | Categórico Nominal | **DROP** | Flag de submuestra. | `Valores Estables` | Ruido operativo. | N/A | N/A |
