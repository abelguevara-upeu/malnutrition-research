# SOLICITUD DE VALIDACIÓN POR JUICIO DE EXPERTOS

**Proyecto:** *Modelo Predictivo de Riesgo de Desnutrición Crónica Infantil en el Perú mediante Machine Learning*

**Institución:** Universidad Peruana Unión (UPeU) — Facultad de Ingeniería y Arquitectura, EP Ingeniería de Sistemas
**Asignatura:** Investigación V (Ciclo X – 2026-II) · **Docente:** Mg. Nemias Saboya Rios
**Equipo:** Abel Guevara Huasco · Verónica Vergara Rojas · Pamela Vallejos Cotrina

---

## 1. Objetivo

Predecir el **perfil de riesgo de desnutrición crónica infantil** en menores de 5 años a partir de
variables sociodemográficas, del hogar y de salud materna recogidas por encuesta, con el fin de
**orientar la focalización de recursos** en salud pública.

El sistema **no reemplaza el diagnóstico clínico ni la medición antropométrica**. Funciona como una
herramienta de **triaje previo**: dado el perfil de un hogar, estima la probabilidad de que el niño
presente desnutrición crónica, permitiendo priorizar a quién visitar primero cuando el presupuesto no
alcanza para cubrir a toda la población.

**Pregunta de investigación:** ¿Puede un modelo de *Machine Learning* identificar, con datos de
encuesta de hogar, qué niños tienen mayor riesgo de desnutrición crónica antes de que un agente de
salud llegue al domicilio?

---

## 2. Método

Se siguió **CRISP-DM** (*Cross-Industry Standard Process for Data Mining*), estándar de la industria
para proyectos de ciencia de datos, organizado en seis fases:

```
1. Comprensión    2. Comprensión    3. Preparación
   del Negocio   →   de los Datos  →   de los Datos
                                            ↓
6. Despliegue  ←  5. Evaluación   ←   4. Modelado
   (aplicativo)     (explicabilidad)     (algoritmos)
```

| Aspecto | Definición |
|---|---|
| Fuente | ENDES — INEI (Encuesta Demográfica y de Salud Familiar), datos públicos |
| Periodo | 2007 – 2025 (19 años) |
| Muestra | **304,271 niños** menores de 5 años con antropometría válida |
| Variable objetivo | Desnutrición crónica: Z-score Talla/Edad (`HC70`) < −2 DE, estándar OMS / KPI 4 del INEI |
| Prevalencia | 15.8% |
| Tipo de problema | Clasificación binaria supervisada |
| Validación | Validación cruzada estratificada 5-*fold* con ponderación muestral del INEI (`HV005`) |

**Decisión metodológica central:** se **excluyeron deliberadamente el peso y la talla directos del
niño** (`HC2`, `HC3`) y los Z-scores derivados. Si el modelo conociera la talla, el diagnóstico sería
trivial y no habría predicción. El modelo aprende únicamente de variables *no obvias* —condiciones del
hogar, historia materna y entorno— que la encuesta puede recoger sin medir al niño.

**Resultados actuales:** LightGBM resultó el algoritmo campeón entre seis evaluados, con
**AUC-ROC 0.8294** (IC 95%: 0.8267 – 0.8324) y **sensibilidad 76.43%** (IC 95%: 75.88% – 76.98%),
verificados mediante *bootstrap* de 1,000 repeticiones. El umbral de decisión es ajustable: elevando la
sensibilidad a ≥ 80% el sistema detecta más casos reales a costa de más falsos positivos, criterio
deliberado en triaje preventivo, donde no detectar a un niño desnutrido es más costoso que una visita
de verificación innecesaria.

---

## 3. Variables que intervienen (45)

Estas son las variables que el modelo utiliza actualmente, agrupadas por dominio. **Son las que
solicitamos encontrar en cualquier conjunto de datos externo con el que se desee contrastar el
sistema.**

