#!/usr/bin/env python3
"""
=============================================================================
CIRCUITO DE PRUEBAS AUTOMATIZADO - CLÚSTER DISTRIBUIDO APACHE SPARK
Grupo 4 - Big Data
=============================================================================
Este script ejecuta de manera integral y automatizada todas las validaciones:
1. Salud de Contenedores Docker (spark-master, worker-1, worker-2, jupyterlab)
2. Verificación de conectividad Web UI
3. Prueba 1: Cálculo Distribuido de Pi (SparkPi / Monte Carlo)
4. Prueba 2: PySpark DataFrame y Filtrado Distribuido
5. Prueba 3: Spark SQL y Agregaciones de Métricas
6. Reporte consolidado con métricas de tiempo y estado.
"""

import sys
import os
import subprocess
import time
import urllib.request
import json

# Asegurar encoding utf-8 en salidas estándar
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# Colores ANSI para presentación en consola
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Habilitar colores en Windows cmd/powershell
if os.name == "nt":
    os.system("")

def print_header(title):
    width = 75
    print("\n" + CYAN + "=" * width + RESET)
    print(BOLD + CYAN + f"  {title.center(width - 4)}" + RESET)
    print(CYAN + "=" * width + RESET)

def print_step(step_num, title):
    print(f"\n{BOLD}{YELLOW}[PASO {step_num}]{RESET} {BOLD}{title}{RESET}")
    print("-" * 75)

def run_command(cmd):
    """Ejecuta un comando en terminal y retorna (código_salida, stdout, tiempo_segundos)"""
    start_time = time.time()
    try:
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        stdout, _ = process.communicate()
        elapsed = time.time() - start_time
        return process.returncode, stdout, elapsed
    except Exception as e:
        elapsed = time.time() - start_time
        return 1, str(e), elapsed

def check_web_ui(port):
    """Verifica si la Web UI responde en el puerto dado"""
    url = f"http://localhost:{port}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            return resp.status == 200, url
    except Exception:
        return False, url

