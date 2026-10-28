# Tablas y figuras del artículo y su justificación

El manuscrito tiene 7 tablas y 10 figuras. Cada una se cita en el texto y responde a un componente del esquema que recomendó el asesor a partir del mapeo de 21 artículos.

## Tablas de Metodología

| Tabla | Contenido | Por qué va |
| --- | --- | --- |
| Variables predictoras por dominio | Las 45 variables del modelo en cinco dominios (niño; madre, embarazo y lactancia; hogar y territorio; agua y saneamiento; vivienda), con su código ENDES | El esquema pide definir las variables "idealmente en una tabla": 18 de los 21 artículos lo hacen. Permite saber qué datos usa el modelo y comprobar que ninguna es posterior a la medición (fuga de información) |
| Configuración de los algoritmos | Hiperparámetros de los seis modelos (iteraciones, profundidad, pesos de clase, semilla) | Hace el experimento reproducible y muestra cómo cada modelo trató el desbalance. 7 de los 21 artículos detallan los hiperparámetros |
| Constructos del instrumento | Los 8 constructos de TAM, TAM2 y TAM3, su modelo de origen y el número de ítems | Justifica el instrumento del panel: cada pregunta proviene de una escala publicada |

## Tablas de Resultados

| Tabla | Contenido | Por qué va |
| --- | --- | --- |
| Características de la muestra | 304,271 niños por sexo, área, región natural y edad, con prevalencia simple y ponderada | 13 de los 21 artículos abren Resultados con la muestra. Muestra dónde se concentra la desnutrición (rural 30.7 %, Sierra 26.2 %) y que la ponderación casi no cambia la prevalencia (15.8 % frente a 16.2 %) |
| Desempeño de los seis algoritmos | AUC-ROC, AUC-PR, sensibilidad, precisión, especificidad y F1, media (DE) en cinco pliegues; mejor valor en negrita | Presente en los 18 artículos de machine learning. Justifica la elección de LightGBM: mayor AUC-ROC (0.8297), sensibilidad (76.4 %) y F1 (49.3 %) |
| Métricas con intervalos de confianza | AUC-ROC, sensibilidad, precisión y F1 de LightGBM con IC 95 % por bootstrap (1,000 repeticiones) | Demuestra que el resultado es estable. Solo 7 de los 21 artículos lo reportan; el asesor lo marcó como rasgo de los artículos recientes, incluido JEEEMI |
| Valoración del panel por constructo | Mediana, rango intercuartílico y acuerdo por constructo, más la valoración global (9 de 10) | Resultado de la evaluación con usuarios; el esquema la pide como último apartado de Resultados |

La tabla de la verificación de suficiencia (cuatro filas idénticas) se retiró: su resultado cabe en una frase.

## Figuras de Metodología

| Figura | Contenido | Por qué va |
| --- | --- | --- |
| 1. Flujo metodológico | Las cinco fases de CRISP-DM y los diez pasos del estudio | Ordena la Metodología: sus fases son los títulos de las subsecciones, como pidió el asesor |
| 2. Integración de la ENDES | Cómo se unieron los cinco módulos de la encuesta con HHID y CASEID | Explica cómo se construyó la base de 304,271 niños a partir de datos crudos dispersos en varios módulos |
| 3. Arquitectura del sistema | Las tres capas de la aplicación: presentación, lógica y datos | Describe el despliegue y que el usuario solo ingresa datos, sin manipular el modelo |

## Figuras de Resultados

| Figura | Contenido | Por qué va |
| --- | --- | --- |
| 4. Tendencia de la prevalencia | Prevalencia ponderada nacional, rural y urbana, 2007–2025 | Muestra el estancamiento en torno al 12 % desde 2018 y la brecha rural, que motivan el estudio |
| 5. Curvas ROC | Curvas ROC de los seis algoritmos | Compara visualmente la discriminación de los modelos; 5 de los 21 artículos la incluyen |
| 6. Matriz de confusión | Aciertos y errores de LightGBM con el umbral de 0.5 | Muestra cuántos niños con y sin desnutrición clasifica bien el modelo; 8 de los 21 artículos la incluyen |
| 7. Importancia global SHAP | Las 15 variables con mayor peso en el modelo | Responde qué factores se asocian más al riesgo; solo 2 de los 21 artículos usan SHAP, lo que distingue al estudio |
| 8. Explicación local | Contribución de cada variable en un perfil de riesgo alto | Muestra cómo la aplicación explica el resultado de un niño concreto |
| 9. Factores por departamento | Peso relativo de los diez factores principales en cada departamento | Sustenta la focalización territorial: los factores cambian entre departamentos |
| 10. Pantallas de la aplicación (pendiente) | Evaluación individual y de un grupo de niños | El asesor pidió mostrar el sistema desplegado en Resultados |
