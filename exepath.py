import psutil
import csv

currentPIDs=psutil.pids()
currentPIDs.remove(0)
print(currentPIDs)




for proc in currentPIDs:
 

    try:
        path=psutil.Process(proc).exe()
        print(path)
        writer.writerow(path)

    except:
        print('undeterminable path')













   
 
