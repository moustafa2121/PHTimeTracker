import time
from auxFile import State, Color

#containers contain a state and the
#informations necessary for it
class Container:
    def __init__(self, state):
        self.state = state
        self.startTime = time.time()
        self.endTime = -1
    def getState(self):
        return self.state
    #called when the timer ends
    def endTimer(self):
        self.endTime = time.time()
    #get the time passed, used to calculate
    #the rectangles
    def getSeconds(self):
        #for currently running contianers
        if self.endTime == -1:
            return time.time() - self.startTime
        else:
            return self.endTime - self.startTime 
    #returns the color of the retangle
    #depending on the state
    def getColor(self):
        if self.state == State.WORKING:
            return Color.blue
        elif self.state == State.INTERRUPTED:
            return Color.yellow	
        elif self.state == State.STARTING_STATE:
            return Color.grey
        elif self.state == State.BREAK:
            return Color.green
        elif self.state == State.WASTED:
            return Color.red
        else:	
            return None
        
#class that keep tracks of containers
#it starts and ends containers
#all tracking is done using seconds
#by calling on the time.time() function
class Tracker:
    def __init__(self):
        #queue used to add up containers
        self.queue = []
        self.currentContainer = None
    def getQueue(self):
        return self.queue
    #appends a new container to the queue
    def appendContainer(self, c):
        self.currentContainer = Container(c)
        self.queue.append(self.currentContainer)
    def endCurrentContainer(self):
        self.currentContainer.endTimer()
    def getCurrentState(self):
        return self.currentContainer.getState()
    def getCurrentStateStr(self):
        state = self.currentContainer.getState()
        if state == State.WORKING:
            return 'Working'
        elif state == State.BREAK:
            return 'Break'
        elif state == State.INTERRUPTED:
            return 'Interrupted'
        elif state == State.WASTED:
            return 'Wasted'
        elif state == State.STARTING_STATE:
            return 'Start'
        else:
            return 'INVALID'
    def getCurrentContainer(self):
        return self.currentContainer
    def getTotalTime(self):
        workTime = 0
        wastedTime = 0
        interruptedTime = 0
        breakTime = 0
        startingState = 0
        for i in self.queue:
            if i.getState() == State.WORKING:
                workTime += i.getSeconds()
            elif i.getState() == State.BREAK:
                breakTime += i.getSeconds()
            elif i.getState() == State.INTERRUPTED:
                interruptedTime += i.getSeconds()
            elif i.getState() == State.WASTED:
                wastedTime += i.getSeconds()
            elif i.getState() == State.STARTING_STATE:
                startingState += i.getSeconds()
        return startingState, workTime, wastedTime, interruptedTime, breakTime
    #checks if the tracker has exceeded the session time of 16
    def exceedLimit(self):
        totalTime = sum(self.getTotalTime())
        if totalTime/3600 >= 16:
            return True
        else:
            return False
            
