@echo off
REM ==============================================================================
REM Script de Ejecución Rápida del Circuito de Pruebas (Windows CMD / Doble Clic)
REM ==============================================================================

cd /d "%~dp0\.."
echo ==========================================================
echo    INICIANDO CIRCUITO DE PRUEBAS DE APACHE SPARK CLUSTER   
echo ==========================================================

where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    python scripts\run_all_tests.py
    pause
    exit /b %ERRORLEVEL%
)

where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    py scripts\run_all_tests.py
    pause
    exit /b %ERRORLEVEL%
)

echo Python no encontrado en PATH. Ejecutando pruebas en modo nativo...
echo.
echo [1/3] Ejecutando SparkPi...
docker exec spark-master /usr/bin/spark-3.5.7-bin-hadoop3/bin/spark-submit --master spark://spark-master:7077 --class org.apache.spark.examples.SparkPi /usr/bin/spark-3.5.7-bin-hadoop3/examples/jars/spark-examples_2.12-3.5.7.jar 10

echo.
echo [2/3] Ejecutando PySpark DataFrames...
docker cp scripts\test_pyspark.py spark-master:/opt/workspace/test_pyspark.py
docker exec spark-master /usr/bin/spark-3.5.7-bin-hadoop3/bin/spark-submit --master spark://spark-master:7077 /opt/workspace/test_pyspark.py

echo.
echo [3/3] Ejecutando PySpark SQL...
docker cp scripts\test_spark_sql.py spark-master:/opt/workspace/test_spark_sql.py
docker exec spark-master /usr/bin/spark-3.5.7-bin-hadoop3/bin/spark-submit --master spark://spark-master:7077 /opt/workspace/test_spark_sql.py

pause
