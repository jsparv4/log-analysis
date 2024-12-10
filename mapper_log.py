#!/usr/bin/env python3

import re
import sys
from datetime import datetime

# Time definitions for day periods
TIME_DEFINITIONS = {
    "morning": (6, 12),
    "afternoon": (12, 18),
    "evening": (18, 24),
    "night": (0, 6)
}

# Regex pattern for log parsing
LOG_PATTERN = re.compile(r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(GET|POST|PUT|DELETE) (.*?) HTTP/1.1" (\d+) (\d+)')

def get_time_period(hour):
    """Determine time period based on the hour."""
    for period, (start, end) in TIME_DEFINITIONS.items():
        if start <= hour < end:
            return period
    return "unknown"

def process_log_line(log_line):
    """Parse and process a single log line."""
    match = LOG_PATTERN.match(log_line.strip())
    if match:
        try:
            # Extract relevant fields
            timestamp = match.group(2)
            method = match.group(3)
            website = match.group(4)
            
            # Parse timestamp and determine day and time period
            dt = datetime.strptime(timestamp.split()[0], "%d/%b/%Y:%H:%M:%S")
            day_of_week = dt.strftime('%A')
            time_period = get_time_period(dt.hour)
            
            # Emit key-value pair
            print(f"{website}\t{day_of_week}\t{time_period}\t1")
        except Exception as e:
            # Handle parsing errors
            sys.stderr.write(f"Error processing line: {log_line} - {e}\n")

def main():
    """Main function to process logs from stdin."""
    for log_line in sys.stdin:
        process_log_line(log_line)

if __name__ == "__main__":
    main()
