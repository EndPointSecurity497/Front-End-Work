### IMPORTS ###
import ctypes
import sys
import os
import psutil
import socket
import time
import pysftp
import warnings
import datetime
from uuid import getnode as get_mac

### CONFIGURABLE VARIABLES ###
sleep_time = 10                 # sets interval between data collections
debug = True                    # if set, prints to console
pull = True                    # if set, attempts to pull malicious process file from AWS
keep = True                    # if set, does not delete files after uploading
ftp_key = 'frontend.pem'        # sets the path to the ftp key
ip_addr = '3.92.144.196'        # sets the ip address of the ftp server
usr = 'frontend'                # sets the username to login to the ftp server

# pull file with malicious processes from the FTP server
def pull_malicious(sftp, fname):
    try:
        sftp.get(fname)
        if debug:
            print("Malicious processes retrieved")
    except:
        if debug:
            print("Could not retrieve malicious processes file")

# uploads given file to the SFTP server to the current working directory
def upload_csv(sftp, fname):
    sftp.put(fname)

# initializes an SFTP conenction object
def init_sftp():
    try:
        # some versions of pysftp has a bug where it 
        # says that you failed to load hostkeys even when you
        # set it to ignore hostkeys. this suppresses that warning
        warnings.filterwarnings('ignore', '.*Failed to load HostKeys.*')

        # sets SFTP connection options
        opts = pysftp.CnOpts()
        opts.hostkeys = None

        # create SFTP connection, change to the upload directory, and return the new connection object
        sftp = pysftp.Connection(ip_addr, username=usr, private_key=ftp_key, cnopts=opts)
        sftp.cwd('upload')
        return sftp
    except:
        # returns None if FTP connection fails
        if debug:
            print('An error occurred trying to connect.')
        return None

# writes process data in an organized csv format
def dump_csv(pslst, fname):
    try:
        # open given file in writing mode, label the data, and write the data for each process to the file
        # finally, close the file when done
        f = open(fname, 'w')
        f.write('time, machine_id, ps_name, mempct, cpupct, memabs, numthreads, user, path, pid\n')
        for ps in pslst:
            f.write(ps + '\n')
        f.close()
    except:
        # tries to reboot program if CSV dump fails
        if debug:
            print('FATAL ERROR\n Could not dump process data to CSV file \n Attempting to relaunch...')
        sys.exit(0)

# returns whether the user is a system administrator
def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()

