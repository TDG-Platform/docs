from datetime import datetime
import numpy as np

#def timedelta(starttime,endtime):
#    if starttime > endtime:
#        return endtime - starttime

def tasknamefromtaskhash(taskhash):
    splitname = taskhash.split('_')
    nametask = ''
    for s in splitname[:-1]:
        nametask += s+'_'
    nametask = nametask[:-1]
    return nametask

def getworkflow(events,taskname):
    isrunning = False
    iscomplete = False


    nametask = tasknamefromtaskhash(taskname)

    for event in events:
        print event
        if tasknamefromtaskhash(event["task"]) == nametask:
            print "***", event["state"]
            if not isrunning and event["state"] == "running":
                isrunning = True #starttime = event["timestamp"]
                starttime = np.datetime64(event["timestamp"])
            elif not iscomplete and event["state"] == "complete":
                iscomplete = True #endtime = event["timestamp"]
                endtime = np.datetime64(event["timestamp"])

                #return timedelta(starttime,endtime)
                return   (endtime - starttime) / np.timedelta64(1, 's')
