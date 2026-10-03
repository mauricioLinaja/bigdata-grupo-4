#!/bin/bash
# Ejecutar cálculo distribuido de SparkPi en el clúster
docker exec spark-master /usr/bin/spark-3.5.7-bin-hadoop3/bin/spark-submit \
  --master spark://spark-master:7077 \
  --class org.apache.spark.examples.SparkPi \
  /usr/bin/spark-3.5.7-bin-hadoop3/examples/jars/spark-examples_2.12-3.5.7.jar 10
