#!/usr/local/bin/python3
# solver2022.py : 2022 Sliding tile puzzle solver
#
# Code by: Code by: [(Dwarakamai Mannemuddu, dwamanne, 2001096476), (Sagar Sahu, sdsahu, 2001078394), (Ronakkumar Bhagchandani, rbhagcha , 2001077918)]
#
# Based on skeleton code by D. Crandall & B551 Staff, Fall 2022
#

import sys
import numpy as np
import itertools
import heapq

ROWS = 5
COLS = 5


def printable_board(board):
    return [('%3d ') * COLS % board[j:(j + COLS)] for j in range(0, ROWS * COLS, COLS)]


# return a list of possible successor states
def get_matrix(state):
    x = np.array([state], dtype=object)
    matrix = np.asarray(x[0])
    return matrix.reshape((ROWS, COLS))


def slide_left(state, n):
    matrix = get_matrix(state)
    row = matrix[n]
    row = np.append(row[1:], row[:1])
    matrix[n] = row
    state = tuple(np.hstack(matrix))
    return state, 'L' + str(n + 1)


def slide_right(state, n):
    matrix = get_matrix(state)
    row = matrix[n]
    row = np.append(row[-1:], row[:-1])
    matrix[n] = row
    state = tuple(np.hstack(matrix))
    return state, 'R' + str(n + 1)


def slide_up(state, n):
    matrix = get_matrix(state)
    row = matrix[:, n]
    row = np.append(row[1:], row[:1])
    matrix[:, n] = row
    state = tuple(np.hstack(matrix))
    return state, 'U' + str(n + 1)


def slide_down(state, n):
    matrix = get_matrix(state)
    row = matrix[:, n]
    row = np.append(row[-1:], row[:-1])
    matrix[:, n] = row
    state = tuple(np.hstack(matrix))
    return state, 'D' + str(n + 1)


def rotate_outer_clockwise(state):
    matrix = get_matrix(state)
    row1 = matrix[0]
    row2 = matrix[ROWS - 1]
    col1 = matrix[:, 0]
    col2 = matrix[:, ROWS - 1]
    temp1 = matrix[1][0]
    temp2 = matrix[ROWS - 1][1]
    temp3 = matrix[3][ROWS - 1]
    temp4 = matrix[0][3]
    row1 = np.append([temp1], row1[:4])
    col1 = np.append(col1[1:5], [temp2])
    row2 = np.append(row2[1:5], [temp3])
    col2 = np.append([temp4], col2[0:4])
    matrix[0] = row1
    matrix[:, 0] = col1
    matrix[ROWS - 1] = row2
    matrix[:, COLS - 1] = col2
    state = tuple(np.hstack(matrix))
    return state, 'Oc'


def rotate_outer_counter_clockwise(state):
    matrix = get_matrix(state)
    row1 = matrix[0]
    row2 = matrix[ROWS - 1]
    col1 = matrix[:, 0]
    col2 = matrix[:, COLS - 1]
    temp1 = matrix[1][ROWS - 1]
    temp2 = matrix[0][1]
    temp3 = matrix[3][0]
    temp4 = matrix[ROWS - 1][3]
    row1 = np.append(row1[1:], [temp1])
    col1 = np.append([temp2], col1[:COLS - 1])
    row2 = np.append([temp3], row2[:ROWS - 1])
    col2 = np.append(col2[1:], [temp4])
    matrix[0] = row1
    matrix[:, 0] = col1
    matrix[ROWS - 1] = row2
    matrix[:, COLS - 1] = col2
    state = tuple(np.hstack(matrix))
    return state, 'Occ'


def rotate_inner_clockwise(state):
    matrix = get_matrix(state)
    row1 = matrix[1][1:ROWS - 1]
    row2 = matrix[3][1:ROWS - 1]
    col1 = matrix[:, 1][1:COLS - 1]
    col2 = matrix[:, 3][1:COLS - 1]
    temp1 = col1[1]
    temp2 = row2[1]
    temp3 = col2[1]
    temp4 = row1[1]
    row1 = np.append([temp1], row1[:2])
    col1 = np.append(col1[1:3], [temp2])
    row2 = np.append(row2[1:3], [temp3])
    col2 = np.append([temp4], col2[:2])
    matrix[1][1:ROWS - 1] = row1
    matrix[:, 1][1:COLS - 1] = col1
    matrix[3][1:ROWS - 1] = row2
    matrix[:, 3][1:COLS - 1] = col2
    state = tuple(np.hstack(matrix))
    return state, 'Ic'


def rotate_inner_counter_clockwise(state):
    matrix = get_matrix(state)
    row1 = matrix[1][1:ROWS - 1]
    row2 = matrix[3][1:ROWS - 1]
    col1 = matrix[:, 1][1:COLS - 1]
    col2 = matrix[:, 3][1:COLS - 1]
    temp1 = col2[1]
    temp2 = row1[1]
    temp3 = col1[1]
    temp4 = row2[1]
    row1 = np.append(row1[1:], [temp1])
    col1 = np.append([temp2], col1[:2])
    row2 = np.append([temp3], row2[:2])
    col2 = np.append(col2[1:], [temp4])
    matrix[1][1:ROWS - 1] = row1
    matrix[:, 1][1:COLS - 1] = col1
    matrix[3][1:ROWS - 1] = row2
    matrix[:, 3][1:COLS - 1] = col2
    state = tuple(np.hstack(matrix))
    return state, 'Icc'


def successors(state):
    boards = []
    for i in range(ROWS):
        boards.append(slide_left(state, i))
        boards.append(slide_right(state, i))
    for j in range(COLS):
        boards.append(slide_up(state, j))
        boards.append(slide_down(state, j))
    boards.append(rotate_outer_clockwise(state))
    boards.append(rotate_outer_counter_clockwise(state))
    boards.append(rotate_inner_clockwise(state))
    boards.append(rotate_inner_counter_clockwise(state))
    return boards


# gives the index of the element in goal state
def get_goal_index(goal, n):
    for i in range(ROWS):
        if n in goal[i]:
            return i, goal[i].index(n)
    return ()


# manhattan distance is heuristic function here
def h(state):
    temp = itertools.count(1)
    goal = [[next(temp) for i in range(COLS)] for i in range(ROWS)]
    matrix = get_matrix(state)
    distance = 0

    for i in range(ROWS):
        for j in range(COLS):
            (row, col) = get_goal_index(goal, matrix[i][j])
            distance = distance + abs(row - i) + abs(col - j)
    return distance


def g(cost):
    return pow(cost, 2) / 2


def f(state, cost):
    return h(state) + g(cost)


# check if we've reached the goal
def is_goal(state):
    tile = 1
    for i in range(len(state)):
        if state[i] != tile:
            return False
        tile += 1
    return True


def solve(initial_board):
    fringe = []
    visited = []
    heapq.heappush(fringe, [f(initial_board, 0), 0, initial_board, []])
    while len(fringe) > 0:
        (totalCost, cost, state, path) = heapq.heappop(fringe)
        visited.append(state)
        if is_goal(state):
            return path
        for s in successors(state):
            if s[0] not in visited:
                heapq.heappush(fringe, [f(s[0], cost + 1), cost + 1, s[0], path + [s[1]]])
    return []


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if (len(sys.argv) != 2):
        raise (Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [int(i) for i in line.split()]

    if len(start_state) != ROWS * COLS:
        raise (Exception("Error: couldn't parse start state file"))

    print("Start state: \n" + "\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))

    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
