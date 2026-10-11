#!/usr/bin/env python3
"""
Script de Automatización de Pruebas de Fallo y Tolerancia a Fallos en HDFS (LG15)
Universidad del Valle - Sistemas Distribuidos / Big Data
Grupo 04: Joel Saavedra, Mauricio Linaja, Rommel Gutierrez

Objetivo:
- Probar experimentalmente el comportamiento de HDFS ante la caída de un DataNode (datanode2).
- Evaluar tanto con Dataset 1 GB como con Dataset 10 GB.
- Registrar metódicamente los estados: ANTES, DURANTE y DESPUÉS de la falla.
- Guardar las salidas y evidencias en archivos estructurados y en HDFS.
"""

import subprocess
import time
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVIDENCIAS_DIR = os.path.join(BASE_DIR, "evidencias")

def run_cmd(cmd: str, desc: str, output_file: str = None):
    print("\n" + "="*70)
    print(f"[*] {desc}")
    print(f"[*] COMANDO: {cmd}")
    print("="*70)
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    out_text = ""
    if result.stdout:
        print("[STDOUT]\n" + result.stdout.strip())
        out_text += result.stdout
    if result.stderr:
        print("[STDERR]\n" + result.stderr.strip())
        out_text += "\n" + result.stderr

    if output_file:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "a", encoding="utf-8") as f:
            f.write(f"\n{'='*70}\n[*] {desc}\n[*] COMANDO: {cmd}\n{'='*70}\n")
            f.write(out_text)
            f.write("\n")

    return result

def wait_for_datanodes(expected_count=3, timeout=90):
    print(f"[*] Esperando que {expected_count} DataNodes estén en estado 'Live'...")
    start = time.time()
    while time.time() - start < timeout:
        res = subprocess.run("docker exec namenode hdfs dfsadmin -report", 
                             shell=True, text=True, capture_output=True)
        live_count = res.stdout.count("Live datanodes (")
        # En el reporte dice: "Live datanodes (3):"
        if f"Live datanodes ({expected_count})" in res.stdout:
            print(f"[+] Confirmado: {expected_count} DataNodes activos y registrados.")
            return True
        time.sleep(5)
    print(f"[!] Advertencia: No se alcanzaron los {expected_count} DataNodes en {timeout}s.")
    return False

