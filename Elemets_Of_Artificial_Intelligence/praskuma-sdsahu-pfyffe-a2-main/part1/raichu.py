#
# raichu.py : Play the game of Raichu
#
# Authors: 
#   Pete Fyffe (pfyffe)
#
# Based on skeleton code by D. Crandall, Oct 2021
#
from argparse import ArgumentError
import math
from re import L, M
import sys
import time
import numpy as np

MAX_H = 3 #depth horizon
INFINITY = 2**31

def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))

def canCapture(player, opponent):
    '''
    Returns true if player can capture opponent. 
    Does not consider positioning.
    player and opponent are chars such as 'W' or '$'
    '''
    #Player is black
    if player == 'b':
        if opponent =='w':
            return True
    elif player == 'B':
        if opponent == 'W' or opponent =='w':
            return True
    elif player == '$':
        if opponent == '@' or opponent == 'W' or opponent == 'w':
            return True

    #Player is white
    elif player == 'w':
        if opponent =='b':
            return True
    elif player == 'W':
        if opponent == 'B' or opponent =='b':
            return True
    elif player == '@': #White Raichu
        if opponent == '$' or opponent == 'B' or opponent == 'b':
            return True

    return False

def isValidTile(state, i, j):
    return i >=0 and j >= 0 and i < len(state) and j < len(state)

def isEmptyTile(state, i, j):
    return isValidTile(state, i, j) and state[i][j] == '.'
    
def movePiece(state, srcI, srcJ, dstI, dstJ):
    '''
    Returns a copy of the board state where the piece at
    the coordinates (srcI, srcJ) should be set to '.' (empty)
    The piece will then occupy the slot at (dstI, dstJ).
    Also, if a piece has reached the opposite side of the board,
    upgrade it to a Raichu.
    '''
    copy = np.copy(state)
    piece = state[srcI][srcJ]

    #Uprade to Raichu if possible.
    if (piece == 'W' or piece == 'w') and dstI == len(state) - 1:
        piece = '@'
    elif (piece == 'B' or piece == 'b') and dstI == 0:
        piece = '$'

    copy[srcI][srcJ] = '.'
    copy[dstI][dstJ] = piece
    return copy


def makeMoveOrCapture(state, fromI, fromJ, toI, toJ, listToAppendTo):
    '''
    Creates a copy of the state array and relocates a piece from the location (fromI, fromJ) 
    to its new location (toI, toJ) only if all tiles between are empty.
    Additionally, if there is 1 opponent in the way, that opponent will be deleted (jumped over). 
    Then, appends the copy to listToAppendTo.
    Does nothing if the new location is out-of-bounds or if there are multiple opponents in the way.
    '''
    if not isValidTile(state, fromI, fromJ) or not isEmptyTile(state, toI, toJ):
        return
    #Determine how the loop will increment or decrement i and j.
    #iStep and jStep will always be -1, 0, or 1. 
    #Ex: If iStep is zero, the loop will check along a column.
    #Ex: If iStep and jStep are nonzero, the loop will check a diagonal.
    iStep = toI - fromI
    if iStep != 0:
        iStep = iStep // abs(iStep)
    jStep = toJ - fromJ
    if jStep != 0:
        jStep = jStep // abs(jStep)

    if iStep == 0 and jStep == 0:
        return ArgumentError("The source and destination tiles cannot be the same.")

    counter = toI - fromI
    i = fromI
    j = fromJ
    foundOpponent = False
    captureAt = ()
    PLAYER = state[fromI][fromJ]
    while i != toI or j != toJ:
        i += iStep
        j += jStep
        if not isValidTile(state, i, j):
            return
        tile = state[i][j]
        if tile != '.':
            if not foundOpponent and canCapture(PLAYER, tile):
                #If a single opponent is in the way, label it for capture
                foundOpponent = True
                captureAt = (i, j)
            else:
                return
        counter -= 1

    copy = movePiece(state, fromI, fromJ, toI, toJ)

    #If one enemy was identified, remove it.
    if foundOpponent:
        copy[captureAt[0]][captureAt[1]] = '.'

    listToAppendTo.append(copy)


