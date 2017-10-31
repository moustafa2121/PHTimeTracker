This is a time tracker usually for a 16 hours session (can be changed). The GUI is created using pygame. This is not meant to be a scheduler as you cannot exactly follow your schedule. Instead, this tracks how the time is spent in 4 different states: Working (blue), Break (green), Wasted (red), and Interrupted (yellow). Working is any kind of productive work or studying or doing chores. Break is for regular breaks, and food break (i.e. lunch). Wasted is when you procrastinate and “extend” your break. Interrupted is when someone you’re not planning to talk to/do something with is interrupting your work, basically time being wasted but not your fault. The black button E is for ending the session. The program will exit and saves the session in the sessions.dat file. Will add graphing mechanisms to project progress over time.

Usually one starts the session at the beginning of the day and picks whatever state that is needed. Clicking on the same state has no effect. The current state can be seen on the left side along with its current timer. The total time for each state in the current session can be seen on the right side. The long bar shows the time state on each state as a bar.

Python modules required: pickle, pygame, os, sys

![alt text](https://raw.githubusercontent.com/moustafa2121/PHTimeTracker/blob/master/Sample.PNG?raw=true "Title")