def main():
    print_header("CIRCUITO DE PRUEBAS DE VALIDACION - APACHE SPARK")
    print(f"{BOLD}Iniciando conjunto de pruebas funcionales y de arquitectura...{RESET}")
    
    results = []

    # -------------------------------------------------------------------------
    # PASO 1: Verificación de Contenedores Docker
    # -------------------------------------------------------------------------
    print_step(1, "Verificando estado de los 4 contenedores Docker...")
    ret, out, dur = run_command("docker ps --format \"{{.Names}}\t{{.Status}}\t{{.Ports}}\"")
    
    expected_containers = ["spark-master", "spark-worker-1", "spark-worker-2", "jupyterlab"]
    missing = []
    
    if ret == 0:
        print(f"{CYAN}Contenedores activos detectados:{RESET}")
        for line in out.strip().split("\n"):
            if line:
                print(f"  * {line}")
        for c in expected_containers:
            if c not in out:
                missing.append(c)
    else:
        missing = expected_containers

    if not missing:
        print(f"\n{GREEN}[OK] Todos los 4 contenedores requeridos estan en ejecucion.{RESET}")
        results.append(("Salud del Cluster (4 Contenedores)", "PASSED", f"{dur:.2f}s", "spark-master, workers 1/2 y jupyterlab activos"))
    else:
        print(f"\n{RED}[FAIL] Faltan contenedores por levantar: {', '.join(missing)}{RESET}")
        print(f"{YELLOW}Sugerencia: Ejecute 'docker compose up -d' antes de las pruebas.{RESET}")
        results.append(("Salud del Cluster", "FAILED", f"{dur:.2f}s", f"Faltan: {', '.join(missing)}"))

    # -------------------------------------------------------------------------
    # PASO 2: Verificación de Interfaz Web UI de Spark Master y Jupyter
    # -------------------------------------------------------------------------
    print_step(2, "Verificando accesibilidad de las Interfaces Web (Master y Jupyter)...")
    
    # Probar puerto 8085 primero (configuración actual) y luego 8080
    master_ui_ok, master_url = check_web_ui(8085)
    if not master_ui_ok:
        master_ui_ok, master_url = check_web_ui(8080)
        
    jupyter_ui_ok, jupyter_url = check_web_ui(8888)

    print(f"  * Spark Master Web UI ({master_url}): {'[' + GREEN + 'OK' + RESET + ']' if master_ui_ok else '[' + RED + 'NO DISPONIBLE' + RESET + ']'}")
    print(f"  * JupyterLab Web UI   ({jupyter_url}): {'[' + GREEN + 'OK' + RESET + ']' if jupyter_ui_ok else '[' + RED + 'NO DISPONIBLE' + RESET + ']'}")
    
    if master_ui_ok and jupyter_ui_ok:
        results.append(("Conectividad Web UIs", "PASSED", "-", f"Master en {master_url} | Jupyter en {jupyter_url}"))
    else:
        results.append(("Conectividad Web UIs", "WARNING", "-", f"Master: {master_ui_ok} | Jupyter: {jupyter_ui_ok}"))

    # -------------------------------------------------------------------------
    # PASO 3: Prueba 1 - Cálculo Distribuido de Pi (SparkPi)
    # -------------------------------------------------------------------------
    print_step(3, "Prueba 1: Calculo Distribuido de Pi (SparkPi / Monte Carlo)...")
    cmd_spark_pi = (
        "docker exec spark-master /usr/bin/spark-3.5.7-bin-hadoop3/bin/spark-submit "
        "--master spark://spark-master:7077 "
        "--class org.apache.spark.examples.SparkPi "
        "/usr/bin/spark-3.5.7-bin-hadoop3/examples/jars/spark-examples_2.12-3.5.7.jar 10"
    )
    print(f"{CYAN}Ejecutando en spark-master:{RESET}\n{cmd_spark_pi}\n")
    ret_pi, out_pi, dur_pi = run_command(cmd_spark_pi)
    
    pi_val = None
    for line in out_pi.split("\n"):
        if "Pi is roughly" in line:
            pi_val = line.strip()
            print(f"{BOLD}{GREEN}>>> {pi_val} <<<{RESET}")
    
    if ret_pi == 0 and pi_val:
        print(f"\n{GREEN}[OK] Prueba 1 completada exitosamente en {dur_pi:.2f} segundos.{RESET}")
        results.append(("Prueba 1: SparkPi (Distribuido)", "PASSED", f"{dur_pi:.2f}s", pi_val))
    else:
        print(f"\n{RED}[FAIL] Fallo el calculo de SparkPi.{RESET}")
        print(out_pi[-500:])
        results.append(("Prueba 1: SparkPi", "FAILED", f"{dur_pi:.2f}s", "Error al ejecutar jar de ejemplos"))

    # -------------------------------------------------------------------------
    # PASO 4: Prueba 2 - PySpark DataFrames y Filtrado Distribuido
    # -------------------------------------------------------------------------
    print_step(4, "Prueba 2: PySpark DataFrame y Filtrado Distribuido...")
    
    # Copiar script
    run_command("docker cp scripts/test_pyspark.py spark-master:/opt/workspace/test_pyspark.py")
    
    cmd_pyspark = (
        "docker exec spark-master /usr/bin/spark-3.5.7-bin-hadoop3/bin/spark-submit "
        "--master spark://spark-master:7077 "
        "/opt/workspace/test_pyspark.py"
    )
    print(f"{CYAN}Ejecutando script:{RESET}\n{cmd_pyspark}\n")
    ret_py, out_py, dur_py = run_command(cmd_pyspark)
    
    # Mostrar salida limpia
    for line in out_py.split("\n"):
        if any(keyword in line for keyword in ["DATAFRAME", "FILTRADO", "Total de registros", "[OK]", "+---", "|Apache", "|Tecnologia"]):
            print(f"  {line}")

    if ret_py == 0 and "Total de registros procesados en el clúster: 5" in out_py:
        print(f"\n{GREEN}[OK] Prueba 2 de DataFrames completada exitosamente en {dur_py:.2f} segundos.{RESET}")
        results.append(("Prueba 2: PySpark DataFrames", "PASSED", f"{dur_py:.2f}s", "5 registros procesados y filtrados"))
    else:
        print(f"\n{RED}[FAIL] Fallo la prueba de PySpark DataFrames.{RESET}")
        results.append(("Prueba 2: PySpark DataFrames", "FAILED", f"{dur_py:.2f}s", "Error en ejecucion de script"))

    # -------------------------------------------------------------------------
    # PASO 5: Prueba 3 - Spark SQL y Agregaciones Analíticas
    # -------------------------------------------------------------------------
    print_step(5, "Prueba 3: Spark SQL y Agregaciones de Metricas Distribuidas...")
    
    # Copiar script sql
    run_command("docker cp scripts/test_spark_sql.py spark-master:/opt/workspace/test_spark_sql.py")
    
    cmd_sql = (
        "docker exec spark-master /usr/bin/spark-3.5.7-bin-hadoop3/bin/spark-submit "
        "--master spark://spark-master:7077 "
        "/opt/workspace/test_spark_sql.py"
    )
    print(f"{CYAN}Ejecutando script:{RESET}\n{cmd_sql}\n")
    ret_sql, out_sql, dur_sql = run_command(cmd_sql)
    
    for line in out_sql.split("\n"):
        if any(keyword in line for keyword in ["AGREGACION", "SPARK SQL", "TELEMETRIA", "[OK]", "[v]", "+---", "|Nodo", "|TipoServicio", "Procesamiento distribuido"]):
            print(f"  {line}")

    if ret_sql == 0 and "Procesamiento distribuido completado exitosamente" in out_sql:
        print(f"\n{GREEN}[OK] Prueba 3 de Spark SQL completada exitosamente en {dur_sql:.2f} segundos.{RESET}")
        results.append(("Prueba 3: Spark SQL & Agregaciones", "PASSED", f"{dur_sql:.2f}s", "Consultas SQL y groupBy distribuidos OK"))
    else:
        print(f"\n{RED}[FAIL] Fallo la prueba de Spark SQL.{RESET}")
        results.append(("Prueba 3: Spark SQL", "FAILED", f"{dur_sql:.2f}s", "Error en ejecucion de script SQL"))

    # -------------------------------------------------------------------------
    # REPORTE FINAL CONSOLIDADO
    # -------------------------------------------------------------------------
    print_header("REPORTE CONSOLIDADO DE PRUEBAS")
    
    print(f"\n{BOLD}{'PRUEBA / VALIDACION':<38} {'ESTADO':<12} {'DURACION':<10} {'DETALLE'}{RESET}")
    print("-" * 85)
    
    all_passed = True
    for name, status, duration, detail in results:
        if status == "PASSED":
            status_str = f"{GREEN}[ PASSED ]{RESET}"
        elif status == "WARNING":
            status_str = f"{YELLOW}[ WARNING ]{RESET}"
        else:
            status_str = f"{RED}[ FAILED ]{RESET}"
            all_passed = False
            
        print(f"{name:<38} {status_str:<21} {duration:<10} {detail}")

    print("-" * 85)
    
    if all_passed:
        print(f"\n{BOLD}{GREEN}RESULTADO GLOBAL: TODAS LAS PRUEBAS PASARON EXITOSAMENTE! (100% OK){RESET}")
        print(f"{CYAN}El cluster Spark distribuido se encuentra 100% operativo y validado.{RESET}\n")
        return 0
    else:
        print(f"\n{BOLD}{RED}RESULTADO GLOBAL: AL MENOS UNA PRUEBA PRESENTO ERRORES.{RESET}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
