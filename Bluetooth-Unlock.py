#!/usr/bin/python
# imports python modules
import sys
import os
import shutil
from optparse import OptionParser
import subprocess
import time

#Detects python version
if (sys.version_info > (3, 0)):
    print("Python 3 has been detected you may continue")
else:
    sys.exit("Python 2 has been detected please run in python3!")


ENV = input("""Please Enter your Desktop Environment can be:
'LOGINCTL' (Recommended)
'KDE'
'GNOME'
'XSCREENSAVER' (You have to enter password!) 
""")
if ENV == "LOGINCTL":
 print("LOGINCTL has been selected")
elif ENV == "KDE":
 print("KDE has been selected")
elif ENV == "GNOME":
 print("GNOME has been selected")
elif ENV == "XSCREENSAVER":
 print("XSCREENSAVER has been selected")
else:
 sys.exit("Unidentified Environment exiting")
	
DEVICEADDR = input("Enter Bluetooth Adress of the device e.g AA:BB:CC:DD:EE:FF: ")#Asks for bluetooth device address

CHECKINTERVAL = 3  # device pinged at this interval (seconds) when screen is unlocked
CHECKREPEAT = 2  # device must be unreachable this many times to lock
mode = 'unlocked'

if __name__ == "__main__":
    while True:
        tries = 0
        while tries < CHECKREPEAT:
            process = subprocess.Popen(['sudo', '/usr/bin/l2ping', DEVICEADDR, '-t', '1', '-c', '1'], shell=False, stdout=subprocess.PIPE)
            process.wait()
            if process.returncode == 0:
                print("ping OK")
                break
            print("ping response code: %d" % (process.returncode))
            time.sleep(1)
            tries = tries + 1

        if process.returncode == 0 and mode == 'locked':
            mode = 'unlocked'
            if ENV == "LOGINCTL":
                subprocess.Popen(['loginctl', 'unlock-session'], shell=False, stdout=subprocess.PIPE)
            elif ENV == "KDE":
                subprocess.Popen(['loginctl', 'unlock-session'], shell=False, stdout=subprocess.PIPE)
            elif ENV == "GNOME":
                subprocess.Popen(['gnome-screensaver-command', '--deactivate'], shell=False, stdout=subprocess.PIPE)
            elif ENV == "XSCREENSAVER":
                subprocess.Popen(['xscreensaver-command', '-deactivate'], shell=False, stdout=subprocess.PIPE)

        if process.returncode == 1 and mode == 'unlocked':
            mode = 'locked'
            if ENV == "LOGINCTL":
                subprocess.Popen(['loginctl', 'lock-session'], shell=False, stdout=subprocess.PIPE) 
            elif ENV == "KDE":
                subprocess.Popen(['loginctl', 'lock-session'], shell=False, stdout=subprocess.PIPE)
            elif ENV == "GNOME":
                subprocess.Popen(['gnome-screensaver-command', '--lock'], shell=False, stdout=subprocess.PIPE)
            elif ENV == "XSCREENSAVER":
                subprocess.Popen(['xscreensaver-command', '-lock'], shell=False, stdout=subprocess.PIPE)
            
        if mode == 'locked':
            time.sleep(1)
        else:
            time.sleep(CHECKINTERVAL)
