#!/usr/bin/python3
import os
import time
import json
import requests
from termcolor import colored
from datetime import datetime
from pprint import pprint

ReloadInterval = 60
APIQueryReattempts = 10

while True:
    print("loading data...")

    I = 0
    while True:
        if I > APIQueryReattempts: raise SystemExit

        # load data from API
        try:
            resp = requests.get("https://helldivers.io/refresh")        

        except Exception as e:
            print(e)
            I += 1
            time.sleep(1)
            continue
        
        # parse out json data
        try:
            data = json.loads(resp.text)

        except Exception as e:
            print(f"{e}\n{resp.text}")
            I += 1
            time.sleep(1)
            continue
        
        break

    os.system("clear")

    planets = sorted(data['mn'], key=lambda x: x['p'], reverse=True)
    print("Planet | Liberation | Players | Completion ETA")
    for planet in planets:
        PlanetName = planet['n']
        Liberation = round(planet['l'], 3)
        LiberationDelta = round(planet['r'], 3)
        PlayerCount = planet['p']
        ETA = planet['ct']

        if planet['c'] == -1: continue

        if PlayerCount > 60000: PlayerCount = colored("{:,}".format(PlayerCount), "green")
        elif PlayerCount < 60000 and PlayerCount > 20000: PlayerCount = colored("{:,}".format(PlayerCount), "yellow")
        else: PlayerCount = colored("{:,}".format(PlayerCount), "red")

        if ETA == 0: ETA = colored("LOSING", "red")
        else: ETA = colored(datetime.fromtimestamp(int(ETA) / 1000).strftime('%d/%m %H:%M'), "green")

        if Liberation > 70: Liberation = colored(str(Liberation), "green")
        elif Liberation < 70 and Liberation > 40: Liberation = colored(str(Liberation), "yellow")
        else: Liberation = colored(str(Liberation), "red")

        if LiberationDelta > 0: LiberationDelta = colored(f"+{LiberationDelta}", "green")
        elif LiberationDelta < 0: LiberationDelta = colored(str(LiberationDelta), "red")
        else: LiberationDelta = colored("stalled", "yellow")

        print(f"{PlanetName} | {Liberation}% ({LiberationDelta}) | {PlayerCount} | {ETA}")

    if (time.time() - (data['lastUpdate'] / 1000)) < 120:
        print(f"\ndata accurate as of {datetime.fromtimestamp(data['lastUpdate'] / 1000).strftime('%H:%M:%S')}")
    
    else:
        print(f"\ndata accurate as of {colored(datetime.fromtimestamp(data['lastUpdate'] / 1000).strftime('%H:%M:%S'), 'red')}")

    for I in range(ReloadInterval):
        print(f"{' '*80}\rreload in {ReloadInterval - (I +1)}s", end="\r")
        time.sleep(1)
