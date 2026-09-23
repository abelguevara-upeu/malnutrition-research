# Diccionario Metodológico y Justificación de Variables

Este documento es un registro vivo (*living document*) diseñado para facilitar la redacción de la sección de **Metodología** y **Selección de Características (Feature Selection)** de tu futuro artículo científico. Aquí documentamos el *porqué* epidemiológico y técnico detrás de la inclusión de cada variable de la ENDES/DHS, dejándolo listo para que luego agreguemos las citas bibliográficas correspondientes.

---

## Módulo Antropometría (RECH6 - El Diagnóstico)
*Contiene la variable objetivo (Target) y mediciones clínicas del menor de 5 años.*

| Variable | Descripción | Justificación Metodológica | Cita Pendiente |
| :--- | :--- | :--- | :--- |
| **`HC70`** | Z-score Talla/Edad | **Variable Objetivo (Target Principal).** Es el indicador estándar de oro (OMS) para medir la **Desnutrición Crónica Infantil** (Stunting), la cual refleja privaciones nutricionales a largo plazo y susceptibilidad a infecciones recurrentes. | *[Citar: Patrones de Crecimiento OMS 2006 / Ficha Técnica INEI]* |
| **`HC71`** | Z-score Peso/Edad | Indicador de Desnutrición Global. Se retiene para análisis complementarios o control de sesgos (Underweight). | |
| **`HC72`** | Z-score Peso/Talla | Indicador de Desnutrición Aguda (Wasting). Refleja pérdidas de peso recientes y severas. | |
| **`HC73`** | Z-score IMC/Edad | Índice de Masa Corporal. Vital para investigar escenarios de *Doble Carga de Malnutrición* (coexistencia de desnutrición crónica y sobrepeso). | |
| **`HC0`** | N° de línea del niño | **Llave Técnica.** Necesaria para enlazar el diagnóstico clínico del niño con su registro demográfico en el *Roster* del hogar (`HVIDX`). | *[Manual DHS de Recodificación]* |

---

## Módulo Roster / Miembros del Hogar (RECH1 - La Demografía)
*Define la elegibilidad, la identidad demográfica y el árbol genealógico del hogar.*

| Variable | Descripción | Justificación Metodológica | Cita Pendiente |
| :--- | :--- | :--- | :--- |
| **`HV103`** | Durmió anoche en casa | **Criterio de Inclusión Estricto.** El INEI exige que el niño haya dormido en la vivienda encuestada la noche anterior para ser considerado residente de facto y evitar sesgos de medición en poblaciones flotantes. | *[Citar: Programas Presupuestales INEI - Ficha Técnica]* |
| **`HV104`** | Sexo | Covariable biológica fundamental. La literatura señala diferencias sistemáticas en el riesgo de desnutrición según el sexo del menor debido a factores fisiológicos o sesgos de cuidado por género. | *[Citar: Estudios de determinantes de desnutrición]* |
| **`HV105`** | Edad en años | Determinante crítico. La prevalencia de la desnutrición crónica es acumulativa y se vuelve irreversible habitualmente después de los 2 años de edad ("Los primeros 1000 días"). | *[Citar: The Lancet Maternal and Child Nutrition Series]* |
| **`HV101`** | Relación con el Jefe de Hogar | Indicador proxy de estructura familiar. Niños que no son hijos directos del jefe de hogar (ej. nietos u otros parientes) pueden enfrentar dinámicas intrafamiliares de distribución de recursos distintas. | |
| **`HV112`** | Línea de la madre biológica | **Llave de Trazabilidad Materna.** Permite mapear al niño con los datos de salud, educación y empoderamiento de su madre en el módulo de Mujeres (MEF), variables que son de los predictores socioeconómicos más fuertes de desnutrición. | |
| **`HVIDX`** | N° de línea (Índice) | **Llave Técnica.** Se empareja con `HC0` para consolidar el join demográfico. | |

---

## Módulo Vivienda / Entorno (RECH0 - Determinantes Estructurales)
*(Sección en construcción. Se actualizará conforme se finalice el EDA de este módulo).*

* **Nota de análisis prospectivo:** Se priorizarán variables de infraestructura de saneamiento (agua, tipo de desagüe, material del piso), ya que la literatura epidemiológica establece un vínculo causal directo entre saneamiento deficiente, enfermedades diarreicas repetitivas, malabsorción de nutrientes (enteropatía ambiental) y el estancamiento del crecimiento lineal (Stunting).

---
> **Comentario de Arquitectura:**  
> Mantener este listado limpio no solo te facilita la escritura del *paper*, sino que durante el modelado predictivo (Machine Learning), esto te servirá como el documento de **"Feature Dictionary"** para explicar la importancia y el peso de cada variable a la hora de interpretar tu modelo.
