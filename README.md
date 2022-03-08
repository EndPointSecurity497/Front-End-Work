# Front-End-Work
NOTE: THIS MUST BE RUN ON WINDOWS OPERATING SYSTEMS ONLY

## Installation Instructions
Install Python if it is not already installed  
We recommend checking the box to add python to the path during the install  
  
Run the following commands in the terminal:  
pip install pysftp  
pip install psutil  

Download the file frontend.pem from the frontend channel in the IPRO discord  
Download ServiceInfo.py from the frontend GitHub repository  
Create the directory where you wish to store the downloaded files (THEY MUST BE THE SAME DIRECTORY)  

### Manual Running  
If you don't want this process to start at launch, just run it from the terminal using  
"python ServiceInfo.py" in the directory where the program is located  

### Advanced Users
If you are familiar with the Windows Task Scheduler, feel free to   
register ServiceInfo.py as an admin process to boot at launch.  
We currently lack knowledge on how exactly to do this, but if you  
have trouble ask the professor, as he was playing around with it.  
If you complete this step ignore the Simple Install instructions  

### Simple Install
Download and run the script startup.py from the frontend GitHub  
Note that startup.py must be run in the same folder as ServiceInfo.py  
Make sure that the default behavior for opening Python files is to run them  

### Configurable Variables
If you wish to change the interval at which the script runs or remove all console print commands  
feel free to change that in the configurable variables section of ServiceInfo.py  

## Final Thoughts
If you have any issues with the installation or discover any bugs, don't hesitate to contact   
Edward or any of the other members of the frontend team on discord  
