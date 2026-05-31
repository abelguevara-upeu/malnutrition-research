# Propuesta de Enfoque Académico: Ingeniería de Sistemas

Este documento redefine el alcance del proyecto para darle una estructura sólida, publicable y defendible frente a un jurado de **Ingeniería de Sistemas**, corrigiendo los excesos teóricos del PPI original.

## 1. El Problema Computacional (Problem Statement)
**Enfoque erróneo (Salud):** "Identificar qué factores sociales causan la desnutrición crónica en niños."
**Enfoque Ingenieril:** "Las bases de datos gubernamentales longitudinales (como la ENDES, 2007-2024) presentan desafíos computacionales severos para el modelado predictivo: **alta dimensionalidad, extrema escasez de datos (sparsity), ruido histórico y un desbalance de clases profundo** (minoría crítica de casos de desnutrición). Los modelos paramétricos tradicionales son ineficientes ante estas anomalías."

## 2. El Aporte de Ingeniería: El Sistema Sociodemográfico y Estructural
La contribución de este artículo no es el descubrimiento médico per se, sino el **desarrollo de un Sistema Predictivo Sociodemográfico y Estructural** capaz de sortear los obstáculos computacionales mencionados. 

Aunque internamente este sistema funciona gracias a una robusta tubería de datos (Pipeline ETL / MLOps), académicamente lo presentaremos como un "Sistema Integral" compuesto por:

### A. Arquitectura de Ingesta y Normalización de Datos
Sistema automatizado (ETL) que normaliza 18 años de datos fragmentados en un esquema relacional unificado.
### B. Ingeniería de Representaciones (Feature Engineering)
Estrategias de imputación algorítmica para manejar nulos y codificación de variables estructurales (saneamiento, vivienda) y sociodemográficas (identidad, factores maternos).
### C. Algoritmos Conscientes del Desbalance
Implementación de técnicas adaptativas (SMOTE, Cost-Sensitive Learning) para forzar al modelo a no ignorar a la minoría de niños desnutridos.
### D. Inteligencia Artificial Explicable (XAI)
Uso de herramientas matemáticas (ej. **SHAP Values**) para demostrar el peso de los determinantes estructurales, generando confianza (Trustworthy AI).

> **Nota de Flexibilidad Empírica:** Las técnicas mencionadas (ej. SMOTE, SHAP, modelos Tree-based) representan el estándar de la industria propuesto para este tipo de desafíos. Sin embargo, en estricto rigor al método científico, la arquitectura final será dinámica y dependerá de lo que los datos dictaminen durante el Análisis Exploratorio (EDA). No nos cerramos a una única técnica algorítmica si el comportamiento estructural de los datos exige otra solución técnica óptima.

---

## 3. Notas Críticas sobre el PPI Legacy (Por qué cambiamos el rumbo)
El PPI original proponía arquitecturas como Redes Neuronales de Grafos (GNN), Autoencoders (dGAE), Modelos Bayesianos CAR-BYM y un enfoque puramente "Geográfico".
* **El problema de lo "Geográfico":** Para usar modelos puramente espaciales bayesianos se requieren coordenadas exactas (Lat/Lon). La ENDES las desplaza por privacidad. El enfoque correcto y flexible es tratar el territorio como un "Determinante Estructural/Sociodemográfico" a nivel distrital o departamental, sin atarnos a una topología espacial estricta si los datos no lo permiten.
* **Por qué es un error usar Deep Learning aquí:** Esas arquitecturas están diseñadas para texto secuencial o imágenes. La base de datos de la ENDES es puramente **Tabular Heterogénea**. En la industria, las Redes Neuronales suelen sufrir de *overfitting* masivo frente a ensambles basados en árboles (Tree-based models como XGBoost o LightGBM) cuando se trata de datos tabulares.

---

## 4. Defensa de Tesis: "¿Cuál es mi aporte ingenieril si uso modelos ya hechos?"
Es muy común que pregunten: *"Si solo vas a importar un modelo que ya existe, ¿cuál es tu aporte como ingeniero?"*. Esta es la respuesta:

> **"El aporte de un Ingeniero de Sistemas en Applied Machine Learning no es inventar un nuevo algoritmo matemático desde cero, sino diseñar la Arquitectura del Sistema que hace que el algoritmo funcione y escale en el mundo real."**

El "modelo predictivo" matemático es solo el 5% del código. El **95% restante es pura ingeniería de software y datos**: procesar gigabytes de microdatos históricos, ensamblar complejas relaciones de bases de datos mediante llaves foráneas, optimizar el uso de memoria e inyectar esos datos masivos en un sistema que evalúe y explique sus predicciones. 

---

## 5. El Aporte a la Ciencia y la Verdadera "Innovación"
En Ingeniería de Sistemas y Ciencia de Datos aplicada, debes defender lo siguiente:

### ¿Cuál es el aporte a la ciencia?
Tu aporte científico se enmarca en la **Informática de la Salud (Health Informatics)**. Aportas **Evidencia Empírica y Escalabilidad Metodológica**. Demuestras que un marco computacional puede procesar 18 años de datos sociodemográficos complejos y extraer patrones predictivos que los métodos estadísticos tradicionales (usados por el Estado) no pueden ver por el volumen de los datos.

### ¿Qué tiene de "Innovador"?
Mucha gente confunde innovar con "crear algoritmos matemáticos desde cero". En la ingeniería moderna, la innovación es la **Integración**. Tu innovación radica en:
1. **La Arquitectura End-to-End:** Tomar datos públicos crudos y transformarlos en un sistema inteligente.
2. **Explicabilidad (XAI):** Aplicar IA Explicable en el contexto de salud pública en Perú. Pasar de simples cuadros de Excel a Sistemas Predictivos Estructurales Interpretables **es una innovación tecnológica absoluta** en este dominio.
