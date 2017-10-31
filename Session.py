import time, pickle, os, sys
import auxFile as ax
from Tracker import Tracker

#the session that's the user is currently on
#typically a day. We can conveniently use the date
#but sometimes we work past midnight
#the tracker is saved here and once the session
#is done the data (inclduing the tracker) are saved
#in a pickle file for later use (i.e. stats)
class Session:
    def __init__(self, status=ax.State.START_SESSION):
        self.tracker = Tracker()
        self.tracker.appendContainer(ax.State.STARTING_STATE)
        self.startTime = time.localtime(time.time())[:]
        self.endTime = -1
        self.sessionName = 'PlaceHolder'
        #load settings from setting.txt
        f = open('userSettings.txt', 'r')
        fileData = f.read().split('\n')
        f.close()
        lastSessionName = fileData[0].split(' = ')[-1]
        self.numberOfSessions = int(fileData[1].split(' = ')[-1])
        
        if lastSessionName == 'None':#no last sessions
            self.status = ax.State.START_SESSION
            #name is given by: ###_dd_mm_yyyy
            self.sessionName = str(self.numberOfSessions+1)+'_'+str(self.startTime[2])+'_'+str(self.startTime[1])+'_'+str(self.startTime[0])
        else:#load the pickle to see if the previous session ended
            lastSession = loadPickle(lastSessionName)#loadPickle(lastSession)
            
            if lastSession.status == ax.State.END_SESSION:#start a new session
                self.status = ax.State.START_SESSION
                self.sessionName = str(self.numberOfSessions+1)+'_'+str(self.startTime[2])+'_'+str(self.startTime[1])+'_'+str(self.startTime[0])
            else:#otherwise this session is the previous session                
                for i in lastSession.__dict__.keys():
                    self.__dict__[i] = lastSession.__dict__[i]
    
    def getTracker(self):
        return self.tracker
    def getStatus(self):
        return self.status
    #ends the sessions or saves it to resume later
    #the passed status represents that
    def endSession(self, status):
        self.endTime = time.localtime(time.time())[:]
        self.status = status
        #save the session and the tracker
        Session.pickleIt(self)
        #update the settings
        Session.saveSettings(self)

    #save the whole thing in the pickle file
    def pickleIt(self):
        f = open('sessions.dat', 'rb')#read the dict
        x = pickle.load(f)
        f.close()
        x[self.sessionName] = self#add to the dict
        f = open('sessions.dat', 'wb')#write the dict
        pickle.dump(x, f)#dump the dict
        f.close()
    #update the settings
    def saveSettings(self):
        f = open('userSettings.txt', 'w')
        tmp = 'lastSession = ' + self.sessionName + '\n'
        tmp += 'numberOfSessions = ' + str(self.numberOfSessions+1)
        f.write(tmp)
        f.close()

#loads a session
#pass session name
#returns Session object
def loadPickle(sessionName):
    f = open('sessions.dat', 'rb')
    x = pickle.load(f)
    f.close()
    return x[sessionName]

#clears the 'sessions.dat' file and puts only a dict
def deleteOldSessions():
    f = open('sessions.dat', 'wb')
    x = dict()
    pickle.dump(x, f)
    f.close()
    f = open('userSettings.txt', 'w')
    tmp = 'lastSession = None' + '\n'
    tmp += 'numberOfSessions = ' + str(0)
    f.write(tmp)
    f.close()
