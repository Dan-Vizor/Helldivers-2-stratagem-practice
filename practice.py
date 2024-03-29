#!/usr/bin/python3
import os
import sys
import json
import time
import keyboard
import platform
import random
from termcolor import colored

def ConvertToArrow(direction):
    return DATA['arrows'][direction]

def AnyValidInput():
    return keyboard.is_pressed(SETTINGS['keybinds']['up']) or keyboard.is_pressed(SETTINGS['keybinds']['down']) or keyboard.is_pressed(SETTINGS['keybinds']['left']) or keyboard.is_pressed(SETTINGS['keybinds']['right'])

def UpdatePlayerData(stratagem:dict, CompletionTime=None, TimesPassed=None, TimesFailed=None):
    if stratagem['name'] == "random": return
    PlayerData = json.loads(open("PlayerData.json", "r").read())
    
    i = 0
    Found = False
    for each in PlayerData['stratagems']:
        if each['name'] == stratagem['name']:
            CurrentData = each
            Found = True
            break

    if not Found:
        CurrentData = {
            "name": stratagem['name'],
            "TimesPassed": 0,
            "TimesFailed": 0,
            "Times": []
        }

    if CompletionTime != None: CurrentData['Times'].append(CompletionTime)
    if TimesPassed != None: CurrentData['TimesPassed'] += 1
    if TimesFailed != None: CurrentData['TimesFailed'] += 1

    # add the modified date back to the file
    if Found: PlayerData['stratagems'][i] = CurrentData
    else: PlayerData['stratagems'].append(CurrentData)
    with open("PlayerData.json", "w") as f: f.write(json.dumps(PlayerData, indent=2))

def MakeCodeOutput(stratagem:dict, CodeIndex:int, JustArrows=False):
    if platform.system() == "Windows":
        if JustArrows: OutputText = f"{' '*(DATA['NamesSpacingsize'] - len(stratagem['name']))}"
        else: OutputText = f"{stratagem['name']}:{' '*(DATA['NamesSpacingsize'] - len(stratagem['name']))}"

    else:
        if JustArrows: OutputText = f"{' '*(DATA['NamesSpacingsize'] - len(stratagem['name']))}\033[1m["
        else: OutputText = f"{stratagem['name']}:{' '*(DATA['NamesSpacingsize'] - len(stratagem['name']))}\033[1m["

    i = 0
    for character in stratagem['code']:
        if i < CodeIndex: OutputText += colored(ConvertToArrow(character), "green")
        else: OutputText += ConvertToArrow(character)
        OutputText += " "

        i += 1

    if platform.system() != "Windows": OutputText += "]\033[0m"
    else: OutputText += "]"

    return OutputText

def main():
    if platform.system() == "Linux": os.system('clear')
    CommandArgs = sys.argv[1:]

    # print help menu and exit
    if "-h" in CommandArgs:
        print(open("help-text.txt", "r").read())
        raise SystemExit

    # identify which mode to use
    if "-r" in CommandArgs or "--random" in CommandArgs: mode = "random"
    elif "-s" in CommandArgs or "--single" in CommandArgs: mode = "single"
    elif "-rs" in CommandArgs or "--random-stratagem" in CommandArgs: mode = "random stratagem"
    elif "-c" in CommandArgs or "--clear" in CommandArgs:
        os.remove("PlayerData.json")
        print("player data has been reset")
        raise SystemExit
    else:
        print("no mode provided\n")
        print(open("help-text.txt", "r").read())
        raise SystemExit

    for i in range(SETTINGS['GameStartTimer']):
        print(f"starting in {SETTINGS['GameStartTimer'] - i} seconds.{'.'*i}", end="\r")
        time.sleep(1)

    # main loop
    CodeIndex = 0
    SelectNew = True
    while True:

        # load stratagem
        if SelectNew:
            StartTime = time.time()

            if mode == "random":
                stratagem = random.choice(DATA['stratagems'])

            elif mode == "single":
                found = False
                for each in DATA['stratagems']:
                    if CommandArgs[-1].lower() in each['name'].lower():
                        stratagem = each
                        found = True
                        break

                if not found:
                    print(f"Error: unknown stratagem name '{CommandArgs[-1]}'")

            elif mode == "random stratagem":
                stratagem = {"name": "random", "code": []}
                for i in range(random.randint(3, 8)):
                    stratagem['code'].append(random.choice(["up", "down", "left", "right"]))

            else:
                print(f"Error: invalid mode '{mode}' used")
                raise SystemExit

            SelectNew = False

        else:
            if CodeIndex >= len(stratagem['code']):
                print(f"{' '*TERMINALWIDTH}\r {colored(stratagem['name'], 'green')}:{MakeCodeOutput(stratagem, 0, JustArrows=True)}")
                UpdatePlayerData(stratagem, CompletionTime=TimeTaken, TimesPassed=1)

                # reset
                CodeIndex = 0
                SelectNew = True
                time.sleep(0.5)
                continue

        # calculate how long it's been
        TimeTaken = (time.time() - StartTime)

        # print code to user
        print(f"{' '*TERMINALWIDTH}\r {MakeCodeOutput(stratagem, CodeIndex)} {round(TimeTaken, 2)}", end="\r")

        # check if any keys are being pressed
        CorrectKey = SETTINGS['keybinds'][stratagem['code'][CodeIndex]]
        if AnyValidInput():
            if keyboard.is_pressed(CorrectKey):
                CodeIndex += 1

                # wait until key is released (will allow the next correct key to be pressed if setting is enabled)
                while AnyValidInput():
                    if CodeIndex < (len(stratagem['code']) -1) and SETTINGS['AllowMultipleInputs']:
                        if keyboard.is_pressed(SETTINGS['keybinds'][stratagem['code'][CodeIndex +1]]):
                            CodeIndex + 1

            else: 
                print(f"{' '*TERMINALWIDTH}\r {stratagem['name']}:{colored(MakeCodeOutput(stratagem, 0, JustArrows=True), 'red')}", end="\r")
                UpdatePlayerData(stratagem, TimesFailed=1)
                CodeIndex = 0
                time.sleep(0.5)

        else:
            continue

# load json files
try:
    SETTINGS = json.loads(open("settings.json", "r", encoding="utf-8").read())
    DATA = json.loads(open("data.json", "r", encoding="utf-8").read())
    TERMINALWIDTH = os.get_terminal_size().columns - 20

except Exception as e:
    print(f"Error: failed to load json files:\n{e}")
    raise SystemExit

if not os.path.exists("PlayerData.json"):
    with open("PlayerData.json", "w") as f: f.write(json.dumps({"stratagems": []}, indent=2))

try:
    main()

except KeyboardInterrupt:
    print("\n\nThank you for playing!\nTo see your stats run 'python3 stats.py'")