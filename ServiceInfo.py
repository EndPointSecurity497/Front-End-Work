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
    
#TODO: NEED TO ACTUALLY USE IN THE MAIN LOOP WHERE WE GET ALL THE STUFF    
def gets_path():
    currentPIDs=psutil.pids()
    currentPIDs.remove(0)
    print(currentPIDs)
    for proc in currentPIDs:
        try:
            print(psutil.Process(proc).exe())

        except:
            print('undeterminable path')

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
                usr = None #proc.username()
                
                pid = None #proc.pid
                #print('test')
                path = None
            
                # ignores many of the windows processes, as we don't want to send those
                # possibly other programs we want to whitelist in the future
                if name != 'svchost.exe':
                    pslst.append(f'{timestamp},{machine_id},{name},{mempct},{memabs},{numthd}, {usr}, {path}, {pid}')
            except (OSError, psutil.AccessDenied):
                print(proc.name(), 'ACCESS DENIED')
                
        dump_csv(pslst, 'foo.txt')
        print('\n*** Ctrl-C to Exit ***\n\n')
        time.sleep(1) # Sleep for 1 second
        
if __name__ == '__main__':
    main()