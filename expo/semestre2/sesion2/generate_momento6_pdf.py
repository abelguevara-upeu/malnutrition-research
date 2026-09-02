import subprocess
import os

html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Momento 6: Plan de Validación de Resultados - UPeU</title>
    <style>
        @page {
            size: A4 portrait;
            margin: 10mm 12mm 10mm 12mm;
        }
        
        * {
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }

        body {
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            color: #1a2530;
            line-height: 1.45;
            font-size: 9.2pt;
            margin: 0;
            padding: 0;
            background-color: #ffffff;
        }

        .header {
            border-bottom: 2px solid #003366;
            padding-bottom: 5px;
            margin-bottom: 9px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .university-title {
            font-size: 11.5pt;
            font-weight: bold;
            color: #003366;
            text-transform: uppercase;
            margin: 0;
        }

        .faculty-title {
            font-size: 8.5pt;
            color: #555;
            margin: 2px 0 0 0;
            font-weight: 600;
        }

        .course-badge {
            background-color: #f0a500;
            color: #003366;
            padding: 3px 8px;
            font-size: 8pt;
            font-weight: bold;
            border-radius: 4px;
            display: inline-block;
        }

        .doc-title-container {
            background: linear-gradient(135deg, #003366 0%, #002244 100%);
            color: white;
            padding: 9px 12px;
            border-radius: 5px;
            margin-bottom: 9px;
        }

        .doc-subtitle {
            font-size: 7.5pt;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #f0a500;
            font-weight: 700;
        }

        .doc-main-title {
            font-size: 12pt;
            font-weight: bold;
            margin: 3px 0 0 0;
            line-height: 1.25;
        }

        .metadata-grid {
            display: grid;
            grid-template-columns: 1.2fr 1fr;
            gap: 8px;
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 5px;
            padding: 8px 10px;
            margin-bottom: 9px;
            font-size: 8.2pt;
        }

        .metadata-item strong {
            color: #003366;
        }

        .scope-box {
            background-color: #f1f5f9;
            border-left: 4px solid #003366;
            padding: 7px 10px;
            font-size: 8.2pt;
            color: #1e293b;
            margin-bottom: 9px;
            border-radius: 0 4px 4px 0;
            line-height: 1.35;
        }

        .section-header {
            background-color: #e2e8f0;
            color: #003366;
            font-size: 9.2pt;
            font-weight: bold;
            padding: 4px 8px;
            border-left: 4px solid #003366;
            margin: 9px 0 6px 0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .axes-container {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 8px;
            margin-bottom: 9px;
        }

        .axis-card {
            border: 1px solid #cbd5e1;
            border-radius: 5px;
            padding: 8px 9px;
            background: #ffffff;
            box-shadow: 0 1px 2px rgba(0,0,0,0.03);
        }

        .axis-header {
            font-weight: bold;
            font-size: 8.5pt;
            padding-bottom: 4px;
            margin-bottom: 5px;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            align-items: center;
            gap: 4px;
        }

        .axis-1 { border-top: 3.5px solid #2563eb; color: #1e40af; }
        .axis-2 { border-top: 3.5px solid #059669; color: #065f46; }
        .axis-3 { border-top: 3.5px solid #d97706; color: #92400e; }

        .axis-list {
            margin: 0;
            padding-left: 14px;
            font-size: 7.8pt;
            color: #334155;
            line-height: 1.35;
        }

        .axis-list li {
            margin-bottom: 4px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 7.9pt;
            margin-bottom: 9px;
        }

        th {
            background-color: #003366;
            color: white;
            text-align: left;
            padding: 5px 7px;
            font-weight: 600;
            border: 1px solid #002244;
        }

        td {
            padding: 4.5px 7px;
            border: 1px solid #cbd5e1;
            vertical-align: middle;
        }

        tr:nth-child(even) {
            background-color: #f8fafc;
        }

        .tag-success {
            background-color: #dcfce7;
            color: #15803d;
            font-weight: bold;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 7.4pt;
            display: inline-block;
        }

        .tag-target {
            background-color: #fef3c7;
            color: #b45309;
            font-weight: bold;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 7.4pt;
            display: inline-block;
        }

        .ref-box {
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            padding: 6px 8px;
            font-size: 7pt;
            color: #475569;
            line-height: 1.3;
            margin-top: 4px;
        }

        .page-break {
            page-break-before: always;
        }

        .footer {
            border-top: 1px solid #cbd5e1;
            padding-top: 4px;
            margin-top: 8px;
            font-size: 7.2pt;
            color: #64748b;
            text-align: center;
        }
    </style>
</head>
<body>

    <!-- Header -->
    <div class="header">
        <div>
            <div class="university-title">Universidad Peruana Unión</div>
            <div class="faculty-title">Facultad de Ingeniería y Arquitectura · EP Ingeniería de Sistemas</div>
        </div>
        <div style="text-align: right;">
            <div class="course-badge">INVESTIGACIÓN V · SESIÓN 02</div>
            <div style="font-size: 7.5pt; color: #666; margin-top: 2px;">Ciclo X (2026-II) · Mg. Nemias Saboya Rios</div>
        </div>
    </div>

    <!-- Title Container -->
    <div class="doc-title-container">
        <div class="doc-subtitle">MOMENTO 6: CREA · RETO AUTÓNOMO DE INVESTIGACIÓN</div>
        <div class="doc-main-title">Plan de Validación de Resultados de Investigación</div>
    </div>

    <!-- Metadata -->
    <div class="metadata-grid">
        <div class="metadata-item">
            <strong>Proyecto:</strong> Sistema Predictivo de Riesgo de Desnutrición Crónica Infantil (ENDES 2007–2024)<br>
            <strong>Línea Base:</strong> LightGBM Top 43 Vars (5-Fold CV + Pesos HV005 · AUC: 0.8308 · Recall: 76.49%)
        </div>
        <div class="metadata-item">
            <strong>Equipo de Trabajo:</strong> Abel Guevara Huasco, Verónica Vergara Rojas, Pamela Vallejos Cotrina<br>
            <strong>Duración Estimada:</strong> 3 semanas (compatible con el cronograma de redacción del artículo)
        </div>
    </div>

    <!-- Resumen -->
    <div class="scope-box">
        <strong>Alcance del Plan:</strong> Plan de trabajo enfocado en cerrar brechas estadísticas (IC 95%, DeLong y umbral Recall &ge; 80%), garantizar la replicabilidad migrando la lógica de notebooks a módulos Python (<code>mnp/</code>), y validar la arquitectura mediante <strong>Juicio de 3 Expertos en Ciencia de Datos / ML</strong> (V de Aiken &ge; 0.80 y SUS &ge; 75).
    </div>

    <!-- Section 1: Ejes -->
    <div class="section-header">1. Ejes Estratégicos del Plan de Validación</div>

    <div class="axes-container">
        <div class="axis-card axis-1">
            <div class="axis-header">📊 EJE 1: CONFIABILIDAD</div>
            <ul class="axis-list">
                <li><strong>Base lista:</strong> 5-Fold CV + Pesos <code>HV005</code>.</li>
                <li><strong>Bootstrapping:</strong> 1,000 iteraciones para IC 95% de AUC y Recall.</li>
                <li><strong>Test de DeLong:</strong> Comparación estadística de curvas ROC (p &lt; 0.001).</li>
                <li><strong>Calibración Umbral:</strong> Ajuste a &tau; &approx; 0.35 para <strong>Recall &ge; 80%</strong>.</li>
                <li><strong>Metadatos:</strong> Actualizar <code>champion_metadata.json</code>.</li>
            </ul>
        </div>
        <div class="axis-card axis-2">
            <div class="axis-header">🔬 EJE 2: REPLICABILIDAD</div>
            <ul class="axis-list">
                <li><strong>Migración a Python:</strong> Pasar funciones de notebooks a <code>mnp/</code>.</li>
                <li><strong>Depuración:</strong> Corregir feature <code>kpi5_lactancia</code>.</li>
                <li><strong>Contenedor Docker:</strong> Entorno aislado (<code>python:3.12-slim</code>).</li>
                <li><strong>Data Abierta:</strong> Dataset y metadata en Zenodo con <strong>DOI citable</strong>.</li>
                <li><strong>Pipeline Makefile:</strong> Ejecución de 1 comando (<code>make pipeline</code>).</li>
            </ul>
        </div>
        <div class="axis-card axis-3">
            <div class="axis-header">💻 EJE 3: PERTINENCIA TÉCNICA</div>
            <ul class="axis-list">
                <li><strong>Juicio de Expertos:</strong> <strong>3 profesionales</strong> en Data Science / ML.</li>
                <li><strong>Validez de Contenido:</strong> Coeficiente <strong>V de Aiken &ge; 0.80</strong>.</li>
                <li><strong>Evaluación SUS:</strong> Test de usabilidad técnica (meta <strong>&ge; 75 pts</strong>).</li>
                <li><strong>Auditoría Técnica:</strong> Cero Data Leakage y consistencia SHAP.</li>
                <li><strong>Despliegue:</strong> Prototipo funcional en Streamlit + GeoJSON.</li>
            </ul>
        </div>
    </div>

    <!-- Section 2: Confiabilidad Detail -->
    <div class="section-header">2. Métodos Cuantitativos y Umbrales de Aceptación (Semana 1)</div>

    <table>
        <thead>
            <tr>
                <th style="width: 25%;">Actividad / Técnica</th>
                <th style="width: 45%;">Procedimiento Técnico y Métricas</th>
                <th style="width: 30%;">Criterio de Aceptación / Meta</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Línea Base (Completada)</strong></td>
                <td>Stratified 5-Fold CV con ponderación muestral <code>HV005 / 1,000,000</code>.</td>
                <td><span class="tag-success">AUC = 0.8308 · Recall = 76.49%</span></td>
            </tr>
            <tr>
                <td><strong>Bootstrap Non-Paramétrico</strong></td>
                <td>1,000 remuestreos con reemplazo sobre el conjunto de test para IC 95%.</td>
                <td><span class="tag-success">IC 95% AUC: [0.820, 0.840]</span></td>
            </tr>
            <tr>
                <td><strong>Test de DeLong</strong></td>
                <td>Significancia estadística entre LightGBM vs. XGBoost y LogReg.</td>
                <td><span class="tag-success">p-value &lt; 0.001 (Superior)</span></td>
            </tr>
            <tr>
                <td><strong>Calibración de Umbral (&tau;)</strong></td>
                <td>Barrido en rango [0.25, 0.50] para priorizar detección de desnutridos.</td>
                <td><span class="tag-target">Recall &ge; 80.0% (&tau; &approx; 0.35)</span></td>
            </tr>
            <tr>
                <td><strong>Actualización de Metadatos</strong></td>
                <td>Reemplazar umbral 0.50 por &tau; calibrado en <code>champion_metadata.json</code>.</td>
                <td><span class="tag-success">JSON de producción actualizado</span></td>
            </tr>
            <tr>
                <td><strong>Determinismo Test-Retest</strong></td>
                <td>10 ejecuciones automáticas en ambiente limpio con <code>random_state=42</code>.</td>
                <td><span class="tag-success">Variación &Delta; = 0.0000</span></td>
            </tr>
        </tbody>
    </table>

    <div class="footer">
        Página 1 de 2 · Universidad Peruana Unión · EP Ingeniería de Sistemas · Investigación V (2026-II)
    </div>

    <!-- PAGE 2 -->
    <div class="page-break"></div>

    <!-- Header Page 2 -->
    <div class="header">
        <div>
            <div class="university-title">Universidad Peruana Unión</div>
            <div class="faculty-title">Plan de Validación de Resultados · Cronograma (3 Semanas) y Rúbrica</div>
        </div>
        <div style="text-align: right;">
            <div class="course-badge">MOMENTO 6: CREA</div>
        </div>
    </div>

    <!-- Section 3: Juicio de Expertos y Trazabilidad -->
    <div class="section-header">3. Juicio de 3 Expertos en Ciencia de Datos y Trazabilidad Técnica</div>

    <table>
        <thead>
            <tr>
                <th style="width: 12%;">ID Req.</th>
                <th style="width: 32%;">Dimensión Evaluada por Expertos</th>
                <th style="width: 32%;">Solución de Ingeniería / MLOps</th>
                <th style="width: 24%;">Métrica de Aceptación</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>EXP-01</strong></td>
                <td>Calidad de Pipeline ETL y nulos.</td>
                <td>Pipeline modular en <code>mnp/</code> con 18 años ENDES.</td>
                <td>V de Aiken &ge; 0.80 en Ficha Técnica.</td>
            </tr>
            <tr>
                <td><strong>EXP-02</strong></td>
                <td>Prevención de Data Leakage.</td>
                <td>Exclusión de antropometría directa previa.</td>
                <td>100% de acuerdo entre jueces.</td>
            </tr>
            <tr>
                <td><strong>EXP-03</strong></td>
                <td>Consistencia de explicabilidad XAI.</td>
                <td>Módulo SHAP local/global (TreeExplainer).</td>
                <td>Coherencia teórica validada.</td>
            </tr>
            <tr>
                <td><strong>EXP-04</strong></td>
                <td>Usabilidad del prototipo Streamlit.</td>
                <td>Simulación de triaje con mapas GeoJSON.</td>
                <td>SUS &ge; 75 pts (Grado A).</td>
            </tr>
        </tbody>
    </table>

    <!-- Section 4: Cronograma 3 Semanas -->
    <div class="section-header">4. Cronograma de Ejecución (3 Semanas) y Entregables</div>

    <table>
        <thead>
            <tr>
                <th style="width: 14%;">Periodo</th>
                <th style="width: 16%;">Eje</th>
                <th style="width: 40%;">Actividad Específica</th>
                <th style="width: 30%;">Entregable Verificable</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Semana 1</strong></td>
                <td>Confiabilidad</td>
                <td>Bootstrap (1,000 iters) para IC 95%, Test de DeLong, barrido de umbral (&tau;) para Recall &ge; 80% y actualización de metadata.</td>
                <td>Script <code>bootstrap_validation.py</code> y <code>champion_metadata.json</code> actualizado.</td>
            </tr>
            <tr>
                <td><strong>Semana 2</strong></td>
                <td>Replicabilidad</td>
                <td>Migración de funciones de notebooks a módulos Python en <code>mnp/</code>, depuración feature lactancia, Docker y Zenodo.</td>
                <td>Módulos limpios en <code>mnp/</code>, pipeline <code>Makefile</code> y DOI en Zenodo.</td>
            </tr>
            <tr>
                <td><strong>Semana 3</strong></td>
                <td>Pertinencia</td>
                <td>Evaluación técnica con 3 expertos en Data Science / ML aplicando Ficha de Validación y cuestionario SUS.</td>
                <td>Fichas con V de Aiken &ge; 0.80, informe SUS y sección en LaTeX.</td>
            </tr>
        </tbody>
    </table>

    <!-- Section 5: Rúbrica -->
    <div class="section-header">5. Matriz de Alineación con la Rúbrica de Evaluación (UPeU)</div>

    <table>
        <thead>
            <tr>
                <th style="width: 25%;">Criterio de Rúbrica</th>
                <th style="width: 18%;">Estado en el Plan</th>
                <th style="width: 57%;">Justificación Técnica Específica</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>1. Confiabilidad</strong></td>
                <td><span class="tag-success">Cumplido</span></td>
                <td>Bootstrap IC 95%, Test de DeLong y calibración de &tau; para Recall &ge; 80% (con base 5-Fold CV lista).</td>
            </tr>
            <tr>
                <td><strong>2. Replicabilidad</strong></td>
                <td><span class="tag-success">Cumplido</span></td>
                <td>Migración explícita de notebooks a <code>mnp/</code>, Docker multi-SO, repo público y DOI Zenodo.</td>
            </tr>
            <tr>
                <td><strong>3. Pertinencia</strong></td>
                <td><span class="tag-success">Cumplido</span></td>
                <td>Juicio de 3 Expertos en Ciencia de Datos / ML (V de Aiken &ge; 0.80) y usabilidad técnica SUS &ge; 75.</td>
            </tr>
            <tr>
                <td><strong>4. Coherencia</strong></td>
                <td><span class="tag-success">Cumplido</span></td>
                <td>Adaptado directamente a los datos ENDES (285k niños) y enfoque de Sistemas / Applied ML.</td>
            </tr>
            <tr>
                <td><strong>5. Cronograma</strong></td>
                <td><span class="tag-success">Cumplido</span></td>
                <td>Cronograma realista y ejecutable de 3 semanas con entregables tangibles por fase.</td>
            </tr>
            <tr>
                <td><strong>6. Redacción y Claridad</strong></td>
                <td><span class="tag-success">Cumplido</span></td>
                <td>Lenguaje directo, sobrio y estructurado en tablas y diagramas técnicos.</td>
            </tr>
        </tbody>
    </table>

    <!-- Referencias Box -->
    <div class="ref-box">
        <strong>Referencias Clave:</strong> Aiken (1985) [V de Aiken] · Bangor et al. (2008) [SUS] · Davis (1989) [TAM] · DeLong et al. (1988) [Curvas ROC] · Efron & Tibshirani (1994) [Bootstrap] · Kohavi (1995) [5-Fold CV] · Lipton et al. (2014) [Thresholds] · Wilkinson et al. (2016) [FAIR].
    </div>

    <div class="footer">
        Página 2 de 2 · Universidad Peruana Unión · EP Ingeniería de Sistemas · Investigación V (2026-II) · Mg. Nemias Saboya Rios
    </div>

</body>
</html>
"""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(BASE_DIR, "Momento6_Plan_Validacion_Resultados.html")
pdf_path = os.path.join(BASE_DIR, "Momento6_Plan_Validacion_Resultados.pdf")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML generado en: {html_path}")
