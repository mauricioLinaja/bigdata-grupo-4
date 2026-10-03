"""
Script de prueba analítica avanzada en Apache Spark
Ejecuta consultas Spark SQL y agregaciones distribuidas sobre el clúster.
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, max, min

def main():
    print("==========================================================")
    print("   PRUEBA ANALÍTICA AVANZADA: SPARK SQL Y AGREGACIONES   ")
    print("==========================================================")
    
    spark = SparkSession.builder \
        .appName("PruebaSparkSQLAgregaciones") \
        .master("spark://spark-master:7077") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    print("\n[✓] Sesion Spark inicializada.")
    print(f"    - Version: {spark.version}")
    print(f"    - Master: {spark.sparkContext.master}")

    # Dataset de transacciones / telemetría distribuida
    datos_telemetria = [
        ("Nodo-A1", "Servidor-Web", 45.2, 1024, 200),
        ("Nodo-A1", "Base-Datos", 82.5, 4096, 200),
        ("Nodo-A2", "Servidor-Web", 50.1, 1024, 500),
        ("Nodo-A2", "Cache-Redis", 22.0, 512, 200),
        ("Nodo-B1", "Servidor-Web", 68.4, 2048, 200),
        ("Nodo-B1", "Base-Datos", 91.0, 8192, 503),
        ("Nodo-B2", "Cache-Redis", 35.8, 512, 200),
        ("Nodo-B2", "Servidor-Web", 55.3, 1024, 200),
        ("Nodo-C1", "Base-Datos", 78.9, 4096, 200),
        ("Nodo-C1", "Servidor-Web", 62.0, 2048, 200),
    ]

    columnas = ["Nodo", "TipoServicio", "UsoCPU_Porcentaje", "MemoriaMB", "CodigoRespuesta"]

    # Crear DataFrame distribuido particionado
    df = spark.createDataFrame(datos_telemetria, columnas).repartition(2)

    print("\n--- 1. DATASET DE TELEMETRÍA (10 REGISTROS EN 2 PARTICIONES) ---")
    df.show(truncate=False)

    print("\n--- 2. AGREGACIÓN POR TIPO DE SERVICIO (Spark DataFrame API) ---")
    resumen_servicios = df.groupBy("TipoServicio").agg(
        count("*").alias("TotalInstancias"),
        avg("UsoCPU_Porcentaje").alias("PromedioCPU"),
        max("MemoriaMB").alias("MemoriaMaxMB"),
        min("MemoriaMB").alias("MemoriaMinMB")
    )
    resumen_servicios.show(truncate=False)

    print("\n--- 3. CONSULTA CON SPARK SQL (Servidores con CPU > 50%) ---")
    df.createOrReplaceTempView("telemetria")
    consulta_sql = spark.sql("""
        SELECT Nodo, TipoServicio, UsoCPU_Porcentaje, CodigoRespuesta
        FROM telemetria
        WHERE UsoCPU_Porcentaje > 50.0
        ORDER BY UsoCPU_Porcentaje DESC
    """)
    consulta_sql.show(truncate=False)

    print(f"[✓] Procesamiento distribuido completado exitosamente con {df.count()} métricas.")
    spark.stop()
    print("[✓] Sesion cerrada correctamente.\n")

if __name__ == "__main__":
    main()
