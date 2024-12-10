#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings

# Suppress FutureWarnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Branding colors for websites
branding_colors = {
    "https://www.facebook.com": "#1877F2",  # Facebook blue
    "https://www.youtube.com": "#FF0000",  # YouTube red
    "https://www.x.com": "#000000",        # X black
    "https://www.instagram.com": "#E1306C",  # Instagram pink
    "https://www.tiktok.com": "#25F4EE",   # TikTok cyan
}

# Create an output folder for images
output_folder = "visualizations"
os.makedirs(output_folder, exist_ok=True)

try:
    # Load the CSV file into a DataFrame
    data = pd.read_csv("final_output.csv")

    # Ensure required columns exist
    required_columns = {"DayOfWeek", "TimePeriod", "Count", "Website"}
    if not required_columns.issubset(data.columns):
        raise ValueError(f"CSV file must contain columns: {required_columns}")

    # Convert Count to numeric
    data["Count"] = pd.to_numeric(data["Count"], errors="coerce")

    # Drop rows with missing values
    data.dropna(subset=["DayOfWeek", "TimePeriod", "Count", "Website"], inplace=True)

    # Define custom sorting orders
    day_order = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    time_period_order = ["night", "morning", "afternoon", "evening"]

    # Convert columns to categorical with custom sorting
    data["DayOfWeek"] = pd.Categorical(data["DayOfWeek"], categories=day_order, ordered=True)
    data["TimePeriod"] = pd.Categorical(data["TimePeriod"], categories=time_period_order, ordered=True)

    # 1. Heatmap
    def create_heatmap(data):
        # Pivot the data for the heatmap
        heatmap_data = data.pivot_table(index="DayOfWeek", columns="TimePeriod", values="Count", aggfunc="sum")

        # Plot the heatmap
        plt.figure(figsize=(10, 6))
        sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="Blues")
        plt.title("Activity Heatmap by Day and Time Period")
        plt.xlabel("Time Period")
        plt.ylabel("Day of Week")
        heatmap_path = os.path.join(output_folder, "heatmap.png")
        plt.savefig(heatmap_path, dpi=300)
        plt.close()
        print(f"Heatmap saved to {heatmap_path}")

    # 2. Time Series Line Chart with Branding Colors
    def create_time_series_chart(data):
        # Combine DayOfWeek and TimePeriod into a single "TimeLabel" with custom sorting
        data["TimeLabel"] = (
            data["DayOfWeek"].astype(str) + " " + data["TimePeriod"].astype(str)
        )
        
        # Group data by the custom "TimeLabel" and Website
        trend_data = data.groupby(["TimeLabel", "Website"])["Count"].sum().reset_index()
        
        # Retain the correct order of TimeLabel by re-merging the sorted original data
        unique_times = (
            data[["DayOfWeek", "TimePeriod", "TimeLabel"]]
            .drop_duplicates()
            .sort_values(by=["DayOfWeek", "TimePeriod"])
        )
        
        # Map TimeLabel to the desired order
        time_order = unique_times["TimeLabel"].tolist()
        trend_data["TimeLabel"] = pd.Categorical(trend_data["TimeLabel"], categories=time_order, ordered=True)

        # Pivot data for plotting
        pivot_data = trend_data.pivot(index="TimeLabel", columns="Website", values="Count")

        # Plot the line chart with branding colors
        plt.figure(figsize=(12, 6))
        for column in pivot_data.columns:
            plt.plot(
                pivot_data.index, 
                pivot_data[column], 
                label=column, 
                marker="o", 
                color=branding_colors.get(column)
            )

        plt.title("Time Series Activity Trends")
        plt.xlabel("Time (Ordered)")
        plt.ylabel("Count")
        plt.xticks(rotation=90)
        plt.legend(title="Website")
        plt.tight_layout()
        line_chart_path = os.path.join(output_folder, "time_series_chart.png")
        plt.savefig(line_chart_path, dpi=300)
        plt.close()
        print(f"Time Series Line Chart saved to {line_chart_path}")

    # Generate visualizations
    create_heatmap(data)
    create_time_series_chart(data)

    print(f"All visualizations saved to the folder: {output_folder}")

except Exception as e:
    print(f"An error occurred: {e}")
