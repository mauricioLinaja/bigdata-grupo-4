# LG15: Tolerancia a Fallos y Replicación de Datos en Apache Hadoop HDFS

[![Hadoop Version](https://img.shields.io/badge/Apache%20Hadoop-3.2.1-blue.svg)](https://hadoop.apache.org/)
[![Docker Compose](https://img.shields.io/badge/Docker%20Compose-v3.8-2496ED.svg)](https://docs.docker.com/compose/)
[![Replication Factor](https://img.shields.io/badge/Replication%20Factor-2-success.svg)]()
[![Cluster Nodes](https://img.shields.io/badge/Cluster-1%20NameNode%20%2B%203%20DataNodes-orange.svg)]()

> **Universidad del Valle - Facultad de Informática y Electrónica**  
> **Asignatura:** Tecnologías Emergentes / Big Data  
> **Práctica de Laboratorio:** LG15 - Tolerancia a Fallos y Replicación de Datos en HDFS  
> **Grupo:** **Grupo 04** (`/grupo04/`)  
> **Integrantes:**  
> - Joel Saavedra  
> - Mauricio Linaja  
> - Rommel Gutierrez  

---

## 1. Objetivo General

Implementar un entorno distribuido Apache Hadoop HDFS compuesto por **1 NameNode** y **3 DataNodes**, configurando un **factor de replicación mínimo de 2**, para analizar experimentalmente el comportamiento de HDFS ante la caída intencional de un DataNode mediante la carga, inspección y recuperación de datasets de **1 GB** y **10 GB**.

El informe y este repositorio demuestran, mediante evidencias verificables, la distribución de los bloques, las réplicas existentes y el comportamiento dinámico del clúster **antes, durante y después** de la caída del nodo de almacenamiento.

---

## 2. Diagrama de Arquitectura

El siguiente diagrama detalla la topología física y lógica desplegada en contenedores Docker conectados mediante una red tipo *bridge* aislada (`hadoop-network-g4`):

```mermaid
flowchart TD
    subgraph Cliente_HDFS["Cliente HDFS / Administrador"]
        CLI["HDFS CLI / Scripts de Automatización"]
    end

    subgraph Capa_Maestra["Capa Maestra (Metadatos)"]
        NN["NameNode (Puerto 9870 / 9000)<br>• Namespace y Tabla de Inodos<br>• Asignación de Bloques<br>• Monitoreo de Heartbeats y Block Reports"]
    end

    subgraph Capa_Almacenamiento["Capa Distribuida de Almacenamiento (DataNodes)"]
        DN1["DataNode 1 (Puerto 9864)<br>• Bloques físicos<br>• Réplicas activas"]
        DN2["DataNode 2 (Puerto 9865)<br>⚠️ NODO EXPUESTO A FALLA<br>(Simulación docker stop)"]
        DN3["DataNode 3 (Puerto 9866)<br>• Bloques físicos<br>• Nodo receptor de re-replicación"]
    end

    CLI -->|Operaciones HDFS| NN
    CLI -.->|Lectura y Escritura de Bloques| DN1
    CLI -.->|Lectura y Escritura de Bloques| DN2
    CLI -.->|Lectura y Escritura de Bloques| DN3

    NN -->|Coordinación y Heartbeats (cada 3s)| DN1
    NN -->|Heartbeat perdido durante falla| DN2
    NN -->|Comandos de Re-replicación| DN3

    DN1 -.->|Tubería de Replicación de Bloques| DN3
```

---

## 3. Identificación Oficial del Grupo (Grupo 04)

Siguiendo estrictamente las directrices del laboratorio, la estructura de directorios y nombres de archivos en el sistema de archivos distribuido HDFS están asociadas a la identidad del grupo:

```text
/grupo04/
├── dataset_1GB/
│   └── dataset_grupo04_1GB       (1 GB exacto = 8 bloques de 128 MB, rep=2)
├── dataset_10GB/
│   └── dataset_grupo04_10GB      (10 GB exacto = 80 bloques de 128 MB, rep=2)
├── resultados/
│   └── resumen_experimentos.txt  (Métricas y comparativas)
└── evidencias/
    ├── evidencia_falla_dataset_1GB.log
    └── evidencia_falla_dataset_10GB.log
```

---

## 4. Requerimientos del Sistema y Parámetros del Clúster

| Componente | Configuración Implementada | Justificación Técnica |
| :--- | :--- | :--- |
| **NameNode** | 1 Instancia (`namenode`) | Nodo maestro centralizado que gestiona el espacio de nombres y los bloques. |
| **DataNodes** | 3 Instancias (`datanode1`, `datanode2`, `datanode3`) | Permite tolerar la caída de 1 nodo manteniendo el factor de replicación de 2 en los restantes. |
| **Factor de Replicación** | `dfs.replication = 2` | Cada bloque físico se almacena en 2 DataNodes distintos simultáneamente. |
| **Tamaño de Bloque** | `dfs.blocksize = 134217728` (128 MB) | Estándar de Hadoop 3.x para balancear el número de bloques e I/O eficiente. |
| **Heartbeat Interval** | `dfs.heartbeat.interval = 3` (3 seg) | Frecuencia de latidos de vida emitidos por los DataNodes al NameNode. |
| **Heartbeat Recheck** | `dfs.namenode.heartbeat.recheck-interval = 30000` (30 seg) | Permite declarar un nodo como `Dead` en ~90 segundos para pruebas ágiles. |

---

## 5. Protocolo de Pruebas de Fallo

El experimento se dividió en dos escenarios independientes: uno con **1 GB** y otro con **10 GB**. En ambos casos se evaluó la secuencia: **Estado Inicial** $\rightarrow$ **Caída Forzada de DataNode 2** $\rightarrow$ **Comportamiento Durante la Falla** $\rightarrow$ **Detección y Recuperación del NameNode**.

### 5.1. Prueba con Dataset de 1 GB (`dataset_grupo04_1GB`)

- **Tamaño:** 1,073,741,824 bytes (1 GB).
- **Número de bloques calculados:** $\frac{1024 \text{ MB}}{128 \text{ MB}} = 8 \text{ bloques}$.
- **Total réplicas esperadas:** $8 \times 2 = 16 \text{ réplicas físicas}$.

```
FASE 1: Estado Inicial
├── DataNodes activos: DN1, DN2, DN3 (Todos en estado 'Live')
├── fsck report: 8 bloques, 16 réplicas totales (Healthy, 0 subreplicados)
└── Ubicación de bloques: Distribuidos balanceadamente entre DN1, DN2 y DN3.

FASE 2: Introducción de la Falla
└── Se ejecuta: docker stop datanode2 (DN2 cae instantáneamente).

FASE 3: Comportamiento Durante la Falla
├── ¿Archivo accesible?: SÍ. El comando 'hdfs dfs -tail' y lecturas de bloques leen sin errores.
├── Causa técnica: Como la replicación es 2, cada uno de los 8 bloques posee al menos una copia en DN1 o DN3.
└── Estado de bloques: Disponibles al 100%, pero con factor de replicación degradado a 1 para los bloques que estaban en DN2.

FASE 4: Detección y Recuperación de HDFS
├── NameNode detecta falta de Heartbeats: datanode2 pasa de 'Stale' a 'Dead'.
├── Detección de subreplicación: HDFS reporta 'Under-replicated blocks: 5' (o los correspondientes a DN2).
└── Proceso de Re-replicación: El NameNode instruye a los DataNodes vivos (DN1 o DN3) a transferir los bloques huérfanos entre sí para restaurar el factor de replicación de 2.
```

---

### 5.2. Prueba con Dataset de 10 GB (`dataset_grupo04_10GB`)

- **Tamaño:** 10,737,418,240 bytes (10 GB).
- **Número de bloques calculados:** $\frac{10240 \text{ MB}}{128 \text{ MB}} = 80 \text{ bloques}$.
- **Total réplicas esperadas:** $80 \times 2 = 160 \text{ réplicas físicas}$.

```
FASE 1: Estado Inicial
├── DataNodes activos: 3 nodos 'Live'.
├── fsck report: 80 bloques, 160 réplicas registradas.
└── Ubicación: 80 bloques distribuidos de manera uniforme (~53-54 réplicas en cada uno de los 3 DataNodes).

FASE 2: Falla de DataNode 2
└── Se ejecuta: docker stop datanode2.

FASE 3: Durante la Falla
├── ¿Archivo accesible?: SÍ, acceso continuo y transparente a los 10 GB de datos.
├── Bloques afectados: Aproximadamente 53 bloques que tenían una réplica alojada en DN2.
└── Ningún bloque quedó con 0 réplicas (ningún bloque corrupto o perdido).

FASE 4: Recuperación y Re-replicación
├── Reporte fsck: Identifica ~53 bloques en estado 'Under-replicated'.
├── Sobrecarga de red distribuida: El NameNode coordina la transferencia masiva de bloques entre DN1 y DN3.
└── Se evidencia el comportamiento dinámico de balanceo de carga y re-replicación a gran escala.
```

---

## 6. Cuadro Comparativo de Resultados

A continuación se presenta la tabla comparativa exigida en el punto 6 de la guía:

| Característica | Dataset 1 GB | Dataset 10 GB |
| :--- | :--- | :--- |
| **Tamaño del Archivo** | 1 GB (1,073,741,824 bytes) | 10 GB (10,737,418,240 bytes) |
| **Tamaño de Bloque (Block Size)** | 128 MB | 128 MB |
| **Número de Bloques Lógicos** | **8 bloques** | **80 bloques** |
| **Factor de Replicación** | 2 | 2 |
| **Total de Réplicas en Clúster** | 16 réplicas físicas | 160 réplicas físicas |
| **DataNode Afectado** | `datanode2` | `datanode2` |
| **Bloques Afectados en DN Caído** | ~5 bloques con réplica en DN2 | ~53 bloques con réplica en DN2 |
| **Bloques Disponibles tras la Falla** | **8 / 8 (100% disponibles)** | **80 / 80 (100% disponibles)** |
| **¿Archivo Accesible y Legible?** | **SÍ**, lectura íntegra sin interrupción | **SÍ**, lectura íntegra sin interrupción |
| **¿Existieron Bloques Subreplicados?**| **SÍ**, aquellos cuya réplica estaba en DN2 | **SÍ**, ~53 bloques en estado subreplicado |
| **Tiempo de Detección Dead Node** | ~90 segundos (según heartbeat timeout) | ~90 segundos |
| **Tiempo de Recuperación / Replicación**| Muy bajo (< 15 segundos) | Moderado (requiere mayor ancho de banda) |
| **Nuevas Réplicas Creadas En** | `datanode1` y/o `datanode3` | `datanode1` y/o `datanode3` |

---

## 7. Análisis Riguroso y Respuestas a las Preguntas de Exposición

### Preguntas del Proceso Experimental

#### ¿Cuántos bloques tenía el archivo y cuántas réplicas cada uno?
- **Dataset 1 GB:** 8 bloques lógicos. Cada bloque cuenta con 2 réplicas físicas (total 16 réplicas).
- **Dataset 10 GB:** 80 bloques lógicos. Cada bloque cuenta con 2 réplicas físicas (total 160 réplicas).

#### ¿En qué DataNodes estaban ubicados antes de la falla?
HDFS distribuye los bloques siguiendo su política de colocación (*Block Placement Policy*). Con 3 DataNodes y factor de replicación 2, cada bloque se coloca en un par de DataNodes aleatorios/balanceados: (DN1, DN2), (DN2, DN3) o (DN1, DN3), distribuyendo la carga de almacenamiento de forma casi equitativa en los 3 nodos.

#### ¿Qué DataNode fue detenido y qué bloques estaban en él?
Fue detenido `datanode2`. En él se encontraban almacenadas aproximadamente la mitad de las réplicas del sistema (~5 réplicas para 1 GB y ~53 réplicas para 10 GB).

#### ¿Existían otras réplicas y el archivo continuó disponible?
**SÍ.** Como la replicación es 2 y ningún bloque almacena sus dos réplicas en el mismo nodo físico, para cada bloque que perdió su réplica en DN2 existía una segunda réplica intacta en DN1 o en DN3. Por lo tanto, **el archivo permaneció disponible al 100%**.

#### ¿Qué cambió en HDFS y qué estado reporta?
1. Durante la desconexión inmediata, el NameNode aún no sabe si el nodo cayó o si la red está lenta; los clientes que intentan leer de DN2 experimentan un timeout de socket y conmutan de forma transparente a la réplica superviviente.
2. Tras expirar el tiempo de *heartbeat*, el NameNode marca a `datanode2` como `Dead`.
3. Al recalcular el catálogo de réplicas, detecta que los bloques afectados tienen factor actual $1 < 2$, etiquetándolos como **Under-replicated blocks**.
4. HDFS programa transferencias de replicación automáticas desde los DataNodes activos hacia el otro nodo disponible para restaurar el factor de 2.

---

### Preguntas Teóricas para la Defensa

#### Pregunta 1: ¿Por qué HDFS puede continuar proporcionando el archivo aunque un DataNode haya fallado?
> Porque HDFS desacopla los metadatos lógicos del almacenamiento físico mediante su arquitectura maestro-esclavo y su **política de replicación distribuida**. Al configurar un factor de replicación $\ge 2$, cada fragmento del archivo (bloque) está duplicado en nodos físicos físicamente separados. Si un DataNode falla, el NameNode redirige las peticiones de lectura del cliente hacia la réplica alternativa que permanece en línea en otro DataNode, garantizando una alta disponibilidad sin pérdida de datos.

#### Pregunta 2: ¿Qué habría ocurrido si el factor de replicación hubiera sido 1?
> Si la replicación hubiera sido 1, cada bloque existiría en un único DataNode. Al detener `datanode2`, aproximadamente un tercio de los bloques del archivo habrían quedado inaccesibles (0 réplicas disponibles). El archivo habría quedado en estado **CORRUPT / Missing Blocks**, provocando que cualquier lectura que requiriera esos bloques fallara con una excepción de entrada/salida (`IOException: Could not obtain block`), perdiéndose la disponibilidad total del dataset.

#### Pregunta 3: ¿Qué habría ocurrido si hubieran fallado dos DataNodes simultáneamente?
> En un clúster de 3 DataNodes con factor de replicación 2, la probabilidad de que al menos un bloque tuviera sus dos únicas réplicas en los dos nodos caídos es sumamente alta. Aquellos bloques compartidos exclusivamente entre los dos nodos caídos no tendrían ninguna réplica disponible en el nodo superviviente, convirtiéndose en bloques perdidos (*Missing blocks*). En consecuencia, **el archivo no habría podido ser leído por completo y el clúster habría sufrido pérdida temporal o permanente de datos**.

#### Pregunta 4: ¿Por qué un factor de replicación de 2 no significa necesariamente que existan dos copias completas del archivo en dos DataNodes?
> Porque HDFS divide un archivo grande en múltiples **bloques independientes** (de 128 MB cada uno). La replicación opera a nivel de bloque individual, no a nivel de archivo completo. El NameNode distribuye los bloques entre los nodos del clúster de manera dispersa: el bloque 1 puede estar en (DN1, DN2), el bloque 2 en (DN2, DN3) y el bloque 3 en (DN1, DN3). Por tanto, ningún DataNode almacena necesariamente la totalidad del archivo como un archivo monolítico; lo que existe son réplicas de los bloques fragmentados distribuidos por todo el clúster.

#### Pregunta 5: ¿Cuál es la relación entre tamaño de bloque y número de bloques?
> Existe una **relación inversamente proporcional**:
> $$\text{Número de Bloques} = \left\lceil \frac{\text{Tamaño Total del Archivo}}{\text{Tamaño de Bloque (Block Size)}} \right\rceil$$
> - Un tamaño de bloque pequeño produce una cantidad enorme de bloques, lo que satura la memoria RAM del NameNode (cada bloque consume metadatos en memoria) y degrada la velocidad por sobrecarga de transferencia.
> - Un tamaño de bloque grande (como 128 MB o 256 MB) minimiza la sobrecarga de metadatos y optimiza las lecturas secuenciales en discos duros, a costa de reducir el paralelismo para archivos muy pequeños.

#### Pregunta 6: ¿Por qué el dataset de 10 GB permite observar un comportamiento más representativo de un sistema distribuido que el dataset de 1 GB?
> El dataset de 1 GB consta únicamente de 8 bloques, lo cual puede distribuirse en pocas combinaciones simples y completarse en segundos. En cambio, el dataset de 10 GB (80 bloques y 160 réplicas físicas):
> 1. Requiere una distribución estadística mucho más amplia entre todos los DataNodes.
> 2. Permite observar fenómenos reales de saturación de I/O en disco y consumo de ancho de banda de red durante la re-replicación.
> 3. Pone a prueba la capacidad del NameNode para gestionar colas masivas de bloques subreplicados y priorizar su recuperación concurrente.

#### Pregunta 7: ¿Qué sucede con los bloques que tenían una réplica en el DataNode que falló?
> Esos bloques pasan al estado **Under-replicated** (subreplicados), ya que su conteo de réplicas vivas cae por debajo del factor configurado ($1 < 2$). Sin embargo, mientras quede al menos una réplica viva, el bloque permanece catalogado como **Live** y accesible. El NameNode coloca esos bloques en una cola de prioridad de replicación para ordenar su clonación hacia otro nodo disponible.

#### Pregunta 8: ¿Quién administra la ubicación y replicación de los bloques: el cliente, el DataNode o el NameNode?
> **El NameNode exclusivamente.**
> - El **NameNode** mantiene en memoria el mapeo completo de bloques a DataNodes y toma todas las decisiones de asignación, balanceo y reposición de réplicas.
> - Los **DataNodes** son ejecutores pasivos: simplemente reportan qué bloques tienen almacenados mediante *Block Reports* y reciben órdenes del NameNode para transferir bloques hacia otros DataNodes.
> - El **Cliente** no decide la topología; únicamente consulta al NameNode la lista de DataNodes donde debe leer o escribir.

#### Pregunta 9: ¿Qué diferencia existe entre disponibilidad del archivo y cumplimiento del factor de replicación después de una falla?
> - **Disponibilidad del archivo:** Se refiere a la capacidad de un cliente de leer la totalidad del archivo sin interrupción. Se mantiene siempre que cada bloque tenga **al menos 1 réplica activa** en cualquier nodo del clúster ($R_{\text{activa}} \ge 1$).
> - **Cumplimiento del factor de replicación:** Se refiere a que la cantidad de copias vivas coincida exactamente con la política establecida ($R_{\text{activa}} = R_{\text{objetivo}} = 2$).
> Inmediatamente después de la caída de un nodo, el archivo suele mantener **100% de disponibilidad** pero **incumple el factor de replicación** (estado subreplicado), quedando en una condición vulnerable ante una segunda falla potencial hasta que concluya el proceso de recuperación.

---

## 8. Guía de Ejecución Rápida

### 8.1. Despliegue del Clúster

```powershell
# Levantar el entorno de 1 NameNode y 3 DataNodes
docker-compose up -d

# Verificar estado de los contenedores
docker-compose ps
```

### 8.2. Inicialización de HDFS y Carga de Datasets

```powershell
python scripts/setup_hdfs_lg15.py
```

### 8.3. Ejecución Automatizada de Pruebas de Fallo

```powershell
python scripts/run_failure_tests.py
```

### 8.4. Comprobaciones Manuales y Diagnóstico

```powershell
# Reporte general de DataNodes y espacio
docker exec -it namenode hdfs dfsadmin -report

# Diagnóstico de integridad de bloques y réplicas
docker exec -it namenode hdfs fsck /grupo04/dataset_1GB/dataset_grupo04_1GB -files -blocks -locations
docker exec -it namenode hdfs fsck /grupo04/dataset_10GB/dataset_grupo04_10GB -files -blocks -locations

# Simular caída de DataNode 2
docker stop datanode2

# Reincorporar DataNode 2
docker start datanode2
```

---

## 9. Interfaces Web de Monitoreo

| Interfaz | URL | Función Principal |
| :--- | :--- | :--- |
| **HDFS NameNode Web UI** | [http://localhost:9870](http://localhost:9870) | Visor de namespace, estado de DataNodes, SafeMode y métricas de réplicas. |
| **DataNode 1 Web UI** | [http://localhost:9864](http://localhost:9864) | Métricas locales de almacenamiento y volumen de DataNode 1. |
| **DataNode 2 Web UI** | [http://localhost:9865](http://localhost:9865) | Métricas locales de almacenamiento de DataNode 2. |
| **DataNode 3 Web UI** | [http://localhost:9866](http://localhost:9866) | Métricas locales de almacenamiento de DataNode 3. |

---

## 10. Estructura del Repositorio

```text
bigdata-grupo-4/
├── docker-compose.yml                     # Definición de 1 NameNode y 3 DataNodes (Replication 2)
├── README.md                              # Informe técnico completo, preguntas y resultados
├── Guia_Demostracion_y_Defensa_LG15_Grupo4.pdf  # Guía imprimible en PDF con oratoria y respuestas
├── scripts/
│   ├── setup_hdfs_lg15.py                 # Preparación de directorios y carga de datasets
│   ├── run_failure_tests.py               # Ejecución automatizada de pruebas de caída y recuperación
│   └── generate_pdf_lg15.py               # Generador de informe formal en PDF
└── evidencias/                            # Logs de salida, trazas de ejecución y diagnósticos FSCK
    ├── evidencia_falla_dataset_1GB.log    # Trazas de falla y recuperación para 1 GB
    └── evidencia_falla_dataset_10GB.log   # Trazas de falla y recuperación para 10 GB
```

---
**Universidad del Valle - 2026**  
*Materia: Tecnologías Emergentes / Big Data (LG15)*
