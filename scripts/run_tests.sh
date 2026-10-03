#!/bin/bash
# ==============================================================================
# Script de Ejecución Rápida del Circuito de Pruebas (Linux / macOS / Git Bash)
# ==============================================================================

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

echo "=========================================================="
echo "   INICIANDO CIRCUITO DE PRUEBAS DE APACHE SPARK CLUSTER   "
echo "=========================================================="

if command -v python3 &>/dev/null; then
    python3 scripts/run_all_tests.py
elif command -v python &>/dev/null; then
    python scripts/run_all_tests.py
else
    echo "Python no encontrado en PATH. Ejecutando pruebas en modo manual..."
    echo "[1/3] Ejecutando SparkPi..."
    docker exec spark-master /usr/bin/spark-3.5.7-bin-hadoop3/bin/spark-submit \
      --master spark://spark-master:7077 \
      --class org.apache.spark.examples.SparkPi \
      /usr/bin/spark-3.5.7-bin-hadoop3/examples/jars/spark-examples_2.12-3.5.7.jar 10
      
    echo "[2/3] Ejecutando PySpark DataFrames..."
    docker cp scripts/test_pyspark.py spark-master:/opt/workspace/test_pyspark.py
    docker exec spark-master /usr/bin/spark-3.5.7-bin-hadoop3/bin/spark-submit \
      --master spark://spark-master:7077 /opt/workspace/test_pyspark.py
      
    echo "[3/3] Ejecutando PySpark SQL..."
    docker cp scripts/test_spark_sql.py spark-master:/opt/workspace/test_spark_sql.py
    docker exec spark-master /usr/bin/spark-3.5.7-bin-hadoop3/bin/spark-submit \
      --master spark://spark-master:7077 /opt/workspace/test_spark_sql.py
fi
