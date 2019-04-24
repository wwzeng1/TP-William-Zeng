from tkinter import *
from chesspiecesandboard import *
from checkLogic import * 
from ai import *
from PIL import Image, ImageTk
import random
import copy
import webbrowser

# course notes framework
def init(data):
    data.mode = "mainScreen"
    data.cursorPos = 0
    data.prevMode = data.mode
    data.aiColor = "White"
    data.imageDict = dict()
    data.size = 100
    initPieces(data)
    importImages(data)

def importImages(data):
    pieces = ["WP", "BP", "WR", "BR", "WN", "BN", "WB", "BB", "WK", "BK", "WQ", "BQ"]
    for piece in pieces:
        pieceImage = Image.open("%s.png" % piece).resize((data.size, data.size), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(pieceImage)
        data.imageDict[piece] = image
    mainScreen = Image.open("mainScreen.png").resize((data.width, data.height), Image.ANTIALIAS)
    data.mainScreen = ImageTk.PhotoImage(mainScreen)
    move = Image.open("move.png").resize((data.size, data.size), Image.ANTIALIAS)
    data.highlight = ImageTk.PhotoImage(move)
    square = Image.open("wsquare.png").resize((data.size, data.size), Image.ANTIALIAS)
    data.square = ImageTk.PhotoImage(square)

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

def timerFired(data):
    if (data.mode == "AI"):AITimerFired(data)
    elif (data.mode == "twoP"): twoPTimerFired(data)

def redrawAll(event, data):
    if (data.mode == "mainScreen"):   mainScreenRedrawAll(event, data)
    elif (data.mode == "twoP"):       twoPRedrawAll(event, data)
    elif (data.mode == "AI"):         AIRedrawAll(event, data)
    elif (data.mode == "help"):       helpRedrawAll(event, data)

######################################################
def mainScreenMousePressed(event, data):
    modes = ["twoP", "AI", "help"]
    if 220 <= event.x <= 580:
        if 380 <= event.y <= 460:
            data.cursorPos = 0
            print(data.cursorPos)
            data.mode = modes[data.cursorPos]
        if 480 <= event.y <= 560:
            data.cursorPos = 1
            print(data.cursorPos)
            data.mode = modes[data.cursorPos]
        elif 580 <= event.y <= 660:
            data.cursorPos = 2
            print(data.cursorPos)
            data.mode = modes[data.cursorPos]

def mainScreenKeyPressed(event, data):
    modes = ["twoP", "AI", "help"]
    if event.keysym == "Down" and data.cursorPos < 2:
        data.cursorPos += 1
    elif event.keysym == "Up" and data.cursorPos > 0:
        data.cursorPos -= 1
    elif event.keysym == "Return":
        data.mode = modes[data.cursorPos]

def mainScreenRedrawAll(canvas, data):
    canvas.create_image(data.width // 2, data.height // 2, image = data.mainScreen)
    canvas.create_line(280, 445 + (105 * data.cursorPos), 520, 445 + (105 * data.cursorPos), fill = "#666666", width = 5)

# these are from course notes
#######################################################

def twoPMousePressed(event, data):
    moveLogic(event, data)
    print(boardValue(data.board))
        
def twoPKeyPressed(event, data):
    if (event.keysym == 'h'):
        data.prevMode = data.mode
        data.mode = "help"
    elif (event.keysym == "p"):
        data.mode = "mainScreen"

def twoPTimerFired(data):
    pass

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
    elif (event.keysym == "p"):
        data.mode = "mainScreen"

def AITimerFired(data):
    aiMoves(data)

def AIRedrawAll(canvas, data):
    drawPiecesAndBoard(canvas, data)

#######################################################

def helpMousePressed(event, data):
    webbrowser.open('https://www.instructables.com/id/Playing-Chess/')

def helpKeyPressed(event, data):
    if event.keysym == "p":
        data.mode = "mainScreen"
    else: 
        data.mode = data.prevMode

def helpRedrawAll(canvas, data):
    canvas.create_text(data.width // 2, data.height // 2, text = "How To play Chess")

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

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
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
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")
run(800, 800)