from chesspiecesandboard import *
from checkLogic import *
import copy
import random
import numpy as np

def AImoveLogic(event, data):
	if (data.isWTurn == True and data.aiColor == "Black") or (data.isWTurn == False and data.aiColor == "White"):
		moveLogic(event, data)

def generalAI(data, aiType):
	if (data.isWTurn == False and data.aiColor == "Black") or (data.isWTurn == True and data.aiColor == "White"):
		data.isWTurn = not data.isWTurn
		if data.aiColor == "White": isMaximisingPlayer = True
		else: isMaximisingPlayer = False
		if aiType == "Easy":
			(square, move) = easyAI(data.board, isMaximisingPlayer)
		elif aiType == "Medium":
			(square, move) = minimaxRoot(2, data.board, isMaximisingPlayer)
		elif aiType == "Hard":
			(square, move) = PVSRoot(5, data.board, data.aiColor)	
		piece = data.board[square[0]][square[1]]
		checkSpecialMoves(piece, move, square, data)
		piece.move(move)
		data.board[move[0]][move[1]] = piece
		data.board[square[0]][square[1]] = 0
		king = findPiece(data.aiColor, King, data.board)
		if inCheck(king, data.board):
			data.gameOver = True
			data.board[move[0]][move[1]] = 0
			data.board[square[0]][square[1]] = piece
		printBoard(data.board)

def checkSpecialMoves(piece, move, square, data):
	if isinstance(piece, Pawn) and move[1] == piece.promRank:
		piece = Queen(data.aiColor, square[0], square[1])
	if isinstance(piece, King) and move == [piece.x + 2, piece.y]:
		data.board[piece.x + 3][piece.y].move([piece.x + 1, piece.y])
		data.board[piece.x + 1][piece.y] = data.board[piece.x + 3][piece.y] 
		data.board[piece.x + 3][piece.y] = 0
	if isinstance(data.selectedPiece, King) and move == [piece.x - 2, piece.y]:
		data.board[piece.x - 4][piece.y].move([piece.x - 1, piece.y])
		data.board[piece.x - 1][piece.y] = data.board[piece.x - 4][piece.y] 
		data.board[piece.x - 4][piece.y] = 0

def generateAllMoves(color, board):
	board = np.array(board)
	pieces = []
	movesList = []
	for index, square in np.ndenumerate(board):
		x = index[0]
		y = index[1]			
		if isinstance(square, Piece) and square.giveColor() == color:
			pieces.append([x, y])
	for piece in pieces:
		x = piece[0]
		y = piece[1]
		oldSquare = [x, y]
		square = board[x][y]
		moveList = square.legalMoves(board)
		if moveList != []:
			for move in moveList:
				oldPiece = board[move[0]][move[1]]
				movesList.append((square, move, oldSquare, oldPiece))
	return movesList

def sortMoveList(movesList):
	copyMoves = copy.deepcopy(movesList)
	for (square, move, oldSquare, oldPiece) in copyMoves:
		if oldPiece != 0:
			if oldPiece.value > 10:
				movesList.insert(0, movesList.pop(movesList.index((square, move, oldSquare, oldPiece))))
	for (square, move, oldSquare, oldPiece) in copyMoves:
		if oldPiece != 0:
			if oldPiece.value > 33:
				movesList.insert(0, movesList.pop(movesList.index((square, move, oldSquare, oldPiece))))
	return movesList

