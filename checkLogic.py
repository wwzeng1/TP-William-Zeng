from chesspiecesandboard import *
import copy
def findPiece(color, PieceType, board):
    squares = []
    for x in range(len(board)):
        for y in range(len(board)):
            if isinstance(board[x][y], PieceType) and board[x][y].giveColor() == color:
                squares.append([x, y])
    if len(squares) == 1:
        return squares[0]
    return squares

def inCheck(king, board):
    copyBoard = copy.deepcopy(board)
    kingX = king[0]
    kingY = king[1]
    for x in range(len(copyBoard)):
        for y in range(len(copyBoard)):
            square = copyBoard[x][y]
            if isinstance(square, Piece) and square.giveColor() != copyBoard[kingX][kingY].giveColor():
                if [kingX, kingY] in square.legalMoves(copyBoard): 
                    return True

def makeMove(board, piece, move, oldSquare):
    copyBoard = copy.deepcopy(board)
    x = move[0]
    y = move[1]
    copyBoard[x][y] = piece
    copyBoard[oldSquare[0]][oldSquare[1]] = 0
    return copyBoard

# def checkmate(king, board):
#     allLegalMoves = []
#     copyBoard = copy.deepcopy(board)
#     kingX = king[0]
#     kingY = king[1]
#     for x in range(len(copyBoard)):
#         for y in range(len(copyBoard)):
#             square = copyBoard[x][y]
#             if isinstance(square, Piece) and square.giveColor() == copyBoard[kingX][kingY].giveColor():
#                 allLegalMoves.extend(square.legalMoves(board))
#     print(allLegalMoves)
#     if allLegalMoves == []:
#         return True
#     return False
