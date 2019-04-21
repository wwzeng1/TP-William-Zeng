from tkinter import *
from chesspiecesandboard import *
from checkLogic import * 
import copy
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

@print2DListResult
def printBoard(board):
    return board

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
    data.gameOver = False






def mousePressed(event, data):
    if data.selectedPiece == 0:
        x = event.x // (data.width // data.cells)
        y = event.y // (data.height // data.cells)
        data.selectedPiece = data.board[x][y]
        data.oldSquare = [x, y]
        if isinstance(data.selectedPiece, Piece):
            king = findPiece(data.selectedPiece.giveColor(), King, data.board)
            data.moveList = data.selectedPiece.legalMoves(data.board)
            copyMoveList = copy.deepcopy(data.moveList)
            for checkMove in data.moveList:
                checkBoard = makeMove(data.board, data.selectedPiece, checkMove, data.oldSquare)
                newKing = findPiece(data.selectedPiece.giveColor(), King, checkBoard)
                if inCheck(newKing, checkBoard):
                    copyMoveList.remove(checkMove)
            data.moveList = copyMoveList
    else:
        x = event.x // (data.width // data.cells)
        y = event.y // (data.height // data.cells)
        pieceX = data.oldSquare[0]
        pieceY = data.oldSquare[1]
        move = [x, y]
        if (move in data.moveList) and data.selectedPiece.isTurn(data.isWTurn):
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
        
# course notes
def keyPressed(event, data):
    pass

# course notes
def redrawAll(canvas, data):
    data.chessBoard.draw(canvas)
    for row in data.board:
        for item in row:
            if item != 0:
                item.draw(canvas, data.width, data.height)
    for move in data.moveList:
        data.chessBoard.highlightPossibleMove(canvas, move)
    if data.gameOver:
        canvas.create(50, 50, data.width - 50, data.height - 50, fill = "Red")

# course notes run function
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