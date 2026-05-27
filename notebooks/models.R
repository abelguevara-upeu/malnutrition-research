source("src-r/core/utils.R")
library(dplyr)
library(tidyr)

# ── Carga y preparacion ──────────────────────────────────────
master <- readRDS("data/silver/validated/master_validated.rds")

data <- master %>%
  mutate(
    durmio   = !grepl("^[Nn]o", as.character(hv103)) & !is.na(hv103),
    hc70_num = as.numeric(hc70),
    peso     = as.numeric(hv005) / 1e6,
    area = case_when(
      as.character(hv025) %in% c("Urbano", "Urbana", "Urban") ~ "Urbano",
      as.character(hv025) %in% c("Rural")                     ~ "Rural",
      TRUE ~ NA_character_
    ),
    sexo = case_when(
      as.character(hv104) %in% c("Hombre", "Male", "Masculino")  ~ "Hombre",
      as.character(hv104) %in% c("Mujer", "Female", "Femenino")  ~ "Mujer",
      TRUE ~ NA_character_
    ),
    departamento = as.character(hv024),
    desnutrido = case_when(
      hc70_num < -200 & hc70_num > -601 ~ 1L,
      hc70_num >= -200 & hc70_num < 601 ~ 0L,
      TRUE ~ NA_integer_
    )
  ) %>%
  filter(durmio, !is.na(desnutrido))

cat("Registros validos:", nrow(data), "\n\n")


# ── 1. Serie longitudinal ponderada ──────────────────────────

serie <- data %>%
  group_by(year_survey) %>%
  summarise(n = n(), dc = round(weighted.mean(desnutrido, peso) * 100, 2), .groups = "drop") %>%
  arrange(year_survey)

cat("== Serie longitudinal ==\n")
print(as.data.frame(serie), row.names = FALSE)


# ── 2. Regresion logistica (factores asociados, 2024) ────────

d24 <- data %>%
  filter(year_survey == 2024, !is.na(area), !is.na(sexo)) %>%
  mutate(area = factor(area, levels = c("Urbano", "Rural")),
         sexo = factor(sexo, levels = c("Mujer", "Hombre")))

fit_glm <- glm(desnutrido ~ area + sexo, data = d24,
               family = binomial, weights = peso)

cat("\n== Modelo logistico (2024) ==\n")
cat("Coeficientes:\n")
print(round(summary(fit_glm)$coefficients, 4))
cat("\nOdds Ratios:\n")
or <- exp(cbind(OR = coef(fit_glm), confint.default(fit_glm)))
print(round(or, 3))


# ── 3. Modelo lineal temporal (tendencia nacional) ───────────

fit_lm <- lm(dc ~ year_survey, data = serie)

cat("\n== Modelo lineal temporal ==\n")
print(round(summary(fit_lm)$coefficients, 4))
cat("R2:", round(summary(fit_lm)$r.squared, 4), "\n")

pred_years <- data.frame(year_survey = 2025:2030)
pred_years$dc_pred <- round(predict(fit_lm, pred_years), 2)

cat("\nProyeccion lineal:\n")
print(pred_years, row.names = FALSE)


# ── 4. Modelo cuadratico (captura desaceleracion) ────────────

fit_quad <- lm(dc ~ year_survey + I(year_survey^2), data = serie)

cat("\n== Modelo cuadratico ==\n")
print(round(summary(fit_quad)$coefficients, 4))
cat("R2:", round(summary(fit_quad)$r.squared, 4), "\n")

pred_years$dc_quad <- round(predict(fit_quad, pred_years), 2)

cat("\nProyeccion cuadratica:\n")
print(pred_years, row.names = FALSE)


# ── 5. Logistico longitudinal (tiempo + area + depto) ────────

data_lon <- data %>%
  filter(!is.na(area), !is.na(departamento)) %>%
  mutate(area = factor(area, levels = c("Urbano", "Rural")),
         t = year_survey - 2007)  # centrar en año base

fit_lon <- glm(desnutrido ~ t + area + t:area, data = data_lon,
               family = binomial, weights = peso)

cat("\n== Modelo logistico longitudinal ==\n")
cat("Coeficientes:\n")
print(round(summary(fit_lon)$coefficients, 4))
cat("\nOdds Ratios:\n")
or_lon <- exp(cbind(OR = coef(fit_lon), confint.default(fit_lon)))
print(round(or_lon, 3))


# ── 6. Comparacion de modelos temporales ─────────────────────

cat("\n== Comparacion de modelos ==\n")
cat(sprintf("%-25s  R2       AIC\n", "Modelo"))
cat(sprintf("%-25s  %.4f   %.1f\n", "Lineal", summary(fit_lm)$r.squared, AIC(fit_lm)))
cat(sprintf("%-25s  %.4f   %.1f\n", "Cuadratico", summary(fit_quad)$r.squared, AIC(fit_quad)))

cat("\nAnalisis finalizado.\n")
