from chesspiecesandboard import *
from checkLogic import * 
import copy
import random


def AImoveLogic(event, data):
	if (data.isWTurn == True and data.aiColor == "Black") or (data.isWTurn == False and data.aiColor == "White"):
		moveLogic(event, data)

def aiMoves(data):
	if not (data.isWTurn == True and data.aiColor == "Black") and not (data.isWTurn == False and data.aiColor == "White"):
		data.isWTurn = not data.isWTurn
		if data.aiColor == "White": isMaximisingPlayer = True
		else: isMaximisingPlayer = False
		(square, move) = minimaxRoot(2, data.board, isMaximisingPlayer)
		print((square, move))
		piece = data.board[square[0]][square[1]]
		print(piece)
		piece.move(move)
		data.board[move[0]][move[1]] = piece
		data.board[square[0]][square[1]] = 0
		printBoard(data.board)		

def generateAllMoves(color, board):
	pieces = []
	movesList = []
	for x in range(len(board)):
		for y in range(len(board)):
			if isinstance(board[x][y], Piece) and board[x][y].giveColor() == color:
				pieces.append([x, y])
	for piece in pieces:
		x = piece[0]
		y = piece[1]
		oldSquare = [x, y]
		square = board[x][y]
		moveList = square.legalMoves(board)
		if moveList != []:
			# for checkMove in moveList:
			# 		checkBoard = makeMove(board, square, checkMove, oldSquare)
			# 		king = findPiece(square.giveColor(), King, checkBoard)
			# 		if inCheck(king, checkBoard):
			# 			moveList.remove(checkMove)
			for move in moveList:
				movesList.append((square, move, oldSquare))
	return movesList

def boardValue(board):
	pST = dict()
	pST["P"] = [[0, 0, 0, 0, 0, 0, 0, 0],
				[5, 5, 5, 5, 5, 5, 5, 5],
				[1, 1, 2, 3, 3, 2, 1, 1],
				[.5, .5, 1, 2.5, 2.5, 1, .5, .5],
				[0, 0, 0, 2, 2, 0, 0, 0],
				[.5, -.5, -1, 0, 0, -1, -.5, .5],
				[.5, 1, 1,-2,-2, 1, 1, .5],
				[0, 0, 0, 0, 0, 0, 0, 0]]
	pST["R"] = [[0, 0, 0, 0, 0, 0, 0, 0],
				[.5, 1, 1, 1, 1, 1, 1, .5],
				[-.5, 0, 0, 0, 0, 0, 0, -.5],
				[-.5, 0, 0, 0, 0, 0, 0, -.5],
				[-.5, 0, 0, 0, 0, 0, 0, -.5],
				[-.5, 0, 0, 0, 0, 0, 0, -.5],
				[-.5, 0, 0, 0, 0, 0, 0, -.5],
				[0, 0, 0, 5, 5, 0, 0, 0]]
	pST["Q"] = [[-2,-1,-1, -.5, -.5,-1,-1,-2],
				[-1,  0,  0,  0,  0,  0,  0,-1],
				[-1,  0,  5,  5,  5,  5,  0,-1],
				[-.5,  0,  .5,  .5,  .5,  .5,  0, -.5],
				[0,  0,  .5,  .5,  .5,  .5,  0, -.5],
				[-1,  .5,  .5,  .5,  .5,  .5,  0, -1],
				[-1,  0,  .5,  0,  0,  0,  0, -1],
				[-2,-1,-1, -.5, -.5,-1,-1,-2]]
	pST["K"] = [[-3,-4,-4,-5,-5,-4,-4,-3],
				[-3,-4,-4,-5,-5,-4,-4,-3],
				[-3,-4,-4,-5,-5,-4,-4,-3],
				[-3,-4,-4,-5,-5,-4,-4,-3],
				[-2,-3,-3,-4,-4,-3,-3,-2],
				[-1,-2,-2,-2,-2,-2,-2,-1],
				[2, 2, 0, 0, 0, 0, 2, 2],
				[2, 3, 1, 0, 0, 1, 3, 2]]
	pST["B"] = [[-2,-1,-1,-1,-1,-1,-1,-2],
				[-1,  0,  0,  0,  0,  0,  0,-1],
				[-1,  0,  .5, 1, 1,  .5,  0,-1],
				[-1,  .5,  .5, 1, 1,  .5,  .5,-1],
				[-1,  0, 1, 1, 1, 1,  0,-1],
				[-1, 1, 1, 1, 1, 1, 1,-1],
				[-1,  .5,  0,  0,  0,  0,  .5,-1],
				[-2,-1,-1,-1,-1,-1,-1,-2]]
	pST["N"] = [[-5,-4,-3,-3,-3,-3,-4,-5],
				[-4,-2,  0,  0,  0,  0,-2,-4],
				[-3,  0, 1, 1.5, 1.5, 1,  0,-3],
				[-3,  5, 1.5, 2, 2, 1.5,  5,-3],
				[-3,  0, 1.5, 2, 2, 1.5,  0,-3],
				[-3,  5, 1, 1.5, 1.5, 1,  5,-3],
				[-4,-2,  0,  5,  5,  0,-2,-4],
				[-5,-4,-3,-3,-3,-3,-4,-5]]
	boardValue = 0
	mult = 0
	for x in range(len(board)):
		for y in range(len(board)):
			piece = board[x][y]
			if isinstance(piece, Piece):
				pieceName = piece.name[1]
				if piece.giveColor() == "Black":
					boardValue += (piece.value * -1)
					rX = 7 - (x % 8)
					boardValue -= pST[pieceName][rX][y]
				elif piece.giveColor() == "White":
					boardValue += (piece.value * 1)
					boardValue += pST[pieceName][x][y]
	return boardValue

