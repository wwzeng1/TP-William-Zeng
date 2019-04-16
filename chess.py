from tkinter import *
# ranks are side to side
class Board():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = 8
    def draw(self, canvas):
        for sideCell in range(self.cells):
            for vertCell in range(self.cells):
                if (sideCell + vertCell) % 2 == 0:
                    canvas.create_rectangle(self.width // self.cells * sideCell, self.height // self.cells * vertCell, 
                        self.width // self.cells * (sideCell + 1), self.height // self.cells * (vertCell + 1))
                else:
                    canvas.create_rectangle(self.width // self.cells * sideCell, self.height // self.cells * vertCell, 
                        self.width // self.cells * (sideCell + 1), self.height // self.cells * (vertCell + 1), fill = "Black")
class Piece():
    def __init__(self, color, rank, file):
        self.rank = rank
        self.file = file
        self.name = "X"
        self.cells = 8
        self.padding = 7
        self.color = color
    def draw(self, canvas, width, height):
        canvas.create_oval((width // self.cells) * self.rank + self.padding, (height // self.cells) * self.file + self.padding, 
                        (width // self.cells) * (self.rank + 1) - self.padding, 
                        (height // self.cells) * (self.file + 1) - self.padding, fill = self.color, outline = "Grey")
        canvas.create_text(width // self.cells * (self.rank + 0.5), height // self.cells * (self.file + 0.5), text = self.name, fill = "Grey")
    def __eq__(self, other):
        return isinstance(other, Piece) and other.rank == self.rank and other.file == self.file
    def __hash__(self):
        return hash(self.color)
class Pawn(Piece):
    def __init__(self, color, rank, file):
        super().__init__(color, rank, file)
        self.name = "P"
    def move(self, move):
        self.rank = move[0]
        self.file = move[1]
    def isLegal(self, move, board):
        checkRank, checkFile = move[0], move[1]  
        square = board[checkRank][checkFile]
        if self.color == "Black":
            return square == 0 
        if self.color == "White":
            return square == 0 
def init(data):
    data.cells = 8
    data.board = [[0 for i in range(data.cells)] for j in range(data.cells)]
    data.chessBoard = Board(data.width, data.height)
    for rank in range(data.cells):
        data.board[rank][1] = Pawn("White", rank, 1)
        data.board[rank][6] = Pawn("Black", rank, 6)
    data.selectedPiece = 0
    data.oldSquare = (0, 0)

def mousePressed(event, data):
    print(data.board)
    if data.selectedPiece == 0:
        rank = event.x // (data.width // data.cells)
        file = event.y // (data.height // data.cells)
        data.selectedPiece = data.board[rank][file]
        data.oldSquare = (rank, file)
        print(data.selectedPiece)
    else:
        rank = event.x // (data.width // data.cells)
        file = event.y // (data.height // data.cells)
        move = (rank, file)
        if data.selectedPiece.isLegal(move, data.board):
            data.selectedPiece.move(move)
            data.board[rank][file] = data.selectedPiece
            data.board[data.oldSquare[0]][data.oldSquare[1]] = 0
            data.selectedPiece = 0
        else:
            data.board[data.oldSquare[0]][data.oldSquare[1]] = 0
            data.selectedPiece = 0
            
    
def keyPressed(event, data):
    pass

def redrawAll(canvas, data):
    data.chessBoard.draw(canvas)
    for row in data.board:
        for item in row:
            if item != 0:
                item.draw(canvas, data.width, data.height)
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

run(400, 400)