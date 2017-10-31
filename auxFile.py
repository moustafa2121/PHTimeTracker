
#pass the seconds and it will calculate
#the ratio needed to display the rectangles properly
def calculateRatio(seconds):
    ratio = seconds/3600
    ratio /= Constant.sessionTime
    return ratio*Dim.workingWidth
#pass the dim of the buttons
#returns a tuple of the center of the rect
#used to write text on the buttons
def getButtonCenter(dim, buttonSize):
	x = (buttonSize/2) + dim[0]
	y = (buttonSize/2) + dim[1]
	return (x, y)

#generate dimensions of the buttons
#this is a generator
def generateButtonDim():
	buttonDistance = 0 
	for i in range(Constant.numButtons):#for the 5 main buttons
		yield [Dim.startLineW+buttonDistance, Dim.displayH/2.2, Dim.buttonSize, Dim.buttonSize]
		buttonDistance += Dim.incrementValue

		
#pass seconds and it will show the time in the format:
#hh:mm:ss
def getTimeDisplay(time):
    properFormat = lambda x: str('0') + str("%.f"%x) if x <10 else str("%.f"%x)
    seconds = float("%.f"%time)
    minutes = str('00')
    hours = str('00')
    if time < 10:
        seconds = properFormat(time)
    elif time < 60:
        seconds = properFormat(time)
    else:
        seconds = properFormat(time%60)
        minutes = time//60
        if minutes >= 60:
            hours = properFormat(minutes//60)
            minutes = properFormat(minutes%60)
        else:
            minutes = properFormat(minutes)
                
    return hours + ':' + minutes + ':' + seconds

class Constant:
    numButtons = 5
    sessionTime = 16
    

#dimensions
class Dim:
        displayW, displayH = 400, 150
        startLineW = displayW/20#where the timer line begins x-axis
        lineHeight = displayH/10
        startLineH = displayH - lineHeight - (displayH/10)
        workingWidth= displayW - (startLineW*2)#the width to work with
        buttonSize = displayW/(Constant.numButtons*2)
        incrementValue = workingWidth/Constant.numButtons + buttonSize/Constant.numButtons
        
class Color:        
	white, black = (255, 255, 255), (0, 0, 0)
	red = (255, 0, 0)
	green = (0, 255, 0)
	blue = (0, 0, 255)
	yellow = (255, 255, 0)
	grey = (105, 105, 105)
	
class State:
	WORKING = 0#blue
	BREAK = 1#green
	WASTED = 2#red	
	INTERRUPTED = 3#yellow
	STARTING_STATE = 4#grey
	END_SESSION = 5
	START_SESSION = 6
	PAUSE = 7#pausing a session when closing the program
