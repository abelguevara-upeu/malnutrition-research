import subprocess
import os

html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Momento 5: Ficha de Auditoría de Validación - UPeU</title>
    <style>
        @page {
            size: A4;
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
            line-height: 1.35;
            font-size: 9.5pt;
            margin: 0;
            padding: 0;
            background-color: #ffffff;
        }

        /* Header Styling */
        .header {
            border-bottom: 2px solid #003366;
            padding-bottom: 6px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .university-title {
            font-size: 12pt;
            font-weight: bold;
            color: #003366;
            text-transform: uppercase;
            margin: 0;
        }

        .faculty-title {
            font-size: 8.5pt;
            color: #555;
            margin: 1px 0 0 0;
            font-weight: 600;
        }

        .course-badge {
            background-color: #f0a500;
            color: #003366;
            padding: 2px 6px;
            font-size: 8pt;
            font-weight: bold;
            border-radius: 3px;
            display: inline-block;
            margin-top: 3px;
        }

        /* Document Title */
        .doc-title-container {
            background: linear-gradient(135deg, #003366 0%, #002244 100%);
            color: white;
            padding: 8px 12px;
            border-radius: 5px;
            margin-bottom: 10px;
        }

        .doc-subtitle {
            font-size: 7.5pt;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #f0a500;
            font-weight: 700;
            margin: 0 0 1px 0;
        }

        .doc-title {
            font-size: 12pt;
            font-weight: 800;
            margin: 0;
        }

        /* Metadata Grid */
        .meta-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 6px;
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            padding: 6px 10px;
            border-radius: 4px;
            margin-bottom: 10px;
            font-size: 8.5pt;
        }

        .meta-item {
            margin-bottom: 1px;
        }

        .meta-label {
            font-weight: bold;
            color: #003366;
        }

        /* Section Titles */
        .section-header {
            font-size: 9.5pt;
            font-weight: bold;
            color: #003366;
            border-left: 3px solid #f0a500;
            padding-left: 6px;
            margin: 10px 0 6px 0;
            text-transform: uppercase;
        }

        /* Table Styling */
        table.audit-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 4px;
            margin-bottom: 10px;
            font-size: 8pt;
            background-color: white;
        }

        table.audit-table th {
            background-color: #003366;
            color: white;
            padding: 6px 8px;
            text-align: left;
            font-weight: 700;
            border: 1px solid #002244;
            text-transform: uppercase;
            font-size: 7.5pt;
        }

        table.audit-table td {
            padding: 5px 8px;
            border: 1px solid #cbd5e1;
            vertical-align: top;
        }

        table.audit-table tr:nth-child(even) {
            background-color: #f8fafc;
        }

        .score-col {
            text-align: center;
            font-weight: bold;
            width: 75px;
            white-space: nowrap;
        }

        .badge-score {
            background-color: #2563eb;
            color: white;
            padding: 2px 6px;
            border-radius: 8px;
            font-size: 7.5pt;
            font-weight: bold;
            display: inline-block;
        }

        .total-row {
            background-color: #fff8e6 !important;
            font-weight: bold;
            font-size: 8.5pt;
        }

        .total-row td {
            border-top: 2px solid #f0a500 !important;
            color: #003366;
        }

        .total-score-badge {
            background-color: #f0a500;
            color: #003366;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 9pt;
            font-weight: 800;
        }

        /* Simple Detail Card */
        .detail-card {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-left: 3px solid #003366;
            border-radius: 4px;
            padding: 5px 8px;
            margin-bottom: 5px;
            font-size: 8pt;
        }

        .detail-title {
            font-weight: bold;
            color: #003366;
            margin-bottom: 1px;
        }

        .detail-desc {
            color: #334155;
            margin: 0;
        }

        /* Footer */
        .footer {
            margin-top: 10px;
            padding-top: 4px;
            border-top: 1px solid #cbd5e1;
            font-size: 7pt;
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
            <div class="course-badge">INVESTIGACIÓN V · SESIÓN 02 (MOMENTO 5)</div>
        </div>
    </div>

    <!-- Document Title -->
    <div class="doc-title-container">
        <div class="doc-subtitle">Aplica - Auditoría de Validación</div>
        <div class="doc-title">Ficha de Auditoría de Validación de Solución Tecnológica</div>
    </div>

    <!-- Metadata Grid -->
    <div class="meta-grid">
        <div>
            <div class="meta-item"><span class="meta-label">Proyecto:</span> Predicción de Riesgo de Desnutrición Crónica Infantil (ENDES 2007-2024)</div>
            <div class="meta-item"><span class="meta-label">Curso:</span> Investigación V (Ciclo X – 2026-II)</div>
        </div>
        <div>
            <div class="meta-item"><span class="meta-label">Docente:</span> Mg. Nemias Saboya Rios</div>
            <div class="meta-item"><span class="meta-label">Equipo:</span> A. Guevara, V. Vergara, P. Vallejos</div>
        </div>
    </div>

    <!-- Section 1: Table -->
    <div class="section-header">1. Ficha de Auditoría de Validación</div>
    
    <table class="audit-table">
        <thead>
            <tr>
                <th style="width: 32%;">Criterio</th>
                <th style="width: 53%;">Evidencia Encontrada en el Proyecto</th>
                <th style="width: 15%; text-align: center;">Puntaje</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>1. Confiabilidad estadística reportada</strong><br><span style="color: #64748b; font-size: 7pt;">(Alfa, Kappa u otra)</span></td>
                <td>Validación cruzada en 5 partes (5-Fold CV) con pesos de encuesta. Métricas: AUC-ROC = 0.83, Recall = 76.5%, Precision = 37.1%. Se validó consistencia de datos en el cruce de tablas.</td>
                <td class="score-col"><span class="badge-score">3 / 4 pts</span></td>
            </tr>
            <tr>
                <td><strong>2. Método de validación de resultados declarado</strong></td>
                <td>Se probó y comparó 6 modelos (LightGBM, XGBoost, CatBoost, Regresión Logística, Árbol de Decisión y Red Neuronal). Modelo ganador: LightGBM.</td>
                <td class="score-col"><span class="badge-score">3 / 4 pts</span></td>
            </tr>
            <tr>
                <td><strong>3. Confiabilidad de sistema / determinismo</strong></td>
                <td>Uso de semilla aleatoria fija (random_state = 42) en el código. El sistema da exactamente el mismo resultado cada vez que se ejecuta.</td>
                <td class="score-col"><span class="badge-score">3 / 3 pts</span></td>
            </tr>
            <tr>
                <td><strong>4. Datos y/o código disponibles públicamente</strong></td>
                <td>Código organizado y subido a GitHub público. Los datos vienen de la encuesta oficial pública ENDES del INEI (2007-2024).</td>
                <td class="score-col"><span class="badge-score">3 / 3 pts</span></td>
            </tr>
            <tr>
                <td><strong>5. Entorno y dependencias documentadas</strong></td>
                <td>Proyecto empaquetado con Docker (Dockerfile y docker-compose) y archivo pyproject.toml con las versiones exactas de las librerías de Python.</td>
                <td class="score-col"><span class="badge-score">3 / 3 pts</span></td>
            </tr>
            <tr>
                <td><strong>6. Pertinencia validada con usuarios reales</strong></td>
                <td>Proyecto enfocado en la necesidad del MINSA para priorizar visitas. Tiene prototipo en Streamlit, pero aún falta probarlo directamente con personal de salud en campo.</td>
                <td class="score-col"><span class="badge-score" style="background-color: #e11d48;">1 / 3 pts</span></td>
            </tr>
            <tr class="total-row">
                <td colspan="2" style="text-align: right; vertical-align: middle; padding-right: 12px;">
                    <strong>PUNTAJE TOTAL LOGRADO:</strong>
                </td>
                <td class="score-col">
                    <span class="total-score-badge">14 / 20</span>
                </td>
            </tr>
        </tbody>
    </table>

    <!-- Section 2 -->
    <div class="section-header">2. Resumen Metodológico</div>

    <div class="detail-card">
        <div class="detail-title">Confiabilidad (6 / 8 Puntos)</div>
        <div class="detail-desc">El modelo se evaluó con validación cruzada y pesos demográficos de la ENDES. Da resultados estables y deterministas al usar una semilla fija (seed=42). Queda pendiente calcular intervalos de confianza al 95%.</div>
    </div>

    <div class="detail-card">
        <div class="detail-title">Replicabilidad (6 / 6 Puntos)</div>
        <div class="detail-desc">El proyecto es 100% reproducible: el código está en GitHub, los datos son públicos de la ENDES y el entorno está listo para correr con Docker y Makefile.</div>
    </div>

    <div class="detail-card">
        <div class="detail-title">Pertinencia (2 / 6 Puntos - Brecha Principal)</div>
        <div class="detail-desc">La solución responde a la necesidad real de triaje para el MINSA y cuenta con prototipo en Streamlit, pero requiere pruebas directas de usabilidad con usuarios finales en campo para completar su validación.</div>
    </div>

    <!-- Section 3 -->
    <div class="section-header">3. Conclusión de la Auditoría</div>
    <div style="background-color: #f8fafc; border: 1px solid #cbd5e1; border-radius: 4px; padding: 6px 10px; font-size: 8pt; color: #1e293b;">
        <strong>Resultado: Puntaje 14 / 20 (Nivel Aceptable).</strong> El proyecto cuenta con buena base técnica y de replicabilidad. La principal mejora para el reto autónomo (Momento 6) es ejecutar las pruebas reales con usuarios de salud y optimizar el umbral de decisión para elevar la cobertura (Recall) al 80%.
    </div>

    <!-- Footer -->
    <div class="footer">
        Universidad Peruana Unión · EP Ingeniería de Sistemas · Investigación V (2026-II) · Mg. Nemias Saboya Rios
    </div>

</body>
</html>
"""

html_path = "/Users/abelguevarah/Desktop/invs/malnutrition-research/expo/semestre2/sesion2/Momento5_Ficha_Auditoria_Validacion.html"
pdf_path = "/Users/abelguevarah/Desktop/invs/malnutrition-research/expo/semestre2/sesion2/Momento5_Ficha_Auditoria_Validacion.pdf"

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

chrome_cmd = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "--headless",
    "--disable-gpu",
    "--no-sandbox",
    f"--print-to-pdf={pdf_path}",
    html_path
]

result = subprocess.run(chrome_cmd, capture_output=True, text=True)
if result.returncode == 0 and os.path.exists(pdf_path):
    print(f"PDF de 1 página generado en: {pdf_path}")
else:
    print(f"Error al generar PDF: {result.stderr}")
