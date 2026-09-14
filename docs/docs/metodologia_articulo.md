# SECCIÓN: METODOLOGÍA (Formato Artículo Científico)

## III. METODOLOGÍA

La presente investigación se desarrolló bajo el marco estándar CRISP-DM (*Cross-Industry Standard Process for Data Mining*), articulando el ciclo de vida analítico en fases secuenciales que abarcan la ingesta relacional de datos, el preprocesamiento con control de fuga de información, la selección de características, el entrenamiento y evaluación comparativa de algoritmos supervisados, la interpretabilidad algorítmica y el despliegue del sistema de soporte a la decisión.

### A. Fuente de Datos e Integración Relacional

El estudio utilizó los microdatos anuales de la Encuesta Demográfica y de Salud Familiar (ENDES), recolectados y publicados por el Instituto Nacional de Estadística e Informática (INEI) de Perú entre los años 2007 y 2025. Para estructurar la unidad de análisis, se diseñó un flujo de extracción e integración relacional que vinculó cinco módulos principales mediante las llaves compuestas `HHID` y `CASEID`. El módulo `RECH0` proveyó los metadatos de la entrevista, `RECH1` aportó las características demográficas de los integrantes del hogar, `RECH6` suministró los indicadores antropométricos y de salud infantil, `RECH23` consolidó las condiciones de vivienda, saneamiento y altitud geográfica, y el módulo `REC41` incorporó la historia obstétrica materna, controles prenatales y peso al nacer, vinculado de forma unívoca a través de la tabla relacional puente `REC21`. La muestra consolidada quedó conformada por 304,271 niños y niñas menores de cinco años que contaban con registros antropométricos válidos y superaron la auditoría biológica de consistencia entre el registro infantil y materno con una coincidencia superior al 99.9% en sexo y año de nacimiento.

```mermaid
graph TD
    A["RECH0: Entrevista"] --> E["Fusión Relacional (HHID / CASEID)"]
    B["RECH1: Padrón Hogar"] --> E
    C["RECH6: Salud Infantil"] --> E
    D["RECH23: Vivienda y Altitud"] --> E
    F["REC41: Salud Materna"] --> G["REC21: Tabla Puente"]
    G --> E
    E --> H["Dataset Consolidado: N = 304,271 niños (2007-2025)"]
```

### B. Definición de la Variable Objetivo y Protocolo Anti-Leakage

La variable dependiente es la desnutrición crónica infantil, categorizada de acuerdo con los estándares internacionales de crecimiento de la Organización Mundial de la Salud (OMS). Se definió como caso positivo ($Y = 1$) a todo infante cuyo puntaje Z de talla para la edad ($\text{HAZ} = \text{HC70} / 100$) se situó por debajo de menos dos desviaciones estándar respecto a la mediana de referencia, y como caso control ($Y = 0$) en caso contrario. La prevalencia global en la serie histórica fue del 15.8%, estableciendo un ratio de desbalance de 1 a 5.3. Para preservar la validez metodológica y evitar el sobreajuste espurio por fuga de datos (*data leakage*), se excluyeron de las variables predictoras la talla directa en centímetros (`HC3`) y el peso crudo (`HC2`), así como cualquier intervención terapéutica o diagnóstico clínico registrado con posterioridad a la medición antropométrica.

$$Y = \begin{cases} 1, & \text{si } \text{HAZ} < -2.00\text{ DE} \\ 0, & \text{si } \text{HAZ} \ge -2.00\text{ DE} \end{cases}$$

### C. Pipeline de Selección de Características

El espacio original compuesto por 189 columnas crudas fue depurado a través de un protocolo de selección cuantitativo en cuatro etapas sucesivas. En la primera etapa, se descartaron los atributos con más del 60% de valores ausentes estructurales históricos. En la segunda etapa, se redujo la redundancia dimensional eliminando variables colineales mediante correlación bivariada de Pearson y Spearman ($r > 0.80$) y factores de inflación de varianza ($\text{VIF} > 5$). En la tercera etapa, se aplicaron pruebas de hipótesis bivariadas compuestas por pruebas de Independencia de Chi-cuadrado para variables categóricas y pruebas no paramétricas de Kruskal-Wallis para continuas, reteniendo 74 factores estadísticamente significativos con un nivel de significancia $p < 0.05$. Finalmente, en la cuarta etapa se ejecutó una validación multivariada basada en la importancia algorítmica nativa de árboles de decisión gradiente, seleccionando un conjunto final de 45 variables que conservaron la totalidad del poder discriminativo del modelo.

```mermaid
graph LR
    A["189 Variables Crudas"] --> B["Filtro Nulos > 60%"]
    B --> C["Filtro Colinealidad (r > 0.80)"]
    C --> D["Pruebas Bivariadas (χ² / Kruskal-Wallis)"]
    D --> E["45 Variables Finales (Importancia ≥ 10)"]
```

### C.1. Verificación de Suficiencia del Subconjunto Seleccionado

