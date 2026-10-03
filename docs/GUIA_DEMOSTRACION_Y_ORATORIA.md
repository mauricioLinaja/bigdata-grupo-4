# 🎓 GUÍA MAESTRA DE DEMOSTRACIÓN Y ORATORIA (DEFENSA LG14)

**Asignatura:** Big Data / Sistemas Distribuidos — **Universidad del Valle**  
**Proyecto:** Despliegue y Validación de un Clúster Distribuido Apache Spark con Docker  
**Criterio de Evaluación Rector:** *"Encontrar → Comprender → Desplegar → Probar → Analizar"*

---

## ⏱️ Estructura Temporal de la Presentación (7 a 10 Minutos)

```mermaid
gantt
    title Cronograma de Exposición y Demostración
    dateFormat  m
    axisFormat %M min
    section 1. Introducción y Selección :active, 0, 1
    section 2. Arquitectura del Clúster :active, 1, 3
    section 3. Demostración en Vivo :crit, 3, 7
    section 4. Comparativa con Hadoop :active, 7, 9
    section 5. Conclusiones y Cierre :active, 9, 10
```

---

## 🎙️ GUION DE ORATORIA PASO A PASO

---

### FASE 1: Introducción y Selección del Repositorio (1 Minuto)
> **Objetivo del PDF:** Cumplir Secciones 1, 2, 3 y 4. Demostrar criterio de selección y registro formal.