### A. Niño (4)
| Código ENDES | Variable |
|---|---|
| `HC1` | Edad en meses |
| `HC27` | Sexo |
| `HC56` | Hemoglobina ajustada por altitud |
| `HC63` | Intervalo respecto al nacimiento anterior |

### B. Salud materna, embarazo y lactancia (13)
| Código | Variable |
|---|---|
| `M13` | Mes de gestación del primer control prenatal |
| `M14` | Número de visitas prenatales |
| `m15` | Lugar del parto |
| `M17` | Parto por cesárea |
| `M18` | Tamaño del niño al nacer |
| `m19` | Peso al nacer (kg) |
| `M4` | Duración de la lactancia |
| `m34` | Horas hasta el inicio de la lactancia |
| `M46` | Días que tomó hierro en el embarazo |
| `M54` | Vitamina A en los primeros 2 meses post parto |
| `M55G` | Fórmula para bebés en los primeros 3 días |
| `M60` | Antiparasitarios durante el embarazo |
| `HC62` | Año más alto de educación de la madre |

### C. Hogar y nivel socioeconómico (7)
| Código | Variable |
|---|---|
| `HV271` | Índice de riqueza del hogar |
| `HV012` | Miembros habituales del hogar |
| `HV014` | Niños menores de 5 años en el hogar |
| `HV219` | Sexo del jefe del hogar |
| `HV220` | Edad del jefe del hogar |
| `HV102` | Residente habitual |
| `HV025` | Área de residencia (urbano / rural) |

### D. Agua, saneamiento e higiene — WASH (10)
| Código | Variable |
|---|---|
| `HV204` | Tiempo de viaje a la fuente de agua |
| `HV225` | Comparte servicio higiénico |
| `HV234` | Prueba de yodo en la sal |
| `HV237` | Tratamiento del agua |
| `HV237A` | Tratamiento del agua: hervir |
| `HV237G` | Consumo de agua embotellada |
| `SH42` | Disponibilidad de agua todo el día |
| `SH48` | Conserva agua |
| `SH49` / `SH50` | Tipo de recipiente y si lo usa con tapa |

### E. Vivienda y entorno (11)
| Código | Variable |
|---|---|
| `HV040` | Altitud del conglomerado (msnm) |
| `HV216` | Habitaciones para dormir |
| `SH71` | Número de habitaciones del hogar |
| `HV240` | Tiene chimenea o campana |
| `HV242` | Cuarto separado para cocinar |
| `SH63` | Otro tipo de combustible para cocinar |
| `SH70` | Fuente de luz |
| `SH76B` / `SH76C` / `SH76D` | Ventanas con cristal / de madera / con malla |
| `SH77F` | Otro tipo de transporte |

> **Nota:** el conjunto es ampliable. El *dataset* original contiene más de 180 variables, de las cuales
> se retuvieron 45 por criterios estadísticos. Si los especialistas consideran relevante alguna
> dimensión no cubierta —consumo dietético, morbilidad reciente, vacunación, antropometría materna—
> puede incorporarse siempre que exista en la fuente de datos.

---

## 3.bis. Especificación de campos

Esta tabla define **cómo debe venir codificada cada variable** en un conjunto de datos externo. El
modelo compara valores de forma literal: una categoría escrita de otra manera (`"URBANO"` en lugar de
`"Urbano"`, o `1`/`0` en lugar de `"Si"`/`"No"`) no produce un error visible, sino una predicción
degradada en silencio. Por eso el formato importa tanto como la variable misma.

**Convenciones**
- *Categórica*: texto, exactamente uno de los valores listados (sensible a mayúsculas y tildes).
- *Código*: número entero que representa una categoría, **no una cantidad**.
- *Numérica*: magnitud continua o discreta, en la unidad indicada.
- Un campo ausente debe dejarse **vacío**, nunca rellenarse con 0, 999 o "NA": el modelo maneja
  valores faltantes de forma nativa y cada variable tolera el porcentaje de vacíos que se indica.

