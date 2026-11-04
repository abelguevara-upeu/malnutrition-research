# El artículo explicado párrafo por párrafo

Esta guía resume qué dice cada parte de `art-prisma.tex` y explica los términos que pueden confundir. Sirve para preparar una reunión o una sustentación.

## La idea en una frase

Usamos datos de una encuesta nacional para entrenar un modelo que señala qué niños tienen más riesgo de desnutrición crónica, explica por qué, y lo pusimos en una aplicación web que evaluaron profesionales de salud.

## Introducción

- **Problema:** la desnutrición crónica afecta el desarrollo de por vida.
- **Perú:** bajó mucho, pero desde 2018 se mantiene alrededor del 12 %.
- **Vacío:** los estudios previos suelen usar una sola ronda de la encuesta, reportan sobre todo la exactitud y no ofrecen una herramienta.
- **Objetivo:** predecir el riesgo y analizar los factores por departamento.

## Metodología

**Inicio:** el estudio siguió CRISP-DM. El problema está en la Introducción y aquí van las otras cinco fases.

- **CRISP-DM:** guía de pasos para proyectos de datos.

### Comprensión de los datos

1. **Fuente y unión:** se unieron cinco módulos de la ENDES y se obtuvieron 304,271 niños.
    - **Módulo:** cada tabla de la encuesta.
    - **Llaves (`HHID`, `CASEID`):** códigos que permiten unir las tablas.
2. **Qué es un caso:** desnutrición crónica si la talla para la edad está por debajo de −2 DE. Los casos son 15.8 % de la muestra.
    - **Puntaje Z o DE:** cuánto se aleja la talla del niño de la referencia OMS.
    - **Desbalance 1:5.3:** por cada caso hay 5.3 niños sin desnutrición.
    - **Fuga de datos:** dar al modelo información que revela la respuesta, como la talla.
    - **HV103:** indica si el niño durmió en el hogar la noche anterior. No se filtró, y el efecto es mínimo.
3. **Variables:** las 45 se agrupan en cinco dominios.
    - **Dominio:** grupo de variables, como vivienda o madre.

### Preparación de los datos

1. **Limpieza:** se unificaron códigos entre años.
2. **Faltantes:** "no sabe" pasó a dato faltante.
    - **Imputar con la mediana:** llenar un dato numérico faltante con el valor central.
    - **Estandarizar:** poner las variables en una escala comparable.
3. **Selección en cuatro etapas:** de 189 columnas a 74 y luego a 45.
    - **Correlación y VIF:** detectan variables que dicen casi lo mismo.
    - **Chi-cuadrado y Kruskal-Wallis:** prueban si una variable se relaciona con la desnutrición.
    - **p < 0.05:** es poco probable que esa relación sea casualidad.
4. **Verificación:** se volvieron a agregar variables descartadas para comprobar que no se perdió algo útil.
    - **`2|AUC − 0.5|`:** mide cuánto separa una variable por sí sola; 0 significa que no separa.

### Modelado

1. **Pesos de clase:** equivocarse con un niño desnutrido cuesta más.
2. **Sin SMOTE:** no se inventaron casos. SMOTE crea registros artificiales.
3. **Factor de expansión:** cada niño cuenta según a cuántos representa. No corrige el desbalance.
4. **Seis algoritmos:** se compararon en igualdad de condiciones.
    - **Ensamble de árboles:** muchos árboles de decisión combinados.
    - **Hiperparámetros:** ajustes fijados antes de entrenar.
    - **Semilla (`random_state`):** hace que el resultado se pueda repetir.
5. **Umbral:** puntaje desde el cual un niño es prioridad. El puntaje sirve para ordenar: 0.45 no significa 45 % de riesgo.

### Evaluación

1. **Métricas:**
    - **Fuera de pliegue:** cada niño se evalúa con un modelo que no lo vio.
    - **AUC-ROC:** capacidad de separar casos y no casos; 0.5 es azar y 1 es perfecto.
    - **Bootstrap:** repite el cálculo con muestras al azar para obtener el IC 95 %.
    - **DeLong:** comprueba si dos AUC realmente difieren.
2. **SHAP:** indica cuánto subió o bajó cada variable el puntaje de un niño.

### Despliegue

1. **Aplicación:** tiene pantalla, lógica y datos.
    - **Coroplético:** mapa pintado por departamento.
2. **Reproducibilidad:** código y modelo en Zenodo.
    - **FAIR:** datos y código fáciles de hallar y reutilizar.
3. **Panel:** cuatro profesionales.
    - **TAM2:** modelo que mide si una tecnología se percibe útil y fácil de usar.
    - **Constructo:** tema medido con varias preguntas.
    - **Likert:** escala de 1 a 5.
    - **Mediana y RIC:** valor central y rango del 50 % central de las respuestas.

## Resultados

1. **Muestra:** prevalencia ponderada de 16.2 % en los 19 años. Es mayor en zona rural y Sierra.
2. **Tendencia:** bajó de 29.2 % a 13.0 %, y desde 2018 ronda 12 %. El 16.2 % es de todo el periodo; el 12 % es por año.
3. **Selección:** agregar diez variables no mejoró el modelo.
    - **η²:** parte de la variación explicada.
4. **Comparación:** LightGBM tuvo el mejor equilibrio.
    - **Sensibilidad:** casos que detecta.
    - **Precisión:** señalados que realmente son casos.
    - **Especificidad:** niños sin desnutrición bien clasificados.
    - **F1:** equilibrio entre sensibilidad y precisión.
    - **AUC-PR:** como el AUC, pero centrado en los casos.
5. **Curvas ROC y matriz:** comparan modelos y muestran aciertos y errores.
    - **Quinto pliegue:** uno de los cinco grupos de validación.
6. **Confiabilidad:** con 0.45, detecta 80.46 % de los casos.
    - **Excluir hemoglobina:** el AUC casi no cambia.
7. **Explicabilidad:** pobreza, peso al nacer, altitud y tamaño al nacer pesan más.
    - **Perfil sintético:** niño de ejemplo, no real.
8. **Sistema:** evalúa uno o varios niños y muestra el mapa.
9. **Panel:** todas las medianas fueron de 4 o más.

## Discusión

1. **Comparación con otros estudios:** una exactitud alta puede engañar si hay pocos casos.
    - **Kappa:** acuerdo más allá del azar.
    - **Exactitud:** total de aciertos; sube aunque el modelo casi no marque casos.
2. **Precisión aceptable:** revisar de más cuesta menos que dejar sin atención a un niño.
    - **Triaje:** ordenar a quién atender primero.
3. **Factores:** coinciden con las causas conocidas, pero son asociaciones, no causas.
4. **Estancamiento:** refuerza la utilidad de focalizar recursos.
5. **Panel:** buena valoración, pero la adopción real depende de cada organización.
6. **Limitaciones:**
    - **Transversal:** mide a cada niño una sola vez.
    - **Validación por periodos:** entrenar con unos años y probar con otros; no se hizo.

## Conclusiones

1. **Hallazgos:** LightGBM y sus factores principales.
2. **Aplicación y futuro:** apoya la priorización, no el diagnóstico.

## Por qué solo prevalencia ponderada

La ENDES no selecciona a todos con la misma probabilidad. El factor de expansión permite estimar la situación del país, y la ficha técnica del INEI calcula así el indicador oficial. El 15.8 % sin ponderar solo describe el desbalance de los datos usados para entrenar.
