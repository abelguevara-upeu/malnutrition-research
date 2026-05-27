library(haven)
source("src-r/core/utils.R")
source("src-r/exploration/inspect.R")

# --- AJUSTES DE VISUALIZACIÓN ---
# Evita que R recorte la tabla en la consola
options(max.print = 100000)
options(width = 250)

# 1. Auditoría GLOBAL (Mapa Maestro)
cat("\n--- MAPA MAESTRO DE TODA LA DATA (BRONZE) ---\n")
mapa_maestro <- audit_global_consistency()

# Mostramos todo en la consola
print(mapa_maestro, row.names = FALSE)

# RECOMENDACIÓN: Usa View para navegar la tabla completa tipo Excel
# View(mapa_maestro)

# 2. Inventario de Archivos (Paso 1: ¿Cuántos hay por año?)
cat("\n--- INVENTARIO DE ARCHIVOS ---\n")
modulo <- "health_survey"
inventario <- audit_module_inventory(modulo)
print(inventario, row.names = FALSE)

# 3. Auditoría de DUPLICADOS 
## Registros birth_history
# registros_a_comparar <- c(
#   "RE223132", 
#   "RE212232", 
#   "REC22312", 
#   "REC223132"
# )
## Registros discipline
# registros_a_comparar <- c(
#   "rec93dvdisciplina", "rec93dv disciplina"
# )
## Registros fertility_nuptiality
# registros_a_comparar <- c(
#   "re516171", "rec516171", "rec567_1"
# )
## Registros health_immunization
# registros_a_comparar <- c(
#   "dit", "rec42"
#   #,"rec43", "rec95"
# )
# Registros health_survey
# registros_a_comparar <- c(
#   "csalud01", "csalud08"
# )
## Registros hiv_aids
#registros_a_comparar <- c(
#  "re758081", "rec7581", "rec75_81"
#   "rec91", "rec82"
#   "rec91", "rec75_81"
#   "rec91", "re758081"
#   "rec91","rec7581"
# )
## Registros household (Referencias + Sospechosos)
# registros_a_comparar <- c(
#   "rechm",
#   "rech8", "rech9", "rech10", "rech11"
# )
## Registros housing
# registros_a_comparar <- c(
#   "rech23", "rech2_h3", "rech2_3"
# )
## Registros mef_basics
# registros_a_comparar <- c(
#   "rec0111","rec01_11"
# )
## Registros mortality_violence
# registros_a_comparar <- c(
#   "re848591", "rec84_91", "rec84_dv", "rec84dv", "rec84"
# )


patron <- paste(registros_a_comparar, collapse = "|")
comparativa <- audit_record_variables(modulo, patron)

# Mostramos las primeras 50 variables para detectar solapamientos
print(head(comparativa, 600), row.names = FALSE)

