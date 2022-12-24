#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : [Sagar Sahu AND sdsahu]
#
# Based on skeleton code provided in CSCI B551, Fall 2022.

import sys

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]
                
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
        moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1))

        # Return only moves that are within the house_map and legal (i.e. go through open space ".")
        return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]

def get_direction(current_move, moves, capture_move):
        if current_move[0] - 1 == moves[0]:
                capture_move += "U"
        elif current_move[0] + 1 == moves[0]: 
                capture_move += "D"
        elif current_move[1] - 1 == moves[1]:
                capture_move += "L"
        elif current_move[1] +1 == moves[1]:
                 capture_move += "R"
        return capture_move


# Perform search on the map
#
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)

def search(house_map):
        # Find pichu start position
        pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0]
        fringe=[(pichu_loc,0, "")]      #Fringe to store current location,distance travelled, directions.
        nodes_visited = [] 
 
        while fringe:
                (curr_move, curr_dist, curr_dir)=fringe.pop()
                move_str = curr_dir
                nodes_visited.append(curr_move) 
                for move in moves(house_map, *curr_move):
                        if house_map[move[0]][move[1]]=="@":
                                return curr_dist+1, get_direction(curr_move,move,move_str)
                        elif move not in nodes_visited:
                            fringe.append((move, curr_dist + 1, get_direction(curr_move,move,move_str)))

        if house_map[move[0]][move[1]] != "@":
                        print('No path exists')
                        print(curr_dist = -1)

# Main Function
if __name__ == "__main__":
        house_map=parse_map(sys.argv[1])
        print("Shhhh... quiet while I navigate!")
        solution = search(house_map)
        print("Here's the solution I found:")
        print(str(solution[0]) + " " + solution[1])