def boardValue(board):
	board = np.array(board)
	pST = dict()
	pST["P"] = [[6, 6, 6, 6, 6, 6, 6, 6],
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
				[-1, 0, 0, 0, 0, 0, 0,-1],
				[-1, 0, 5, 5, 5, 5, 0,-1],
				[-.5, 0, .5, .5, .5, .5, 0, -.5],
				[-.5, 0, .5, .5, .5, .5, 0, -.5],
				[-1, .5, .5, .5, .5, .5, 0, -1],
				[-1, 0, .5, 0, 0, 0, 0, -1],
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
				[-1, 0, 0, 0, 0, 0, 0, -1],
				[-1, 0, .5, 1, 1, .5, 0,-1],
				[-1, .5, .5, 1, 1, .5, .5,-1],
				[-1, 0, 1, 1, 1, 1, 0,-1],
				[-1, 1, 1, 1, 1, 1, 1,-1],
				[-1, .5, 0, 0, 0, 0, .5,-1],
				[-2,-1,-1,-1,-1,-1,-1,-2]]
	pST["N"] = [[-5,-4,-3,-3,-3,-3,-4,-5],
				[-5,-2, 0, 0, 0, 0,-2,-5],
				[-3, 0, 1, 1.5, 1.5, 1, 0,-3],
				[-3, 0, 1.5, 2, 2, 1.5, 0,-3],
				[-3, 0, 1.5, 2, 2, 1.5, 0,-3],
				[-3, 5, 1, 1.5, 1.5, 1, 5,-3],
				[-4,-2, 0, 5, 5, 0,-2,-4],
				[-5,-4,-3,-3,-3,-3,-4,-5]]
	boardValue = 0
	for (index, square) in np.ndenumerate(board):
		x = index[0]
		y = index[1]
		if isinstance(square, Piece):
			pieceName = square.name[1]
			if square.giveColor() == "Black":
				boardValue -= square.value
				rX = 7 - (x % 8)
				boardValue -= pST[pieceName][y][rX]
			elif square.giveColor() == "White":
				boardValue += square.value
				boardValue += pST[pieceName][y][x]
	return boardValue

def checkMove(board, piece, move, oldSquare, oldPiece):
    x = move[0]
    y = move[1]
    board[x][y] = piece
    board[oldSquare[0]][oldSquare[1]] = 0
    return board

def reverseMove(board, piece, move, oldSquare, oldPiece):
    x = move[0]
    y = move[1]
    board[x][y] = oldPiece
    board[oldSquare[0]][oldSquare[1]] = piece
    return board

# found from online https://medium.freecodecamp.org/simple-chess-ai-step-by-step-1d55a9266977
def PVSRoot(depth, board, isMaximisingPlayer):
    if isMaximisingPlayer: color = "White"
    else: color = "Black"
    allMoves = generateAllMoves(color, board)
    copyAllMoves = copy.deepcopy(allMoves)
    for (square, move, oldSquare, oldPiece) in copyAllMoves:
        checkBoard = makeMove(board, square, move, oldSquare)
        newKing = findPiece(square.giveColor(), King, checkBoard)
        if inCheck(newKing, checkBoard):
            allMoves.remove((square, move, oldSquare, oldPiece))
    allMoves = sortMoveList(allMoves)
    bestSquare = []
    bestMove = -9999
    bestMoveFound = []
    mList = []
    for (square, move, oldSquare, oldPiece) in allMoves:
        board = checkMove(board, square, move, oldSquare, oldPiece)
        value = PVS(depth, board, -10000, 10000, not isMaximisingPlayer)
        printBoard(board)
        board = reverseMove(board, square, move, oldSquare, oldPiece)
        if value > bestMove:
            mList.append((move, value))
            bestMove = value
            bestMoveFound = move
            bestSquare = oldSquare
        print(mList)
    return (bestSquare, bestMoveFound)

