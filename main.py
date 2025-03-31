import time
import csv
import os
from datetime import datetime, timedelta

DATA_FILE = "work_stats.csv"

# Load existing stats or initialize
def load_stats():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, newline='') as file:
        reader = csv.DictReader(file)
        stats = {row['date']: int(row['seconds']) for row in reader}
    return stats

# Save stats to file
def save_stats(stats):
    with open(DATA_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["date", "seconds"])
        for date, seconds in stats.items():
            writer.writerow([date, seconds])

# Calculate work durations
def calculate_stats(stats):
    today = datetime.now().strftime("%Y-%m-%d")
    week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%m-%d")
    month_start = datetime.now().replace(day=1).strftime("%Y-%m-%d")
    
    total_today = stats.get(today, 0)
    total_week = sum(seconds for date, seconds in stats.items() if date >= week_start)
    total_month = sum(seconds for date, seconds in stats.items() if date >= month_start)
    
    return total_today, total_week, total_month

# Work timer function
def work_timer():
    stats = load_stats()
    today = datetime.now().strftime("%Y-%m-%d")
    
    print("Start pracy. Naciśnij ENTER, aby zakończyć.")
    start_time = time.time()
    input()
    end_time = time.time()
    
    elapsed_time = int(end_time - start_time)
    stats[today] = stats.get(today, 0) + elapsed_time
    save_stats(stats)
    
    total_today, total_week, total_month = calculate_stats(stats)
    print(f"Dziś pracowałeś: {total_today // 3600}h {(total_today % 3600) // 60}m")
    print(f"W tym tygodniu: {total_week // 3600}h {(total_week % 3600) // 60}m")
    print(f"W tym miesiącu: {total_month // 3600}h {(total_month % 3600) // 60}m")

if __name__ == "__main__":
    work_timer()
