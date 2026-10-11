"""
Script para generar el documento PDF formal de la Guía de Demostración y Defensa Oral (LG15)
Universidad del Valle - Big Data / Sistemas Distribuidos
Grupo 04: Joel Saavedra, Mauricio Linaja, Rommel Gutierrez
Práctica: LG15 - Tolerancia a Fallos y Replicación de Datos en HDFS
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#4A5568"))
        
        # Header (páginas posteriores a la 1)
        if self._pageNumber > 1:
            self.drawString(36, 762, "UNIVERSIDAD PRIVADA DEL VALLE | Big Data (LG15) - Tolerancia a Fallos en HDFS (Grupo 04)")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(36, 754, 576, 754)
        
        # Footer en todas las páginas
        footer_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(576, 25, footer_text)
        self.setFont("Helvetica", 8)
        self.drawString(36, 25, "Joel Saavedra | Mauricio Linaja | Rommel Gutierrez — Grupo 04 (LG15)")
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(36, 35, 576, 35)
        self.restoreState()

def build_pdf(filename="Guia_Demostracion_y_Defensa_LG15_Grupo4.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1A365D'),
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#2B6CB0'),
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1A365D'),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=colors.HexColor('#2C5282'),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#2D3748'),
        spaceAfter=5
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    pregunta_q = ParagraphStyle(
        'PreguntaQ',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#9B2C2C'),
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    pregunta_a = ParagraphStyle(
        'PreguntaA',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#1A202C'),
        spaceAfter=6
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#2D3748')
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell,
        fontName='Helvetica-Bold'
    )

    story = []

    # PORTADA / ENCABEZADO
    story.append(Paragraph("UNIVERSIDAD PRIVADA DEL VALLE", title_style))
    story.append(Paragraph("FACULTAD DE INFORMÁTICA Y ELECTRÓNICA — INGENIERÍA DE SISTEMAS", subtitle_style))
    story.append(Paragraph("<b>LG15: TOLERANCIA A FALLOS Y REPLICACIÓN DE DATOS EN HDFS</b>", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1A365D'), spaceBefore=2, spaceAfter=8))

    meta_data = [
        [Paragraph("<b>Asignatura:</b> Tecnologías Emergentes / Big Data", body_style),
         Paragraph("<b>Grupo Oficial:</b> Grupo 04 (/grupo04/)", body_style)],
        [Paragraph("<b>Integrantes:</b> Joel Saavedra, Mauricio Linaja, Rommel Gutierrez", body_style),
         Paragraph("<b>Topología:</b> 1 NameNode + 3 DataNodes (Rep = 2)", body_style)]
    ]
    meta_table = Table(meta_data, colWidths=[300, 240])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EDF2F7')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # SECCION 1: OBJETIVO Y ARQUITECTURA
    story.append(Paragraph("1. Objetivo del Laboratorio y Topología de Red", h1_style))
    story.append(Paragraph(
        "Implementar un entorno distribuido Apache Hadoop HDFS compuesto por 1 NameNode y 3 DataNodes, "
        "configurando un factor de replicación mínimo de 2 (dfs.replication=2) y tamaño de bloque de 128 MB. "
        "El propósito es analizar experimentalmente la distribución de bloques y la tolerancia a fallos "
        "ante la caída intencional de un nodo de almacenamiento (DataNode 2), validando el comportamiento con "
        "datasets de 1 GB y 10 GB.",
        body_style
    ))

    cluster_info = [
        [Paragraph("Componente", table_header), Paragraph("Nombre / Host", table_header), Paragraph("Puertos Web / IPC", table_header), Paragraph("Rol en el Clúster HDFS", table_header)],
        [Paragraph("NameNode", table_cell_bold), Paragraph("namenode", table_cell), Paragraph("9870 (WebUI) / 9000 (RPC)", table_cell), Paragraph("Maestro: Namespace, inodos y mapeo de bloques", table_cell)],
        [Paragraph("DataNode 1", table_cell_bold), Paragraph("datanode1", table_cell), Paragraph("9864 (WebUI)", table_cell), Paragraph("Esclavo de almacenamiento: Bloques y réplicas", table_cell)],
        [Paragraph("DataNode 2", table_cell_bold), Paragraph("datanode2", table_cell), Paragraph("9865 (WebUI)", table_cell), Paragraph("Esclavo (Nodo objetivo de la simulación de falla)", table_cell)],
        [Paragraph("DataNode 3", table_cell_bold), Paragraph("datanode3", table_cell), Paragraph("9866 (WebUI)", table_cell), Paragraph("Esclavo de almacenamiento: Receptor de re-replicación", table_cell)],
    ]
    t_cluster = Table(cluster_info, colWidths=[70, 80, 110, 280])
    t_cluster.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1A365D')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_cluster)
    story.append(Spacer(1, 8))

    # SECCION 2: CUADRO COMPARATIVO
    story.append(Paragraph("2. Comparación Experimental entre Dataset 1 GB y Dataset 10 GB", h1_style))
    comp_data = [
        [Paragraph("Característica Evaluada", table_header), Paragraph("Dataset 1 GB (dataset_grupo04_1GB)", table_header), Paragraph("Dataset 10 GB (dataset_grupo04_10GB)", table_header)],
        [Paragraph("Tamaño Físico", table_cell_bold), Paragraph("1,073,741,824 bytes (1 GB)", table_cell), Paragraph("10,737,418,240 bytes (10 GB)", table_cell)],
        [Paragraph("Tamaño de Bloque (Blocksize)", table_cell_bold), Paragraph("128 MB (134,217,728 bytes)", table_cell), Paragraph("128 MB (134,217,728 bytes)", table_cell)],
        [Paragraph("Número de Bloques Lógicos", table_cell_bold), Paragraph("<b>8 bloques</b> (1024 MB / 128 MB)", table_cell), Paragraph("<b>80 bloques</b> (10240 MB / 128 MB)", table_cell)],
        [Paragraph("Factor de Replicación", table_cell_bold), Paragraph("2", table_cell), Paragraph("2", table_cell)],
        [Paragraph("Total Réplicas en Clúster", table_cell_bold), Paragraph("16 réplicas físicas", table_cell), Paragraph("160 réplicas físicas", table_cell)],
        [Paragraph("DataNode Afectado por Falla", table_cell_bold), Paragraph("datanode2 (docker stop datanode2)", table_cell), Paragraph("datanode2 (docker stop datanode2)", table_cell)],
        [Paragraph("Bloques Afectados en DN Caído", table_cell_bold), Paragraph("~5 bloques que residían en DN2", table_cell), Paragraph("~53 bloques que residían en DN2", table_cell)],
        [Paragraph("Bloques Disponibles tras Falla", table_cell_bold), Paragraph("<b>8 de 8 (100% de disponibilidad)</b>", table_cell), Paragraph("<b>80 de 80 (100% de disponibilidad)</b>", table_cell)],
        [Paragraph("¿Archivo Accesible y Legible?", table_cell_bold), Paragraph("<b>SÍ</b> (lectura íntegra sin fallos)", table_cell), Paragraph("<b>SÍ</b> (lectura continua y sin errores)", table_cell)],
        [Paragraph("¿Bloques Subreplicados Detectados?", table_cell_bold), Paragraph("<b>SÍ</b> (HDFS marca bloques con rep=1)", table_cell), Paragraph("<b>SÍ</b> (~53 bloques en estado subreplicado)", table_cell)],
        [Paragraph("Tiempo de Detección Dead Node", table_cell_bold), Paragraph("~90 segundos (Heartbeat timeout)", table_cell), Paragraph("~90 segundos (Heartbeat timeout)", table_cell)],
        [Paragraph("Nuevas Réplicas Creadas En", table_cell_bold), Paragraph("datanode1 o datanode3 automáticamente", table_cell), Paragraph("datanode1 o datanode3 automáticamente", table_cell)],
    ]
    t_comp = Table(comp_data, colWidths=[150, 195, 195])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2B6CB0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F7FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 10))

    # SECCION 3: CUESTIONARIO Y DEFENSA ORAL
    story.append(PageBreak())
    story.append(Paragraph("3. Respuestas Teóricas y Metodológicas para la Defensa Oral", h1_style))
    story.append(Paragraph(
        "A continuación se exponen con rigor técnico las 9 preguntas requeridas para la exposición formal de la práctica:",
        body_style
    ))

    preguntas = [
        ("Pregunta 1: ¿Por qué HDFS puede continuar proporcionando el archivo aunque un DataNode haya fallado?",
         "HDFS desacopla la capa de metadatos (NameNode) de la capa física de almacenamiento (DataNodes). Al tener configurado un factor de replicación mayor o igual a 2, cada bloque del archivo tiene copias idénticas en al menos dos DataNodes distintos. Cuando un DataNode falla, el NameNode consulta la tabla de bloques en memoria y redirige transparentemente al cliente para que lea desde el DataNode alternativo que contiene la réplica viva, asegurando la continuidad del servicio sin que el cliente perciba la caída."),

        ("Pregunta 2: ¿Qué habría ocurrido si el factor de replicación hubiera sido 1?",
         "Si dfs.replication = 1, cada uno de los bloques existe únicamente en un solo DataNode. Al detener datanode2, todos los bloques almacenados exclusivamente en él habrían quedado completamente inaccesibles (0 réplicas disponibles). HDFS habría marcado el archivo en estado CORRUPT con Missing Blocks, y cualquier lectura fallaría con un error de entrada/salida (IOException: Could not obtain block), perdiendo la disponibilidad."),

        ("Pregunta 3: ¿Qué habría ocurrido si hubieran fallado dos DataNodes simultáneamente?",
         "En un clúster de 3 DataNodes con factor de replicación 2, la probabilidad combinatoria de que al menos un bloque tuviera sus dos únicas réplicas en los dos DataNodes caídos es sumamente alta. Dichos bloques compartidos no tendrían ninguna copia en el nodo superviviente, causando pérdida temporal o permanente de bloques y haciendo imposible la lectura completa del archivo."),

        ("Pregunta 4: ¿Por qué un factor de replicación de 2 no significa necesariamente que existan dos copias completas del archivo en dos DataNodes?",
         "Porque HDFS no replica a nivel de archivo completo monolítico, sino a nivel de fragmentos discretos denominados bloques (de 128 MB). La política de colocación de bloques (Block Placement Policy) dispersa los bloques entre todos los nodos disponibles. El bloque 1 puede estar en (DN1, DN2), el bloque 2 en (DN2, DN3) y el bloque 3 en (DN1, DN3). En consecuencia, ningún DataNode posee forzosamente el 100% de los bloques del archivo; la totalidad del archivo solo existe en la unión del clúster."),

        ("Pregunta 5: ¿Cuál es la relación entre tamaño de bloque y número de bloques?",
         "La relación es estrictamente inversamente proporcional: Número_de_Bloques = Ceil(Tamaño_Archivo / Block_Size). Un tamaño de bloque pequeño produce millones de bloques, sobrecargando la memoria RAM del NameNode (cada bloque consume ~150 bytes de metadatos) y aumentando la latencia de red. Un tamaño de bloque grande (128 MB o 256 MB) optimiza el throughput de disco secuencial y mantiene la tabla de inodos compacta, aunque puede limitar el paralelismo en archivos pequeños."),

        ("Pregunta 6: ¿Por qué el dataset de 10 GB permite observar un comportamiento más representativo de un sistema distribuido que el dataset de 1 GB?",
         "El dataset de 1 GB consta únicamente de 8 bloques (16 réplicas), una cantidad trivial que se transfiere en pocos segundos y no estresa los recursos. En cambio, el dataset de 10 GB cuenta con 80 bloques y 160 réplicas físicas distribuidas, lo que permite observar fenómenos reales de contención de I/O en disco, saturación de la tubería de red y la gestión de colas concurrentes de subreplicación en el NameNode."),

        ("Pregunta 7: ¿Qué sucede con los bloques que tenían una réplica en el DataNode que falló?",
         "Pasan al estado 'Under-replicated' (subreplicados). Sin embargo, siguen estando 100% disponibles para lectura porque conservan una réplica viva en el otro DataNode. El NameNode detecta que el número de réplicas es menor al configurado (1 < 2) y programa tareas de replicación automáticas para que el DataNode vivo clone el bloque hacia el tercer DataNode disponible."),

        ("Pregunta 8: ¿Quién administra la ubicación y replicación de los bloques: el cliente, el DataNode o el NameNode?",
         "El NameNode de forma exclusiva y centralizada. El NameNode decide dónde se coloca cada bloque nuevo, detecta fallos por omisión de heartbeats y ordena la re-replicación. Los DataNodes son meros ejecutores pasivos que almacenan bloques y emiten Block Reports. El cliente se limita a consultar al NameNode las direcciones de los DataNodes donde debe transferir los datos."),

        ("Pregunta 9: ¿Qué diferencia existe entre disponibilidad del archivo y cumplimiento del factor de replicación después de una falla?",
         "Disponibilidad significa que los datos pueden ser leídos por los usuarios (requiere al menos 1 réplica viva por bloque). Cumplimiento del factor de replicación significa que el sistema satisface la redundancia configurada (R_activa = 2). Tras una falla, el archivo mantiene disponibilidad del 100%, pero incumple temporalmente el factor de replicación (estado degradado/vulnerable) hasta que HDFS culmina la auto-recuperación.")
    ]

    for q_text, a_text in preguntas:
        q_flow = KeepTogether([
            Paragraph(f"<b>{q_text}</b>", pregunta_q),
            Paragraph(a_text, pregunta_a),
            Spacer(1, 2)
        ])
        story.append(q_flow)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Documento PDF generado exitosamente: {filename}")

if __name__ == "__main__":
    build_pdf()