def checkMove(board, piece, move, oldSquare):
    x = move[0]
    y = move[1]
    board[x][y] = piece
    board[oldSquare[0]][oldSquare[1]] = 0
    return board

def reverseMove(board, piece, move, oldSquare):
    x = move[0]
    y = move[1]
    board[x][y] = 0
    board[oldSquare[0]][oldSquare[1]] = piece
    return board

# found from online https://medium.freecodecamp.org/simple-chess-ai-step-by-step-1d55a9266977
def minimaxRoot(depth, board, isMaximisingPlayer):
    if isMaximisingPlayer: color = "White"
    else: color = "Black"
    allMoves = generateAllMoves(color, board)
    bestSquare = []
    bestMove = -9999
    bestMoveFound = []
    mList = []
    for (square, move, oldSquare) in allMoves:
        board = copy.deepcopy(board)
        board = checkMove(board, square, move, oldSquare)
        value = minimax(depth, board, -10000, 10000, not isMaximisingPlayer)
        board = reverseMove(board, square, move, oldSquare)
        if value > bestMove:
            mList.append((move, value))
            bestMove = value
            bestMoveFound = move
            bestSquare = oldSquare
        print(mList)
    return (bestSquare, bestMoveFound)

def minimax(depth, board, alpha, beta, isMaximisingPlayer):
    if isMaximisingPlayer: color = "White"
    else: color = "Black"
    if (depth == 0):
        return boardValue(board)
    allMoves = generateAllMoves(color, board)
    if (isMaximisingPlayer):
        bestMove = -9999
        for (square, move, oldSquare) in allMoves:
            board = checkMove(board, square, move, oldSquare)
            bestMove = max(bestMove, minimax(depth - 1, board, alpha, beta, not isMaximisingPlayer))
            board = reverseMove(board, square, move, oldSquare)
            alpha = max(alpha, bestMove)
            if beta < alpha:
                return bestMove
        return bestMove
    else:
        bestMove = 9999
        for (square, move, oldSquare) in allMoves:
            board = checkMove(board, square, move, oldSquare)
            bestMove = min(bestMove, minimax(depth - 1, board, alpha, beta, not isMaximisingPlayer))
            board = reverseMove(board, square, move, oldSquare)
            beta = max(beta, bestMove)
            if beta < alpha:
                return bestMove
        return bestMove