### Niño
| Código | Tipo | Valores admitidos | Unidad | % nulos tolerado |
|---|---|---|---|---:|
| `HC1` | Numérica | 0 – 59 | meses | 0.0 |
| `HC27` | Categórica | `Hombre` / `Mujer` | — | 0.0 |
| `HC56` | Numérica | 4 – 20 (hemoglobina ajustada) | g/dL | 9.6 |
| `HC63` | Numérica | 7 – 388 | meses desde el parto anterior | 36.3 |

### Salud materna, embarazo y lactancia
| Código | Tipo | Valores admitidos | Unidad | % nulos tolerado |
|---|---|---|---|---:|
| `M13` | Código | 0 – 9 | mes de gestación del 1.er control | 19.7 |
| `M14` | Numérica | 0 – 20 | número de visitas | 18.6 |
| `m15` | Categórica | `Institucional` / `Domiciliario` | — | 6.6 |
| `M17` | Código | `1` = cesárea, `0` = no | — | 5.8 |
| `M18` | Código | 1 = muy grande … 5 = muy pequeño | — | 5.8 |
| `m19` | Numérica | 0.5 – 6.0 | kilogramos (decimal) | 10.6 |
| `M4` | Numérica | 0 – 59 | meses de lactancia | 5.8 |
| `m34` | Numérica | 0 – 2352 | horas hasta iniciar lactancia | 6.2 |
| `M46` | Numérica | 0 – 364 | días que tomó hierro | 18.7 |
| `M54` | Código | `1` = sí, `0` = no | vitamina A post parto | 19.7 |
| `M55G` | Código | `1` = sí, `0` = no | fórmula en los 3 primeros días | 6.8 |
| `M60` | Código | `1` = sí, `0` = no | antiparasitarios en el embarazo | 19.9 |
| `HC62` | Código | 0 – 9 | año más alto de educación materna | 4.8 |

### Hogar y nivel socioeconómico
| Código | Tipo | Valores admitidos | Unidad | % nulos tolerado |
|---|---|---|---|---:|
| `HV271` | Numérica | −215987 a 205316 | índice de riqueza (escala INEI ×10⁵) | 0.8 |
| `HV012` | Numérica | 0 – 25 | personas | 0.0 |
| `HV014` | Código | 0 – 10 | niños menores de 5 años | 0.0 |
| `HV219` | Categórica | `Masculino` / `Femenino` | sexo del jefe del hogar | 0.0 |
| `HV220` | Numérica | 12 – 97 | años | 0.0 |
| `HV102` | Categórica | `Sí` / `No` | **con tilde** | 2.4 |
| `HV025` | Categórica | `Urbano` / `Rural` | — | 0.0 |

### Agua, saneamiento e higiene (WASH)
| Código | Tipo | Valores admitidos | Unidad | % nulos tolerado |
|---|---|---|---|---:|
| `HV204` | Numérica | 0 – 600 | minutos hasta la fuente | 0.1 |
| `HV225` | Categórica | `Si` / `No` | **sin tilde** | 10.8 |
| `HV234` | Código | 0, 7, 15, 30 | yodo en sal (ppm por colorimetría) | 4.8 |
| `HV237` | Categórica | `Si` / `No` | **sin tilde** | 0.0 |
| `HV237A` | Categórica | `Si` / `No` | **sin tilde** | 0.0 |
| `HV237G` | Categórica | `Si` / `No` | **sin tilde** | 8.1 |
| `SH42` | Categórica | `Sí` / `No` | **con tilde** | 20.4 |
| `SH48` | Categórica | `Sí` / `No` | **con tilde** | 15.8 |
| `SH49` | Código | 0 – 8, 96, 98 | tipo de recipiente | 20.4 |
| `SH50` | Código | 0 – 8 | lo usa con tapa | 19.3 |

