# collector.py collects data from pulse.c
import json, subprocess, time, sqlite3
from datetime import datetime

conn = sqlite3.connect("pulse.db")
conn.execute(
"""
    CREATE TABLE IF NOT EXISTS readings (
        id INTEGER PRIMARY KEY,
        timestamp TEXT,
        uptime_s REAL,
        mem_available_kb INTEGER,
        cpu_temp_c REAL
    )
""")
conn.commit()

try:
    while True: 
        result = subprocess.run(["./pulse"], capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)

        conn.execute(
            "INSERT INTO readings(timestamp,uptime_s, mem_available_kb, cpu_temp_c) VALUES ( ?, ?, ?, ?)",
            (datetime.now().isoformat(), data["uptime_s"], data["mem_available_kb"], data["cpu_temp_c"])
        )
        conn.commit()

        print(data)

        temp = data["cpu_temp_c"]
        if temp is not None and temp >= 70:
            print("WARNING: CPU Temp exceeding 70°C")

        time.sleep(10)

except KeyboardInterrupt:
    print("\nCollector Stopping")

finally:
    conn.close()