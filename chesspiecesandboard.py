from tkinter import *
from PIL import Image, ImageTk
class Board():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = 8
        self.padding = 30
    def draw(self, canvas, image):     
        for sideCell in range(self.cells):
            for vertCell in range(self.cells):
                if (sideCell + vertCell) % 2 == 0:
                    canvas.create_rectangle(self.width // self.cells * sideCell, self.height // self.cells * vertCell, 
                        self.width // self.cells * (sideCell + 1), self.height // self.cells * (vertCell + 1), fill = "White", width = 0)
                else:
                    canvas.create_image(self.width // self.cells * (sideCell + 0.5), self.height // self.cells * (vertCell + 0.5), image = image)
    def highlightPossibleMove(self, canvas, move, image):
        canvas.create_image((self.width // self.cells * (move[0] + 0.5)), (self.height // self.cells * (move[1] + 0.5)), 
                        image = image)
    def drawMate(self, canvas, width, height):
        canvas.create_text(width // 2, height // 2, text = "CHECKMATE", font=("Courier", 44))
    
class Piece():
    def __init__(self, color, x, y):
        self.x = x
        self.y = y
        self.name = "X"
        self.cells = 8
        self.padding = 7
        self.color = color
    def draw(self, canvas, width, height, imageDict):
        canvas.create_image(100 * (self.x + 0.5), 100 * (self.y + 0.5), image = imageDict[self.name])
    def __eq__(self, other):
        return isinstance(other, Piece) and other.x == self.x and other.y == self.y
    def __repr__(self):
        return self.name
    def __hash__(self):
        return hash(self.color)
    def giveColor(self):
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
        self.value = 10
        if self.color == "White": self.promRank = 0
        else: self.promRank = 7
    def move(self, move):
        self.x = move[0]
        self.y = move[1]
    def legalMoves(self, board):
        possibleMoves = []
        if self.color == "Black":
            if board[self.x][self.y + 1] == 0:
                possibleMoves.append([self.x, self.y + 1])
                if (self.y == 1) and board[self.x][self.y + 2] == 0:
                    possibleMoves.append([self.x, self.y + 2])
            if self.x > 0 and board[self.x - 1][self.y + 1] != 0 and board[self.x - 1][self.y + 1].color != "Black":
                possibleMoves.append([self.x - 1, self.y + 1])
            if self.x < 7 and board[self.x + 1][self.y + 1] != 0 and board[self.x + 1][self.y + 1].color != "Black":
                possibleMoves.append([self.x + 1, self.y + 1])
        if self.color == "White":
            if board[self.x][self.y - 1] == 0:
                possibleMoves.append([self.x, self.y - 1])
                if (self.y == 6) and board[self.x][self.y - 2] == 0:
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
        self.value = 1000
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
                if not rook.hasMoved():
                    possibleMoves.append([self.x + 2, self.y])
            if board[self.x - 1][self.y] == board[self.x - 2][self.y] == board[self.x - 3][self.y] == 0 \
            and isinstance(board[self.x - 4][self.y], Rook):
                rook = board[self.x - 4][self.y]
                if not rook.hasMoved():
                    possibleMoves.append([self.x - 2, self.y])
        return possibleMoves

    

class Bishop(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.name = self.color[0] + "B"
        self.value = 32
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
        self.value = 50
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
        self.value = 31
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
        self.value = 90
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