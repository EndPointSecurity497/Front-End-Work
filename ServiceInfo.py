### IMPORTS ###
import psutil
import socket
import time
import datetime
from uuid import getnode as get_mac #import statment for getting mac adress
### END IMPORTS ###

def dump_csv(pslst, fname):
    # BUG: IF FILE IS ALREADY OPEN THEN THIS FAILS
    f = open(fname, 'w')
    f.write('time, machine_id, ps_name, mempct, cpupct, memabs, numthreads, user, path, pid\n')
    
    for ps in pslst:
        f.write(ps + '\n')
    f.close()

def main():
    sys_mem = psutil.virtual_memory()[0]

    while True:
        timestamp = datetime.datetime.now()
        pslst = []
        machine_id = get_mac()

        # iterates through every process
        for proc in psutil.process_iter():
            try:
                name = proc.name()
                mempct = proc.memory_percent()
                memabs = sys_mem * mempct / 100 / 10**6
                cpupct = proc.cpu_percent()
                numthd = proc.num_threads()
                
                ### NEEDS ADMIN PRIVILEGES
                usr = proc.username()
                
                usr = usr.replace("NT AUTHORITY\\", "", 1)  # removes "NT AUTHORITY" from the user field
                usr = usr.replace(socket.gethostname() + "\\", "", 1)  # removes hostname (device name) from before username. 

                pid = proc.pid
                ###
                
                #### WONT WORK WITHOUT A PID, NEED TO ACCOUNT FOR THIS
                path = None
                if pid != 0:
                    path = psutil.Process(pid).exe()
            
                    # BUG: IF USER NAMES MALWARE SVCHOST.EXE THIS WILL ALLOW MALWARE TO RUN
                    # ignores many of the windows processes, as we don't want to send those
                    # possibly other programs we want to whitelist in the future
                    if name != 'svchost.exe':
                        pslst.append(f'{timestamp},{machine_id},{name},{mempct},{cpupct},{memabs} MB,{numthd},{usr},{path},{pid}')
            except (OSError, psutil.AccessDenied):
                print(proc.name(), 'ACCESS DENIED')
                
        dump_csv(pslst, f"{datetime.datetime.now():%Y-%m-%d_h%Hm%Ms%Sa}"+str(machine_id) + '.csv')
        print('\n*** Ctrl-C to Exit ***\n\n')
        time.sleep(1) # Sleep for 1 second
        
if __name__ == '__main__':
    main()