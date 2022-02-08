### IMPORTS ###
import psutil
import mysql.connector
import time
import datetime
from uuid import getnode as get_mac #import statment for getting mac adress
### END IMPORTS ###

def macaddr():
    # figure out what to take from this to get mac addr
    sub_dict = {'Name': [],'Memory Percent': [], 'Mac': []}

    while True:
        print(datetime.datetime.now())
        for proc in psutil.process_iter():
            try:
                pr = proc.as_dict()
                mac = get_mac() #command to get mac address
                print(f'{pr["name"]}\t{pr["memory_percent"]}\t{"mac"}')
            except (OSError, psutil.AccessDenied):
                print(pr.name(), 'ACCESS DENIED')
        print('\n*** Ctrl-C to Exit ***\n\n')
        time.sleep(30) # Sleep for 10 Mins

def dump_csv(pslst, fname):
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
        
        # iterates through every process
        for proc in psutil.process_iter():
            try:
                name = proc.name()
                machine_id = get_mac()
                mempct = proc.memory_percent()
                memabs = sys_mem * mempct
                cpupct = proc.cpu_percent()
                numthd = proc.num_threads()
                
                ### NEEDS ADMIN PRIVILEGES
                usr = proc.username()
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
                        pslst.append(f'{timestamp},{machine_id},{name},{mempct},{cpupct},{memabs},{numthd},{usr},{path},{pid}')
            except (OSError, psutil.AccessDenied):
                print(proc.name(), 'ACCESS DENIED')
                
        dump_csv(pslst, 'foo.csv')
        print('\n*** Ctrl-C to Exit ***\n\n')
        time.sleep(1) # Sleep for 1 second
        
if __name__ == '__main__':
    main()