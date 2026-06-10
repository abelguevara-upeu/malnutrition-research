# 📋 PROTOCOLO DE AUDITORÍA LONGITUDINAL ENDES (INEI)

**Contexto para el Asistente:**
Vamos a limpiar y estandarizar un módulo de la encuesta ENDES del Perú que abarca 18 años (2007-2024). El INEI es infame por cambiar nombres de columnas, reciclar variables para preguntas distintas, cometer errores tipográficos (mayúsculas/minúsculas) y abandonar preguntas a la mitad de la década.

Tu misión es crear un archivo `decisiones-de-limpieza.md` donde clasifiques CADA variable a través de un proceso estructurado en **3 pasadas preliminares**.

### Las 3 Pasadas Preliminares de Auditoría

Para armar el archivo maestro de decisiones, debes realizar obligatoriamente estas tres pasadas iterativas sobre el módulo:

1. **Pasada 1: Clasificación y Categoría Temática**
   - Extraer la lista de todas las variables que sobrevivieron o murieron en los 18 años.
   - Asignar obligatoriamente a cada variable una **Categoría Temática** de negocio (ej. "Antropometría Básica", "Demografía", "Saneamiento", "Infraestructura"). Esto permite agruparlas lógicamente y no tratar la base como una simple "sopa de letras".

2. **Pasada 2: Auditoría de Etiquetas de Valor (Value Labels Consistency) y Tipos (Dtypes)**
   - Revisar si el significado interno de las categorías ha mutado en el tiempo (ej. si `1` significa "Amazonas" en 2007 pero en 2024 significa "Tierra").
   - Inspeccionar rigurosamente los **Dtypes** originales para que valores categóricos ordinales o llaves foráneas en formato SPSS no rompan el pipeline al importarse erróneamente como numéricos de coma flotante (`float64`).

3. **Pasada 3: Matriz de Nulos y Falsos Numéricos**
   - Evaluar los porcentajes de nulos año por año.
   - Cruzar los nulos con códigos falsos numéricos (ej. `98`, `99`, `9998`) de SPSS para tomar la decisión final sobre qué variables retener o descartar.

**Reglas de Decisión que debes aplicar estrictamente (La Regla de Oro: Cero Suposiciones):**

1. **La Regla del `DROP` (Eliminación Crítica)**:
   * Aplica `DROP` si la variable tiene **100% de nulos en todos los años** (variable fantasma).
   * Aplica `DROP` si la variable "muere" prematuramente (ej. tiene datos 2007-2010 pero 100% nulos de 2011-2024) y no aporta valor longitudinal.
   * Aplica `DROP` a toda variable que sea puro **metadato administrativo ruidoso** (Hora/Minuto de inicio de entrevista, Número de encuestador, etc.).

2. **La Regla del `KEEP` (Conservación Estructural)**:
   * Aplica `KEEP` a las variables con un porcentaje de nulos estable y saludable a lo largo del tiempo.
   * Variables geográficas, de estrato y ponderación (ej. `HV005`, UBIGEO, cluster) deben ser preservadas celosamente.

3. **La Regla del `SPLIT` (Columnas Recicladas)**:
   * Detecta reciclaje: Si una columna tiene, por ejemplo, 60% de nulos de 2007-2009 y de pronto baja a 5% de nulos en 2010-2024, el INEI recicló el ID para una pregunta distinta.
   * Aplica `SPLIT`: Divide la columna mentalmente en dos variables temporales (ej. `Var_Pre2010` y `Var_Post2010`) indicando con qué otra columna debe fusionarse cada pedazo.

4. **La Regla del `COALESCE` (Resurrección de Cadenas)**:
   * El INEI suele romper cadenas (ej. pregunta "X" se llamó `V100` en 2007-2008, `V200` en 2009 y `V300` en 2010+).
   * Usa `COALESCE` para fusionar (merge) estas columnas en una sola variable maestra que cubra los 18 años sin huecos.

5. **Manejo de Falsos Numéricos (Top-Coding y NS/NR)**:
   * Detecta e indica si códigos como `98.0` (No Sabe), `99.0` (Missing), o `8.0` deben ser convertidos a `NaN` antes del modelado estadístico para evitar sesgar la media. **La IA NUNCA debe imputar o autorrellenar** en la fase de auditoría.

**Flujo de Trabajo:**
Yo (el usuario) te iré pegando la información según la pasada en la que estemos. Tu trabajo será documentar tu decisión justificándola. ¡No asumas nada, confía solo en los diccionarios, dtypes y la matriz de nulos!

---

### 💡 Estructura Obligatoria de Documentación:

Para asegurar que llenes la tabla correctamente, mantén este formato impecable:

```markdown
| Variable | Categoría Temática | Descripción | Años Presentes | Nulos (%) | Tipo | Acción | Estado | Advertencia | Nota | Column Label (Latest) | Value Label (Latest) |
```

* **Categoría Temática**: La agrupación de negocio definida en la Pasada 1.
* **Acción**: La instrucción técnica para Python (`KEEP`, `DROP`, `SPLIT`, `COALESCE`).
* **Estado**: Una justificación breve de la decisión tomada.
* **Advertencia**: Clasifica la salud histórica. Usa etiquetas como: `Valores Estables`, `Valores Mutados`, `CORE` (fundamental), `CORE ESTRUCTURAL` (variables geográficas/diseño muestral), o `Error INEI`.
* **Nota**: Instrucciones específicas para quien programe el Python (ej. "Reemplazar 99.0 por NaN", "Forzar a String").
* **Column Label / Value Label**: Indica de qué año o diccionario provendrá la etiqueta oficial.