def successors(state, i, j, N, playerIsWhite):
    '''
    Returns a list of successors for a certain piece at position (i, j).
    Each successor is a copy of the state that represents one possible move or jump
    for the target game piece. 
    '''
    output = []
    player = state[i][j]
    if player == 'w' and playerIsWhite: #white Pichu 
        #Diagonal jumps
        if not isEmptyTile(state, i+1, j-1):
            makeMoveOrCapture(state, i, j, i+2, j-2, output)
        if not isEmptyTile(state, i+1, j+1):
            makeMoveOrCapture(state, i, j, i+2, j+2, output)
        #Diagonal moves
        makeMoveOrCapture(state, i, j, i+1, j-1, output)
        makeMoveOrCapture(state, i, j, i+1, j+1, output)
    elif player == 'b' and not playerIsWhite: #black Pichu 
        #Diagonal jumps
        if not isEmptyTile(state, i-1, j-1):
            makeMoveOrCapture(state, i, j, i-2, j-2, output)
        if not isEmptyTile(state, i-1, j+1):
            makeMoveOrCapture(state, i, j, i-2, j+2, output)
        #Diagonal moves
        makeMoveOrCapture(state, i, j, i-1, j-1, output)
        makeMoveOrCapture(state, i, j, i-1, j+1, output)
    elif (player == 'B' and not playerIsWhite) or (player == 'W' and playerIsWhite): #Pikachu
        #Forward movement/jumping is dependent on team color.
        if playerIsWhite:
            direction = 1
        else: #black Pikachu
            direction = -1
        
        #1-step forward MOVE
        if isEmptyTile(state, i + 1*direction, j):
            makeMoveOrCapture(state, i, j, i + 1*direction, j, output)
        #2-step forward MOVE or JUMP
        makeMoveOrCapture(state, i, j, i + 2*direction, j, output) 
        #3-step forward JUMP
        if not isEmptyTile(state, i + 1*direction, j) or not isEmptyTile(state, i + 2*direction, j): 
            makeMoveOrCapture(state, i, j, i + 3*direction, j, output)

        #Horizontal 1-step MOVES
        if isEmptyTile(state, i, j+1):
            makeMoveOrCapture(state, i, j, i, j+1, output)
        if isEmptyTile(state, i, j-1):
            makeMoveOrCapture(state, i, j, i, j-1, output)
        #Horizontal 2-step MOVES/JUMPS
        makeMoveOrCapture(state, i, j, i, j+2, output)
        makeMoveOrCapture(state, i, j, i, j-2, output)
        #Horizontal 3-step JUMPS: ensure an opponent is in the path
        if not isEmptyTile(state, i, j+1) or not isEmptyTile(state, i, j+2):
            makeMoveOrCapture(state, i, j, i, j+3, output)
        if not isEmptyTile(state, i, j-1) or not isEmptyTile(state, i, j-2):
            makeMoveOrCapture(state, i, j, i, j-3, output)
    elif (player == '$' and not playerIsWhite) or (player == '@' and playerIsWhite): #Raichu
        #Diagonal moves/captures: determine the left side of the board, then loop from there
        #Top left to bottom right diagonal
        row = i
        col = j
        while row > 0 and col > 0:
            row -= 1
            col -= 1
        while row < N and col < N:
            if row != i or col != j:
                makeMoveOrCapture(state, i, j, row, col, output)
            row += 1
            col += 1

        #Bottom left to top right diagonal
        row = i
        col = j
        while row > 0 and col > 0:
            row += 1
            col -= 1
        while row >= 0 and col < N:
            if row != i or col != j:
                makeMoveOrCapture(state, i, j, row, col, output)
            row -= 1
            col += 1
        
        #Horizontal moves/captures
        for col in range(0, N):
            if col != j:
                makeMoveOrCapture(state, i, j, i, col, output)
        #Vertical moves/captures
        for row in range(0, N):
            if row != i:
                makeMoveOrCapture(state, i, j, row, j, output)
    
    return output



def evaluate(s, playerIsWhite):
    '''
    An evaluation function that adds up the total number of the 
    player's pieces with certain pieces being more valuable than others
    then adds in the total distance all the player's non-Raichu pieces are 
    from the opposite side of the board. 
    The opponent's stats are subtracted from this to lower the favorability.
    '''
    N = len(s)
    totalWhite = 0
    totalBlack = 0
    #Compute weighted sum of pieces
    for i in range(0, N):
        for j in range(0, N):
            piece = s[i][j]
            #Add arbitrarily amount of points based on each piece's type.
            if piece == 'b':
                totalBlack += 1
            elif piece == 'B':
                totalBlack += 2
            elif piece == '$':
                totalBlack += 4
            ###################
            elif piece == 'w':
                totalWhite += 1
            elif piece == 'W':
                totalWhite += 2
            elif piece == '@':
                totalWhite += 4 

    #Next, compute total distance each non-Raichu piece is from the end of the board 
    whiteDistance = 0
    blackDistance = 0
    for i in range(0, N):
        for j in range(0, N):
            piece = s[i][j]
            if piece == 'b' or piece == 'B':
                blackDistance += i
            ###################
            elif piece == 'w' or piece == 'W':
                whiteDistance += N - i - 1

    #Make scores negative if they lower the favorability for a team
    if playerIsWhite:
        totalBlack = -totalBlack
        whiteDistance = -whiteDistance
    else:
        totalWhite = -totalWhite
        blackDistance = -blackDistance

    return (totalBlack + totalWhite)*2 + whiteDistance + blackDistance


def minimax(state, isMaxTurn, playerIsWhite, h, isWhiteTurn, alpha, beta):
    if h >= MAX_H:
        evaluation = evaluate(state, playerIsWhite)
        return evaluation

    if isMaxTurn:
        bestRating = -INFINITY
    else:
        bestRating = INFINITY
    bestState = state #It's unnecessary to track this, but it helps for printing
    N = len(state)
    successorList = []
    for i in range(0, N):
        for j in range(0, N):
            if state[i][j] != '.': 
                successorList = successorList + successors(state, i, j, N, isWhiteTurn)
    
    for sPrime in successorList:
        if isMaxTurn:
            eval = minimax(sPrime, not isMaxTurn, playerIsWhite, h + 1, not isWhiteTurn, alpha, beta)
            if eval > bestRating:
                bestRating = eval
                bestState = sPrime
            alpha = max(eval, alpha)
            if beta <= alpha:
                break
        else:
            eval = minimax(sPrime, not isMaxTurn, playerIsWhite, h + 1, not isWhiteTurn, alpha, beta)
            if eval < bestRating:
                bestRating = eval
                bestState = sPrime
            beta = min(eval, beta)
            if beta <= alpha:
                break
    
    if h == 0:
        #Convert from 2D array to string and print
        flatList = list(bestState.reshape((1, N*N))[0])
        print(''.join(flatList))

    return bestRating



def find_best_move(board, N, playerColor, timelimit):
    board = np.array( [[j for j in i] for i in board] ).reshape((N, N))
    playerIsWhite =  playerColor == 'w'
    isWhiteTurn = playerIsWhite #white always goes first
    global MAX_H
    while True:
        minimax(board, True, playerIsWhite, 0, isWhiteTurn, -INFINITY, INFINITY)
        MAX_H += 1


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    for new_board in find_best_move(board, N, player, timelimit):
        print(new_board)