import tkinter as tk
import array as arr
import csv

import time
import sys

from networktables import NetworkTables
global used_combinations
start = True

def scoringLevel(button, place):
    for butt in buttons2:
        if butt['bg'] == '#FD8930':
            butt['bg'] = 'gray'
    button['bg'] = '#FD8930'


    print(place + " was chosen")
    sidecarTables.putString("scoringLevel", place)

def algaeSelect():
    global gamePieceMode
    if gamePieceMode == "coral":
        gamePieceMode = "algae"

        algaeButton.config(bg="#08C2AC") #blue
        for butt in buttons2:
            butt['bg'] = "#FD8930"
        buttons2[3].config(bg='gray', command=obsolete)
        leftButton.config(bg='gray', command=obsolete)
        rightButton.config(bg='gray', command=obsolete)
        coralButton.config(bg='gray')

    print("Intake mode " + gamePieceMode + " was chosen")
    sidecarTables.putString("gamePieceMode", gamePieceMode)

def coralSelect():
    global gamePieceMode
    global start
    if (gamePieceMode == "algae"):
        gamePieceMode = "coral"

        algaeButton.config(bg="gray") 
        coralButton.config(bg="#FC59CE") #purple
        for butt in buttons2:
            butt['bg'] = "#FD8930"
        leftButton.config(bg='#bcff7d', command=leftSelect) #green
        rightButton.config(bg='#bcff7d', command=rightSelect) #green
        buttons2[3].config(bg="#FD8930", command=lambda: scoringLevel(buttons2[3], "Level 4"))
    elif start == True:
        start = False
        leftButton.config(bg='#bcff7d', command=leftSelect) #green
        rightButton.config(bg='#bcff7d', command=rightSelect) #green
        algaeButton.config(bg='gray')
    else:
        algaeButton.config(bg="gray") 

    print("Intake mode " + gamePieceMode + " was chosen")
    sidecarTables.putString("gamePieceMode", gamePieceMode)

def leftSelect():
    global position
    if position == "right":
        position = "left"

        rightButton.config(bg='gray')
        leftButton.config(bg='#FEDF78') #yellow
    print("Position " + position + " was chosen")
    sidecarTables.putString("Position", position)

def rightSelect():
    global position
    if position == "left":
        position = "right"

        rightButton.config(bg='#FEDF78')
        leftButton.config(bg='gray')
    elif position == "right":
        position = "right"

        rightButton.config(bg='#FEDF78')
        leftButton.config(bg='gray')
    print("Position " + position + " was chosen")
    sidecarTables.putString("Position", position)

def algaeIndicatorChange():
    global algaeIndicator
    if algaeIndicator == False: 
        algaeIndicator = True
        algaeIndicatorButton.config(bg="#2efa23")
    else:
        algaeIndicator = False
        algaeIndicatorButton.config(bg='gray')
    print("Algae in robot is " + str(algaeIndicator))
    sidecarTables.putBoolean("hasAlgae", algaeIndicator)

def coralIndicatorChange():
    global coralIndicator
    if coralIndicator == False: 
        coralIndicator = True
        coralIndicatorButton.config(bg="#2efa23")
    else:
        coralIndicator = False
        coralIndicatorButton.config(bg='gray')
    print("Coral in robot is " + str(coralIndicator))
    sidecarTables.putBoolean("hasCoral", coralIndicator)

def algaeIndicatorState(table, key, value, isNew):
    global algaeIndicator
    global window
    print("Algae in robot is " + str(value))
    window.after(0, lambda: algaeIndicatorButton.config(bg="#2efa23" if value == True else 'gray'))
    algaeIndicator = value

def coralIndicatorState(table, key, value, isNew):
    global coralIndicator
    global window
    print("Coral in robot is " + str(value))
    window.after(0, lambda: coralIndicatorButton.config(bg="#2efa23" if value == True else 'gray'))
    coralIndicator = value

#change color of hexagon depending on alliance color
def valueChanged(table, key, value, isNew): 
    global g_allianceColor
    global EventName
    global MatchNumber
    print("valueChanged: key: '%s'; value: %s; isNew: %s" % (key, value, isNew))
    if key == "IsRedAlliance":
        if value == True:
            g_allianceColor = "#DC143C"
        else:
            g_allianceColor = "#1E90FF"

