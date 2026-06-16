# 📋 Decisiones de Limpieza - Módulo Salud Materna (REC41 / Embarazo, Parto y Lactancia)

## Auditoría Final (Pasadas 1, 2 y 3)

| Variable | Categoría Temática | Descripción | Años Presentes | Nulos (%) | Tipo | Acción | Estado | Advertencia | Nota |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CASEID** | Identificadores | Identificación de la madre | 18 años | 0% | String | `KEEP` | Esencial | CORE | Llave primaria. |
| **MIDX** | Identificadores | Orden de nacimiento | 18 años | 0% | Numérico | `KEEP` | Esencial | CORE | |
| **M14** | Control Prenatal | Número de visitas prenatales | 18 años | 10% - 20% | Numérico | `KEEP` | Aprobado | CORE | Nulos estables, manejables. |
| **M18** | Antropometría | Tamaño al nacer | 18 años | ~0% | Categórico | `KEEP` | Aprobado | CORE | Excelente salud de datos. |
| **M19** | Antropometría | Peso al nacer (kg) | 18 años | ~0% | Numérico | `KEEP` | Aprobado | CORE | Excelente salud de datos. |
| **M45** | Suplementación | Tomó tabletas de hierro | 18 años | 10% - 20% | Binario | `KEEP` | Aprobado | CORE | Mismos nulos que M14 (ligados al control). |
| **M46** | Suplementación | Días que tomó hierro | 18 años | 15% - 46% | Numérico | `KEEP` | Aprobado | Condicionado | Alto % de nulos porque quienes responden NO en M45 saltan esta pregunta. Imputar con 0 si M45=No. |
| **M4 / M5**| Lactancia | Meses de lactancia | 18 años | ~0% | Numérico | `KEEP` | Aprobado | CORE | Variables estrella. Excelente salud. |
| **M55A-C, E-I, X, Z**| Alimentación Infantil | Líquidos primeros 3 días | 18 años | ~0% | Binario | `KEEP` | Aprobado | | Permite medir lactancia materna exclusiva temprana. |
| **M55D, J, K, L, M, N**| Alimentación Infantil | Fantasmas | 18 años | 100% | Binario | `DROP` | Descartado| Fantasmas | Variables 100% vacías en todos los años. (Ej. M55D "agua" mudó a M55B "agua sola"). |

---
**Diagnóstico Final:** 
La matriz de nulos es **maravillosa**. Salvo las variables fantasmas de país específico (`M55J-N`) y `M55D`, el resto de indicadores biológicos y prenatales críticos rondan el 0% a 20% de nulos, lo cual es altísima calidad para una encuesta pública latinoamericana. Estamos listos para limpiar.
