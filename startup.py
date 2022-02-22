# This script assumes that the other script's name is "ServiceInfo.py" and that the other script is in the same folder as this file.
import os
import shutil

username = os.getlogin()  # the current username is required to get to the startup path
startupPath = "C:/Users/" + username + "/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"  # Gets the path to Windows' startup folder. This script works by adding ServiceInfo.py to the Startup folder.
mainScript = os.path.dirname(__file__) + "/ServiceInfo.py"  # path to ServiceInfo.py

file = open(startupPath + '/' + os.path.basename(mainScript), 'w')  # open the file in the startup folder, creating it if it doesn't exist.
shutil.copyfile(mainScript, startupPath + '/' + os.path.basename(mainScript))  # copies ServiceInfo.py to the startup folder
file.close()  # close the file in the startup folder
print("FILE ADDED TO STARTUP FOLDER")

