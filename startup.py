# This script assumes that the other script's name is "ServiceInfo.py" and that the other script is in the same folder as this file.
import os
import shutil

# the current username is required to get to the startup path
username = os.getlogin()  
# Gets the path to Windows' startup folder. This script works by adding ServiceInfo.py to the Startup folder.
startupPath = "C:/Users/" + username + "/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"  
# path to ServiceInfo.py
mainScript = os.path.dirname(__file__) + "/ServiceInfo.py"  

# open the file in the startup folder, creating it if it doesn't exist.
file = open(startupPath + '/' + os.path.basename(mainScript), 'w')  
# copies ServiceInfo.py to the startup folder
shutil.copyfile(mainScript, startupPath + '/' + os.path.basename(mainScript))  
# close the file in the startup folder
file.close()  

print("FILE ADDED TO STARTUP FOLDER")

