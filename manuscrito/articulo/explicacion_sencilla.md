# El artículo explicado en palabras sencillas

Esta guía resume qué dice cada parte del artículo (`art-prisma.tex`) sin lenguaje técnico, para poder explicarlo en una reunión o en la sustentación.

## La idea en una frase

Usamos datos de una encuesta nacional para entrenar un programa que señala qué niños tienen más riesgo de desnutrición crónica, explica por qué, y lo pusimos en una aplicación web que profesionales de salud evaluaron como útil.

## 1. Introducción: el problema

- La **desnutrición crónica** es cuando un niño mide menos de lo que debería para su edad. Afecta su desarrollo de por vida.
- En el Perú bajó mucho entre 2007 y 2017 (de 29 % a 13 %), pero **desde 2018 se estancó en torno al 12 %**. Las estrategias de siempre ya no la bajan más.
- La brecha sigue: en el campo afecta a 1 de cada 5 niños; en la ciudad, a menos de 1 de cada 10.
- **Nuestra propuesta:** en lugar de esperar a medir a cada niño, usar sus datos (nacimiento, madre, hogar) para saber a quién conviene priorizar.

## 2. Metodología: qué hicimos

Seguimos cinco fases ordenadas (el método se llama CRISP-DM). Están dibujadas en la Figura 1.

### Comprensión de los datos

- Usamos la **ENDES**, la encuesta de salud que el INEI hace cada año en todo el país. Tomamos 19 años (2007–2025).
- La encuesta viene repartida en varias tablas (hogar, niño, madre). Las unimos y obtuvimos **304,271 niños menores de 5 años** (Figura 2).
- Definimos qué es un caso: un niño con desnutrición crónica según la tabla de la OMS.
- Quitamos los datos que serían "trampa", como la talla del niño: si el programa la viera, adivinaría la respuesta sin aprender nada útil.

### Preparación de los datos

- Limpiamos los datos: códigos como "no sabe" pasaron a "dato faltante" y unificamos códigos que cambiaron entre años.
- De 189 datos posibles por niño nos quedamos con **45** en cuatro filtros: quitar los que casi siempre faltan, los repetidos, los que no se relacionan con la desnutrición y los que menos ayudan (Tabla de variables).
- Comprobamos que no dejamos fuera nada importante: al volver a agregar las variables descartadas, el resultado no cambió.

### Modelado

- **Desbalance:** hay 5 niños sanos por cada niño con desnutrición. Si no se corrige, el programa aprende a decir siempre "sano" y acierta mucho, pero no sirve. Le indicamos que **equivocarse con un niño desnutrido cuesta más** que equivocarse con uno sano.
- **Factor de expansión:** la encuesta entrevista más hogares en unas zonas que en otras. Este factor corrige eso para que los resultados representen a todo el país. No es lo mismo que el desbalance.
- Probamos **6 programas** distintos (algoritmos), desde uno simple hasta una red neuronal.

### Evaluación

- Para no hacernos trampa, cada programa se entrenó con una parte de los niños y se probó con otra que no había visto. Se repitió 5 veces con grupos distintos y se promedió.
- Medimos varias cosas: cuántos casos detecta, cuántos de los señalados de verdad tienen desnutrición, y cuánto acierta en general.
- Usamos **SHAP**, una técnica que dice qué datos de cada niño subieron o bajaron su puntaje. Así el programa no es una caja negra.

### Despliegue

- Hicimos una **aplicación web** donde se evalúa un niño o una lista de niños de un archivo Excel (Figura 3).
- **Cuatro profesionales de salud** (tres nutricionistas y un enfermero) la probaron y respondieron un cuestionario basado en el modelo TAM, que mide si una tecnología se percibe útil y fácil de usar.

## 3. Resultados: qué encontramos

| Resultado | En palabras sencillas | Dónde está |
| --- | --- | --- |
| La muestra | Más desnutrición en el campo (31 %) que en la ciudad (9 %), y en la Sierra (26 %) que en Lima (5 %) | Tabla de la muestra, Figura 4 |
| El mejor programa | **LightGBM** fue el que mejor distinguió a los niños en riesgo | Tabla de modelos |
| Cuántos detecta | De cada 100 niños con desnutrición, encuentra **80** | Tabla de confiabilidad |
| Cuántos falsos avisos | De cada 3 niños que señala, **1** de verdad tiene desnutrición. Para priorizar visitas es aceptable: es mejor revisar de más que dejar a un niño sin atención | Tabla de confiabilidad |
| Los otros programas | Dos de ellos parecían buenos, pero solo encontraban a 3 de cada 10 niños | Tabla de modelos, Figura 5 |
| Los factores principales | Pobreza del hogar, bajo peso al nacer, altitud y tamaño pequeño al nacer | Figura 7 |
| Cada niño | La aplicación muestra qué datos de ese niño suben su riesgo | Figura 8 |
| Cada departamento | Los factores cambian por zona: en Puno pesa más la altitud; en Huancavelica, el intervalo entre partos | Figura 9 |
| La aplicación | Funciona con un niño o con una lista; con 300 niños reales marcó 100 como prioridad | Figura 10 |
| El panel | Todos los aspectos con nota de 4 o más sobre 5; nota global de 9 sobre 10 | Tabla del panel |

## 4. Discusión: qué significa

- Nuestro resultado es parecido al de estudios en Etiopía, Zambia y Ruanda, pero con muchos más niños y años.
- Los factores que encontró el programa coinciden con lo que ya se sabe sobre las causas de la desnutrición, lo que da confianza.
- El programa muestra **asociaciones, no causas**: que la altitud pese no significa que la altitud cause la desnutrición.
- **Limitaciones** (lo que no pudimos hacer):
    - La encuesta mira a cada niño una sola vez, no lo sigue en el tiempo.
    - No probamos el programa entrenando con unos años y evaluando con otros.
    - El índice de pobreza se calcula distinto cada año.
    - Cuatro profesionales son pocos para generalizar su opinión.

## 5. Conclusiones

- Es posible priorizar a los niños en riesgo con datos que ya existen, sin medirlos a todos primero.
- La herramienta sirve para **ordenar a quién atender primero**, no para diagnosticar. El diagnóstico sigue siendo medir talla y edad.
- A futuro: probarla por periodos, corregir el índice de pobreza, usar datos de los establecimientos de salud y ampliarla al sobrepeso y la anemia.

## Glosario rápido

| Término | Qué significa |
| --- | --- |
| AUC-ROC | Qué tan bien separa el programa a niños con y sin desnutrición. 0.5 es adivinar al azar; 1 es perfecto. El nuestro: 0.83 |
| Sensibilidad | De los niños que sí tienen desnutrición, cuántos encuentra (80 %) |
| Precisión | De los niños que señala, cuántos de verdad la tienen (34 %) |
| Umbral | El puntaje a partir del cual un niño se marca como prioridad. Usamos 45 de 100 |
| Validación cruzada | Probar el programa 5 veces con niños que no vio al entrenar |
| SHAP | Técnica que explica qué datos subieron o bajaron el puntaje de cada niño |
| TAM | Cuestionario estándar para medir si una tecnología se percibe útil y fácil de usar |
