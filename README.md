# Helldivers 2 Stratagem Practice
"Ok, listen up Helldivers! While you're all in cryo we'll plug you into this practice program to help you master your stratagems. I expect you all to be masters of calling in Hellbombs once we thaw you out!" - General Brasch

*Notice: failure to achieve at least 80% accuracy will result in you being ejected from the Super Destroyer.*

![stratagem image](https://github.com/Dan-Vizor/helldivers-stratagem-practice/blob/master/Stratagems.png)

## Installation
### Linux
```console
# clone the repo
$ git clone https://github.com/Dan-Vizor/Helldivers-2-stratagem-practice.git

# change the working directory to stratagem practice
$ cd helldivers-stratagem-practice

# install the requirements
$ sudo python3 -m pip install -r requirements.txt
```

### Windows
Install WSL (Windows Subsystem for Linux) using [this guide](https://learn.microsoft.com/en-us/windows/wsl/install), Now Reboot. There will then be an app called 'Ubuntu', open it and then follow the Linux install steps inside WSL.

### MacOS
Follow [this guide](https://macpaw.com/how-to/install-python-mac) to install Python and then follow the Linux install steps.

## Usage
```console
# random mode
sudo python3 practice.py -r

# single stratagem mode
sudo python3 practice.py -s "Hellbomb"

# reset stats
sudo python3 practice.py -c

# display stats
python3 stats.py
```
This program uses the default PC keybinds for stratagems. You can set alternate keybinds by editing the **settings.json** file.

To exit the game press CTRL+C

## Note
Currently requires root access to run due to using the 'keyboard' Python module. Will be fixed in a future update.