def obsolete():
    print("Button obsolete for selected intake mode")

def connectionListener(connected, info):
    print(info, "; Connected=%s" % connected)


# Set the RoboRIO IP address (from old nt code)
ip = "10.23.99.2"

NetworkTables.initialize(server=ip)
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

nt = NetworkTables.getTable("FMSInfo")
nt.addEntryListener(valueChanged)
EventName = nt.getString("EventName", "")
MatchNumber = nt.getNumber("MatchNumber", 0)

time.sleep(1)

if NetworkTables.isConnected():
    print("Connected to NetworkTables server")
else:
    print("Failed to connect to NetworkTables server")


#creates table and alage/coral listeners
sidecarTables = NetworkTables.getTable("sidecarTable")
sidecarTables.addEntryListener(listener=algaeIndicatorState, key="hasAlgae", immediateNotify=True)
sidecarTables.addEntryListener(listener=coralIndicatorState, key="hasCoral", immediateNotify=True)

#sets scoring level to none
sidecarTables.putString("scoringLevel", "")

#set default intake mode to coral
gamePieceMode = "coral"
sidecarTables.putString("gamePieceMode", gamePieceMode)

#set default left/right to right
position = "right"
sidecarTables.putString("Position", position)

algaeIndicator = False
coralIndicator = False

#set default location and level to nothing
location = ""
level = ""
used_combinations = set()

#window
window = tk.Tk() #create window
window.geometry("850x500") #size
window.title("sidecar") #title
#window.config(bg=g_allianceColor)

#buttons for selecting game piece
algaeButton = tk.Button(window, text="Algae", bg="#08C2AC", font=("Fira Mono", 80))
algaeButton.config(command=algaeSelect)
algaeButton.place(x=50, y=150, height=250, width=300)

coralButton = tk.Button(window,  text="Coral", bg="#FC59CE", font=("Fira Mono", 80))
coralButton.config(command=coralSelect)
coralButton.place(x=410, y=150, height=250, width=300)

leftButton = tk.Button(window, text="Left", bg="#FEDF78", font=("Fira Mono", 80))
leftButton.place(x=50, y=420, height=250, width=300)

rightButton = tk.Button(window, text="Right", bg="#FEDF78", font=("Fira Mono", 80))
rightButton.place(x=410, y=420, height=250, width=300)

algaeIndicatorButton = tk.Button(window, text="hasAlgae", bg="gray", font=("Fira Mono", 23))
algaeIndicatorButton.config(command=algaeIndicatorChange)
algaeIndicatorButton.place(x=125, y=30, height=100, width=140)

coralIndicatorButton = tk.Button(window, text="hasCoral", bg="gray", font=("Fira Mono", 23))
coralIndicatorButton.config(command=coralIndicatorChange)
coralIndicatorButton.place(x=485, y=30, height=100, width=140)

buttons2 = []
j = 0
while j <= 3:
    button = tk.Button(
        window,
        text=('L' + str(j+1)),
        bg="#FD8930", #orange
        font=('Fira Mono', 80),
    )
    buttons2.append(button)
    j += 1

buttons2[3].place(x=800, y=70, height=125, width=430)
buttons2[3].config(command=lambda: scoringLevel(buttons2[3], "Level 4"))

buttons2[2].place(x=800, y=220, height=125, width=430)
buttons2[2].config(command=lambda: scoringLevel(buttons2[2], "Level 3"))

buttons2[1].place(x=800, y=370, height=125, width=430)
buttons2[1].config(command=lambda: scoringLevel(buttons2[1], "Level 2"))

buttons2[0].place(x=800, y=520, height=125, width=430)
buttons2[0].config(command=lambda: scoringLevel(buttons2[0], "Level 1"))

#run
window.mainloop()

#Write to a CSV file after program is finished running
with open("output.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow((EventName, MatchNumber))
    writer.writerows(used_combinations)

print("Data written to output.csv")