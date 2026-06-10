# Decisiones de Limpieza - RECH1 (Household Roster)

Esta tabla documenta las decisiones de limpieza, estandarización y fusión para el módulo **RECH1** (Listado de miembros del hogar) a lo largo de los 18 años de la ENDES (2007-2024).

## Reglas de Limpieza
1. **Conservar solo variables predictoras/estructurales**: Descartar metadatos operativos (encuestadores, estado de las visitas).
2. **Priorizar Códigos Dtypes (`str`)**: Las llaves de cruce (`HHID`, `HVIDX`, etc.) deben ser siempre `str` para evitar corrupción de ceros a la izquierda.
3. **Mapeo de Value Labels**: Las variables categóricas siempre incluirán el año del diccionario entre paréntesis en la columna de Value Labels (ej. `1.0 (Masculino) (2024)`).

---

## Matriz de Decisiones

| Variable | Categoría Temática | Descripción | Años Presentes | Nulos (%) | Tipo | Acción | Estado | Advertencia | Nota | Column Label (Latest) | Value Label (Latest) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
