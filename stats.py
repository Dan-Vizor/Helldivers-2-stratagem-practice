#!/usr/bin/python3
import os
import json
import platform
from termcolor import colored

def CalculateMean(numbers:list, RoundTo=3):
    if numbers == []: return 0
    return round(sum(numbers) / len(numbers), RoundTo)

def CalculateRatio(num1, num2, RoundTo=3):
    if num1 == 0 or num2 == 0: return 0
    return round(num1 / num2, RoundTo)

def BarChart(ChartName:str, data:list):
    data = sorted(data, key=lambda x: x['value'], reverse=True)
    max_value = max(entry['value'] for entry in data)
    scale_factor = 50 / max_value  # Adjust the scale to fit within 50 characters

    print(f"\033[1m{ChartName}:\033[0m")
    for entry in data:
        if entry['value'] == 0: continue

        bar_length = int(entry['value'] * scale_factor)
        # Calculate the spacing to make sure bars start at the same position
        spacing = " " * (max(len(entry['name']) for entry in data) - len(entry['name']))
        print(f"{entry['name']}{spacing} | {'█' * bar_length} {entry['value']}")

# load player data
if not os.path.exists("PlayerData.json"):
    print("Error: no player data found")
    raise SystemExit

PlayerData = json.loads(open("PlayerData.json", "r").read())

if platform.system() == "Linux": os.system("clear")
BarChart(
    "Mean time taken (in seconds)",
    [{"name": entry['name'], "value": CalculateMean(entry['Times'])} for entry in PlayerData['stratagems']]
)
print("\n")
BarChart(
    "Successful Inputs",
    [{"name": entry['name'], "value": entry['TimesPassed']} for entry in PlayerData['stratagems']]
)
print("\n")
BarChart(
    "Failed Inputs",
    [{"name": entry['name'], "value": entry['TimesFailed']} for entry in PlayerData['stratagems']]
)
print("\n")
BarChart(
    "Success to Failure Ratio",
    [{"name": entry['name'], "value": CalculateRatio(entry['TimesFailed'], entry['TimesPassed'])} for entry in PlayerData['stratagems']]
)

print("\nto reset these stats please run 'sudo python3 practice.py --clear'")