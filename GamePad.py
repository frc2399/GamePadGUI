import tkinter as tk
import array as arr
import csv

import time
import sys

from networktables import NetworkTables
global location
global level
global gamePiece
global g_allianceColor
global EventName
global MatchNumber
global used_combinations
g_allianceColor="white"

def buttonPressed(i):

    print(location + " was chosen")
    sidecarTables.putString("scoringLocation", location)
    combinationater(location, level)

def scoringLevel(button, place):
    for butt in buttons2:
        if butt['bg'] == g_allianceColor:
            butt['bg'] = 'white'
    button['bg'] = g_allianceColor


    print(place + " was chosen")
    sidecarTables.putString("scoringLevel", place)
    level = place
    combinationater(location, place)


def algaeSelect():
    global gamePieceMode
    if gamePieceMode == "coral":
        gamePieceMode = "algae"
        coralButton.config(bg="#e3e3e3")

        buttons2[0].config(bg='gray', command=obsolete)
        buttons2[3].config(bg='gray', command=obsolete)
    else:
        gamePieceMode = "coral"
        coralButton.config(bg="#9400D3", text="Coral")

        buttons2[0].config(bg='white', command=lambda: scoringLevel(buttons2[0], "Level 1"))
        buttons2[3].config(bg='white', command=lambda: scoringLevel(buttons2[3], "Level 4"))

    print("Intake mode " + gamePieceMode + " was chosen")
    sidecarTables.putString("currentIntakeMode", gamePieceMode)

def coralSelect():
    global gamePieceMode
    if gamePieceMode == "coral":
        gamePieceMode = "algae"
        coralButton.config(bg="#e3e3e3")
    else:
        gamePieceMode = "algae"

        buttons2[0].config(bg='white', command=lambda: scoringLevel(buttons2[0], "Level 1"))
        buttons2[3].config(bg='white', command=lambda: scoringLevel(buttons2[3], "Level 4"))

    print("Intake mode " + gamePieceMode + " was chosen")
    sidecarTables.putString("currentIntakeMode", gamePieceMode)


#change color of hexagon depending on alliance color
def valueChanged(table, key, value, isNew): 

    print("valueChanged: key: '%s'; value: %s; isNew: %s" % (key, value, isNew))
    if key == "IsRedAlliance":
        if value == True:
            g_allianceColor = "#DC143C"
        else:
            g_allianceColor = "#1E90FF"

#log all used combinations
def combinationater(place, level):
    new_combination = (place, level)

    if new_combination not in used_combinations:
        used_combinations.add(new_combination)
        print("New combination added: " + str(new_combination))
    else:
        print("Combination " + str(new_combination) + " already used")


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
sidecarTables = NetworkTables.getTable("sidecarTable")
sidecarTables.putString("scoringLocation", "")
sidecarTables.putString("scoringLevel", "")

#set default intake mode to coral
gamePieceMode = "coral"
sidecarTables.putString("GameMode", gamePieceMode)

#set default location and level to nothing
location = ""
level = ""
used_combinations = set()

#window
window = tk.Tk() #create window
window.geometry("850x500") #size
window.title("sidecar") #title


#buttons for selecting game piece
coralButton = tk.Button(window, text="Coral", bg="#fca7a7", font=("Book Antiqua", 18))
coralButton.config(command=coralSelect)
coralButton.place(x=50, y=50, height=150, width=150)

algaeButton = tk.Button(window,  text="Algae", bg="#8bd7f7", font=("Book Antiqua", 18))
algaeButton.config(command=algaeSelect)
algaeButton.place(x=300, y=50, height=150, width=150)

leftButton = tk.Button(window, text="Left", bg="#bcff7d", font=("Book Antiqua", 18))
leftButton.place(x=50, y=250, height=150, width=150)

rightButton = tk.Button(window, text="Right", bg="#bcff7d", font=("Book Antiqua", 18))
rightButton.place(x=300, y=250, height=150, width=150)

resetButton = tk.Button(window, text="Reset", bg="#faf5af", font=("Book Antiqua", 18))
resetButton.place(x=50, y=430, height=40, width=450)

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