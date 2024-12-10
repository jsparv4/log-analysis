#!/usr/bin/env python3

import csv
import os

# Path to the Hadoop output directory
OUTPUT_DIR = "hadoop_output"
CSV_FILE = "final_output.csv"

def merge_and_convert_to_csv(output_dir, csv_file):
    with open(csv_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Website", "DayOfWeek", "TimePeriod", "Count"])  # Write header
        
        for file_name in os.listdir(output_dir):
            if file_name.startswith("part-"):
                with open(os.path.join(output_dir, file_name), "r") as part_file:
                    for line in part_file:
                        line = line.strip()
                        website, day_of_week, time_period, count = line.split("\t")
                        writer.writerow([website, day_of_week, time_period, count])

if __name__ == "__main__":
    merge_and_convert_to_csv(OUTPUT_DIR, CSV_FILE)
    print(f"CSV file generated: {CSV_FILE}")
