# collector.py collects data from pulse.c
import json, subprocess, time

while True : 
    result = subprocess.run(["./pulse"], capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)
    print(data)

    temp = data["cpu_temp_c"]
    if temp is not None and temp >= 70:
        print("WARNING: CPU Temp exceeding 70°C")

    time.sleep(10)

