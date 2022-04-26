# Front-End-Work
NOTE: THIS MUST BE RUN ON WINDOWS OPERATING SYSTEMS ONLY

## Running the .exe
If you have no need to edit the progam and just use it as is, you can download the FinalBuild.zip file, unzip it, and run ServiceInfo.exe
See the section Simple Install for how to make it run automatically when you launch your computer

## Installation Instructions
Install Python if it is not already installed  
We recommend checking the box to add Python to the path during the install  
  
Run the following commands in the terminal:  
pip install pysftp  
pip install psutil  

Download the file frontend.pem from this IPRO's Google Drive
Download ServiceInfo.py from the frontend GitHub repository  
Create the directory where you wish to store the downloaded files (THEY MUST BE THE SAME DIRECTORY)  

### Manual Running  
If you don't want this process to start at launch, just run it from the terminal using  
"python ServiceInfo.py" in the directory where the program is located  

### Simple Install
Download and run the script startup.ps1 from the frontend GitHub  
Note that startup.ps1 must be run in the same folder as ServiceInfo.exe  
This will make the default behavior to launch ServiceInfo.exe when you log in to your computer
Alternatively you can set it to open the Python file by changing the file extension to .py in the startup.ps1 script

### Configurable Variables
If you wish to change the interval at which the script runs or remove all console print commands  
feel free to change that in the configurable variables section of ServiceInfo.py  

## Final Thoughts
If you have any issues with the installation or discover any bugs, don't hesitate to contact   
Edward or any of the other members of the frontend team on discord  
