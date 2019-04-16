from tkinter import *
# ranks are side to side
def print2DListResult(f):
    def p(*args):
        lst = f(*args)
        # spaces and rows for formatting, also uses indents
        row, total, space, indentNum = "", "", " ", 5
        indent = space * (indentNum - 1)
        # 2d list that creates rows, appends them to a longer string
        for i in lst:
            for j in i:
                j = str(j)
                spaces = space * (indentNum - len(j) + 1)
                row += j + spaces
            # uses a new line and also clears each row to fill it in again
            total += "[" + indent + row + "]" + "\n"
            row = ""
        print(total)
    return p

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
        canvas.create_oval((width // self.cells) * self.file + self.padding, (height // self.cells) * self.rank + self.padding, 
                        (width // self.cells) * (self.file + 1) - self.padding, 
                        (height // self.cells) * (self.rank + 1) - self.padding, fill = self.color, outline = "Grey")
        canvas.create_text(width // self.cells * (self.file + 0.5), height // self.cells * (self.rank + 0.5), text = self.name, fill = "Grey")
    def __eq__(self, other):
        return isinstance(other, Piece) and other.rank == self.rank and other.file == self.file
    def __repr__(self):
        return self.name
    def __hash__(self):
        return hash(self.color)
    def color(self):
        return self.color
    def isTurn(self, isTurn):
        if self.color == "White" and isTurn:
            return True
        elif self.color == "Black" and not isTurn:
            return True
class Pawn(Piece):
    def __init__(self, color, rank, file):
        super().__init__(color, rank, file)
        self.name = self.color[0] + "P"
    def move(self, move):
        self.rank = move[0]
        self.file = move[1]
    def isLegal(self, move, board):
        checkRank, checkFile = move[0], move[1]  
        square = board[checkRank][checkFile]
        numMoves = False
        capture = False
        if self.color == "Black" and square == 0:
            if self.rank == 1: 
                numMoves = ((checkRank in (self.rank + 1, self.rank + 2) and checkFile == self.file))
            else:
                numMoves = ((checkRank == self.rank + 1) and checkFile == self.file)
            return numMoves
        elif self.color == "White" and square == 0:
            if self.rank == 6: 
                numMoves = ((checkRank in (self.rank - 1, self.rank - 2) and checkFile == self.file))
            else:
                numMoves = ((checkRank == self.rank - 1) and checkFile == self.file)
            return numMoves
        elif isinstance(square, Piece) and square.color != self.color:
            if self.color == "White":
                capture = ((self.rank - checkRank) == 1 and abs(self.file - checkFile) == 1) 
            elif self.color == "Black":
                capture = ((self.rank - checkRank) == -1 and abs(self.file - checkFile) == 1)
            return capture 




class King(Piece):
    def __init__(self, color, rank, file):
        super().__init__(color, rank, file)
        self.name = self.color[0] + "K"
    def move(self, move):
        self.rank = move[0]
        self.file = move[1]
    def isLegal(self, move, board):
        checkRank, checkFile = move[0], move[1]  
        square = board[checkRank][checkFile]
        numMoves = False
        if square == 0:
            numMoves = (abs(checkFile - self.file) <= 1 and abs(checkRank - self.rank) <= 1)
            return numMoves
        elif isinstance(square, Piece) and square.color != self.color:
                return abs(self.rank - checkRank) <= 1 and abs(self.file - checkFile) <= 1

class Bishop(Piece):
    def __init__(self, color, rank, file):
        super().__init__(color, rank, file)
        self.name = self.color[0] + "B"
    def move(self, move):
        self.rank = move[0]
        self.file = move[1]
    def isLegal(self, move, board):
        checkRank, checkFile = move[0], move[1]
        diagonal = False
        empty = True
        rSign, fSign = sign(checkRank - self.rank), sign(checkFile - self.file)
        if abs(checkRank - self.rank) == abs(checkFile - self.file):
            diagonal = True
        for eRank in range(checkRank, (self.rank - rSign), rSign):
            for eFile in range(checkFile, (self.file - fSign), fSign):
                print(board[eRank][eFile])
                if board[eRank][eFile] != 0:
                    empty = False
        print(str((rSign, fSign)) + str(empty) + str(diagonal) + " " + str(checkRank) + " " + str(self.rank) + " " + str(checkFile) + " " + str(self.file))
        return empty and diagonal
def init(data):
    data.cells = 8
    data.board = [[0 for i in range(data.cells)] for j in range(data.cells)]
    data.chessBoard = Board(data.width, data.height)
    for file in range(data.cells):
        data.board[6][file] = Pawn("White", 6, file)
        data.board[1][file] = Pawn("Black", 1, file)
    data.board[7][4] = King("White", 7, 4)
    data.board[7][5] = Bishop("White", 7, 5)
    data.board[7][2] = Bishop("White", 7, 2) 
    data.board[0][4] = King("Black", 0, 4)
    data.board[0][5] = Bishop("Black", 0, 5)
    data.board[0][2] = Bishop("Black", 0, 2) 
    data.selectedPiece = 0
    data.oldSquare = (0, 0)
    data.isWTurn = True

def sign(num):
    if num >= 0:
        return 1
    else:
        return -1

def findKing(data, color, board):
    for rank in range(len(board)):
        for file in range(len(board[rank])):
            if isinstance(board[rank][file], King) and board[rank][file].color == color:
                return (rank, file)
@print2DListResult
def printBoard(data):
    return data.board
def mousePressed(event, data):
    printBoard(data)
    if data.selectedPiece == 0:
        rank = event.y // (data.height // data.cells)
        file = event.x // (data.width // data.cells)
        data.selectedPiece = data.board[rank][file]
        data.oldSquare = (rank, file)
        print(data.selectedPiece)
    else:
        king = findKing(data, data.selectedPiece.color, data.board)
        file = event.x // (data.width // data.cells)
        rank = event.y // (data.height // data.cells)
        move = (rank, file)
        if data.selectedPiece.isLegal(move, data.board) and data.selectedPiece.isTurn(data.isWTurn):
            data.selectedPiece.move(move)
            data.board[rank][file] = data.selectedPiece
            data.board[data.oldSquare[0]][data.oldSquare[1]] = 0
            data.selectedPiece = 0
            data.isWTurn = not data.isWTurn
        else:
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

run(600, 600)