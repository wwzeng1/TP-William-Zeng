from tkinter import *
from chesspiecesandboard import *
from checkLogic import * 
import random
import copy

def init(data):
    data.mode = "mainScreen"
    data.prevMode = data.mode
    data.aiColor = random.choice(["Black", "White"])
    initPieces(data)
# course notes
def mousePressed(event, data):
    if (data.mode == "mainScreen"):   mainScreenMousePressed(event, data)
    elif (data.mode == "twoP"):       twoPMousePressed(event, data)
    elif (data.mode == "AI"):         AIMousePressed(event, data)
    elif (data.mode == "help"):       helpMousePressed(event, data)

def keyPressed(event, data):
    if (data.mode == "mainScreen"):   mainScreenKeyPressed(event, data)
    elif (data.mode == "twoP"):       twoPKeyPressed(event, data)
    elif (data.mode == "AI"):         AIKeyPressed(event, data)
    elif (data.mode == "help"):       helpKeyPressed(event, data)

def redrawAll(event, data):
    if (data.mode == "mainScreen"):   mainScreenRedrawAll(event, data)
    elif (data.mode == "twoP"):       twoPRedrawAll(event, data)
    elif (data.mode == "AI"):         AIRedrawAll(event, data)
    elif (data.mode == "help"):       helpRedrawAll(event, data)

######################################################
def mainScreenMousePressed(event, data):
    pass

def mainScreenKeyPressed(event, data):
    data.mode = "twoP"

def mainScreenRedrawAll(canvas, data):
    canvas.create_text(data.width/2, data.height/2-20,
                       text="This is a main screen!", font="Arial 26 bold")
    canvas.create_text(data.width/2, data.height/2+20,
                       text="Press any key to play!", font="Arial 20")

# these are from course notes
#######################################################

def twoPMousePressed(event, data):
    moveLogic(event, data)
        
def twoPKeyPressed(event, data):
    if (event.keysym == 'h'):
        data.prevMode = data.mode
        data.mode = "help"


def twoPRedrawAll(canvas, data):
    drawPiecesAndBoard(canvas, data)

# course notes run function
#######################################################

def AIMousePressed(event, data):
    AImoveLogic(event, data)
        
def AIKeyPressed(event, data):
    if (event.keysym == 'h'):
        data.prevMode = data.mode
        data.mode = "help"

def AIRedrawAll(canvas, data):
    drawPiecesAndBoard(canvas, data)

#######################################################

def helpMousePressed(event, data):
    data.mode == "twoP"

def helpKeyPressed(event, data):
    data.mode = data.prevMode

def helpRedrawAll(canvas, data):
    canvas.create_text(data.width // 2, data.height // 2, text = "How to play Chess")

#######################################################
def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    redrawAllWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")
run(800, 800)