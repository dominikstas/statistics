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

# Format seconds to hours and minutes
def format_time(seconds):
    return f"{seconds // 3600}h {(seconds % 3600) // 60}m"

# Calculate work durations
def calculate_stats(stats):
    today = datetime.now().strftime("%Y-%m-%d")
    week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%m-%d")
    month_start = datetime.now().replace(day=1).strftime("%Y-%m-%d")
   
    total_today = stats.get(today, 0)
    total_week = sum(seconds for date, seconds in stats.items() if date >= week_start)
    total_month = sum(seconds for date, seconds in stats.items() if date >= month_start)
   
    return total_today, total_week, total_month

# Get last 7 days stats
def get_last_7_days_stats(stats):
    result = []
    today = datetime.now().date()
    
    for i in range(6, -1, -1):  # From 6 days ago to today
        day_date = today - timedelta(days=i)
        day_str = day_date.strftime("%Y-%m-%d")
        day_name = day_date.strftime("%A")  # Day name (Monday, Tuesday, etc.)
        seconds = stats.get(day_str, 0)
        result.append((day_str, day_name, seconds))
    
    return result

# Work timer function
def work_timer():
    stats = load_stats()
    today = datetime.now().strftime("%Y-%m-%d")
   
    print("\nStart pracy. Naciśnij ENTER, aby zakończyć.")
    start_time = time.time()
    input()
    end_time = time.time()
   
    elapsed_time = int(end_time - start_time)
    stats[today] = stats.get(today, 0) + elapsed_time
    save_stats(stats)
   
    total_today = stats.get(today, 0)
    print(f"\nDodano sesję: {format_time(elapsed_time)}")
    print(f"Dziś pracowałeś: {format_time(total_today)}")

# Show detailed statistics
def show_statistics():
    stats = load_stats()
    total_today, total_week, total_month = calculate_stats(stats)
    last_7_days = get_last_7_days_stats(stats)
    
    print("\n=== STATYSTYKI ===")
    print(f"Dziś pracowałeś: {format_time(total_today)}")
    
    print("\nOstatnie 7 dni:")
    for day_date, day_name, seconds in last_7_days:
        print(f"  {day_name} ({day_date}): {format_time(seconds)}")
    
    print(f"\nŁącznie w tym tygodniu: {format_time(total_week)}")
    print(f"Łącznie w tym miesiącu: {format_time(total_month)}")

# Main menu function
def main_menu():
    while True:
        stats = load_stats()
        today = datetime.now().strftime("%Y-%m-%d")
        total_today = stats.get(today, 0)
        
        print("\n=== MENU ===")
        print(f"Dziś pracowałeś: {format_time(total_today)}")
        print("\nWybierz opcję:")
        print("ENTER - Rozpocznij pomiar czasu pracy")
        print("S - Pokaż statystyki")
        print("Q - Wyjdź z programu")
        
        choice = input().lower()
        
        if choice == "":
            work_timer()
        elif choice == "s":
            show_statistics()
        elif choice == "q":
            print("Do widzenia!")
            break
        else:
            print("Nieznana opcja, spróbuj ponownie.")

if __name__ == "__main__":
    print("Siemano!")
    main_menu()