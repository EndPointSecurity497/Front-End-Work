### IMPORTS ###
import psutil
import mysql.connector
import time
import datetime
### END IMPORTS ###

def dump_csv(pslst, fname):
    f = open(fname, 'w')
    f.write('time, machine_id, ps_name, mempct, cpupct, memabs, numthreads, user, path, pid\n')
    
    for ps in pslst:
        f.write(ps + '\n')

def main():
    while True:
        # WE WANT TO FILTER THIS POSSIBLY AND FORMAT IT DIFFERENTLY
        timestamp = datetime.datetime.now()
        pslst = []
        # iterates through every process
        for proc in psutil.process_iter():
            try:
                name = proc.name()
                machine_id = None
                mempct = proc.memory_percent()
                memabs = None
                cpupct = proc.cpu_percent()
                numthd = proc.num_threads()
                
                ### NEEDS ADMIN PRIVILEGES
                usr = proc.username()
                pid = proc.pid
                ###
                
                path = None
                if pid != 0:
                    path = psutil.Process(pid).exe()
            
                # ignores many of the windows processes, as we don't want to send those
                # possibly other programs we want to whitelist in the future
                if name != 'svchost.exe':
                    pslst.append(f'{timestamp},{machine_id},{name},{mempct},{memabs},{numthd},{usr},{path},{pid}')
            except (OSError, psutil.AccessDenied):
                print(proc.name(), 'ACCESS DENIED')
                
        dump_csv(pslst, 'foo.txt')
        print('\n*** Ctrl-C to Exit ***\n\n')
        time.sleep(1) # Sleep for 1 second
        
if __name__ == '__main__':
    main()