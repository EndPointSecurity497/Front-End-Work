### IMPORTS ###
import psutil
import mysql.connector
import time
import datetime
### END IMPORTS ###

while True:
    # WE WANT TO FILTER THIS POSSIBLY AND FORMAT IT DIFFERENTLY
    print(datetime.datetime.now())
    # iterates through every process
    for proc in psutil.process_iter():
        try:
            pr = proc.as_dict()
            # ignores many of the windows processes, as we don't want to send those
            # possibly other programs we want to whitelist in the future
            if pr["name"] != 'svchost.exe':
                print(f'{pr["name"]}\t{pr["cpu_percent"]}\t{pr["memory_percent"]}\t{pr["num_threads"]}\t{pr["username"]}\t{pr["pid"]}')
        except (OSError, psutil.AccessDenied):
            print(pr.name(), 'ACCESS DENIED')
    print('\n*** Ctrl-C to Exit ***\n\n')
    time.sleep(1) # Sleep for 1 second
