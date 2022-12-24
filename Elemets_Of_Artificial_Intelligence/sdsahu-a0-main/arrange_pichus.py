#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : [Sagar Sahu AND sdsahu]
#
# Based on skeleton code in CSCI B551, Fall 2022.

import sys
# Parse the map from a given filename

def parse_map(filename):
    with open(filename, "r") as f:
        return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]

# Count total # of pichus on house_ma

def count_pichus(house_map):
    return sum([row.count('p') for row in house_map])

# Return a string with the house_map rendered in a human-pichuly format

def printable_house_map(house_map):
    return "\n".join(["".join(row) for row in house_map])

# Add a pichu to the house_map at the given position, and return a new house_map (doesn't change original)

def add_pichu(house_map, row, col):
    return house_map[0:row] + [house_map[row][0:col] + ['p', ] + house_map[row][col+1:]] + house_map[row+1:]

# Get list of successors of given house_map state

def successors(house_map):
    # we will add one more condition here before returning the position
    # we will utilize the new valid_move function we wrote to check if
    # the move we are making is valid or not

    return [add_pichu(house_map, row, col) for row in range(0, len(house_map)) for col in range(0, len(house_map[0])) if verify_path(house_map, row, col) and house_map[row][col] == '.']

# check if house_map is a goal state

def is_goal(house_map, k):
    return count_pichus(house_map) == k

def verify_path(house_map, row, col):
    check_if = ['X','@']

    current_row = row
    while current_row >= 0:
        if house_map[current_row][col] == '.':
            current_row = current_row - 1
        elif house_map[current_row][col] in check_if:
            break
        else:
            return False

    current_row = row
    while current_row < len(house_map):
        if house_map[current_row][col] == '.':
            current_row = current_row + 1
        elif house_map[current_row][col] in check_if:
            break
        else:
            return False

    current_column = col
    while current_column < len(house_map[0]):
        if house_map[row][current_column] == '.':
            current_column = current_column + 1
        elif house_map[row][current_column] in check_if:
            break
        else:
            return False

    current_column = col
    while current_column >= 0:
        if house_map[row][current_column] == '.':
            current_column = current_column - 1
        elif house_map[row][current_column] in check_if:
            break
        else:
            return False

    current_row, current_column = row, col

    while current_column < len(house_map[0]) and current_row >= 0:
        if house_map[current_row][current_column] == '.':
            current_column = current_column + 1
            current_row = current_column - 1
        elif house_map[current_row][current_column] in check_if:
            break
        else:
            return False

    current_row, current_column = row, col

    while current_column < len(house_map[0]) and current_row < len(house_map):
        if house_map[current_row][current_column] == '.':
            current_column = current_column + 1
            current_row = current_row + 1
        elif house_map[current_row][current_column] in check_if:
            break
        else:
            return False

    # CHECK TRAVERSE LEFT UP
    current_row, current_column = row, col

    while current_column >= 0 and current_row >= 0:
        if house_map[current_row][current_column] == '.':
            current_column = current_column - 1
            current_row = current_row - 1
        elif house_map[current_row][current_column] in check_if:
            break
        # We found a 'p'
        else:
            return False

    current_row, current_column = row, col

    while current_column >= 0 and current_row < len(house_map):
        if house_map[current_row][current_column] == '.':
            current_column = current_column - 1
            current_row = current_row + 1
        elif house_map[current_row][current_column] in check_if:
            break
        else:
            return False
 
    return True
    
# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_house_map, success), where:
# - new_house_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#
def solve(initial_house_map, k):
    fringe = [initial_house_map]
    while len(fringe) > 0:
        for new_house_map in successors(fringe.pop()):
            if is_goal(new_house_map, k):
                return(new_house_map, True)
            fringe.append(new_house_map)

    return (initial_house_map, False)

# Main Function
if __name__ == "__main__":
    house_map = parse_map(sys.argv[1])
    # This is k, the number of agents
    k = int(sys.argv[2])
    print("Starting from initial house map:\n" +
          printable_house_map(house_map) + "\n\nLooking for solution...\n")
    solution = solve(house_map, k)
    print("Here's what we found:")
    print(printable_house_map(solution[0]) if solution[1] else "False")