# infinite loop of data collection, dumping, and killing
def main():
    if not is_admin():
        # Re-run the program with admin rights
        if debug:
            print('I AM NOT AN ADMIN')
            print('ATTEMPTING TO RELAUNCH AS ADMIN')
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)
    else:
        if debug:
            print('LOGGED IN AS ADMIN')

    # on the first run, CPU% always shows 0
    # so we should not upload that data
    first = True 

    # gets total amount of system memory (RAM)
    sys_mem = psutil.virtual_memory()[0] 

    # initializes ftp connection
    sftp = init_sftp() 

    # BUG: need to check if the CSV actually matches our format or if it's just random junk
    # creates a list for any files we fail to upload with ftp
    # populates the list with files from any previous runs of the program
    failed_files = [] 
    for filename in os.listdir(os.path.dirname(__file__)):
        if filename.endswith('.csv'):
            failed_files.append(filename)

    # TODO: EACH TIME THIS RUNS WE WANNA PULL BAD PROCESSES FROM THE AWS FTP SERVER
    # AND KILL THEM IF THEY'RE BAD
    # keep most recent copy of the bad processes on the machine
    while True:
        # maps process names to their pid
        proc_dict = {} 

        # collect data that is the same for each process
        timestamp = datetime.datetime.now()
        pslst = []
        machine_id = get_mac()

        # currently not being dumped
        cores = os.cpu_count()
        clock_speed = psutil.cpu_freq()

        # iterates through every process and collects various data about it
        for proc in psutil.process_iter():
            try:
                # collect process dependent data
                name = proc.name()
                mempct = proc.memory_percent()
                cpupct = proc.cpu_percent()
                numthd = proc.num_threads()

                # collects absolute memory usage in MB
                memabs = sys_mem * mempct / 100000000

                ### LAST 2 ITEMS REQUIRE ADMIN PRIVILEGES
                usr = proc.username()

                # clean up username field
                usr = usr.replace("NT AUTHORITY\\", "", 1)  # removes "NT AUTHORITY" from the user field
                usr = usr.replace(socket.gethostname() + "\\", "", 1)  # removes hostname (device name) from before username. 

                pid = proc.pid

                # map process name to the pid
                if name in proc_dict:
                    proc_dict[name].append(pid)
                else:
                    proc_dict[name] = [pid]

                if name.endswith('.cxp'):
                    try:
                        os.kill(pid, 9)

                        if debug:
                            print('Killed ' + line + ' with pid ' + str(pid))
                    except:
                        if debug:
                            print('Process ' + line + ' with pid ' + str(pid) + 'not found' )

                
                path = None
                if pid != 0: # pid 0 is a dummy process initiated by windows that causes errors
                    path = psutil.Process(pid).exe()
            
                    # BUG: IF USER NAMES MALWARE SVCHOST.EXE THIS WILL ALLOW MALWARE TO RUN
                    # ignores many of the windows processes, as we don't want to send those
                    # possibly other programs we want to whitelist in the future
                    if name != 'svchost.exe':
                        pslst.append(f'{timestamp},{machine_id},{name},{mempct},{cpupct},{memabs} MB,{numthd},{usr},{path},{pid}')
            except:
                if debug:
                    print('ERROR: Some process data could not be collected for unknown reasons')
                
        # dump the csv with a unique name based on the date, time, and mac address
        fname = f"{datetime.datetime.now():%Y-%m-%d_h%Hm%Ms%Sa}" + str(machine_id) + '.csv'
        if not first:
            dump_csv(pslst, fname)

        try:
            # attempt to establish an sftp connection if the previous one failed
            if sftp == None:
                sftp = init_sftp()

            # upload the CSV and delete it from disk
            if not first:
                upload_csv(sftp, fname)
                if debug:
                    print('UPLOAD SUCCEEDED')
                if not keep:
                    os.remove(fname)
            else:
                first = False

            # if upload succeeds try and dump any previously failed uploads
            while len(failed_files) > 0:
                file = failed_files[-1]
                upload_csv(sftp, file)
                if debug:
                    print('PREVIOUSLY FAILED UPLOAD SUCCEEDED')

                if not keep:
                    os.remove(file)
                del failed_files[-1]

            # pull most recent version of malcious process file from server
            if pull and sftp != None:
                pull_malicious(sftp, 'bad.txt')

        except OSError:
            first = False
            if debug:
                print('file could not be deleted')
        except:
            first = False
            # set sftp connection to none to let us know that there is a connection issue
            sftp = None
            # if fails add the current file to a queue of files that we didn't upload
            if debug:
                print("UPLOAD FAILED")
            failed_files.append(fname)
        
        # try and open malicious process file and kill bad processes if they're running
        f = None
        try:
            f = open('bad.txt', 'r')
            if debug:
                print('Found malicious processes file on disk')
        except:
            f = None
            if debug:
                print('Bad process file could not be opened')

        if f != None:
            for line in f:
                line = line.strip()
                if line in proc_dict:
                    for pid in proc_dict[line]:
                        try:
                            os.kill(pid, 9)

                            if debug:
                                print('Killed ' + line + ' with pid ' + str(pid))
                        except:
                            if debug:
                                print('Process ' + line + ' with pid ' + str(pid) + 'not found' )
            f.close()

        # Pause data collection for some period of time
        time.sleep(sleep_time) 
        
# run the script
if __name__ == '__main__':
    main()
