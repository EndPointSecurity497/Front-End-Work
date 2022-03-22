# This script assumes that the other script's name is "ServiceInfo.py" and that the other script is in the same folder as this file.
import os
from win32com.client import Dispatch

username = os.getlogin()  # the current username is required to get to the startup path
startupPath = "C:/Users/" + username + "/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"  # Gets the path to Windows' startup folder. This script works by adding ServiceInfo.py to the Startup folder.
mainScript = os.path.dirname(__file__) + "/ServiceInfo.py"  # path to ServiceInfo.py
shortcutPath = os.path.join(startupPath, "ServiceInfo.lnk")

shell = Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut(shortcutPath)
shortcut.Targetpath = mainScript
# shortcut.IconLocation = icon  # not needed, but if we want an icon, here is where we need to set the link to it
shortcut.save()

# file = open(startupPath + '/' + os.path.basename(mainScript), 'w')  # open the file in the startup folder, creating it if it doesn't exist.
# shutil.copyfile(mainScript, startupPath + '/' + os.path.basename(mainScript))  # copies ServiceInfo.py to the startup folder
# file.close()  # close the file in the startup folder
print("FILE ADDED TO STARTUP FOLDER")