### Vivienda y entorno
| Código | Tipo | Valores admitidos | Unidad | % nulos tolerado |
|---|---|---|---|---:|
| `HV040` | Numérica | 0 – 5053 | metros sobre el nivel del mar | 0.0 |
| `HV216` | Numérica | 0 – 14 | habitaciones para dormir | 0.0 |
| `HV240` | Código | 0, 1, 2 | tiene chimenea o campana | 55.9 |
| `HV242` | Categórica | `Si` / `No` | **sin tilde** | 9.3 |
| `SH63` | Categórica | `Si` / `No` | **sin tilde** | 2.1 |
| `SH70` | Código | 1 – 6, 96, 99 | fuente de luz | 1.6 |
| `SH71` | Numérica | 1 – 30 | habitaciones del hogar | 0.0 |
| `SH76B` | Categórica | `Si` / `No` | ventanas con cristal | 16.2 |
| `SH76C` | Categórica | `Si` / `No` | ventanas de madera | 16.2 |
| `SH76D` | Categórica | `Si` / `No` | ventanas con malla | 16.2 |
| `SH77F` | Categórica | `Si` / `No` | otro tipo de transporte | 0.0 |

> **Advertencia sobre la codificación heredada.** Las tres irregularidades que siguen provienen de la
> propia ENDES y se conservaron para no alterar la fuente; se señalan aquí porque condicionan el
> formato de entrega:
>
> 1. **`Si` frente a `Sí`.** Unas variables llevan tilde y otras no, según el módulo de origen. La
>    tabla indica cuál corresponde en cada caso y la distinción debe respetarse.
> 2. **Binarias en dos formatos.** `M17`, `M54`, `M55G` y `M60` se codifican `1`/`0`, mientras que el
>    resto de las dicotómicas usan texto `Si`/`No`.
> 3. **Códigos especiales en campos numéricos.** `SH49` (96, 98) y `SH70` (96, 99)
>    reservan esos valores para *otro* o *no sabe*. No representan magnitudes y deben transcribirse
>    tal cual, sin convertirlos ni sustituirlos por promedios.
>
> Si el conjunto de datos externo emplea otra codificación, basta con entregarlo acompañado de su
> diccionario de valores: el equipo se encarga de la homologación.

---

## 3.ter. Variables adicionales deseables

Las 45 variables anteriores son las que el modelo **usa hoy** y constituyen el mínimo necesario para
contrastarlo. Las que siguen **no están en el modelo actual** y se solicitan porque la literatura
epidemiológica las identifica como determinantes de la desnutrición crónica que la ENDES no permite
cubrir con suficiente completitud.

Su inclusión es **opcional**: el sistema funciona sin ellas. Pero cada dimensión que el conjunto de
datos externo pueda aportar abre la posibilidad de una versión mejorada del modelo, y su ausencia es
hoy una limitación declarada del estudio.

El marco de referencia es el **modelo conceptual de UNICEF** sobre desnutrición infantil, que ordena
las causas en tres niveles. El modelo actual cubre bien los niveles básico y subyacente —pobreza,
educación, agua y saneamiento, vivienda— pero tiene un vacío en el **nivel inmediato**, que es
precisamente donde actúa la intervención nutricional.

### Prioridad alta — nivel inmediato (el vacío principal)

| Dimensión | Campo sugerido | Por qué importa |
|---|---|---|
| Morbilidad reciente | Episodios de diarrea en las últimas 2 semanas (sí/no) | Vía infecciosa hacia la malabsorción de nutrientes |
| Morbilidad reciente | Infección respiratoria aguda en las últimas 2 semanas (sí/no) | Impacto directo sobre el estado nutricional |
| Ingesta | Diversidad dietética mínima (número de grupos de alimentos en 24 h) | Indicador OMS de calidad de la alimentación |
| Ingesta | Frecuencia mínima de comidas según edad | Complemento del anterior |
| Suplementación | Recibe micronutrientes o hierro (sí/no, frecuencia) | Intervención directa y modificable |

### Prioridad media — estado nutricional materno y servicios

