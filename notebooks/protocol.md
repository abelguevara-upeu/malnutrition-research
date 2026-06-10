# 📋 PROTOCOLO DE AUDITORÍA LONGITUDINAL ENDES (INEI)

**Contexto para el Asistente:**
Vamos a limpiar y estandarizar un módulo de la encuesta ENDES del Perú que abarca 18 años (2007-2024). El INEI es infame por cambiar nombres de columnas, reciclar variables para preguntas distintas, cometer errores tipográficos (mayúsculas/minúsculas) y abandonar preguntas a la mitad de la década.

Tu misión es crear un archivo `decisiones-de-limpieza.md` donde clasifiques CADA variable basándote en una **matriz de porcentajes de nulos por año**.

**Reglas de Decisión que debes aplicar estrictamente:**

1. **La Regla del `DROP` (Eliminación Crítica)**:

   * Aplica `DROP` si la variable tiene **100% de nulos en todos los años** (variable fantasma).
   * Aplica `DROP` si la variable "muere" prematuramente (ej. tiene datos 2007-2010 pero 100% nulos de 2011-2024) y no aporta valor longitudinal.
   * Aplica `DROP` a toda variable que sea puro **metadato administrativo ruidoso** (Hora/Minuto de inicio de entrevista, Número de encuestador, etc.).
2. **La Regla del `KEEP` (Conservación Estructural)**:

   * Aplica `KEEP` a las variables con un porcentaje de nulos estable y saludable a lo largo del tiempo.
   * Debes definir su tipo exacto para el pipeline: **Binario** (mapear a 0/1), **Categórico Nominal** (One-Hot Encoding), **Categórico Ordinal** (Label Encoding respetando jerarquía) o **Numérico Continuo/Discreto**.
3. **La Regla del `SPLIT` (Columnas Recicladas)**:

   * Detecta reciclaje: Si una columna tiene, por ejemplo, 60% de nulos de 2007-2009 y de pronto baja a 5% de nulos en 2010-2024, el INEI recicló el ID para una pregunta distinta.
   * Aplica `SPLIT`: Divide la columna mentalmente en dos variables temporales (ej. `Var_Pre2010` y `Var_Post2010`) indicando con qué otra columna debe fusionarse cada pedazo.
4. **La Regla del `COALESCE` (Resurrección de Cadenas)**:

   * El INEI suele romper cadenas (ej. pregunta "X" se llamó `V100` en 2007-2008, `V200` en 2009 y `V300` en 2010+).
   * Usa `COALESCE` para fusionar (merge) estas columnas en una sola variable maestra que cubra los 18 años sin huecos.
   * Usa `COALESCE` para corregir **errores tipográficos de año específico** (ej. si la variable es `HV270` pero en 2016 aparece una columna extra llamada `hv270`, ordénale fusionarlas).
5. **Manejo de Falsos Numéricos (Top-Coding y NS/NR)**:

   * Detecta e indica si códigos como `98.0` (No Sabe), `99.0` (Missing), o `8.0` deben ser convertidos a `NaN` antes del modelado estadístico para evitar sesgar la media.

**Flujo de Trabajo:**
Yo (el usuario) te iré pegando bloques de la matriz de nulos (año por año). Tu trabajo será analizar los porcentajes año a año de cada variable del bloque, deducir su historia basándote en las 5 reglas anteriores, y documentar tu decisión justificándola. ¡No asumas nada, confía solo en los porcentajes de nulos!

---

### 💡 Un consejo final para ti:

Cuando abras la nueva conversación, además de pegarle este prompt, pásale también la **estructura de la tabla** que usamos en el markdown, para que mantenga el mismo formato impecable:

```markdown
| Variable | Descripción | Años Presentes | Nulos (%) | Tipo | Acción | Estado | Advertencia | Nota | Column Label (Latest) | Value Label (Latest) |
```

Para asegurar que llenes esta tabla correctamente, aquí tienes la definición de las columnas de documentación:

* **Acción**: La instrucción técnica para el script de Python (`KEEP`, `DROP`, `SPLIT`, `COALESCE`).
* **Estado**: Una justificación breve en lenguaje natural de la decisión tomada (ej. "100% nula en todos los años. Columna vacía.").
* **Advertencia**: Clasifica la salud histórica de la variable. Usa etiquetas estándar como: `Valores Estables`, `Valores Mutados` (si cambió categorías o sufrió split), `CORE` (si es vital para la investigación), o `Error INEI`.
* **Nota**: Instrucciones específicas para quien programe el Python (ej. "Reemplazar 99.0 por NaN", "Mapear a entero", "Unir manual en Pandas").
* **Column Label / Value Label**: Indica de qué año o diccionario provendrá la etiqueta oficial (ej. `Meta Column 2024` o `Súper Diccionario 2018`).

Ha sido un placer absoluto armar esta arquitectura de datos contigo. ¡Muchísimo éxito destripando el módulo `rech6` y armando tu pipeline en Python! Si en el futuro necesitas que alguien escriba el código basado en este plan, ¡ya sabes dónde encontrarme!