# adapted from pseudocode found on wikipedia
def PVS(depth, board, alpha, beta, isMaximisingPlayer):
    firstChild = True
    if isMaximisingPlayer: color = "White"
    else: color = "Black"
    if (depth == 0):
        return boardValue(board)
    allMoves = generateAllMoves(color, board)
    allMoves = sortMoveList(allMoves)
    if (isMaximisingPlayer):
        bestMove = -9999
        for (square, move, oldSquare, oldPiece) in allMoves:
            if firstChild:
            	board = checkMove(board, square, move, oldSquare, oldPiece)
            	bestMove = max(bestMove, PVS(depth - 1, board, alpha, beta, not isMaximisingPlayer))
            	board = reverseMove(board, square, move, oldSquare, oldPiece)
            	firstChild = False
            else:
                board = checkMove(board, square, move, oldSquare, oldPiece)
                bestMove = max(bestMove, PVS(depth - 1, board, alpha, alpha - 1, not isMaximisingPlayer))
                board = reverseMove(board, square, move, oldSquare, oldPiece)
                if beta < bestMove < alpha:
                	board = checkMove(board, square, move, oldSquare, oldPiece)
                	bestMove = max(bestMove, PVS(depth - 1, board, alpha, bestMove, not isMaximisingPlayer))
                	board = reverseMove(board, square, move, oldSquare, oldPiece)
            alpha = max(alpha, bestMove)
            if beta <= alpha:
                return bestMove
        return bestMove
    else:
        bestMove = 9999
        for (square, move, oldSquare, oldPiece) in allMoves:
            if firstChild:
                board = checkMove(board, square, move, oldSquare, oldPiece)
                bestMove = min(bestMove, PVS(depth - 1, board, alpha, beta, not isMaximisingPlayer))
                board = reverseMove(board, square, move, oldSquare, oldPiece)
                firstChild = False
            else:
                board = checkMove(board, square, move, oldSquare, oldPiece)
                bestMove = min(bestMove, PVS(depth - 1, board, alpha, alpha - 1, not isMaximisingPlayer))
                board = reverseMove(board, square, move, oldSquare, oldPiece)
                if beta < bestMove < alpha:
                	board = checkMove(board, square, move, oldSquare, oldPiece)
                	bestMove = min(bestMove, PVS(depth - 1, board, alpha, bestMove, not isMaximisingPlayer))
                	board = reverseMove(board, square, move, oldSquare, oldPiece)
            alpha = max(alpha, bestMove)
            if beta <= alpha:
                return bestMove
        return bestMove

# found from online https://medium.freecodecamp.org/simple-chess-ai-step-by-step-1d55a9266977
def minimaxRoot(depth, board, isMaximisingPlayer):
    if isMaximisingPlayer: color = "White"
    else: color = "Black"
    allMoves = generateAllMoves(color, board)
    allMoves = sortMoveList(allMoves)
    bestSquare = []
    bestMove = -9999
    bestMoveFound = []
    mList = []
    for (square, move, oldSquare, oldPiece) in allMoves:
        board = checkMove(board, square, move, oldSquare, oldPiece)
        value = minimax(depth, board, -10000, 10000, not isMaximisingPlayer)
        board = reverseMove(board, square, move, oldSquare, oldPiece)
        if value > bestMove:
            mList.append((move, value))
            bestMove = value
            bestMoveFound = move
            bestSquare = oldSquare
    return (bestSquare, bestMoveFound)

def minimax(depth, board, alpha, beta, isMaximisingPlayer):
    if isMaximisingPlayer: color = "White"
    else: color = "Black"
    if (depth == 0):
        return boardValue(board)
    allMoves = generateAllMoves(color, board)
    if (isMaximisingPlayer):
        bestMove = -9999
        for (square, move, oldSquare, oldPiece) in allMoves:
            board = checkMove(board, square, move, oldSquare, oldPiece)
            bestMove = max(bestMove, minimax(depth - 1, board, alpha, beta, not isMaximisingPlayer))
            board = reverseMove(board, square, move, oldSquare, oldPiece)
            alpha = max(alpha, bestMove)
            if beta <= alpha:
                return bestMove
        return bestMove
    else:
        bestMove = 9999
        for (square, move, oldSquare, oldPiece) in allMoves:
            board = checkMove(board, square, move, oldSquare, oldPiece)
            bestMove = min(bestMove, minimax(depth - 1, board, alpha, beta, not isMaximisingPlayer))
            board = reverseMove(board, square, move, oldSquare, oldPiece)
            beta = max(beta, bestMove)
            if beta <= alpha:
                return bestMove
        return bestMove

def easyAI(board, isMaximisingPlayer):
	if isMaximisingPlayer: color = "White"
	else: color = "Black"
	allMoves = generateAllMoves(color, board)
	copyAllMoves = copy.deepcopy(allMoves)
	for (square, move, oldSquare, oldPiece) in copyAllMoves:
		checkBoard = makeMove(board, square, move, oldSquare)
		newKing = findPiece(square.giveColor(), King, checkBoard)
		if inCheck(newKing, checkBoard):
			allMoves.remove((square, move, oldSquare, oldPiece))
	(square, move, oldSquare, oldPiece) = random.choice(allMoves)
	return (oldSquare, move)