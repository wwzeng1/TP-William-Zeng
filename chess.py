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
        bMoves = [[self.x, self.y + 1], [self.x, self.y + 2]]
        bCapture = [[self.x - 1, self.y + 1], [self.x + 1, self.y + 1]]
        if self.color == "Black":
            if board[self.x][self.y + 1] == 0:
                possibleMoves.append([self.x, self.y + 1])
                if board[self.x][self.y + 2] == 0 and (self.y == 1):
                    possibleMoves.append([self.x, self.y + 2])
            if self.x > 0 and board[self.x - 1][self.y + 1] != 0 and board[self.x - 1][self.y + 1].color != "Black":
                possibleMoves.append([self.x - 1, self.y + 1])
            if self.x < 7 and board[self.x + 1][self.y + 1] != 0 and board[self.x + 1][self.y + 1].color != "Black":
                possibleMoves.append([self.x + 1, self.y + 1])
        if self.color == "White":
            if board[self.x][self.y - 1] == 0:
                possibleMoves.append([self.x, self.y - 1])
                if board[self.x][self.y - 2] == 0 and (self.y == 6):
                    possibleMoves.append([self.x, self.y - 2])
            if self.x > 0 and board[self.x - 1][self.y - 1] != 0 and board[self.x - 1][self.y - 1].color != "White":
                possibleMoves.append([self.x - 1, self.y - 1])
            if self.x < 7 and board[self.x + 1][self.y - 1] != 0 and board[self.x + 1][self.y - 1].color != "White":
                possibleMoves.append([self.x + 1, self.y - 1])
        return possibleMoves

class King(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.name = self.color[0] + "K"
        self.moved = False
    def move(self, move):
        self.x = move[0]
        self.y = move[1]
        self.moved = True
    def legalMoves(self, board):
        possibleMoves = []
        moves = [[self.x, self.y + 1], [self.x, self.y - 1], [self.x + 1, self.y], \
        [self.x - 1, self.y], [self.x + 1, self.y + 1], [self.x + 1, self.y - 1], \
        [self.x - 1, self.y + 1], [self.x - 1, self.y - 1]]
        for move in moves:
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7: 
                checkSquare = board[move[0]][move[1]]
                if checkSquare == 0 or checkSquare.color != self.color:
                    possibleMoves.append(move)
        if not self.moved:
            if board[self.x + 1][self.y] == board[self.x + 2][self.y] == 0 \
            and isinstance(board[self.x + 3][self.y], Rook):
                rook = board[self.x + 3][self.y]
                print("KINGSIDE CASTLE")
                if not rook.hasMoved():
                    possibleMoves.append([self.x + 2, self.y])
            if board[self.x - 1][self.y] == board[self.x - 2][self.y] == board[self.x - 3][self.y] == 0 \
            and isinstance(board[self.x - 4][self.y], Rook):
                rook = board[self.x - 4][self.y]
                print("QUEENSIDE CASTLE")
                if not rook.hasMoved():
                    possibleMoves.append([self.x - 2, self.y])
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
        self.moved = False
    def move(self, move):
        self.x = move[0]
        self.y = move[1]
        self.moved = True
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
    def hasMoved(self):
        return self.moved

class Knight(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.name = self.color[0] + "N"
    def move(self, move):
        self.x = move[0]
        self.y = move[1]
    def legalMoves(self, board):
        possibleMoves = []
        moves = [[self.x + 1, self.y + 2], [self.x + 1, self.y - 2], [self.x + 2, self.y + 1], \
        [self.x + 2, self.y - 1], [self.x - 2, self.y + 1], [self.x - 2, self.y - 1], \
        [self.x - 1, self.y + 2], [self.x - 1, self.y - 2]]
        for move in moves:
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7: 
                checkSquare = board[move[0]][move[1]]
                if checkSquare == 0 or checkSquare.color != self.color:
                    possibleMoves.append(move)
        return possibleMoves

class Queen(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.name = self.color[0] + "Q"
    def move(self, move):
        self.x = move[0]
        self.y = move[1]
    def legalMoves(self, board): # return list of possible moves
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
        
def init(data):
    data.cells = 8
    data.board = [[0 for i in range(data.cells)] for j in range(data.cells)]
    data.chessBoard = Board(data.width, data.height)
    for x in range(data.cells):
        data.board[x][6] = Pawn("White", x, 6)
        data.board[x][1] = Pawn("Black", x, 1)
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

def findPiece(color, PieceType, board):
    squares = []
    for x in range(len(board)):
        for y in range(len(board[x])):
            if isinstance(board[x][y], PieceType) and board[x][y].color == color:
                squares.append([x, y])
    return squares

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
        king = findPiece(data.selectedPiece.color, King, data.board)
        x = event.x // (data.width // data.cells)
        y = event.y // (data.height // data.cells)
        pieceX = data.oldSquare[0]
        pieceY = data.oldSquare[1]
        move = [x, y]
        print(data.moveList)
        if (move in data.moveList):# and data.selectedPiece.isTurn(data.isWTurn):
            data.selectedPiece.move(move)
            if isinstance(data.selectedPiece, King) and move == [pieceX + 2, pieceY]:
                data.board[pieceX + 3][pieceY].move([pieceX + 1, pieceY])
                data.board[pieceX + 1][pieceY] = data.board[pieceX + 3][pieceY] 
                data.board[pieceX + 3][pieceY] = 0
            if isinstance(data.selectedPiece, King) and move == [pieceX - 2, pieceY]:
                data.board[pieceX - 4][pieceY].move([pieceX - 1, pieceY])
                data.board[pieceX - 1][pieceY] = data.board[pieceX - 4][pieceY] 
                data.board[pieceX - 4][pieceY] = 0
             # is king checked helper function, return True if not checked
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