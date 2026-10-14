# Pendientes (no ejecutados)

Dos temas que salieron de la validación con el panel y de la revisión de datos. Ninguno está
aplicado: el modelo, los datos y la app siguen como en el commit `587b99d`.

## 1. Validación por época

**Qué.** Dos modelos separados, uno con 2007–2019 y otro con 2020–2025. Cada uno se valida con su
propia partición de validación cruzada estratificada de 5 pliegues, dentro de su periodo. Mismas
variables, misma configuración y métricas ponderadas con HV005.

**Para qué.** Responde a lo que pidieron los evaluadores (años de referencia, equivalencia temporal,
antes y después de la pandemia): si el modelo rinde igual en cada época y si basta con datos recientes.

**Cómo comparar.**
- AUC y cobertura. El acierto (precisión) depende de la prevalencia, que es distinta (~19% frente a
  ~12%), así que se compara por cuántas veces mejora al azar (lift).
- Importancia de las variables (SHAP) en cada época, por si cambió el patrón.

**Cautelas.** La validación dentro de cada época sigue siendo algo optimista, porque niños del mismo
conglomerado caen a ambos lados de la partición. El sesgo es parecido en las dos épocas, así que la
comparación entre ellas es justa, pero el valor absoluto no debe citarse como desempeño en campo.

**Por confirmar antes de correr.**
1. Los periodos son 2007–2019 y 2020–2025, sin separar la pandemia (2020–2021).
2. Se usan las mismas variables en ambos, sin volver a seleccionar por época.
3. Se compara también SHAP por época.

**Descartado.** Entrenar con 2007–2019 y probar en 2020–2025. Mide otra cosa (generalización a años
no vistos mezclada con el cambio de época) y no responde la pregunta de los evaluadores.

## 2. Escala de HV271 y códigos de yodo en la limpieza

Hallazgos sobre los datos, no sobre el modelo.

**`HV271` (índice de riqueza) llega en escalas distintas según el año:**

| Años | Escala en el archivo original | Con la limpieza actual |
|---|---|---|
| 2007–2017 | ×100,000 | correcto al dividir entre 100,000 |
| 2013 | ×1,000,000 | queda en ±20 |
| 2018–2025 | ya en decimales | se divide de más: ±0.00002 |
| 2019 | decimales, con una fila en ×100,000 | esa fila queda en otra escala |

**`HV234` (yodo en la sal):** los códigos 994 («no se hizo la prueba») y 995 («no hay sal») se cuelan
en 2009–2010 por las columnas antiguas `SH107` y `SH124`, que no estaban en la limpieza de falsos
numéricos. Además, `HV234` está vacío en 94% de los niños de 2023 y 86% de 2024.

**Parche listo:** [hv271_escala_por_anio.patch](hv271_escala_por_anio.patch). Agrega a
`run_phase1_engine` el paso `rescale_by_year` (deduce la escala de cada año por el percentil 99) y
suma `SH107` y `SH124` a la limpieza de falsos numéricos. Se aplica con `git apply`.

**Advertencia.** Aplicarlo obliga a regenerar los datos y reentrenar. En una prueba con el parche, el
AUC de validación cruzada quedó igual (0.830), pero el conjunto de variables cambió (salieron área de
residencia y sexo del jefe del hogar y entró la lactancia exclusiva), lo que obligaría a actualizar la
app y los documentos. Por eso no se aplicó.
