import tkinter as tk
import array as arr
import csv

import time
import sys

from networktables import NetworkTables
gameMode = 1
g_allianceColor="white"

def buttonPressed(i):
    global location
    location = buttonLabels[i]

    print(location + " was chosen")
    scoringStateTables.putString("scoringLocation", location)

def scoringLevel(button, place):
    global level
    for butt in buttons2:
        if butt['bg'] == g_allianceColor:
            butt['bg'] = 'white'
    button['bg'] = g_allianceColor


    print(place + " was chosen")
    scoringStateTables.putString("scoringLevel", place)
    level = place

#changes layout according to the game piece mode
def gamePieceSelect():
    global currentIntakeMode
    global gamePiece
    if currentIntakeMode == 1:
        currentIntakeMode = 2
        gamePiece.config(bg="#00CED1", text="Algae")

        buttons2[0].config(bg='gray', command=obsolete)
        buttons2[3].config(bg='gray', command=obsolete)
    else:
        currentIntakeMode = 1
        gamePiece.config(bg="#9400D3", text="Coral")

        buttons2[0].config(bg='white', command=lambda: scoringLevel(buttons2[0], "Level 1"))
        buttons2[3].config(bg='white', command=lambda: scoringLevel(buttons2[3], "Level 4"))

    print("Intake mode " + str(currentIntakeMode) + " was chosen")
    scoringStateTables.putNumber("currentIntakeMode", currentIntakeMode)

def testValueChange():
    global gameMode
    if gameMode == 1:
        gameMode = 2
        testButton.config(text="Test2")
    else:
        gameMode = 1
        testButton.config(text="Test1")
    print("Game mode is " + str(gameMode))
    scoringStateTables.putNumber("GameMode", gameMode)

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

def reset():
    for butt in buttons2:
        butt['bg'] = "white"
    
    currentIntakeMode = 1
    gamePieceSelect()

    scoringStateTables.putString("scoringLocation", "")
    scoringStateTables.putString("scoringLevel", "")


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


#creates table and sets to none
scoringStateTables = NetworkTables.getTable("sidecarTable")
scoringStateTables.putString("scoringLocation", "")
scoringStateTables.putString("scoringLevel", "")

#set default intake mode to coral
currentIntakeMode = 1
scoringStateTables.putNumber("currentIntakeMode", currentIntakeMode)

#set default location and level to nothing
location = ""
level = ""
used_combinations = set()

#window
window = tk.Tk() #create window
window.geometry("850x500") #size
window.title("sidecar") #title

#buttons for selecting level
gamePiece = tk.Button(window, text="Coral", bg="#9400D3", font=("Book Antiqua", 18))
gamePiece.config(command=gamePieceSelect)
gamePiece.place(x=50, y=100, height=100, width=100)

resetButton = tk.Button(window, text="Reset", bg="white", font=("Book Antiqua", 18))
resetButton.config(command=reset)
resetButton.place(x=50, y=330, height=100, width=100)

testButton = tk.Button(window, text="Test", bg="white", font=("Book Antiqua", 18))
testButton.config(command=testValueChange)
testButton.place(x=50, y=210, height=100, width=100)

buttons2 = []
j = 0
while j <= 3:
    button = tk.Button(
        window,
        text=('L' + str(j+1)),
        bg="white",
        font=('Book Antiqua', 18),
    )
    buttons2.append(button)
    j += 1

buttons2[3].place(x=600, y=60, height=75, width=200)
buttons2[3].config(command=lambda: scoringLevel(buttons2[3], "Level 4"))

buttons2[2].place(x=600, y=162, height=75, width=200)
buttons2[2].config(command=lambda: scoringLevel(buttons2[2], "Level 3"))

buttons2[1].place(x=600, y=263, height=75, width=200)
buttons2[1].config(command=lambda: scoringLevel(buttons2[1], "Level 2"))

buttons2[0].place(x=600, y=365, height=75, width=200)
buttons2[0].config(command=lambda: scoringLevel(buttons2[0], "Level 1"))

#run
window.mainloop()

#Write to a CSV file after program is finished running
with open("output.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow((EventName, MatchNumber))
    writer.writerows(used_combinations)

print("Data written to output.csv")