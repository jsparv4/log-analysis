#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define variables
APACHE_LOGS_FOLDER="apache_logs"
GEN_LOG_SCRIPT="gen_log.py"
HADOOP_STREAMING_JAR=${HADOOP_STREAMING_JAR:-"/default/path/to/hadoop-streaming.jar"}
HADOOP_INPUT_FOLDER="/user/student/input/apache_logs"
HADOOP_OUTPUT_FOLDER="/user/student/output"
GEN_CSV_SCRIPT="gen_csv.py"
DATA_VIZ_SCRIPT="data_viz.py"

echo "=== Pipeline Script Started ==="

# Run gen_log.py to generate logs
echo "Running $GEN_LOG_SCRIPT to generate logs..."
python3 "$GEN_LOG_SCRIPT"
echo "Log generation completed."

# Run Hadoop Streaming Job
echo "Starting Hadoop Streaming job..."

# Remove old Hadoop input and output directories if they exist
hdfs dfs -rm -r "$HADOOP_INPUT_FOLDER" || true
hdfs dfs -rm -r "$HADOOP_OUTPUT_FOLDER" || true

# Upload new input files to HDFS
hdfs dfs -mkdir -p "$HADOOP_INPUT_FOLDER"
hdfs dfs -put $APACHE_LOGS_FOLDER/* "$HADOOP_INPUT_FOLDER"

# Run Hadoop Streaming
hadoop jar "$HADOOP_STREAMING_JAR" \
    -input "$HADOOP_INPUT_FOLDER" \
    -output "$HADOOP_OUTPUT_FOLDER" \
    -mapper "mapper_log.py" \
    -reducer "reducer_log.py"

echo "Hadoop Streaming job completed."

# Download Hadoop output
echo "Downloading Hadoop output..."
rm -rf hadoop_output  # Ensure local output folder is clean
hdfs dfs -get "$HADOOP_OUTPUT_FOLDER" hadoop_output

# Run gen_csv.py to generate CSV from Hadoop output
echo "Running $GEN_CSV_SCRIPT to generate CSV..."
python3 "$GEN_CSV_SCRIPT"
echo "CSV generation completed."

# Run data_viz.py to generate visualizations
echo "Running $DATA_VIZ_SCRIPT to create visualizations..."
python3 "$DATA_VIZ_SCRIPT" 2>/dev/null
echo "Visualization generation completed."

echo "=== Pipeline Script Completed Successfully ==="
