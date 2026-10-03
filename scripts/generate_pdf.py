"""
Script para generar el PDF elegante de la Guía de Demostración y Oratoria
Optimizado para un diseño impecable de 3 páginas completas sin desbordes.
"""
import os
import subprocess
import sys

html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Guía Maestra de Demostración y Oratoria - LG14</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Fira+Code:wght@400;500;600&display=swap');

        @page {
            size: A4;
            margin: 12mm 14mm 12mm 14mm;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            color: #1e293b;
            background-color: #ffffff;
            line-height: 1.45;
            font-size: 11.5px;
            margin: 0;
            padding: 0;
        }

        .header-box {
            background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
            color: #ffffff;
            padding: 16px 20px;
            border-radius: 10px;
            margin-bottom: 14px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        .header-box h1 {
            margin: 0 0 4px 0;
            font-size: 19px;
            font-weight: 800;
            letter-spacing: -0.5px;
        }

        .header-box .meta {
            font-size: 11px;
            opacity: 0.95;
            line-height: 1.5;
        }

        .badge-pill {
            display: inline-block;
            background: rgba(255, 255, 255, 0.22);
            padding: 2px 10px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 10px;
            margin-top: 5px;
            letter-spacing: 0.2px;
        }

        h2 {
            font-size: 14px;
            font-weight: 700;
            color: #0f172a;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 4px;
            margin-top: 14px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 10px 14px;
            margin-bottom: 10px;
            page-break-inside: avoid;
        }

        .card-title {
            font-weight: 700;
            font-size: 12.5px;
            color: #1e3a8a;
            margin-bottom: 5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .tag-time {
            background: #dbeafe;
            color: #1e40af;
            font-size: 10px;
            font-weight: 700;
            padding: 2px 7px;
            border-radius: 5px;
        }

        blockquote {
            margin: 6px 0;
            padding: 8px 12px;
            background: #eff6ff;
            border-left: 3.5px solid #3b82f6;
            color: #1e293b;
            font-style: italic;
            border-radius: 0 6px 6px 0;
            font-size: 11px;
            line-height: 1.45;
        }

        .point-highlight {
            background: #fefce8;
            border: 1px solid #fef08a;
            padding: 6px 10px;
            border-radius: 6px;
            color: #854d0e;
            font-size: 10.5px;
            margin-top: 6px;
            font-weight: 500;
        }

        pre, code {
            font-family: 'Fira Code', Consolas, Monaco, monospace;
        }

        code {
            background: #e2e8f0;
            color: #0f172a;
            padding: 1px 4px;
            border-radius: 3px;
            font-size: 10.5px;
        }

        pre {
            background: #0f172a;
            color: #f8fafc;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 10.5px;
            margin: 6px 0;
            line-height: 1.35;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 10.5px;
            margin: 8px 0;
            page-break-inside: avoid;
        }

        th, td {
            padding: 6px 8px;
            text-align: left;
            border: 1px solid #cbd5e1;
        }

        th {
            background: #1e293b;
            color: #ffffff;
            font-weight: 600;
        }

        tr:nth-child(even) {
            background: #f8fafc;
        }

        .faq-box {
            background: #fdf4ff;
            border: 1px solid #f5d0fe;
            border-left: 3.5px solid #c026d3;
            padding: 8px 12px;
            border-radius: 0 6px 6px 0;
            margin-bottom: 8px;
            page-break-inside: avoid;
        }

        .faq-q {
            font-weight: 700;
            color: #86198f;
            margin-bottom: 3px;
            font-size: 11.5px;
        }

        .faq-a {
            color: #334155;
            font-size: 11px;
            line-height: 1.4;
        }

        .checklist {
            list-style: none;
            padding-left: 0;
            margin: 6px 0;
        }

        .checklist li {
            padding: 3px 0;
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 11.5px;
        }

        .page-break {
            page-break-before: always;
        }
    </style>
</head>
<body>

    <!-- ==================== PÁGINA 1 ==================== -->
    <div class="header-box">
        <h1>🎓 Guía Maestra de Demostración y Oratoria</h1>
        <div class="meta">
            <strong>Asignatura:</strong> Big Data / Sistemas Distribuidos — <strong>Universidad del Valle</strong> (LG14)<br>
            <strong>Proyecto:</strong> Despliegue y Validación de un Clúster Distribuido Apache Spark con Docker (Grupo 4)
        </div>
        <div class="badge-pill">Criterio Rector: Encontrar → Comprender → Desplegar → Probar → Analizar</div>
    </div>

    <h2>⏱️ 1. Cronograma de la Presentación (7 a 10 Minutos)</h2>
    <table>
        <thead>
            <tr>
                <th style="width: 25%;">Fase</th>
                <th style="width: 14%;">Tiempo</th>
                <th>Objetivo Principal de la Demostración</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>1. Introducción y Selección</strong></td>
                <td>1 min</td>
                <td>Justificar la elección de Apache Spark y registro formal del repositorio.</td>
            </tr>
            <tr>
                <td><strong>2. Arquitectura del Clúster</strong></td>
                <td>2 min</td>
                <td>Explicar los 4 contenedores, red Bridge, volumen compartido y flujo RPC.</td>
            </tr>
            <tr>
                <td><strong>3. Demostración en Vivo</strong></td>
                <td>4 min</td>
                <td>Validar <code>docker ps</code>, Master UI (2 workers) y ejecutar las 3 pruebas funcionales.</td>
            </tr>
            <tr>
                <td><strong>4. Comparativa con Hadoop</strong></td>
                <td>2 min</td>
                <td>Defender ventajas de Spark en memoria vs MapReduce en disco.</td>
            </tr>
            <tr>
                <td><strong>5. Conclusiones y Cierre</strong></td>
                <td>1 min</td>
                <td>Presentar historial de 5 commits y lecciones aprendidas.</td>
            </tr>
        </tbody>
    </table>

    <h2>🎙️ 2. Guion de Oratoria y Acciones en Pantalla</h2>

    <div class="card">
        <div class="card-title">
            <span>FASE 1: Introducción y Selección del Repositorio</span>
            <span class="tag-time">1 Minuto</span>
        </div>
        <p style="margin: 3px 0;"><strong>🖥️ Acción en pantalla:</strong> Mostrar portada del <code>README.md</code> (Sección 1 y 2).</p>
        <blockquote>
            "Buenas tardes, docente y compañeros. Para la práctica LG14 seleccionamos el repositorio público <strong>spark-standalone-cluster-on-docker</strong> de André Perez, un proyecto open-source activamente mantenido con más de 500 estrellas.<br><br>
            Seleccionamos <strong>Apache Spark 3.5.7</strong> en lugar del esquema tradicional de Hadoop porque representa el estado del arte en Big Data moderno: procesamiento distribuido en memoria RAM, lo que permite consultas hasta 100 veces más rápidas que MapReduce y soporte analítico directo en Python mediante PySpark y JupyterLab."
        </blockquote>
        <div class="point-highlight">
            📌 <strong>Punto Clave a Resaltar del Requisito:</strong> Cumple con ser diferente al repositorio base, utiliza Docker Compose, posee arquitectura distribuida real y permite múltiples pruebas funcionales.
        </div>
    </div>

    <div class="card">
        <div class="card-title">
            <span>FASE 2: Comprensión y Análisis de la Arquitectura</span>
            <span class="tag-time">2 Minutos</span>
        </div>
        <p style="margin: 3px 0;"><strong>🖥️ Acción en pantalla:</strong> Mostrar el Diagrama Mermaid de Arquitectura en el <code>README.md</code> (Sección 4.3).</p>
        <blockquote>
            "Analizando la arquitectura técnica, nuestro entorno está compuesto por <strong>4 contenedores Docker</strong> orquestados en una red Bridge privada:<br>
            1. <strong>spark-master</strong>: Nodo coordinador. Expone el puerto <code>7077</code> para RPC interno y su Web UI en el puerto <code>8085</code> para monitoreo.<br>
            2. <strong>spark-worker-1 y spark-worker-2</strong>: Nodos ejecutores, cada uno con 1 Core de CPU y 1 GB de memoria RAM.<br>
            3. <strong>jupyterlab</strong>: Capa cliente en el puerto <code>8888</code> para desarrollo analítico en Python sin saturar los nodos de procesamiento.<br>
            4. <strong>Volumen <code>hadoop-distributed-file-system</code></strong>: Montado en <code>/opt/workspace</code> en todos los contenedores para persistencia común de datasets y scripts."
        </blockquote>
        <div class="point-highlight">
            📌 <strong>Punto Clave a Resaltar:</strong> Los workers dependen del Master (<code>depends_on: [spark-master]</code>) y se registran dinámicamente mediante heartbeats RPC.
        </div>
    </div>

    <div class="page-break"></div>

    <!-- ==================== PÁGINA 2 ==================== -->
    <div class="card">
        <div class="card-title">
            <span>FASE 3: Despliegue y Demostración Práctica en Vivo</span>
            <span class="tag-time">4 Minutos</span>
        </div>

        <p style="margin: 4px 0;"><strong>1. Estado de los Contenedores en Terminal:</strong></p>
        <pre><code>docker ps</code></pre>
        <blockquote>"Podemos observar que los 4 contenedores están en estado <strong>Up</strong>, con sus puertos correctamente mapeados y saludables."</blockquote>

        <p style="margin: 4px 0;"><strong>2. Monitoreo en la Web UI de Spark Master:</strong></p>
        <p style="margin: 2px 0;">Abrir en el navegador: <code>http://localhost:8085</code></p>
        <blockquote>"Al ingresar a la interfaz del Master, confirmamos el estado <strong>ALIVE</strong> y la métrica fundamental de Big Data: <strong>Alive Workers = 2</strong>, con 2 Cores y 2 GB de memoria totales listos para cómputo."</blockquote>

        <p style="margin: 4px 0;"><strong>3. Ejecución del Circuito de Pruebas Distribuidas:</strong></p>
        <pre><code>python scripts/run_all_tests.py</code></pre>
        
        <p style="margin: 4px 0;"><strong>Explicación de cada prueba durante la ejecución en vivo:</strong></p>
        <ul style="margin: 4px 0; padding-left: 18px;">
            <li><strong>Prueba 1 (SparkPi - Monte Carlo):</strong> <em>"Dividió el cálculo de Pi en 10 particiones asignadas en paralelo a los dos workers (<code>172.21.0.3</code> y <code>172.21.0.4</code>), imprimiendo <code>Pi is roughly 3.14...</code> y demostrando paralelismo de CPU real."</em></li>
            <li><strong>Prueba 2 (PySpark DataFrames):</strong> <em>"Ejecuta <code>test_pyspark.py</code> aplicando transformaciones en memoria y filtrado distribuido sobre 5 registros en menos de 10 segundos."</em></li>
            <li><strong>Prueba 3 (Spark SQL y Agregaciones):</strong> <em>"Ejecuta <code>test_spark_sql.py</code> con consultas SQL nativas y agregaciones <code>groupBy</code> de telemetría de CPU y memoria sobre datos particionados."</em></li>
        </ul>
    </div>

    <div class="card">
        <div class="card-title">
            <span>FASE 4: Análisis Comparativo con docker-hadoop</span>
            <span class="tag-time">2 Minutos</span>
        </div>
        <p style="margin: 3px 0;"><strong>🖥️ Acción en pantalla:</strong> Mostrar la Tabla Comparativa en el <code>README.md</code> (Sección 8).</p>
        <table>
            <thead>
                <tr>
                    <th>Característica</th>
                    <th>docker-hadoop (Referencia)</th>
                    <th>spark-standalone-cluster (Nuestro)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Tecnología Principal</strong></td>
                    <td>Apache Hadoop (HDFS + MapReduce)</td>
                    <td><strong>Apache Spark (v3.5.7)</strong></td>
                </tr>
                <tr>
                    <td><strong>Paradigma de Cómputo</strong></td>
                    <td>En Disco (I/O intensivo en cada etapa)</td>
                    <td><strong>En Memoria RAM (hasta 100x más veloz)</strong></td>
                </tr>
                <tr>
                    <td><strong>Contenedores</strong></td>
                    <td>5 (Namenode, Datanode, Resourcemanager, etc.)</td>
                    <td><strong>4 (Master, 2 Workers, JupyterLab)</strong></td>
                </tr>
                <tr>
                    <td><strong>Entorno Analítico</strong></td>
                    <td>Compilación manual de Jars Java</td>
                    <td><strong>JupyterLab interactivo (PySpark/Scala/R)</strong></td>
                </tr>
                <tr>
                    <td><strong>Caso de Uso</strong></td>
                    <td>Batch histórico y almacenamiento masivo</td>
                    <td><strong>Analítica interactiva, ML y streaming</strong></td>
                </tr>
            </tbody>
        </table>
        <blockquote>
            "Conclusión: Hadoop es excelente para archivo y procesamiento por lotes en frío, pero <strong>Spark es la herramienta líder para analítica moderna, consultas interactivas y ciencia de datos</strong>."
        </blockquote>
    </div>

    <div class="page-break"></div>

    <!-- ==================== PÁGINA 3 ==================== -->
    <div class="card">
        <div class="card-title">
            <span>FASE 5: Conclusiones y Cumplimiento de Entrega</span>
            <span class="tag-time">1 Minuto</span>
        </div>
        <blockquote>
            "Para finalizar, el proyecto se encuentra publicado en nuestro repositorio público de GitHub <strong>bigdata-grupo-4</strong>, cumpliendo con la documentación técnica completa, diagramas de arquitectura, scripts de validación y un historial de <strong>5 commits</strong> que evidencian el avance incremental del trabajo. Quedamos a disposición para preguntas."
        </blockquote>
    </div>

    <h2>🛡️ 3. Banco de Preguntas Defensivas</h2>

    <div class="faq-box">
        <div class="faq-q">❓ P1: ¿Cómo demuestran que las tareas realmente se ejecutan de forma distribuida y no en un solo nodo?</div>
        <div class="faq-a"><strong>Respuesta:</strong> En los logs de ejecución de <code>SparkPi</code> y <code>test_pyspark.py</code>, el <code>DAGScheduler</code> de Spark divide el trabajo en <code>ResultStages</code> con múltiples particiones. En los logs se observan los ejecutores <code>app-.../0</code> y <code>app-.../1</code> operando en las IPs distintas de ambos nodos (<code>172.21.0.3</code> de worker-1 y <code>172.21.0.4</code> de worker-2). Además, en la Web UI (<code>localhost:8085</code>) se ve el balanceo de Cores y memoria en ambos trabajadores.</div>
    </div>

    <div class="faq-box">
        <div class="faq-q">❓ P2: ¿Qué sucede si se cae un nodo trabajador (Worker)?</div>
        <div class="faq-a"><strong>Respuesta:</strong> Apache Spark posee tolerancia a fallos mediante el linaje de RDDs (Resilient Distributed Datasets). Si un worker cae, el Master redistribuye automáticamente las particiones faltantes al worker restante sin interrumpir la sesión del usuario.</div>
    </div>

    <div class="faq-box">
        <div class="faq-q">❓ P3: ¿Por qué configuraron el puerto Web del Master en 8085?</div>
        <div class="faq-a"><strong>Respuesta:</strong> Para evitar colisiones en entornos locales donde el puerto estándar <code>8080</code> suele estar reservado por servidores del sistema (como Oracle XE o Apache HTTP), mapeamos <code>8085:8080</code> en el host manteniendo intacto el puerto interno <code>8080</code> dentro del contenedor.</div>
    </div>

    <h2>📋 4. Checklist Pre-Presentación</h2>
    <ul class="checklist">
        <li><input type="checkbox" checked> Docker Desktop iniciado y en verde (<strong>Engine running</strong>).</li>
        <li><input type="checkbox" checked> Contenedores arriba (<code>docker ps</code> muestra los 4 contenedores Up).</li>
        <li><input type="checkbox" checked> Pestaña 1 lista: Spark Master en <code>http://localhost:8085</code> (2 Alive Workers).</li>
        <li><input type="checkbox" checked> Pestaña 2 lista: JupyterLab en <code>http://localhost:8888</code>.</li>
        <li><input type="checkbox" checked> Pestaña 3 lista: <code>README.md</code> en GitHub/VSCode para mostrar arquitectura y comparativa.</li>
        <li><input type="checkbox" checked> Terminal abierta lista para ejecutar <code>python scripts/run_all_tests.py</code>.</li>
    </ul>

</body>
</html>
"""

temp_html = os.path.abspath("docs/guia_temp.html")
pdf_output = os.path.abspath("docs/GUIA_DEMOSTRACION_Y_ORATORIA.pdf")

with open(temp_html, "w", encoding="utf-8") as f:
    f.write(html_content)

edge_paths = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
]

browser_exe = None
for p in edge_paths:
    if os.path.exists(p):
        browser_exe = p
        break

if not browser_exe:
    print("Error: No se encontró navegador compatible.")
    sys.exit(1)

cmd = [
    browser_exe,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_output}",
    f"file:///{temp_html.replace(os.sep, '/')}"
]

subprocess.run(cmd, capture_output=True, text=True)

if os.path.exists(pdf_output) and os.path.getsize(pdf_output) > 0:
    print(f"[OK] PDF optimizado generado exitosamente: {pdf_output}")
    try:
        os.remove(temp_html)
    except Exception:
        pass
    sys.exit(0)
else:
    sys.exit(1)