| Dimensión | Campo sugerido | Por qué importa |
|---|---|---|
| Antropometría materna | Talla de la madre (cm) | Predictor consistente de retraso del crecimiento intergeneracional |
| Antropometría materna | Peso / IMC de la madre | Estado nutricional del hogar |
| Servicios de salud | Controles CRED al día (sí/no, número) | Seguimiento del crecimiento en el sistema peruano |
| Servicios de salud | Esquema de vacunación completo para la edad (sí/no) | *Proxy* de acceso efectivo a servicios |

### Prioridad media — contexto social

| Dimensión | Campo sugerido | Por qué importa |
|---|---|---|
| Etnicidad | Lengua materna de la madre | Marcador de exclusión estructural especialmente relevante en el Perú |
| Seguridad alimentaria | Escala de inseguridad alimentaria del hogar (ELCSA o similar) | Acceso efectivo a alimentos, no solo capacidad económica |
| Cuidado | Situación laboral de la madre / cuidador principal | Tiempo disponible para prácticas de cuidado |
| Programas sociales | Beneficiario de Juntos, Cuna Más, Qali Warma (sí/no) | Permite evaluar cobertura frente a necesidad |

> **Sobre el formato.** Estas variables no requieren la codificación estricta de la sección 3.bis, ya
> que aún no forman parte del modelo. Basta con entregarlas tal como estén registradas, acompañadas de
> su diccionario de valores. El equipo se encarga de homologarlas.

> **Una aclaración necesaria.** Las variables de morbilidad reciente (diarrea, IRA) son causas
> inmediatas, pero también son *concurrentes* con el desenlace: si un agente de salud ya sabe que el
> niño tuvo diarrea, es porque hubo contacto previo con el sistema. Por eso se solicitan para
> **análisis explicativo** y para una eventual versión del modelo orientada a seguimiento, no
> necesariamente para el triaje anticipado, cuyo valor reside justamente en operar sin visita previa.


---

## 4. Qué esperamos de esta validación

Solicitamos la participación de **cinco especialistas** en nutrición, salud pública, epidemiología o
enfermería, idealmente con representación territorial (**2 de costa, 2 de sierra, 1 de selva**), para
dos procesos complementarios:

### 4.1 Pertinencia
Valoración de la **utilidad percibida** del sistema mediante un instrumento estructurado que el
especialista completará tras una demostración del aplicativo. Se evalúa si la herramienta resulta útil,
comprensible y aplicable en la práctica real de focalización sanitaria, y qué limitaciones o variables
faltantes identifica desde su experiencia profesional.

*Modalidad:* sesión virtual, coordinada según disponibilidad. El equipo provee el protocolo, conduce la
demostración y registra la sesión.

### 4.2 Replicabilidad
Contraste del modelo frente a **datos externos** distintos de la ENDES. El procedimiento consiste en que
el especialista aporte registros de su ámbito —incluyendo casos con y sin desnutrición diagnosticada—,
el sistema emita su estimación de riesgo, y se compare con el diagnóstico clínico conocido.

Esto permite medir si el modelo mantiene su desempeño en una realidad distinta de aquella con la que fue
entrenado. Se requieren **datos crudos** (no reportes agregados), con las variables listadas en la
sección 3.

---

## 5. Consideraciones éticas

Los datos con los que se construyó el modelo son de **acceso público y libre** (portal de microdatos del
INEI), por lo que su tratamiento no requirió aprobación de comité de ética.

Para la fase de validación con datos institucionales, el equipo se compromete a tramitar los permisos
formales correspondientes y a someter el protocolo a comité de ética cuando la institución lo exija. Los
datos que se reciban se usarán exclusivamente con fines de validación técnica, de forma anonimizada, y
no serán publicados ni compartidos con terceros.

---

## 6. Contribución esperada para los participantes

Los especialistas que participen serán reconocidos en el artículo científico resultante. Asimismo, el
equipo queda disponible para integrarse como soporte técnico en investigaciones posteriores que deseen
aplicar el modelo en estudios de campo, intervención o gestión sanitaria.

---

*Contacto: equipo de investigación — EP Ingeniería de Sistemas, Universidad Peruana Unión.*
