from tkinter import *
# xs are side to side
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
        self.padding = 30
    def draw(self, canvas):
        for sideCell in range(self.cells):
            for vertCell in range(self.cells):
                if (sideCell + vertCell) % 2 == 0:
                    canvas.create_rectangle(self.width // self.cells * sideCell, self.height // self.cells * vertCell, 
                        self.width // self.cells * (sideCell + 1), self.height // self.cells * (vertCell + 1))
                else:
                    canvas.create_rectangle(self.width // self.cells * sideCell, self.height // self.cells * vertCell, 
                        self.width // self.cells * (sideCell + 1), self.height // self.cells * (vertCell + 1), fill = "Black")
    def highlightPossibleMove(self, canvas, move):
        canvas.create_oval((self.width // self.cells * move[0]) + self.padding, (self.height // self.cells * move[1]) + self.padding, 
                        (self.width // self.cells * (move[0] + 1)) - self.padding, (self.height // self.cells * (move[1] + 1)) - self.padding, fill = "Dark Grey", width = 0)
    
class Piece():
    def __init__(self, color, x, y):
        self.x = x
        self.y = y
        self.name = "X"
        self.cells = 8
        self.padding = 7
        self.color = color
    def draw(self, canvas, width, height):
        canvas.create_oval((width // self.cells) * self.x + self.padding, (height // self.cells) * self.y + self.padding, 
                        (width // self.cells) * (self.x + 1) - self.padding, 
                        (height // self.cells) * (self.y + 1) - self.padding, fill = self.color, outline = "Grey")
        canvas.create_text(width // self.cells * (self.x + 0.5), height // self.cells * (self.y + 0.5), text = self.name, fill = "Grey")
    def __eq__(self, other):
        return isinstance(other, Piece) and other.x == self.x and other.y == self.y
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
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.name = self.color[0] + "P"
    def move(self, move):
        self.x = move[0]
        self.y = move[1]
    def legalMoves(self, board):
        possibleMoves = []
        return possibleMoves

class King(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.name = self.color[0] + "K"
    def move(self, move):
        self.x = move[0]
        self.y = move[1]
    def legalMoves(self, board):
        possibleMoves = []
        moves = [[self.rank, self.file + 1], [self.rank, self.file - 1], [self.rank + 1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
        return possibleMoves

class Bishop(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.name = self.color[0] + "B"
    def move(self, move):
        self.x = move[0]
        self.y = move[1]
    def legalMoves(self, board): 
        possibleMoves = []
        
        checkSquare = [self.x, self.y]
        if checkSquare[0] - 1 >= 0 and checkSquare[1] - 1 >= 0 and isinstance(board[checkSquare[0] - 1][checkSquare[1] - 1], Piece) \
            and board[checkSquare[0] - 1][checkSquare[1] - 1].color != self.color:
                possibleMoves.append([checkSquare[0] - 1, checkSquare[1] - 1])
        while checkSquare[0] - 1 >= 0 and checkSquare[1] - 1 >= 0 and board[checkSquare[0] - 1][checkSquare[1] - 1] == 0:
            checkSquare = [checkSquare[0] - 1, checkSquare[1] - 1]
            possibleMoves.append(checkSquare)
            if checkSquare[0] - 1 >= 0 and checkSquare[1] - 1 >= 0 and isinstance(board[checkSquare[0] - 1][checkSquare[1] - 1], Piece) \
            and board[checkSquare[0] - 1][checkSquare[1] - 1].color != self.color:
                possibleMoves.append([checkSquare[0] - 1, checkSquare[1] - 1])

        checkSquare = [self.x, self.y]
        if checkSquare[0] + 1 <= 7 and checkSquare[1] - 1 >= 0 and isinstance(board[checkSquare[0] + 1][checkSquare[1] - 1], Piece) \
            and board[checkSquare[0] + 1][checkSquare[1] - 1].color != self.color:
                possibleMoves.append([checkSquare[0] + 1, checkSquare[1] - 1])
        while checkSquare[0] + 1 <= 7 and checkSquare[1] - 1 >= 0 and board[checkSquare[0] + 1][checkSquare[1] - 1] == 0:
            checkSquare = [checkSquare[0] + 1, checkSquare[1] - 1]
            possibleMoves.append(checkSquare)
            if checkSquare[0] + 1 <= 7 and checkSquare[1] - 1 >= 0 and isinstance(board[checkSquare[0] + 1][checkSquare[1] - 1], Piece) \
            and board[checkSquare[0] + 1][checkSquare[1] - 1].color != self.color:
                possibleMoves.append([checkSquare[0] + 1, checkSquare[1] - 1])

        checkSquare = [self.x, self.y]
        if checkSquare[0] + 1 <= 7 and checkSquare[1] + 1 <= 7 and isinstance(board[checkSquare[0] + 1][checkSquare[1] + 1], Piece) \
            and board[checkSquare[0] + 1][checkSquare[1] + 1].color != self.color:
                possibleMoves.append([checkSquare[0] + 1, checkSquare[1] + 1])
        while checkSquare[0] + 1 <= 7 and checkSquare[1] + 1 <= 7 and board[checkSquare[0] + 1][checkSquare[1] + 1] == 0:
            checkSquare = [checkSquare[0] + 1, checkSquare[1] + 1]
            possibleMoves.append(checkSquare)
            if checkSquare[0] + 1 <= 7 and checkSquare[1] + 1 <= 7 and isinstance(board[checkSquare[0] + 1][checkSquare[1] + 1], Piece) \
            and board[checkSquare[0] + 1][checkSquare[1] + 1].color != self.color:
                possibleMoves.append([checkSquare[0] + 1, checkSquare[1] + 1])

        checkSquare = [self.x, self.y]
        if checkSquare[0] - 1 >= 0 and checkSquare[1] + 1 <= 7 and isinstance(board[checkSquare[0] - 1][checkSquare[1] + 1], Piece) \
            and board[checkSquare[0] - 1][checkSquare[1] + 1].color != self.color:
                possibleMoves.append([checkSquare[0] - 1, checkSquare[1] + 1])
        while checkSquare[0] - 1 >= 0 and checkSquare[1] + 1 <= 7 and board[checkSquare[0] - 1][checkSquare[1] + 1] == 0:
            checkSquare = [checkSquare[0] - 1, checkSquare[1] + 1]
            possibleMoves.append(checkSquare)
            if checkSquare[0] - 1 >= 0 and checkSquare[1] + 1 <= 7 and isinstance(board[checkSquare[0] - 1][checkSquare[1] + 1], Piece) \
            and board[checkSquare[0] - 1][checkSquare[1] + 1].color != self.color:
                possibleMoves.append([checkSquare[0] - 1, checkSquare[1] + 1])

        return possibleMoves

class Rook(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.name = self.color[0] + "R"
    def move(self, move):
        self.x = move[0]
        self.y = move[1]
    def legalMoves(self, board): 
        possibleMoves = []

        checkSquare = [self.x, self.y]
        if checkSquare[1] - 1 >= 0 and isinstance(board[checkSquare[0]][checkSquare[1] - 1], Piece) \
        and board[checkSquare[0]][checkSquare[1] - 1].color != self.color:
            possibleMoves.append([checkSquare[0], checkSquare[1] - 1])
        while checkSquare[1] - 1 >= 0 and board[checkSquare[0]][checkSquare[1] - 1] == 0:
            checkSquare = [checkSquare[0], checkSquare[1] - 1]
            possibleMoves.append(checkSquare)
            if checkSquare[1] - 1 >= 0 and isinstance(board[checkSquare[0]][checkSquare[1] - 1], Piece) \
            and board[checkSquare[0]][checkSquare[1] - 1].color != self.color:
                possibleMoves.append([checkSquare[0], checkSquare[1] - 1])

        checkSquare = [self.x, self.y]
        if checkSquare[1] + 1 <= 7 and isinstance(board[checkSquare[0]][checkSquare[1] + 1], Piece) \
        and board[checkSquare[0]][checkSquare[1] + 1].color != self.color:
            possibleMoves.append([checkSquare[0], checkSquare[1] + 1])
        while checkSquare[1] + 1 <= 7 and board[checkSquare[0]][checkSquare[1] + 1] == 0:
            checkSquare = [checkSquare[0], checkSquare[1] + 1]
            possibleMoves.append(checkSquare)
            if checkSquare[1] + 1 <= 7 and isinstance(board[checkSquare[0]][checkSquare[1] + 1], Piece) \
            and board[checkSquare[0]][checkSquare[1] + 1].color != self.color:
                possibleMoves.append([checkSquare[0], checkSquare[1] + 1])

        checkSquare = [self.x, self.y] 
        if checkSquare[0] - 1 >= 0 and isinstance(board[checkSquare[0] - 1][checkSquare[1]], Piece) \
            and board[checkSquare[0] - 1][checkSquare[1]].color != self.color:
                possibleMoves.append([checkSquare[0] - 1, checkSquare[1]])   
        while checkSquare[0] - 1 >= 0 and board[checkSquare[0] - 1][checkSquare[1]] == 0:
            checkSquare = [checkSquare[0] - 1, checkSquare[1]]
            possibleMoves.append(checkSquare)
            if checkSquare[0] - 1 >= 0 and isinstance(board[checkSquare[0] - 1][checkSquare[1]], Piece) \
            and board[checkSquare[0] - 1][checkSquare[1]].color != self.color:
                possibleMoves.append([checkSquare[0] - 1, checkSquare[1]])

        checkSquare = [self.x, self.y]
        if checkSquare[0] + 1 <= 7 and isinstance(board[checkSquare[0] + 1][checkSquare[1]], Piece) \
            and board[checkSquare[0] + 1][checkSquare[1]].color != self.color:
                possibleMoves.append([checkSquare[0] + 1, checkSquare[1]])    
        while checkSquare[0] + 1 <= 7 and board[checkSquare[0] + 1][checkSquare[1]] == 0:
            checkSquare = [checkSquare[0] + 1, checkSquare[1]]
            possibleMoves.append(checkSquare)
            if checkSquare[0] + 1 <= 7 and isinstance(board[checkSquare[0] + 1][checkSquare[1]], Piece) \
            and board[checkSquare[0] + 1][checkSquare[1]].color != self.color:
                possibleMoves.append([checkSquare[0] + 1, checkSquare[1]])
        return possibleMoves

class Knight(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.name = self.color[0] + "N"
    def move(self, move):
        self.x = move[0]
        self.y = move[1]
    def isLegal(self, move, board): # return list of possible moves
        pass

class Queen(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.name = self.color[0] + "Q"
    def move(self, move):
        self.x = move[0]
        self.y = move[1]
    def isLegal(self, move, board): # return list of possible moves
        pass

def init(data):
    data.cells = 8
    data.board = [[0 for i in range(data.cells)] for j in range(data.cells)]
    data.chessBoard = Board(data.width, data.height)
    # for y in range(data.cells):
    #     data.board[6][y] = Pawn("White", 6, y)
    #     data.board[1][y] = Pawn("Black", 1, y)
    data.board[4][7] = King("White", 4, 7)
    data.board[3][7] = Queen("White", 3, 7)
    data.board[5][7] = Bishop("White", 5, 7)
    data.board[2][7] = Bishop("White", 2, 7) 
    data.board[6][7] = Knight("White", 6, 7)
    data.board[1][7] = Knight("White", 1, 7) 
    data.board[7][7] = Rook("White", 7, 7)
    data.board[0][7] = Rook("White", 0, 7)

    data.board[4][0] = King("Black", 4, 0)
    data.board[3][0] = Queen("Black", 3, 0)
    data.board[5][0] = Bishop("Black", 5, 0)
    data.board[2][0] = Bishop("Black", 2, 0)
    data.board[6][0] = Knight("Black", 6, 0)
    data.board[1][0] = Knight("Black", 1, 0) 
    data.board[7][0] = Rook("Black", 7, 0)
    data.board[0][0] = Rook("Black", 0, 0)

    data.selectedPiece = 0
    data.oldSquare = (0, 0)
    data.isWTurn = True
    data.moveList = []

def sign(num):
    if num >= 0:
        return 1
    else:
        return -1

def findKing(data, color, board):
    for x in range(len(board)):
        for y in range(len(board[x])):
            if isinstance(board[x][y], King) and board[x][y].color == color:
                return (x, y)

@print2DListResult
def printBoard(data):
    return data.board
# find all possible moves,


def mousePressed(event, data):
    printBoard(data)
    if data.selectedPiece == 0:
        x = event.x // (data.width // data.cells)
        y = event.y // (data.height // data.cells)
        data.selectedPiece = data.board[x][y]
        if isinstance(data.selectedPiece, Piece):
            data.moveList = data.selectedPiece.legalMoves(data.board)
        data.oldSquare = [x, y]
    else:
        king = findKing(data, data.selectedPiece.color, data.board)
        x = event.x // (data.width // data.cells)
        y = event.y // (data.height // data.cells)
        move = [x, y]
        print(data.moveList)
        if (move in data.moveList): # and data.selectedPiece.isTurn(data.isWTurn) and data.oldSquare != move:
            data.selectedPiece.move(move) # is king checked helper function, return True if not checked
            # make move then check if the king is checked, then undo move 
            data.board[x][y] = data.selectedPiece
            data.board[data.oldSquare[0]][data.oldSquare[1]] = 0
            data.selectedPiece = 0
            data.isWTurn = not data.isWTurn
            data.moveList = []
        else:
            data.selectedPiece = 0
            data.moveList = []
        
def keyPressed(event, data):
    pass

def redrawAll(canvas, data):
    data.chessBoard.draw(canvas)
    for row in data.board:
        for item in row:
            if item != 0:
                item.draw(canvas, data.width, data.height)
    for move in data.moveList:
        data.chessBoard.highlightPossibleMove(canvas, move)
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