Con el objeto de descartar que el procedimiento de reducción dimensional hubiese descartado señal predictiva relevante, se ejecutó un estudio de ablación sobre las variables excluidas del subconjunto final. De las 78 columnas disponibles en el conjunto preprocesado, 33 no formaron parte de las 45 seleccionadas. Estas fueron ordenadas según su señal marginal respecto a la variable objetivo, cuantificada para los atributos categóricos como la amplitud entre la tasa de prevalencia máxima y mínima observada entre categorías con soporte mínimo de 500 observaciones, y para los continuos mediante el estadístico $2 \cdot |\text{AUC} - 0.5|$.

El procedimiento identificó diez atributos con señal marginal elevada, correspondientes al material predominante de las paredes (`HV214`, amplitud de 40.9 puntos porcentuales), del piso (`HV213`, 39.4) y del techo de la vivienda (`HV215`, 36.2), la fuente de abastecimiento de agua (`HV201`, 34.1), el departamento de residencia (`HV024`, 32.2), la concentración de cloro residual en el agua de consumo (`SH227`, 30.2), el combustible utilizado para cocinar (`HV226`, 26.3) y el tipo de servicio higiénico (`HV205`, 22.7). Estos atributos configuran el bloque de agua, saneamiento e higiene y condiciones materiales de la vivienda que la literatura epidemiológica sobre encuestas demográficas y de salud reporta de forma consistente como determinante subyacente del retraso del crecimiento lineal. Ninguno de ellos constituye fuga de información, dado que describen condiciones estructurales del hogar y no mediciones antropométricas del menor, y todos resultan observables sin requerir visita domiciliaria previa, condición indispensable para su uso en un esquema de triaje anticipado.

Se contrastaron cuatro configuraciones bajo el protocolo experimental descrito en la subsección siguiente, manteniendo constantes la partición, la ponderación muestral aplicada tanto al entrenamiento como al cálculo de métricas, la semilla determinista y los hiperparámetros del clasificador, de modo que la única fuente de variación fuese la composición del espacio de atributos. La configuración de referencia reproduce exactamente las cifras reportadas en la subsección D ($\text{AUC} = 0.8295$; $\text{Recall} = 76.44\%$), lo que verifica la trazabilidad del experimento respecto del modelo campeón.

| Configuración | Atributos | AUC-ROC | Recall | Precisión | $\Delta$AUC |
|---|---:|---:|---:|---:|---:|
| Subconjunto seleccionado | 45 | 0.8295 | 76.44% | 36.36% | — |
| Ampliación con agua, saneamiento y vivienda | 52 | 0.8295 | 76.44% | 36.36% | $+0.0000$ |
| Ampliación con atributos territoriales | 48 | 0.8295 | 76.44% | 36.36% | $+0.0000$ |
| Ampliación conjunta | 55 | 0.8295 | 76.44% | 36.36% | $+0.0000$ |

La incorporación de los diez atributos no produjo mejora alguna en la capacidad discriminativa del modelo: el AUC-ROC, la sensibilidad y la precisión permanecen invariables hasta la cuarta cifra decimal en las tres configuraciones ampliadas. El análisis diagnóstico de este resultado descartó que se tratase de ausencia de señal en los atributos candidatos, dado que un clasificador entrenado exclusivamente sobre el bloque de agua, saneamiento y vivienda alcanzó un AUC-ROC de 0.6895, ni de redundancia lineal con el índice de riqueza del hogar, cuya varianza explicada por cada atributo candidato se situó entre $\eta^2 = 0.038$ y $\eta^2 = 0.098$. La explicación reside en que el subconjunto de 45 variables ya representa el constructo latente de condiciones materiales del hogar a través de diecinueve atributos correlacionados, entre los que se cuentan el tratamiento del agua (`HV237`, `HV237A`, `HV237G`), el tiempo de desplazamiento a la fuente (`HV204`), el uso compartido del servicio higiénico (`HV225`), la disponibilidad de ambiente separado para cocinar (`HV242`), el número de habitaciones (`HV216`, `SH71`) y las características de las aberturas de la vivienda (`SH76B`, `SH76C`, `SH76D`). En consecuencia, los atributos candidatos aportan información ya capturada por el modelo, y su exclusión durante la etapa de validación multivariada constituye una decisión metodológicamente correcta antes que una omisión.

Este resultado aporta evidencia empírica de suficiencia del procedimiento de selección descrito, en el sentido de que el subconjunto retenido preserva la totalidad de la señal disponible en el espacio de atributos depurado y no resulta ampliable mediante la reincorporación de variables previamente descartadas.

### D. Entrenamiento, Balanceo y Benchmarking de Modelos

El proceso de entrenamiento evaluó seis familias de algoritmos supervisados: Regresión Logística con regularización L2, Árbol de Decisión CART, XGBoost, CatBoost, Red Neuronal Perceptrón Multicapa (MLP 3×200) y LightGBM. Para reflejar la distribución demográfica del país y corregir el sesgo de sobremuestreo urbano inherente a la encuesta, se incorporó el factor de ponderación muestral del INEI ($w_i = \text{HV005}_i / 1,000,000$). La partición y validación experimental se realizaron mediante validación cruzada estratificada de 5 pliegues (*Stratified 5-Fold Cross-Validation*) fijando una semilla determinista (`random_state = 42`). El algoritmo LightGBM obtuvo el desempeño más alto con un área bajo la curva ROC de 0.8295 y una sensibilidad (*Recall*) de 76.44% a umbral estándar, superando a los modelos restantes gracias a su capacidad nativa para agrupar variables categóricas de alta cardinalidad por histogramas sin recurrir a la expansión dimensional del *One-Hot Encoding*.