#### 🖥️ ¿Qué mostrar en pantalla?
* Portada del [README.md](file:///c:/Users/wiget/OneDrive/Desktop/bigdata-grupo-4/README.md) (Sección 1 y 2).

#### 🗣️ ¿Qué decir? (Guion sugerido):
> *"Buenas tardes, docente y compañeros. Para la práctica LG14 seleccionamos el repositorio público **`spark-standalone-cluster-on-docker`** de André Perez (`cluster-apps-on-docker`), un proyecto open-source activamente mantenido con más de 500 estrellas.*
> 
> *Seleccionamos **Apache Spark 3.5.7** en lugar del esquema tradicional de Hadoop porque representa el estado del arte en Big Data moderno: procesamiento distribuido en memoria RAM, lo que permite consultas hasta 100 veces más rápidas que MapReduce y soporte analítico directo en Python mediante PySpark y JupyterLab."*

📌 **Puntos Clave a Resaltar del Documento:**
* Cumple la consigna de ser **diferente al repositorio base**, utiliza **Docker Compose**, tiene **arquitectura distribuida real** y permite **múltiples pruebas funcionales**.

---

### FASE 2: Comprensión y Análisis de la Arquitectura (2 Minutos)
> **Objetivo del PDF:** Cumplir Sección 5. Demostrar que se comprende cada componente, red, volumen y flujo de datos (diagrama real, no genérico).

#### 🖥️ ¿Qué mostrar en pantalla?
* El Diagrama de Arquitectura Mermaid en [README.md](file:///c:/Users/wiget/OneDrive/Desktop/bigdata-grupo-4/README.md) (Sección 4.3).

#### 🗣️ ¿Qué decir? (Guion sugerido):
> *"Analizando la arquitectura técnica, nuestro entorno está compuesto por **4 contenedores Docker** orquestados en una red Bridge privada:*
>
> 1. ***`spark-master`**: Es el nodo coordinador. Expone el puerto `7077` para comunicación RPC interna y su Web UI en el puerto `8085` para monitoreo de recursos.*
> 2. ***`spark-worker-1` y `spark-worker-2`**: Son los nodos de ejecución distribuida (Executors), cada uno configurado con 1 Core de CPU y 1 GB de memoria RAM.*
> 3. ***`jupyterlab`**: Es la capa interactiva cliente en el puerto `8888`, permitiendo a los científicos de datos programar notebooks en Python sin saturar los nodos de procesamiento.*
> 4. ***Volumen compartido `hadoop-distributed-file-system`**: Montado en `/opt/workspace` en los 4 contenedores, garantizando persistencia y acceso común a datasets y scripts."*

📌 **Puntos Clave a Resaltar del Documento:**
* **Aislamiento y Escalabilidad:** Los workers dependen del Master (`depends_on: [spark-master]`) y se registran dinámicamente mediante heartbeats RPC.

---

### FASE 3: Despliegue y Demostración Práctica en Vivo (4 Minutos)
> **Objetivo del PDF:** Cumplir Sección 7 (Pasos 1 al 7) y Pruebas Funcionales Obligatorias.

#### 🖥️ Acción 1: Estado del Clúster en Terminal
Ejecutar en la consola:
```bash
docker ps
```
#### 🗣️ Explicación:
> *"Podemos observar que los 4 contenedores están en estado **Up**, con sus puertos correctamente mapeados y saludables."*

---

#### 🖥️ Acción 2: Monitoreo en Spark Master Web UI
Abrir en el navegador: **[http://localhost:8085](http://localhost:8085)**
#### 🗣️ Explicación:
> *"Al ingresar a la interfaz del Master, confirmamos el estado **ALIVE** y la métrica fundamental de Big Data: **Alive Workers = 2**. Tenemos un pool total de 2 Cores y 2 GB de memoria listos para recibir cargas distribuidas."*

---

#### 🖥️ Acción 3: Ejecución de las Pruebas Distribuidas (Demostración de Cómputo Real)

Ejecutar el circuito automatizado de pruebas:
```bash
python scripts/run_all_tests.py
```
*(O ejecutar las pruebas manuales paso a paso si el docente lo solicita)*.

#### 🗣️ Explicación de cada prueba durante la ejecución:

1. **Prueba 1 — Cálculo de $\pi$ Distribuido (SparkPi / Monte Carlo):**
   > *"En esta prueba sometemos un trabajo de cálculo probabilístico de Pi dividido en 10 particiones. Si observamos los logs, el Spark Master asignó tareas en paralelo a `172.21.0.3` (Worker 1) y `172.21.0.4` (Worker 2). El clúster calcula: `Pi is roughly 3.14...` demostrando paralelismo de CPU real."*

2. **Prueba 2 — PySpark DataFrames y Filtrado en Memoria:**
   > *"Ejecutamos un script en Python (`test_pyspark.py`) que crea un DataFrame distribuido y aplica transformaciones perezosas (lazy evaluation) y filtrado en memoria sobre las tecnologías Big Data. Procesa 5 registros distribuidos con tiempo de respuesta inferior a 10 segundos."*

3. **Prueba 3 — Spark SQL y Agregaciones de Métricas:**
   > *"En esta prueba avanzada (`test_spark_sql.py`), ejecutamos consultas SQL nativas sobre datos particionados y realizamos agregaciones `groupBy` con cálculo de promedios de CPU y métricas de infraestructura, demostrando la capacidad de Spark para analítica estructurada."*

---

### FASE 4: Análisis Comparativo con `docker-hadoop` (2 Minutos)
> **Objetivo del PDF:** Cumplir Sección 8 y 9. Demostrar capacidad de análisis crítico de tecnologías.

#### 🖥️ ¿Qué mostrar en pantalla?
* La Tabla Comparativa en [README.md](file:///c:/Users/wiget/OneDrive/Desktop/bigdata-grupo-4/README.md) (Sección 8).

#### 🗣️ ¿Qué decir? (Guion sugerido):
> *"Comparando nuestra solución con el repositorio base de la materia (`docker-hadoop` de Big Data Europe):*
>
> * **1. Modelo de Cómputo:** Hadoop usa **MapReduce**, el cual escribe en disco en cada etapa intermedia, generando un cuello de botella en I/O. Spark opera **completamente en memoria RAM**, logrando un procesamiento hasta 100 veces más rápido.*
> * **2. Usabilidad y Desarrollo:** Hadoop requiere compilar Jars monolíticos en Java. Nuestro despliegue de Spark integra **JupyterLab interactivo**, permitiendo analítica ágil en Python/PySpark.*
> * **3. Complejidad Operativa:** El clúster Hadoop requiere 5 servicios acoplados (NameNode, DataNodes, YARN, ResourceManager), mientras que Spark Standalone logra procesamiento distribuido resiliente con solo 4 contenedores ligeros.*
>
> *Conclusión: Hadoop es excelente para archivo y batch histórico en frío, pero **Spark es la herramienta por excelencia para analítica moderna, streaming y machine learning**."*

---

### FASE 5: Conclusiones y Cumplimiento de Entrega (1 Minuto)
> **Objetivo del PDF:** Cumplir Sección 10. Requisitos de repositorio y commits.

#### 🗣️ ¿Qué decir? (Guion sugerido):
> *"Para finalizar, el proyecto se encuentra publicado en nuestro repositorio público de GitHub **`bigdata-grupo-4`**, cumpliendo con la documentación técnica completa, diagramas de arquitectura, scripts de validación y un historial de **5 commits** que evidencian el avance incremental del trabajo.*
>
> *Quedamos a disposición para cualquier consulta. Muchas gracias."*

---

## 🛡️ BANCO DE PREGUNTAS Y RESPUESTAS DEFENSIVAS

Si el docente hace preguntas técnicas, responde con estas claves:

### ❓ P1: ¿Cómo demuestran que las tareas realmente se ejecutan de forma distribuida y no en un solo nodo?
> **Respuesta:** *"En los logs de ejecución de `SparkPi` y `test_pyspark.py`, el `DAGScheduler` de Spark divide el trabajo en `ResultStages` con múltiples particiones. En los logs se observan los IDs de los ejecutores `app-.../0` y `app-.../1` operando en las direcciones IP distintas de ambos nodos (`172.21.0.3` de worker-1 y `172.21.0.4` de worker-2). Además, en la Web UI (`localhost:8085`) se ve el conteo de Cores y memoria asignada en ambos trabajadores."*

### ❓ P2: ¿Qué sucede si se cae un nodo trabajador (Worker)?
> **Respuesta:** *"Apache Spark posee tolerancia a fallos mediante el linaje de RDDs (Resilient Distributed Datasets). Si un worker cae, el Master redistribuye automáticamente las particiones faltantes al worker restante sin interrumpir la sesión del usuario."*

### ❓ P3: ¿Por qué cambiaron el puerto Web del Master a 8085?
> **Respuesta:** *"Para evitar colisiones en entornos locales donde el puerto estándar `8080` suele estar reservado por servidores del sistema (como Oracle XE o Apache HTTP), mapeamos `8085:8080` en el host manteniendo intacto el puerto interno `8080` dentro del contenedor."*

---

## 📋 CHECKLIST RÁPIDO ANTES DE LA PRESENTACIÓN

- [ ] Docker Desktop iniciado y en verde (**Engine running**).
- [ ] Contenedores arriba (`docker compose up -d` o verificar con `docker ps`).
- [ ] Pestaña 1 abierta: Spark Master en [http://localhost:8085](http://localhost:8085).
- [ ] Pestaña 2 abierta: JupyterLab en [http://localhost:8888](http://localhost:8888).
- [ ] Pestaña 3 abierta: [README.md](file:///c:/Users/wiget/OneDrive/Desktop/bigdata-grupo-4/README.md) en GitHub / VSCode para mostrar arquitectura y tabla comparativa.
- [ ] Terminal lista en la carpeta del proyecto para ejecutar `python scripts/run_all_tests.py`.
