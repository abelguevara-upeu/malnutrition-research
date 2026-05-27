source("src-r/core/utils.R")
source("src-r/core/indicators.R")
library(haven)

# 1. Año específico
anio_a_testear <- 2024
res <- calculate_chronic_malnutrition(anio_a_testear)
print(res)

# 2. Serie histórica
anios_disponibles <- get_available_years()
serie_historica <- lapply(anios_disponibles, function(y) {
  tryCatch({ calculate_chronic_malnutrition(y) }, error = function(e) NULL)
})

serie_final <- do.call(rbind, serie_historica)
print(serie_final, row.names = FALSE)
