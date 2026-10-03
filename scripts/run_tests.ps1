<#
.SYNOPSIS
    Script de Ejecución Rápida del Circuito de Pruebas (PowerShell)
#>

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location (Join-Path $ScriptDir "..")

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   INICIANDO CIRCUITO DE PRUEBAS DE APACHE SPARK CLUSTER   " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

if (Get-Command python -ErrorAction SilentlyContinue) {
    python scripts/run_all_tests.py
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    py scripts/run_all_tests.py
} else {
    Write-Host "Python no encontrado en PATH. Ejecutando pruebas en modo nativo Docker..." -ForegroundColor Yellow
    
    Write-Host "`n[1/3] Ejecutando SparkPi..." -ForegroundColor Cyan
    docker exec spark-master /usr/bin/spark-3.5.7-bin-hadoop3/bin/spark-submit --master spark://spark-master:7077 --class org.apache.spark.examples.SparkPi /usr/bin/spark-3.5.7-bin-hadoop3/examples/jars/spark-examples_2.12-3.5.7.jar 10
    
    Write-Host "`n[2/3] Ejecutando PySpark DataFrames..." -ForegroundColor Cyan
    docker cp scripts/test_pyspark.py spark-master:/opt/workspace/test_pyspark.py
    docker exec spark-master /usr/bin/spark-3.5.7-bin-hadoop3/bin/spark-submit --master spark://spark-master:7077 /opt/workspace/test_pyspark.py
    
    Write-Host "`n[3/3] Ejecutando PySpark SQL..." -ForegroundColor Cyan
    docker cp scripts/test_spark_sql.py spark-master:/opt/workspace/test_spark_sql.py
    docker exec spark-master /usr/bin/spark-3.5.7-bin-hadoop3/bin/spark-submit --master spark://spark-master:7077 /opt/workspace/test_spark_sql.py
}
