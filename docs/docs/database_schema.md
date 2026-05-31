# Arquitectura de Datos ENDES (Modelo de Relaciones)

Este documento mantiene el registro visual y técnico de cómo se cruzan los módulos de la ENDES a medida que avanzamos en el Análisis Exploratorio de Datos (EDA).

## 1. Relación Base: Antropometría y Roster del Hogar

El punto de partida del modelo predictivo es el estado nutricional del niño (`RECH6`), el cual debe cruzarse obligatoriamente con el censo del hogar (`RECH1`) para confirmar su identidad demográfica y cumplir con los requisitos metodológicos del INEI (verificar que el niño durmió en la vivienda).

### Diagrama de Relación (ERD)

```mermaid
erDiagram
    RECH1_ROSTER ||--o| RECH6_ANTROPOMETRIA : "Cruce 1:1 (HHID + HVIDX = HC0)"
    
    RECH6_ANTROPOMETRIA {
        string HHID "Identificador del Hogar (Llave Casa)"
        int HC0 "Número de línea del niño (Llave Persona)"
        float HC70 "Z-score Talla/Edad (TARGET)"
        float HC71 "Z-score Peso/Edad"
        float HC72 "Z-score Peso/Talla"
        float HC73 "Z-score IMC/Edad"
    }
    
    RECH1_ROSTER {
        string HHID "Identificador del Hogar (Llave Casa)"
        int HVIDX "Número de línea de la persona (Llave Persona)"
        int HV103 "Durmió anoche en casa (Regla de oro INEI)"
        int HV104 "Sexo"
        int HV105 "Edad en años"
        int HV101 "Relación con el jefe de hogar"
        int HV120 "Elegibilidad para medición"
    }
```

> [!IMPORTANT]  
> **Lógica del Cruce (Left Join desde RECH6):**
> Dado que `RECH1` contiene a todos los habitantes (adultos, abuelos, etc.), la relación general es que una persona del Roster tiene *cero o un* registro de antropometría. 
> Al cruzar partiendo desde `RECH6`, el resultado será un cruce perfecto **1 a 1** que descartará automáticamente a los millones de adultos que no son niños medidos.

*(Este documento se actualizará añadiendo `RECH0` / Housing y `MEF` / Madres conforme se analicen).*
