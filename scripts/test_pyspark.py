"""
Script de prueba funcional en Apache Spark
Calcula transformaciones distribuidas sobre un DataFrame con PySpark
conectándose al nodo maestro del clúster.
"""
from pyspark.sql import SparkSession

def main():
    print("Iniciando sesión de Spark conectada a spark://spark-master:7077...")
    spark = SparkSession.builder \
        .appName("PruebaFuncionalBigData") \
        .master("spark://spark-master:7077") \
        .getOrCreate()

    # Reducir verbosidad de logs
    spark.sparkContext.setLogLevel("WARN")

    print("\n[OK] Sesion iniciada exitosamente.")
    print(f"Version de Spark: {spark.version}")

    # Creación de datos de prueba
    datos = [
        ("Apache Spark", "Procesamiento en memoria", 2014, 100),
        ("Apache Hadoop", "Almacenamiento HDFS", 2006, 95),
        ("Apache Kafka", "Streaming de eventos", 2011, 98),
        ("Apache Flink", "Streaming en tiempo real", 2015, 92),
        ("Apache Cassandra", "Base de datos NoSQL", 2008, 90),
    ]

    columnas = ["Tecnologia", "Especialidad", "AnioLanzamiento", "Popularidad"]

    df = spark.createDataFrame(datos, columnas)

    print("\n--- DATAFRAME DISTRIBUIDO CREADO ---")
    df.show(truncate=False)

    print("\n--- FILTRADO DISTRIBUIDO (Anio >= 2011) ---")
    df_filtrado = df.filter(df["AnioLanzamiento"] >= 2011)
    df_filtrado.show(truncate=False)

    total_registros = df.count()
    print(f"\nTotal de registros procesados en el clúster: {total_registros}")

    spark.stop()
    print("\n[OK] Sesion de Spark finalizada correctamente.")

if __name__ == "__main__":
    main()
