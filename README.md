# Helldivers 2 Stratagem Practice
"Ok, listen up Helldivers! While you're all in cryo we'll plug you into this practice program to help you master your stratagems. I expect you all to be masters of calling in Hellbombs once we thaw you out!" - General Brasch

*Notice: failure to achieve at least 80% accuracy will result in you being ejected from the Super Destroyer.*

![stratagem image](https://github.com/Dan-Vizor/helldivers-stratagem-practice/blob/master/images/Stratagems.png)

## Installation
### Linux
```console
# clone the repo
git clone https://github.com/Dan-Vizor/Helldivers-2-stratagem-practice.git
cd Helldivers-2-stratagem-practice

# install the requirements
sudo apt update && sudo apt upgrade
sudo apt install python3-pip
sudo pip3 install -r requirements.txt
```

### Windows
Install python from [here](https://www.microsoft.com/store/productId/9NRWMJP3717K?ocid=pdpshare) as well as git from [here](https://git-scm.com/download/win). Then open windows command line (press start and type 'cmd') and run the following commands
```console
cd path\to\where\you\want\to\download\to
git clone https://github.com/Dan-Vizor/Helldivers-2-stratagem-practice.git
cd Helldivers-2-stratagem-practice
pip install -r requirements.txt
```

## Usage
### Linux
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

### Windows
Open File Explorer and navagate to where you downloaded this repo. Then open CMD like shown below. 
![open CMD example image](https://github.com/Dan-Vizor/helldivers-stratagem-practice/blob/master/images/OpenCMD.png)


```console
# random mode
python practice.py -r

# single stratagem mode
python practice.py -s "Hellbomb"

# reset stats
python practice.py -c

# display stats
python stats.py
```

This program uses the default PC keybinds for stratagems. You can set alternate keybinds by editing the **settings.json** file.

To exit the game press CTRL+C

## Note
Currently requires root access on Linux to run due to using the 'keyboard' Python module. Will be fixed in a future update.
