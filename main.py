import auxFile as ax
from Tracker import Tracker
import pygame, time
from Session import Session

pygame.init()
gameDisplay = pygame.display.set_mode((ax.Dim.displayW, ax.Dim.displayH))
pygame.display.set_caption('Scheduler')
clock = pygame.time.Clock()

#draw rectangle
def drawRect(dim, color):
	pygame.draw.rect(gameDisplay, color, dim)

#pass tex and dim to write
def writeText(text, dim, fontSize=15, color=ax.Color.white):	
	font = pygame.font.Font('freesansbold.ttf', fontSize)
	textSurface = font.render(text, True, color)
	textRect = textSurface.get_rect()	
	textRect.center = dim
	gameDisplay.blit(textSurface, textRect)	

#write on buttons!
def writeOnButtons():
	x = ax.generateButtonDim()
	writeText('W', ax.getButtonCenter(next(x), ax.Dim.buttonSize))	
	writeText('B', ax.getButtonCenter(next(x), ax.Dim.buttonSize))
	writeText('W', ax.getButtonCenter(next(x), ax.Dim.buttonSize))
	writeText('I', ax.getButtonCenter(next(x), ax.Dim.buttonSize))
	writeText('E', ax.getButtonCenter(next(x), ax.Dim.buttonSize))
	
#label the timeline with hours
def hourLabels():
        for i in range(ax.Constant.sessionTime+1)[::2]:
                writeText(str(i), (ax.Dim.startLineW+ax.calculateRatio(3600*i),
                                ax.Dim.displayH - 10), fontSize=10, color=ax.Color.black)
#dispaly the time of the current container
#and the total time of all containers
def displayTimers(tracker):
	seconds = tracker.getCurrentContainer().getSeconds()
	writeText(ax.getTimeDisplay(seconds), (ax.Dim.startLineW+32, 55), color=ax.Color.black)
	_, workTime, wastedTime, interruptedTime, breakTime = tracker.getTotalTime()
	writeText('Total work time: '+ax.getTimeDisplay(workTime), (ax.Dim.startLineW+190+30, 10), color=ax.Color.black)
	writeText('Total break time: '+ax.getTimeDisplay(breakTime), (ax.Dim.startLineW+192+30, 25), color=ax.Color.black)	
	writeText('Total wasted time: '+ax.getTimeDisplay(wastedTime), (ax.Dim.startLineW+196+30, 40), color=ax.Color.black)
	writeText('Total interrupted time: '+ax.getTimeDisplay(interruptedTime), (ax.Dim.startLineW+212+30, 55), color=ax.Color.black)
	writeText(tracker.getCurrentStateStr(), (ax.Dim.startLineW+30, 30), color=ax.Color.black)
#draws the buttons
def drawButtons():
	x = ax.generateButtonDim()
	drawRect(next(x), ax.Color.blue)	
	drawRect(next(x), ax.Color.green)
	drawRect(next(x), ax.Color.red)
	drawRect(next(x), ax.Color.yellow)
	drawRect(next(x), ax.Color.black)
	writeOnButtons()
	
#takes a tracker 
#displays time
def displayContainers(tracker):
    oldLength = 0
    for i in tracker.getQueue():
        length = ax.calculateRatio(i.getSeconds())
        drawRect([ax.Dim.startLineW+oldLength, ax.Dim.startLineH, length, ax.Dim.lineHeight], i.getColor())
        oldLength += length
        
#pass mouse coordinates
#returns a Constant.state depending on where it is located
def mouseHoverState(pos):
	lst = []
	for i in ax.generateButtonDim():
		if i[0] < pos[0] < i[0]+i[2] and i[1] < pos[1] <i[1]+i[3]:
			lst.append(1)
		else:
			lst.append(0)
	if 1 in lst:
		return lst.index(max(lst))
	else:
		return -1
        
#a wrapper function for bunch of elements on the GUI
def displayWrapper(tracker):
        gameDisplay.fill(ax.Color.white)
        drawRect([ax.Dim.startLineW, ax.Dim.startLineH, ax.Dim.workingWidth, ax.Dim.lineHeight], ax.Color.black)
        drawButtons()
        hourLabels()
        displayContainers(tracker)
        displayTimers(tracker)

#used when the time limit has reached its end
def displayEnd():
        gameDisplay.fill(ax.Color.white)
        writeText('Session has reached its limit. Exiting', [ax.Dim.displayW/2, ax.Dim.displayH/2], 15, ax.Color.black)
        pygame.display.update()
        clock.tick(60)
        #wait 2 seconds before exiting
        waitTime = time.time()
        while time.time()-waitTime < 2:
                pass
        
def main():
    sess = Session()
    tracker = sess.getTracker()
    while True:
        if tracker.exceedLimit():
                sess.endSession(status=ax.State.END_SESSION)
                displayEnd()
                pygame.quit()
                quit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sess.endSession(status=ax.State.PAUSE)
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONUP:
                stateClicked = mouseHoverState(event.pos)
		#the click is somewhere of value and it is not the current state
                if stateClicked != -1 and stateClicked != tracker.getCurrentState():
                    tracker.endCurrentContainer()
                    if stateClicked == ax.State.WORKING:
                        tracker.appendContainer(ax.State.WORKING)
                    elif stateClicked == ax.State.INTERRUPTED:
                        tracker.appendContainer(ax.State.INTERRUPTED)
                    elif stateClicked == ax.State.BREAK:
                        tracker.appendContainer(ax.State.BREAK)
                    elif stateClicked == ax.State.WASTED:
                        tracker.appendContainer(ax.State.WASTED)
                    else:
                        sess.endSession(status=ax.State.END_SESSION)
                        pygame.quit()
                        quit()
                        
        displayWrapper(tracker)
        pygame.display.update()
        clock.tick(60)
main()
