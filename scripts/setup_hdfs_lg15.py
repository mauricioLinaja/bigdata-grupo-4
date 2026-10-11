#!/usr/bin/env python3
"""
Script de Preparación y Carga de Datasets en HDFS (LG15)
Universidad del Valle - Sistemas Distribuidos / Big Data
Grupo 04: Joel Saavedra, Mauricio Linaja, Rommel Gutierrez

Objetivo:
- Verificar que el clúster (NameNode + 3 DataNodes) esté operativo.
- Crear la jerarquía de directorios oficial /grupo04/.
- Generar y cargar el Dataset 1 (1 GB, 8 bloques de 128 MB, rep=2).
- Generar y cargar el Dataset 2 (10 GB, 80 bloques de 128 MB, rep=2).
"""

import subprocess
import time
import sys

def run_cmd(cmd: str, desc: str, check: bool = True):
    print("\n" + "="*70)
    print(f"[*] {desc}")
    print(f"[*] COMANDO: {cmd}")
    print("="*70)
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if result.stdout:
        print("[STDOUT]\n" + result.stdout.strip())
    if result.stderr:
        print("[STDERR]\n" + result.stderr.strip())
    if check and result.returncode != 0:
        print(f"[!] ERROR: Falló la ejecución (código {result.returncode})")
    else:
        print("[+] Operación exitosa")
    return result

def wait_for_namenode():
    print("[*] Esperando a que NameNode salga de SafeMode y reconozca a los 3 DataNodes...")
    for i in range(30):
        res = subprocess.run("docker exec namenode hdfs dfsadmin -safemode get", 
                             shell=True, text=True, capture_output=True)
        if "Safe mode is OFF" in res.stdout or "Safe mode is OFF" in res.stderr:
            print("[+] NameNode está listo y fuera de Modo Seguro.")
            break
        # Intentar desactivar SafeMode explícitamente si ya hay DataNodes
        subprocess.run("docker exec namenode hdfs dfsadmin -safemode leave", 
                       shell=True, text=True, capture_output=True)
        time.sleep(3)
    else:
        print("[!] Advertencia: Tiempo de espera agotado para SafeMode.")

def main():
    print("====================================================================")
    print("  LG15: TOLERANCIA A FALLOS Y REPLICACIÓN EN HDFS - GRUPO 04        ")
    print("  Integrantes: Joel Saavedra, Mauricio Linaja, Rommel Gutierrez     ")
    print("====================================================================")

    # 1. Verificar estado de contenedores
    run_cmd("docker ps", "Paso 1: Verificar contenedores activos del clúster")

    # Esperar que NameNode esté listo
    wait_for_namenode()

    # 2. Verificar reporte de DataNodes
    run_cmd("docker exec namenode hdfs dfsadmin -report", 
            "Paso 2: Reporte inicial de almacenamiento y DataNodes registrados")

    # 3. Crear jerarquía de directorios de Grupo 04
    dirs = [
        "/grupo04",
        "/grupo04/dataset_1GB",
        "/grupo04/dataset_10GB",
        "/grupo04/resultados",
        "/grupo04/evidencias"
    ]
    for d in dirs:
        run_cmd(f"docker exec namenode hdfs dfs -mkdir -p {d}", 
                f"Paso 3: Crear directorio {d} en HDFS")

    run_cmd("docker exec namenode hdfs dfs -ls -R /grupo04", 
            "Paso 4: Listar estructura creada en /grupo04")

    # 4. Generar y cargar Dataset 1 (1 GB = 1024 MB = 8 bloques de 128 MB)
    print("\n--------------------------------------------------------------------")
    print("   GENERANDO Y CARGANDO DATASET 1 (1 GB) EN HDFS                     ")
    print("--------------------------------------------------------------------")
    # Generamos directamente por pipe para optimizar I/O y no saturar disco del host
    cmd_1gb = (
        'docker exec namenode bash -c "'
        'dd if=/dev/zero bs=1M count=1024 2>/dev/null | '
        'hdfs dfs -D dfs.replication=2 -D dfs.blocksize=134217728 '
        '-put -f - /grupo04/dataset_1GB/dataset_grupo04_1GB"'
    )
    run_cmd(cmd_1gb, "Paso 5: Cargar dataset_grupo04_1GB (1 GB, rep=2, blocksize=128MB)")

    # Verificar metadatos y distribución de bloques del Dataset 1 GB
    run_cmd("docker exec namenode hdfs dfs -ls -h /grupo04/dataset_1GB", 
            "Paso 6: Verificar metadatos de dataset_grupo04_1GB")
    run_cmd("docker exec namenode hdfs fsck /grupo04/dataset_1GB/dataset_grupo04_1GB -files -blocks -locations", 
            "Paso 7: FSCK de dataset_grupo04_1GB (Bloques y ubicaciones)")

    # 5. Generar y cargar Dataset 2 (10 GB = 10240 MB = 80 bloques de 128 MB)
    print("\n--------------------------------------------------------------------")
    print("   GENERANDO Y CARGANDO DATASET 2 (10 GB) EN HDFS                    ")
    print("--------------------------------------------------------------------")
    cmd_10gb = (
        'docker exec namenode bash -c "'
        'dd if=/dev/zero bs=1M count=10240 2>/dev/null | '
        'hdfs dfs -D dfs.replication=2 -D dfs.blocksize=134217728 '
        '-put -f - /grupo04/dataset_10GB/dataset_grupo04_10GB"'
    )
    run_cmd(cmd_10gb, "Paso 8: Cargar dataset_grupo04_10GB (10 GB, rep=2, blocksize=128MB)")

    # Verificar metadatos y distribución de bloques del Dataset 10 GB
    run_cmd("docker exec namenode hdfs dfs -ls -h /grupo04/dataset_10GB", 
            "Paso 9: Verificar metadatos de dataset_grupo04_10GB")
    run_cmd("docker exec namenode hdfs fsck /grupo04/dataset_10GB/dataset_grupo04_10GB -files -blocks -locations", 
            "Paso 10: FSCK de dataset_grupo04_10GB (Bloques y ubicaciones)")

    print("\n[+] Configuración inicial y carga de datasets completada con éxito.")

if __name__ == "__main__":
    main()
