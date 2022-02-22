# This script assumes that the other script's name is "main.py" and that the other script is in the same folder as this file.
import os
import shutil

username = os.getlogin()
startupPath = "C:/Users/" + username + "/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
mainScript = os.path.dirname(__file__) + "/main.py"

file = open(startupPath + '/' + os.path.basename(mainScript), 'w')
shutil.copyfile(mainScript, startupPath + '/' + os.path.basename(mainScript))
file.close()
print("FILE ADDED TO STARTUP FOLDER")
