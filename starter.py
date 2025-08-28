import random
import sqlite3
import datetime
import pandas as pd
import matplotlib.pyplot as plt

# --- Database Setup ---
conn = sqlite3.connect("wearable_data.db")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS health_data (
                    timestamp TEXT,
                    heart_rate INTEGER,
                    steps INTEGER,
                    calories INTEGER,
                    spo2 INTEGER,
                    sleep_hours REAL
                )''')
conn.commit()

# --- Simulate wearable data ---
def generate_data():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    heart_rate = random.randint(60, 120)   # bpm
    steps = random.randint(100, 200)       # per session
    calories = random.randint(50, 150)
    spo2 = random.randint(92, 100)         # %
    sleep_hours = round(random.uniform(5, 9), 1)  # hrs
    
    cursor.execute("INSERT INTO health_data VALUES (?, ?, ?, ?, ?, ?)",
                   (timestamp, heart_rate, steps, calories, spo2, sleep_hours))
    conn.commit()

# Generate sample data
for _ in range(10):   # simulate 10 records
    generate_data()

# --- Analysis ---
df = pd.read_sql_query("SELECT * FROM health_data", conn)
print(df.head())

print("\nAverage Heart Rate:", df["heart_rate"].mean())
print("Total Steps:", df["steps"].sum())
print("Average Sleep Hours:", df["sleep_hours"].mean())

# --- Visualization ---
plt.figure(figsize=(8,4))
plt.plot(df["timestamp"], df["heart_rate"], marker='o')
plt.xticks(rotation=45)
plt.title("Heart Rate Trend")
plt.ylabel("BPM")
plt.xlabel("Time")
plt.tight_layout()
plt.show()

conn.close()


