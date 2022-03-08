### IMPORTS ###
import ctypes
import sys
import os
import psutil
import socket
import time
import pysftp
import datetime
from uuid import getnode as get_mac #import statment for getting mac adress
### END IMPORTS ###

def pull_malicious():
    pass

def upload_csv(sftp, fname):
    sftp.put(fname)

def init_sftp():
    try:
        foobar = pysftp.CnOpts()
        foobar.hostkeys = None
        sftp = pysftp.Connection('3.92.144.196', username='frontend', private_key='frontend.pem', cnopts=foobar)
        sftp.cwd('upload')   #Put path to directory here
        return sftp
    except:
        print('An error occurred trying to connect.')
        return None

# writes process data in an organized csv format
def dump_csv(pslst, fname):
    # BUG: IF FILE IS ALREADY OPEN THEN THIS FAILS
    try:
        f = open(fname, 'w')
        f.write('time, machine_id, ps_name, mempct, cpupct, memabs, numthreads, user, path, pid\n')
    except:
        print('could not dump to csv file\n fatal error\nexiting...') 
        sys.exit(0)
    
    for ps in pslst:
        f.write(ps + '\n')
    f.close()

def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()

def main():
    if not is_admin():
        # Re-run the program with admin rights
        print('I AM NOT AN ADMIN')
        print('ATTEMPTING TO RELAUNCH AS ADMIN')
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)
    else:
        print('LOGGED IN AS ADMIN')

    sleep_time = 30
    sys_mem = psutil.virtual_memory()[0] # gets total amount of system memory
    sftp = init_sftp() # initializes ftp connection
    failed_files = [] # creates a list for any files we fail to upload with ftp
    proc_dict = {} # maps processnames to a pid

    # TODO: EACH TIME THIS RUNS WE WANNA PULL BAD PROCESSES FROM THE AWS FTP SERVER
    # AND KILL THEM IF THEY'RE BAD
    # keep most recent copy of the bad processes on the machine
    while True:
        # collect data that is the same for each process
        timestamp = datetime.datetime.now()
        pslst = []
        machine_id = get_mac()

        # not being dumped
        cores = os.cpu_count()
        ### FEATURE: POSSIBLY ADD CORES AND CLOCK SPEED
        clock_speed = psutil.cpu_freq()

        # iterates through every process and collects various data about it
        for proc in psutil.process_iter():
            try:
                # collect process dependent data
                name = proc.name()
                mempct = proc.memory_percent()
                memabs = sys_mem * mempct / 100 / 10**6
                cpupct = proc.cpu_percent()
                numthd = proc.num_threads()

                ### NEEDS ADMIN PRIVILEGES
                usr = proc.username()

                # clean up username field
                usr = usr.replace("NT AUTHORITY\\", "", 1)  # removes "NT AUTHORITY" from the user field
                usr = usr.replace(socket.gethostname() + "\\", "", 1)  # removes hostname (device name) from before username. 

                pid = proc.pid
                ###

                proc_dict[name] = pid
                
                #### WONT WORK WITHOUT A PID, NEED TO ACCOUNT FOR THIS
                path = None
                if pid != 0: # pid 0 is a dummy process initiated by windows that causes errors
                    path = psutil.Process(pid).exe()
            
                    # BUG: IF USER NAMES MALWARE SVCHOST.EXE THIS WILL ALLOW MALWARE TO RUN
                    # ignores many of the windows processes, as we don't want to send those
                    # possibly other programs we want to whitelist in the future
                    if name != 'svchost.exe':
                        pslst.append(f'{timestamp},{machine_id},{name},{mempct},{cpupct},{memabs} MB,{numthd},{usr},{path},{pid}')
            except:
                print('ACCESS DENIED')
                
        # dump the csv
        fname = f"{datetime.datetime.now():%Y-%m-%d_h%Hm%Ms%Sa}" +str(machine_id) + '.csv'
        dump_csv(pslst, fname)

        # try and connect files to the sftp
        try:
            print('UPLOAD SUCCEEDED')
            upload_csv(sftp, fname)
            os.remove(fname) #removes a file.
            # if upload succeeds dump to server and delete the file
            for file in failed_files:
                upload_csv(sftp, file)
                os.remove(file)
        except:
            # if fails add the current file to a queue of files that we didn't upload
            print("UPLOAD FAILED")
            failed_files.append(fname)
        
        time.sleep(sleep_time) # Sleep for 30 seconds
        
if __name__ == '__main__':
    main()