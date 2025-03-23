import subprocess
import time
import csv
from datetime import datetime
import re


def run_fan_command():
    res = subprocess.run(
        "ipmitool -I lanplus -H 192.168.1.104 -P 12345678 -U user -A PASSWORD sdr type fan",
        shell=True,
        text=True,
        capture_output=True,
    )
    out = res.stdout.split("\n")
    pattern = r"(\d+\.\d+)\spercent"

    def get_speed(s: str):
        match = re.search(pattern, s)
        if match:
            return match.group(1)
        return "0.0"

    result = []
    for i in range(0, len(out) - 2, 3):
        result.append(get_speed(out[i]))

    return result


def run_temp_command():
    res = subprocess.run(
        "ipmitool -I lanplus -H 192.168.1.104 -P 12345678 -U user -A PASSWORD sdr type Temperature",
        shell=True,
        text=True,
        capture_output=True,
    )
    out = res.stdout.split("\n")
    pattern = r"(\d+)\sdegrees"

    def get_temp(s: str):
        match = re.search(pattern, s)
        if match:
            return match.group(1)
        return "20"

    result = []
    for s in out:
        result.append(get_temp(s))

    return result


with open("fans.csv", mode="a", newline="") as fans:
    with open("temps.csv", mode="a", newline="") as temps:
        fans_writer = csv.writer(fans)
        temps_writer = csv.writer(temps)

        fans_writer.writerow(["timestamp"] + [f"fan#{i}" for i in range(1, 8)])
        temps_writer.writerow(["timestamp"] + [f"dev#{i:02}" for i in range(1, 38)])

        while True:
            timestamp = datetime.now().strftime("%H:%M:%S")
            output_fan = run_fan_command()
            output_temp = run_temp_command()

            print(f"timestamp: {timestamp}")
            print(f"fans: {output_fan}")
            print(f"temp: {output_temp}")

            fans_writer.writerow([timestamp] + output_fan)
            temps_writer.writerow([timestamp] + output_temp)
            time.sleep(60)
