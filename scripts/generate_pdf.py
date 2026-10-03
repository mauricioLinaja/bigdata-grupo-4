"""
Script para generar el PDF de la Guía de Demostración y Oratoria
Con la tabla comparativa completa de 11 criterios y diseño contrastado de alta legibilidad.
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
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Fira+Code:wght@400;500;600&display=swap');

        @page {
            size: A4;
            margin: 10mm 12mm 10mm 12mm;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            color: #0f172a;
            background-color: #ffffff;
            line-height: 1.4;
            font-size: 11px;
            margin: 0;
            padding: 0;
        }

        .header-box {
            background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
            color: #ffffff;
            padding: 14px 18px;
            border-radius: 8px;
            margin-bottom: 10px;
        }

        .header-box h1 {
            margin: 0 0 4px 0;
            font-size: 18px;
            font-weight: 800;
        }

        .header-box .meta {
            font-size: 10.5px;
            opacity: 0.95;
            line-height: 1.4;
        }

        .badge-pill {
            display: inline-block;
            background: rgba(255, 255, 255, 0.25);
            padding: 2px 8px;
            border-radius: 15px;
            font-weight: 600;
            font-size: 9.5px;
            margin-top: 4px;
        }

        h2 {
            font-size: 13px;
            font-weight: 700;
            color: #0f172a;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 3px;
            margin-top: 10px;
            margin-bottom: 8px;
        }

        .card {
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            padding: 8px 12px;
            margin-bottom: 8px;
            page-break-inside: avoid;
        }

        .card-title {
            font-weight: 700;
            font-size: 12px;
            color: #1e3a8a;
            margin-bottom: 4px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .tag-time {
            background: #dbeafe;
            color: #1e40af;
            font-size: 9.5px;
            font-weight: 700;
            padding: 1px 6px;
            border-radius: 4px;
        }

        blockquote {
            margin: 5px 0;
            padding: 6px 10px;
            background: #f0f9ff;
            border-left: 3px solid #0284c7;
            color: #0c4a6e;
            font-style: italic;
            border-radius: 0 4px 4px 0;
            font-size: 10.5px;
            line-height: 1.35;
        }

        .point-highlight {
            background: #fefce8;
            border: 1px solid #fef08a;
            padding: 4px 8px;
            border-radius: 4px;
            color: #854d0e;
            font-size: 10px;
            margin-top: 4px;
            font-weight: 500;
        }

        pre, code {
            font-family: 'Fira Code', Consolas, Monaco, monospace;
        }

        code {
            background: #f1f5f9;
            color: #0f172a;
            padding: 1px 3px;
            border-radius: 3px;
            font-size: 10px;
        }

        pre {
            background: #0f172a;
            color: #f8fafc;
            padding: 6px 10px;
            border-radius: 4px;
            font-size: 10px;
            margin: 4px 0;
            line-height: 1.3;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 9.5px;
            margin: 6px 0;
            page-break-inside: avoid;
        }

        th, td {
            padding: 4.5px 7px;
            text-align: left;
            border: 1px solid #94a3b8;
            color: #0f172a;
        }

        th {
            background: #1e293b;
            color: #ffffff !important;
            font-weight: 700;
        }

        tr:nth-child(even) {
            background: #f8fafc;
        }

        tr:nth-child(odd) {
            background: #ffffff;
        }

        .faq-box {
            background: #faf5ff;
            border: 1px solid #e9d5ff;
            border-left: 3.5px solid #a855f7;
            padding: 6px 10px;
            border-radius: 0 4px 4px 0;
            margin-bottom: 6px;
            page-break-inside: avoid;
        }

        .faq-q {
            font-weight: 700;
            color: #6b21a8;
            margin-bottom: 2px;
            font-size: 10.5px;
        }

        .faq-a {
            color: #334155;
            font-size: 10px;
            line-height: 1.35;
        }

        .checklist {
            list-style: none;
            padding-left: 0;
            margin: 4px 0;
        }

        .checklist li {
            padding: 2px 0;
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 10.5px;
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
                <td>Defender la tabla de 11 criterios: Spark en memoria vs MapReduce en disco.</td>
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
        <p style="margin: 2px 0;"><strong>🖥️ Acción en pantalla:</strong> Mostrar portada del <code>README.md</code> (Sección 1 y 2).</p>
        <blockquote>
            "Buenas tardes, docente y compañeros. Para la práctica LG14 seleccionamos el repositorio público <strong>spark-standalone-cluster-on-docker</strong> de André Perez, un proyecto open-source activamente mantenido con más de 500 estrellas.<br>
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
        <p style="margin: 2px 0;"><strong>🖥️ Acción en pantalla:</strong> Mostrar el Diagrama Mermaid de Arquitectura en el <code>README.md</code> (Sección 4.3).</p>
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

        <p style="margin: 3px 0;"><strong>1. Estado de los Contenedores en Terminal:</strong></p>
        <pre><code>docker ps</code></pre>
        <blockquote>"Podemos observar que los 4 contenedores están en estado <strong>Up</strong>, con sus puertos correctamente mapeados y saludables."</blockquote>

        <p style="margin: 3px 0;"><strong>2. Monitoreo en la Web UI de Spark Master:</strong></p>
        <p style="margin: 1px 0;">Abrir en el navegador: <code>http://localhost:8085</code></p>
        <blockquote>"Al ingresar a la interfaz del Master, confirmamos el estado <strong>ALIVE</strong> y la métrica fundamental de Big Data: <strong>Alive Workers = 2</strong>, con 2 Cores y 2 GB de memoria totales listos para cómputo."</blockquote>

        <p style="margin: 3px 0;"><strong>3. Ejecución del Circuito de Pruebas Distribuidas:</strong></p>
        <pre><code>python scripts/run_all_tests.py</code></pre>
        
        <p style="margin: 3px 0;"><strong>Explicación de cada prueba durante la ejecución en vivo:</strong></p>
        <ul style="margin: 2px 0; padding-left: 16px;">
            <li><strong>Prueba 1 (SparkPi - Monte Carlo):</strong> <em>"Dividió el cálculo de Pi en 10 particiones asignadas en paralelo a los dos workers (<code>172.21.0.3</code> y <code>172.21.0.4</code>), imprimiendo <code>Pi is roughly 3.14...</code> y demostrando paralelismo de CPU real."</em></li>
            <li><strong>Prueba 2 (PySpark DataFrames):</strong> <em>"Ejecuta <code>test_pyspark.py</code> aplicando transformaciones en memoria y filtrado distribuido sobre 5 registros en menos de 10 segundos."</em></li>
            <li><strong>Prueba 3 (Spark SQL y Agregaciones):</strong> <em>"Ejecuta <code>test_spark_sql.py</code> con consultas SQL nativas y agregaciones <code>groupBy</code> de telemetría de CPU y memoria sobre datos particionados."</em></li>
        </ul>
    </div>

    <div class="card">
        <div class="card-title">
            <span>FASE 4: Análisis Comparativo Completo con docker-hadoop (11 Criterios)</span>
            <span class="tag-time">2 Minutos</span>
        </div>
        <p style="margin: 2px 0;"><strong>🖥️ Acción en pantalla:</strong> Mostrar la Tabla Comparativa Completa:</p>
        <table>
            <thead>
                <tr>
                    <th style="width: 22%;">Criterio Oficial</th>
                    <th style="width: 39%;">docker-hadoop (Referencia Univalle)</th>
                    <th style="width: 39%;">spark-standalone-cluster (Nuestro Proyecto)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>1. Tecnología Principal</strong></td>
                    <td>Apache Hadoop (HDFS + MapReduce / YARN)</td>
                    <td><strong>Apache Spark (v3.5.7)</strong></td>
                </tr>
                <tr>
                    <td><strong>2. Docker</strong></td>
                    <td>Sí (Imágenes Debian/Alpine)</td>
                    <td><strong>Sí (Debian con SapMachine Java 21)</strong></td>
                </tr>
                <tr>
                    <td><strong>3. Docker Compose</strong></td>
                    <td>Sí (Versión 2.x/3.x)</td>
                    <td><strong>Sí (Orquestación con named volumes)</strong></td>
                </tr>
                <tr>
                    <td><strong>4. Contenedores</strong></td>
                    <td>5 (Namenode, Datanode, Resourcemanager, etc.)</td>
                    <td><strong>4 (Spark Master, Worker 1, Worker 2, JupyterLab)</strong></td>
                </tr>
                <tr>
                    <td><strong>5. Almacenamiento</strong></td>
                    <td>HDFS con replicación por bloques</td>
                    <td><strong>Volumen compartido <code>shared-workspace</code> (/opt/workspace)</strong></td>
                </tr>
                <tr>
                    <td><strong>6. Procesamiento</strong></td>
                    <td>MapReduce por lotes (I/O intensivo en disco)</td>
                    <td><strong>En Memoria RAM (RDDs / DataFrames, hasta 100x más rápido)</strong></td>
                </tr>
                <tr>
                    <td><strong>7. Interfaces Web</strong></td>
                    <td>NameNode (`9870`), YARN (`8088`), History (`8188`)</td>
                    <td><strong>Spark Master (`8085`), Workers (`8081/8082`), Jupyter (`8888`)</strong></td>
                </tr>
                <tr>
                    <td><strong>8. Persistencia</strong></td>
                    <td>Volúmenes dedicados NameNode/DataNodes</td>
                    <td><strong>Docker Named Volume persistente <code>hadoop-distributed-file-system</code></strong></td>
                </tr>
                <tr>
                    <td><strong>9. Complejidad Inst.</strong></td>
                    <td>Media-Alta (formateo HDFS y sincronización YARN)</td>
                    <td><strong>Baja-Media (despliegue ágil y escalado directo de workers)</strong></td>
                </tr>
                <tr>
                    <td><strong>10. Documentación</strong></td>
                    <td>Enfocada en infraestructura básica de clúster</td>
                    <td><strong>Enfocada en ciencia de datos interactiva (Python, Scala, R)</strong></td>
                </tr>
                <tr>
                    <td><strong>11. Caso de Uso</strong></td>
                    <td>Batch histórico y almacenamiento masivo</td>
                    <td><strong>Analítica en tiempo real, streaming, SQL y Machine Learning</strong></td>
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
    r"C:\Program Files\Google\Chrome\Application\chrome.exe"
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
    print(f"[OK] PDF actualizado con tabla completa de 11 criterios: {pdf_output}")
    try:
        os.remove(temp_html)
    except Exception:
        pass
    sys.exit(0)
else:
    sys.exit(1)
