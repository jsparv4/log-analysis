#!/usr/bin/env python3

import sys
from collections import defaultdict

def reducer():
    # Dictionary to store aggregated counts
    counts = defaultdict(int)
    
    for line in sys.stdin:
        try:
            # Parse the mapper output
            line = line.strip()
            *key_parts, count = line.split("\t")
            key = "\t".join(key_parts)
            counts[key] += int(count)
        except Exception as e:
            # Log errors to stderr
            sys.stderr.write(f"Error processing line: {line} - {e}\n")

    # Output results to stdout
    for key, count in counts.items():
        print(f"{key}\t{count}")

if __name__ == "__main__":
    reducer()
