# 📋 Decisiones de Limpieza - Módulo Salud Materna (REC41 / Embarazo, Parto y Lactancia)

## Auditoría Final (Pasadas 1, 2 y 3)

| Variable | Categoría Temática | Descripción | Años Presentes | Nulos (%) | Tipo Exacto | Acción | Estado | Advertencia (Falsos Numéricos) | Nota / Labeling |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CASEID** | Identificadores | Identificación de la madre | 18 años | 0% | String | `KEEP` | Esencial | | Llave primaria. |
| **MIDX** | Identificadores | Orden de nacimiento | 18 años | 0% | Numérico Discreto | `KEEP` | Esencial | | |
| **M13** | Control Prenatal | Mes de gestación en el 1er control | 18 años | ~15.8% | Numérico Discreto | `KEEP` | Aprobado | **Falsos: 98, 99** | SIN ETIQUETA (Mantener valor puro) |
| **M14** | Control Prenatal | Número de visitas prenatales | 18 años | 10% - 20% | Numérico Discreto | `KEEP` | Aprobado | **Falsos: 98, 99** | SIN ETIQUETA (Mantener valor puro) |
| **M15** | Nacimiento | Lugar del parto | 18 años | ~1.6% | Categórico Nominal | `KEEP` | Aprobado | **Falsos: 98** | **ETIQUETAR (Aplica Config F3)** |
| **M17** | Nacimiento | Parto por cesárea | 18 años | 0.0% | Binario | `KEEP` | Aprobado | | SIN ETIQUETA (0 y 1 puros) |
| **M18** | Antropometría | Tamaño al nacer | 18 años | ~0% | Categórico Ordinal | `KEEP` | Aprobado | **Falsos: 8** | SIN ETIQUETA (Mantener 1 al 5 por orden matemático) |
| **M19** | Antropometría | Peso al nacer (kg) | 18 años | ~0% | Numérico Continuo | `KEEP` | Aprobado | **Falsos: 9996, 9997, 9998** | SIN ETIQUETA (Mantener valor puro) |
| **M45** | Suplementación | Tomó tabletas de hierro | 18 años | 10% - 20% | Binario | `KEEP` | Aprobado | **Falsos: 8** | SIN ETIQUETA (0 y 1 puros) |
| **M46** | Suplementación | Días que tomó hierro | 18 años | 15% - 46% | Numérico Discreto | `KEEP` | Aprobado | **Falsos: 998, 999** | Imputar con 0 si M45=No. SIN ETIQUETA |
| **M34** | Lactancia | Cuando empezó a darle el pecho | 18 años | ~1.0% | Numérico Compuesto | `KEEP` | Aprobado | | **SIN ETIQUETA (Decodificar matemáticamente luego)** |
| **M4 / M5**| Lactancia | Meses de lactancia | 18 años | ~0% | Numérico Discreto | `KEEP` | Aprobado | **Falsos: 95 al 98** | El código 94 se debe imputar como 0. SIN ETIQUETA |
| **M54** | Inmunización | Vitamina A primeros 2 meses post-parto | 18 años | ~17% | Binario | `KEEP` | Aprobado | | SIN ETIQUETA (0 y 1 puros) |
| **M60** | Salud Materna | Tomó antiparasitarios en el embarazo | 18 años | ~16% | Binario | `KEEP` | Aprobado | **Falsos: 8** | SIN ETIQUETA (0 y 1 puros) |
| **M70** | Salud Infantil | Chequeo médico en el primer mes | 18 años | ~15.1% | Binario | `KEEP` | Aprobado | **Falsos: 8** | SIN ETIQUETA (0 y 1 puros) |
| **M55A-C, E-I, X, Z**| Alimentación Infantil | Líquidos primeros 3 días | 18 años | ~0% | Binario | `KEEP` | Aprobado | **Falsos: 8** | Permite medir lactancia materna exclusiva temprana. |

---
**Diagnóstico Final:** 
La matriz de nulos es **maravillosa**. Salvo las variables fantasmas de país específico (`M55J-N`) y `M55D`, el resto de indicadores biológicos y prenatales críticos rondan el 0% a 20% de nulos, lo cual es altísima calidad para una encuesta pública latinoamericana. Estamos listos para limpiar.
