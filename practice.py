#!/usr/bin/python3
import os
import sys
import json
import time
import keyboard
import random
from termcolor import colored

def ConvertToArrow(direction):
    return DATA['arrows'][direction]

def AnyValidInput():
    return keyboard.is_pressed(SETTINGS['keybinds']['up']) or keyboard.is_pressed(SETTINGS['keybinds']['down']) or keyboard.is_pressed(SETTINGS['keybinds']['left']) or keyboard.is_pressed(SETTINGS['keybinds']['right'])

def MakeCodeOutput(stratagem:dict, CodeIndex:int, JustArrows=False):
    if JustArrows: OutputText = f"\033[1m"
    else: OutputText = f"{stratagem['name']}: \033[1m"

    i = 0
    for character in stratagem['code']:
        if i < CodeIndex: OutputText += colored(ConvertToArrow(character), "green")
        else: OutputText += ConvertToArrow(character)
        OutputText += " "

        i += 1

    OutputText += "\033[0m"
    return OutputText

os.system('clear')
CommandArgs = sys.argv[1:]

# print help menu and exit
if "-h" in CommandArgs:
    print(open("help-text.txt", "r").read())
    raise SystemExit

# load json files
try:
    SETTINGS = json.loads(open("settings.json", "r").read())
    DATA = json.loads(open("data.json", "r").read())

except Exception as e:
    print(f"Error: failed to load json files:\n{e}")
    raise SystemExit

# identify which mode to use
if "-r" in CommandArgs or "--random" in CommandArgs: mode = "random"
elif "-s" in CommandArgs or "--single" in CommandArgs: mode = "single"
else:
    print("no mode provided\n")
    print(open("help-text.txt", "r").read())
    raise SystemExit

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
                if each['name'] == CommandArgs[-1]:
                    stratagem = each
                    found = True
                    break

            if not found:
                print(f"Error: unknown stratagem name '{CommandArgs[-1]}'")

        SelectNew = False

    else:
        if CodeIndex == len(stratagem['code']):
            print(f"{' '*100}\r {colored(stratagem['name'], 'green')}: {MakeCodeOutput(stratagem, 0, JustArrows=True)}")
            
            # reset
            CodeIndex = 0
            SelectNew = True
            time.sleep(1)
            continue

    # fail if time is up
    TimeRemaining = SETTINGS['timer'] - (time.time() - StartTime)
    if TimeRemaining <= 0:
        print(f"{' '*100}\r {colored(stratagem['name'], 'red')}: {MakeCodeOutput(stratagem, 0, JustArrows=True)}")
            
        # reset
        CodeIndex = 0
        SelectNew = True
        time.sleep(1)
        continue

    # print code to user
    print(f"{' '*100}\r {MakeCodeOutput(stratagem, CodeIndex)} {round(TimeRemaining, 2)}", end="\r")

    # check if any keys are being pressed
    CorrectKey = SETTINGS['keybinds'][stratagem['code'][CodeIndex]]
    if AnyValidInput():
        if keyboard.is_pressed(CorrectKey): CodeIndex += 1
        else: CodeIndex = 0

        # wait until key is released
        while AnyValidInput(): pass

    else:
        continue

print()