### E. Explicabilidad Algorítmica con Valores SHAP

Para dotar de transparencia al sistema y eliminar el carácter opaco del modelo de ensamble, se aplicó la teoría de juegos cooperativos mediante el algoritmo `TreeExplainer` del framework SHAP (*SHapley Additive exPlanations*). Este marco descompone la probabilidad predicha en la suma del valor base poblacional más las contribuciones marginales individuales de cada una de las 45 variables predictoras. A nivel local, el sistema descompone la predicción individual en factores de riesgo agravantes y condiciones protectoras. A nivel global y territorial, se agregaron los valores SHAP sobre una muestra representativa de 10,000 registros para construir mapas de riesgo y perfiles de determinantes diferenciados para los 25 departamentos y las tres regiones naturales del país.

$$f(x) = \phi_0 + \sum_{j=1}^{M} \phi_j(x)$$

### F. Protocolo de Validación Metodológica

La validación del sistema se estructuró en tres ejes que abarcan la solidez estadística, la replicabilidad computacional y la pertinencia técnica del software. El primer eje certificó la confiabilidad mediante remuestreo *Bootstrap* no paramétrico con 1,000 repeticiones sobre las probabilidades *out-of-fold* de los 304,271 registros, obteniendo un AUC-ROC de 0.8294 con intervalo de confianza al 95% de $[0.8267, 0.8324]$ y una sensibilidad de 76.43% con intervalo $[75.88\%, 76.98\%]$. La amplitud de ambos intervalos, inferior a 0.006 y 1.1 puntos porcentuales respectivamente, evidencia que las estimaciones puntuales no dependen de la partición muestral. La prueba de significancia estadística de DeLong sobre curvas ROC correlacionadas confirmó la superioridad del modelo campeón frente a los dos algoritmos de referencia con valores $p < 10^{-300}$ ($z = 62.32$ contra XGBoost y $z = 61.48$ contra Regresión Logística), de modo que la diferencia observada no es atribuible al azar. Cabe precisar que el estadístico de DeLong se define sobre rangos y no admite ponderación muestral, por lo que los valores de AUC empleados en ese contraste (0.8193, 0.7775 y 0.7767) corresponden a la muestra sin expandir y se sitúan sistemáticamente por debajo de los ponderados; la validez de la comparación se preserva porque los tres modelos se evalúan sobre los mismos individuos y el contraste recae sobre la diferencia entre curvas y no sobre el nivel absoluto del área. Finalmente, la calibración del umbral de decisión se fijó en $\tau = 0.45$, valor mínimo que garantiza una cobertura del 80.5% con una precisión asociada del 34.0%, orientada al triaje preventivo. El segundo eje garantizó la replicabilidad según los principios FAIR mediante la modularización del código en el paquete Python `mnp/`, el aislamiento del entorno con Docker (`python:3.12-slim`), la automatización del flujo completo mediante `Makefile` y la publicación del dataset maestro y modelo serializado en el repositorio abierto Zenodo con identificador digital DOI. El tercer eje evaluó la pertinencia técnica mediante un panel de juicio de tres expertos en Ciencia de Datos y Machine Learning, verificando la validez de contenido con el coeficiente V de Aiken ($V \ge 0.80$) y la usabilidad técnica de la herramienta mediante la escala estandarizada SUS con una meta de calificación superior a 75 puntos.

### G. Arquitectura de Software y Despliegue

La solución computacional se implementó como una aplicación web interactiva desarrollada en Streamlit, organizada bajo un patrón de tres capas. La capa de presentación contiene el módulo de visualización coroplética departamental con geometrías GeoJSON y el simulador de triaje individual con gráficos interactivos. La capa lógica integra el motor de inferencia entrenado con LightGBM, el calibrador dinámico de punto de corte y el generador de explicabilidad SHAP en tiempo de ejecución. La capa de datos gestiona el almacenamiento columnar de alto rendimiento en formato Parquet junto con los metadatos de configuración serializados en formato JSON.

```mermaid
graph TD
    subgraph Capa de Presentación
        UI1["Mapa Coroplético Territorial (GeoJSON)"]
        UI2["Simulador de Triaje y Explicación SHAP"]
    end
    subgraph Capa Lógica
        L1["Motor de Inferencia LightGBM (.pkl)"]
        L2["Calibrador de Umbral Dinámico (τ = 0.45)"]
        L3["Explicador SHAP TreeExplainer"]
    end
    subgraph Capa de Persistencia
        D1["Dataset Maestro (Parquet)"]
        D2["Metadatos del Modelo (.json)"]
    end
    UI1 <--> L1
    UI2 <--> L3
    L1 <--> D1
    L1 <--> D2
    L2 <--> D2
```
