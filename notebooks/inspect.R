# Inspección jerárquica de objetos ENDES
get_endes_structure <- function(obj, obj_name = "hogar", max_fields = 5) {
  tree_data <- data.frame(Name = character(), Type = character(), Value = character(), stringsAsFactors = FALSE)
  tree_data[nrow(tree_data) + 1, ] <- c(obj_name, paste0("list [", length(obj), "]"), paste0("List of length ", length(obj)))
  
  anios <- names(obj)
  for (anio in anios) {
    sub_obj <- obj[[anio]]
    tree_data[nrow(tree_data) + 1, ] <- c(paste0("  ", anio), paste0("list [", length(sub_obj), "]"), paste0("List of length ", length(sub_obj)))
    
    registros <- names(sub_obj)
    for (reg in registros) {
      df <- sub_obj[[reg]]
      tree_data[nrow(tree_data) + 1, ] <- c(paste0("    ", reg), "tbl_df", paste0("Tibble [", nrow(df), " x ", ncol(df), "]"))
      
      campos <- names(df)[1:min(length(names(df)), max_fields)]
      for (cam in campos) {
        col <- df[[cam]]
        lbl <- attr(col, "label")
        val <- paste(head(as.character(col), 2), collapse = ", ")
        tree_data[nrow(tree_data) + 1, ] <- c(paste0("      ", cam), class(col)[1], paste0("[", lbl, "] ", val, "..."))
      }
    }
  }
  return(tree_data)
}

# Auditoría de variables entre anios (Versión Comparativa)
compare_endes_schema <- function(data_list, record_pattern) {
  anios <- names(data_list)
  
  # Extraer nombres de variables y el nombre del registro fuente
  # var_info será una lista de listas: year -> list(record_name -> colnames)
  var_info <- lapply(data_list, function(df) {
    if (is.null(df)) return(NULL)
    
    # Si es un data.frame directo (un solo registro cargado)
    if (is.data.frame(df)) {
      return(list(Source = record_pattern, Vars = tolower(colnames(df))))
    }
    
    # Si es una lista de registros (módulo completo o múltiples coincidencias)
    match_indices <- grep(record_pattern, names(df), ignore.case = TRUE)
    if (length(match_indices) == 0) return(NULL)
    
    # Retornar info de todos los registros que coincidan en ese año (FORZAR MINÚSCULAS)
    lapply(match_indices, function(i) {
      list(Source = names(df)[i], Vars = tolower(colnames(df[[i]])))
    })
  })
  
  # Aplanar para obtener todas las variables únicas
  all_vars <- sort(unique(unlist(lapply(var_info, function(y) {
    if (is.null(y)) return(NULL)
    if ("Vars" %in% names(y)) return(y$Vars)
    unlist(lapply(y, function(r) r$Vars))
  }))))
  
  if (length(all_vars) == 0) return(data.frame(Mensaje = "No se encontraron variables"))
  
  trace_matrix <- data.frame(Variable = all_vars, stringsAsFactors = FALSE)
  
  for (y in anios) {
    year_data <- var_info[[y]]
    if (is.null(year_data)) {
      trace_matrix[[y]] <- ""
      next
    }
    
    # Para cada variable, ver en qué registro(s) está
    cell_values <- sapply(all_vars, function(v) {
      sources <- c()
      if ("Vars" %in% names(year_data)) {
        if (v %in% year_data$Vars) sources <- year_data$Source
      } else {
        sources <- sapply(year_data, function(r) if (v %in% r$Vars) r$Source else NULL)
        sources <- unlist(sources)
      }
      paste(unique(sources), collapse = ", ")
    })
    trace_matrix[[y]] <- cell_values
  }
  
  # Métricas
  trace_matrix$Presentes <- apply(trace_matrix[, anios], 1, function(x) sum(x != ""))
  trace_matrix$Faltantes <- length(anios) - trace_matrix$Presentes
  
  # Calcular el Rango con detección de huecos (ej: 1996, 2005-2024)
  trace_matrix$Rango <- apply(trace_matrix[, anios], 1, function(row) {
    format_year_ranges(anios[row != ""])
  })
  
  return(trace_matrix[, c("Variable", "Rango", "Presentes", "Faltantes", anios)])
}


#' Auditoría profunda de variables para uno o más registros (comparativa)
#' @param module_alias Alias del módulo (ej: "birth_history")
#' @param record_pattern Patrón o vector de registros (ej: "RE223132|REC223132")
audit_record_variables <- function(module_alias, record_pattern) {
  cat(paste0("\n🔍 Iniciando trazabilidad comparativa para: ", module_alias, " -> [", record_pattern, "]\n"))
  
  # Cargar el módulo completo de esos años para poder comparar entre registros
  # Usamos el módulo completo porque si pedimos un registro y no existe con ese nombre exacto, load_endes fallaría
  # Cargar el módulo completo (solo headers para velocidad)
  history <- load_endes_history(module = module_alias, record = NULL, clean = FALSE, n_max = 1)
  
  if (length(history) == 0) {
    stop("No se encontraron datos para este módulo en la historia.")
  }
  
  # Generar el mapa comparativo
  mapa <- compare_endes_schema(history, record_pattern)
  rownames(mapa) <- NULL
  return(mapa)
}


