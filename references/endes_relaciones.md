# Relaciones entre tablas ENDES 2024

```mermaid
erDiagram
    HOGAR ||--o{ MIEMBRO : "HHID + HVIDX"
    HOGAR ||--|| VIVIENDA : "HHID"
    MIEMBRO ||--o| MUJER : "CASEID contiene HHID"
    MUJER ||--o{ HIJO : "CASEID + BIDX"

    HOGAR {
        string HHID "HV001+HV002+HV002A"
        table RECH0 "Características del hogar"
    }

    VIVIENDA {
        string HHID
        table RECH23 "Características de vivienda"
    }

    MIEMBRO {
        string HHID
        string HVIDX "Línea del miembro"
        table RECH1 "Listado de miembros"
        table RECH4 "Elegibilidad"
        table RECH5 "Antropometría adulto"
        table RECH6 "Antropometría niño"
        table PS_BECA18 "Programa social"
        table PS_COMEDOR "Programa social"
        table PS_PENSION65 "Programa social"
        table PS_QALIWARMA "Programa social"
        table PS_WAWAWASI "Programa social"
        table PS_VL "Programa social"
        table PS_TRABAJA "Programa social"
    }

    MUJER {
        string CASEID "HHID + línea mujer"
        table REC0111 "Datos de la mujer"
        table RE223132 "Fecundidad"
        table RE516171 "Planificación familiar"
        table RE758081 "Nupcialidad y VIH"
        table REC84DV "Violencia doméstica"
        table REC91 "Salud reproductiva"
    }

    HIJO {
        string CASEID
        string BIDX "Índice del hijo"
        table REC21 "Nacimientos"
        table REC41 "Prenatal y parto"
        table REC42 "Inmunización"
        table REC43 "Salud infantil"
        table REC44 "Nutrición infantil"
        table DIT "Desarrollo infantil"
        table REC94 "Lactancia"
        table REC95 "Suplementos"
    }
```

## Jerarquía simplificada

```mermaid
graph TD
    H["🏠 HOGAR<br/>HHID"]
    H --> V["🏗️ VIVIENDA<br/>RECH23"]
    H --> M["👤 MIEMBRO<br/>HHID + HVIDX<br/>RECH1, RECH4, RECH5, RECH6<br/>Programas Sociales"]
    M --> W["👩 MUJER<br/>CASEID<br/>REC0111, RE223132<br/>RE516171, RE758081<br/>REC84DV, REC91"]
    W --> C["👶 HIJO<br/>CASEID + BIDX<br/>REC21, REC41, REC42<br/>REC43, REC44, DIT"]
    H --> S["🏥 SALUD COMUNAL<br/>HHID + QSNUMERO<br/>CSALUD01, CSALUD08"]
    W --> MR["⚰️ MORTALIDAD<br/>CASEID + MMIDX / VCOL<br/>REC82, REC83"]
    W --> D["👧 DISCIPLINA<br/>CASEID + QCOL93<br/>REC93DVdisciplina"]

    style H fill:#4a90d9,color:#fff
    style M fill:#7cb342,color:#fff
    style W fill:#ab47bc,color:#fff
    style C fill:#ff7043,color:#fff
    style V fill:#5c6bc0,color:#fff
    style S fill:#26a69a,color:#fff
    style MR fill:#78909c,color:#fff
    style D fill:#ffa726,color:#000
```

## Cómo hacer JOINs

| Quiero cruzar... | JOIN por |
|---|---|
| Hogar ↔ Vivienda | `HHID` |
| Hogar ↔ Miembro | `HHID` (+ `HVIDX` para miembro específico) |
| Miembro ↔ Mujer | `HV001, HV002, HV002A` (componentes de HHID dentro de CASEID) |
| Mujer ↔ Hijo | `CASEID` (+ `BIDX` para hijo específico) |
| Hogar ↔ Salud comunal | `HHID` |