def ejecutar_prueba_dataset(dataset_name: str, hdfs_path: str, size_desc: str):
    log_file = os.path.join(EVIDENCIAS_DIR, f"evidencia_falla_{dataset_name}.log")
    if os.path.exists(log_file):
        os.remove(log_file)

    print("\n" + "#"*75)
    print(f"### INICIANDO EXPERIMENTO DE TOLERANCIA A FALLOS: {size_desc} ({dataset_name})")
    print("#"*75)

    # -------------------------------------------------------------
    # 1. ESTADO INICIAL (DN1, DN2, DN3 Activos)
    # -------------------------------------------------------------
    print("\n>>> FASE 1: REGISTRO DEL ESTADO INICIAL (TODOS LOS DATANODES ACTIVOS)")
    run_cmd("docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'", 
            "Contenedores activos en Docker", log_file)
    run_cmd("docker exec namenode hdfs dfsadmin -report", 
            "Reporte HDFS DFSAdmin - Estado Inicial de los 3 DataNodes", log_file)
    run_cmd(f"docker exec namenode hdfs fsck {hdfs_path} -files -blocks -locations", 
            f"FSCK inicial del {dataset_name} (Bloques, réplicas y ubicaciones en DNs)", log_file)

    # -------------------------------------------------------------
    # 2. INTRODUCCIÓN DE LA FALLA: Detener DataNode 2
    # -------------------------------------------------------------
    print("\n>>> FASE 2: SIMULACIÓN DE FALLA EN NODO DE ALMACENAMIENTO (STOP DATANODE2)")
    run_cmd("docker stop datanode2", "Detención forzada del contenedor datanode2", log_file)

    # -------------------------------------------------------------
    # 3. VERIFICACIÓN DURANTE LA FALLA
    # -------------------------------------------------------------
    print("\n>>> FASE 3: COMPORTAMIENTO DEL SISTEMA DURANTE LA FALLA")
    # Dar unos segundos para que se refleje la desconexión
    time.sleep(5)
    run_cmd("docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'", 
            "Estado de contenedores post-caída (datanode2 detenido)", log_file)
    
    # Comprobar accesibilidad y lectura del archivo
    run_cmd(f"docker exec namenode hdfs dfs -tail {hdfs_path}", 
            f"Prueba de lectura directa con -tail sobre {hdfs_path} (¿Archivo accesible?)", log_file)
    
    # Ejecutar FSCK inmediato
    run_cmd(f"docker exec namenode hdfs fsck {hdfs_path} -files -blocks -locations", 
            f"FSCK durante la falla - Análisis de réplicas disponibles y bloques faltantes en DN2", log_file)

    # -------------------------------------------------------------
    # 4. DETECCIÓN DE DEAD DATANODE Y SUBREPLICACIÓN
    # -------------------------------------------------------------
    print("\n>>> FASE 4: DETECCIÓN POR PARTE DEL NAMENODE (DEAD NODE Y RE-REPLICACIÓN)")
    print("[*] Esperando ciclo de detección de nodo caído (heartbeat timeout ~60-90s)...")
    time.sleep(65)
    
    run_cmd("docker exec namenode hdfs dfsadmin -report", 
            "Reporte HDFS DFSAdmin - NameNode detecta Dead DataNode (datanode2)", log_file)
    run_cmd(f"docker exec namenode hdfs fsck {hdfs_path} -files -blocks -locations", 
            f"FSCK tras timeout - Verificación de bloques subreplicados y reconstrucción", log_file)

    # -------------------------------------------------------------
    # 5. RESTAURACIÓN DEL DATANODE PARA SIGUIENTES PRUEBAS
    # -------------------------------------------------------------
    print("\n>>> FASE 5: RECUPERACIÓN Y REINCORPORACIÓN DE DATANODE2")
    run_cmd("docker start datanode2", "Reinicio y reincorporación de datanode2 al clúster", log_file)
    wait_for_datanodes(3, timeout=60)
    run_cmd("docker exec namenode hdfs dfsadmin -report", 
            "Reporte HDFS DFSAdmin - 3 DataNodes activos nuevamente tras reincorporación", log_file)

    print(f"\n[+] Experimento para {size_desc} finalizado. Evidencia guardada en:\n    {log_file}")

def main():
    print("====================================================================")
    print("  EJECUCIÓN DE PRUEBAS DE FALLO HDFS (DATASET 1 GB & DATASET 10 GB) ")
    print("  Grupo 04 - Universidad del Valle                                  ")
    print("====================================================================")

    # Asegurar que los 3 DataNodes estén listos antes de iniciar
    wait_for_datanodes(3, timeout=30)

    # Experimento 1: Dataset 1 GB
    ejecutar_prueba_dataset(
        dataset_name="dataset_1GB",
        hdfs_path="/grupo04/dataset_1GB/dataset_grupo04_1GB",
        size_desc="Dataset 1 GB (8 Bloques de 128 MB)"
    )

    # Pausa de estabilización entre experimentos
    time.sleep(10)

    # Experimento 2: Dataset 10 GB
    ejecutar_prueba_dataset(
        dataset_name="dataset_10GB",
        hdfs_path="/grupo04/dataset_10GB/dataset_grupo04_10GB",
        size_desc="Dataset 10 GB (80 Bloques de 128 MB)"
    )

    # Subir evidencias y resultados a HDFS en /grupo04/evidencias y /grupo04/resultados
    print("\n" + "="*70)
    print("[*] Sincronizando evidencias generadas hacia HDFS...")
    print("="*70)
    run_cmd("docker exec namenode hdfs dfs -put -f /evidencias/evidencia_falla_dataset_1GB.log /grupo04/evidencias/", 
            "Subir log de 1 GB a /grupo04/evidencias/")
    run_cmd("docker exec namenode hdfs dfs -put -f /evidencias/evidencia_falla_dataset_10GB.log /grupo04/evidencias/", 
            "Subir log de 10 GB a /grupo04/evidencias/")
    run_cmd("docker exec namenode hdfs dfs -ls -R /grupo04", 
            "Verificar árbol final y archivos de resultados en /grupo04")

    print("\n====================================================================")
    print("   [+] TODAS LAS PRUEBAS DE FALLO FUERON COMPLETADAS EXITOSAMENTE   ")
    print("====================================================================")

if __name__ == "__main__":
    main()