#' Inventario rápido de archivos por año para un módulo
#' @param module_alias Alias del módulo (ej: "birth_history")
audit_module_inventory <- function(module_alias) {
  cat(paste0("\n📦 Inventario de archivos para el módulo: ", module_alias, "\n"))
  
  bronze_path <- file.path("data", "bronze")
  if (!dir.exists(bronze_path)) stop("No existe la carpeta data/bronze")
  
  anios <- sort(list.dirs(bronze_path, full.names = FALSE, recursive = FALSE), decreasing = TRUE)
  inventory <- data.frame(Anio = character(), Num_Archivos = integer(), Archivos = character(), stringsAsFactors = FALSE)
  
  for (y in anios) {
    y_path <- file.path(bronze_path, y)
    mod_dirs <- list.dirs(y_path, full.names = TRUE, recursive = FALSE)
    
    found_in_year <- FALSE
    for (d in mod_dirs) {
      meta_file <- file.path(d, "metadata.json")
      if (file.exists(meta_file)) {
        meta <- fromJSON(meta_file)
        if (normalize_module_name(meta$module_name) == module_alias) {
          sav_files <- list.files(d, pattern = "\\.sav$", ignore.case = TRUE)
          norm_names <- sapply(sav_files, normalize_record_name)
          inventory <- rbind(inventory, data.frame(
            Anio = y,
            Num_Archivos = length(sav_files),
            Archivos = paste(norm_names, collapse = ", "),
            stringsAsFactors = FALSE
          ))
          found_in_year <- TRUE
          break
        }
      }
    }
    if (!found_in_year) {
      inventory <- rbind(inventory, data.frame(Anio = y, Num_Archivos = 0, Archivos = "---", stringsAsFactors = FALSE))
    }
  }
  
  rownames(inventory) <- NULL
  return(inventory)
}

#' Auditoría Global de todos los módulos y registros en el disco
#'
#' @return Un data.frame con la relación Módulo -> Registro -> Presencia por Anio
audit_global_consistency <- function() {
  library(jsonlite)
  bronze_path <- file.path("data", "bronze")
  if (!dir.exists(bronze_path)) stop("No existe la carpeta data/bronze")
  
  anios <- sort(as.numeric(list.dirs(bronze_path, full.names = FALSE, recursive = FALSE)), decreasing = TRUE)
  anios <- as.character(anios[!is.na(anios)])
  
  # 1. Escaneo masivo leyendo metadatos
  base_data <- data.frame(Modulo = character(), Registro = character(), Anio = character(), Codigo = character(), stringsAsFactors = FALSE)
  
  for (y in anios) {
    mod_dirs <- list.dirs(file.path(bronze_path, y), full.names = TRUE, recursive = FALSE)
    for (m_path in mod_dirs) {
      # Intentar leer metadatos
      meta_file <- file.path(m_path, "metadata.json")
      if (!file.exists(meta_file)) next
      
      meta <- fromJSON(meta_file)
      
      # Normalizar nombre del módulo
      mod_alias <- normalize_module_name(meta$module_name)
      mod_code  <- as.character(meta$module_code)
      
      sav_files <- list.files(m_path, pattern = "\\.sav$", ignore.case = TRUE)
      records <- sapply(sav_files, normalize_record_name)
      
      if (length(records) > 0) {
        base_data <- rbind(base_data, data.frame(
          Modulo = mod_alias,
          Registro = records,
          Anio = y,
          Codigo = mod_code,
          stringsAsFactors = FALSE
        ))
      }
    }
  }
  
  # 2. Crear matriz final agrupada
  all_pairs <- unique(base_data[, c("Modulo", "Registro")])
  all_pairs <- all_pairs[order(all_pairs$Modulo, all_pairs$Registro), ]
  rownames(all_pairs) <- NULL # Resetear índices para que sean secuenciales (1, 2, 3...)
  
  for (y in anios) {
    current_year_data <- base_data[base_data$Anio == y, ]
    # Mapear el código al registro correspondiente
    pair_keys <- paste(all_pairs$Modulo, all_pairs$Registro, sep = "|")
    year_keys <- paste(current_year_data$Modulo, current_year_data$Registro, sep = "|")
    
    match_idx <- match(pair_keys, year_keys)
    all_pairs[[y]] <- ifelse(!is.na(match_idx), current_year_data$Codigo[match_idx], "")
  }
  
  # 3. Resumen numérico y de códigos
  all_pairs$Presentes <- apply(all_pairs[, anios], 1, function(x) sum(x != ""))
  all_pairs$Faltantes <- length(anios) - all_pairs$Presentes
  
  all_pairs$Codigos <- apply(all_pairs[, anios], 1, function(x) {
    paste(sort(unique(x[x != ""])), collapse = ", ")
  })
  
  return(all_pairs[, c("Modulo", "Registro", "Codigos", "Presentes", "Faltantes", anios)])
}
