#!/usr/bin/env python3

import os
import random
from datetime import datetime, timedelta
from faker import Faker

# Seed for reproducibility
SEED = 42
random.seed(SEED)
Faker.seed(SEED)
fake = Faker()

# Parameters
OUTPUT_FOLDER = "apache_logs"
FILE_COUNT = 25
LINES_PER_FILE = 10000

# Social media sites
TOP_SITES = [
    "https://www.facebook.com",
    "https://www.youtube.com",
    "https://www.x.com",
    "https://www.instagram.com",
    "https://www.tiktok.com",
]

# Time periods and their weights
TIME_DEFINITIONS = {
    "morning": (6, 12, 20),  # 6 AM to 12 PM, weight 20%
    "afternoon": (12, 18, 35),  # 12 PM to 6 PM, weight 35%
    "evening": (18, 24, 30),  # 6 PM to 12 AM, weight 30%
    "night": (0, 6, 15),  # 12 AM to 6 AM, weight 15%
}

# Base weights for website popularity by time period
BASE_WEIGHTS = {
    "morning": [30, 20, 10, 25, 15],
    "afternoon": [25, 30, 10, 20, 15],
    "evening": [20, 25, 10, 15, 30],
    "night": [10, 15, 30, 20, 25],
}

# Days of the week weights
DAY_WEIGHTS = [18, 20, 17, 15, 12, 10, 8]

# HTTP methods and their weights
HTTP_METHODS = ["GET", "POST", "PUT", "DELETE"]
HTTP_METHOD_WEIGHTS = [60, 25, 10, 5]  # 60% GET, 25% POST, etc.

# Status codes and response sizes
STATUS_CODES = [200, 201, 301, 302, 400, 401, 403, 404, 500, 503]
RESPONSE_SIZES = range(100, 5000)

# Create output folder
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Function to dynamically calculate website weights
def get_website_weights(time_period):
    return BASE_WEIGHTS[time_period]

# Function to select a random time period based on weights
def get_time_period():
    time_periods = list(TIME_DEFINITIONS.keys())
    time_weights = [TIME_DEFINITIONS[period][2] for period in time_periods]
    return random.choices(time_periods, weights=time_weights, k=1)[0]

# Function to generate a log entry
def generate_log_entry():
    # Select a random day of the week and time
    day_of_week = random.choices(range(7), weights=DAY_WEIGHTS, k=1)[0]
    random_date = fake.date_this_year()
    random_date += timedelta(days=(day_of_week - random_date.weekday()) % 7)

    time_period = get_time_period()
    start_hour, end_hour, _ = TIME_DEFINITIONS[time_period]
    random_hour = random.randint(start_hour, end_hour - 1)
    random_minute = random.randint(0, 59)
    random_second = random.randint(0, 59)

    log_time = datetime.combine(random_date, datetime.min.time()) + timedelta(
        hours=random_hour, minutes=random_minute, seconds=random_second
    )

    ip_address = fake.ipv4()
    formatted_time = log_time.strftime("%d/%b/%Y:%H:%M:%S")
    method = random.choices(HTTP_METHODS, weights=HTTP_METHOD_WEIGHTS, k=1)[0]
    
    # Select a website based on dynamic weights
    website_weights = get_website_weights(time_period)
    website = random.choices(TOP_SITES, weights=website_weights, k=1)[0]

    status_code = random.choice(STATUS_CODES)
    response_size = random.choice(RESPONSE_SIZES)

    # Return the formatted log entry
    return (
        f"{ip_address} - - [{formatted_time}] "
        f'"{method} {website} HTTP/1.1" {status_code} {response_size}'
    )

# Generate and save log files
for i in range(FILE_COUNT):
    output_file = os.path.join(OUTPUT_FOLDER, f"apache_logs_file_{i + 1}.log")
    with open(output_file, "w") as f:
        log_entries = "\n".join(generate_log_entry() for _ in range(LINES_PER_FILE))
        f.write(log_entries + "\n")

print(f"Apache log files saved in the folder: {OUTPUT_FOLDER}")
