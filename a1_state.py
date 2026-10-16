#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hinger Project
Coursework 001 for: CMP-6058A Artificial Intelligence

Includes a State class for Task 1

@author: <group number> (<your ID>, <partner ID>, <partner ID>, <partner ID>)
@date:   13/10/2026
"""

# board size fixed by the spec
ROWS = 5
COLS = 5


class State:

    def __init__(self, grid):
        if len(grid) != ROWS:  # catches invalid row length
            raise ValueError("Invalid Grid Size")

        for row in grid: # catches invalid col length
            if len(row) != COLS:
                raise ValueError("Invalid Grid Size")

        self.grid = [row[:] for row in grid] # copying each row

    def __str__(self):  # returns the grid as rows of numbers separated by spaces
        lines = []

        for row in self.grid:
            cells = []
            for cell in row:
                cells.append(str(cell))
            lines.append(" ".join(cells))

        return "\n".join(lines)

    def letter_to_cell(self, letter):  # converts move letter to (row, col)

        if (letter.isnumeric()):
            return

        index = ord(letter) - ord('A')  # gets index as number code 'A' is just zero
        row = index // COLS
        col = index % COLS
        return (row, col)

    def move(self, letter):  # removes one from the cell named by letter
        if len(letter) != 1 or letter not in "ABCDEFGHIJKLMNOPQRSTUVWXY": # checks for valid letter, no Z thats index 25 off board
            raise ValueError("Invalid Move")

        row, col = self.letter_to_cell(letter)

        if not self.grid[row][col]: # empty cell check
            raise ValueError("Invalid Grid Cell")

        self.grid[row][col] -= 1

    def successors(self):  # yields all states reachable in one move
        for row in range(ROWS):
            for col in range(COLS):
                if self.grid[row][col] > 0: # only active cells check
                    child = State(self.grid) # its own copy
                    child.grid[row][col] -= 1
                    yield child

    def numRegions(self):  # return number of active regions on board
        # create set to keep track of visited counters
        already_visited = set()
        regions = 0

        for row in range(ROWS):
            for col in range(COLS):
                # if row has not been visited and is active
                if (row, col) not in already_visited and self.grid[row][col] > 0:
                    regions += 1
                    already_visited.add((row, col))
                    # visit all neighbours to ensure no duplicate regions
                    neighbours = [(row, col)]
                    while neighbours:
                        # check neighbours to see if active and not visited
                        neighbour_row, neighbour_column = neighbours.pop()
                        for i in range(-1, 2):
                            for j in range(-1, 2):
                                new_row = neighbour_row + i
                                new_col = neighbour_column + j
                                # if neighbour counter in bounds, active and not already visited
                                if (5 > new_row >= 0 and 5 > new_col >= 0) and \
                                    (self.grid[new_row][new_col] > 0) and \
                                        ((new_row, new_col) not in already_visited):
                                            # add counter to already visited set and neigbours list
                                            already_visited.add((new_row, new_col))
                                            neighbours.append((new_row, new_col))

        return regions

    def numHingers(self): # return number of hinger cells based off current state
        num_hingers = 0
        for row in range(ROWS):
            for col in range(COLS):
                # if cell is active
                if (self.grid[row][col] == 1):
                    # count regions
                    base_num_regions = self.numRegions()
                    # set cell to 0 to see if num of regions increase - if so, hinger cell found
                    self.grid[row][col] = 0
                    if (base_num_regions < self.numRegions()):
                        num_hingers += 1
                    # set counter back to original value
                    self.grid[row][col] = 1

        return num_hingers


def tester():  # main test harness

    def check(label, expected, result):  # helper function to provide test results
        status = "PASS" if expected == result else "FAIL"
        print("{} | {}: expected {}, got {}".format(status, label, expected, result))

    s1_grid = [[1, 1, 0, 0, 1],
               [1, 1, 0, 0, 0],
               [0, 0, 1, 1, 1],
               [0, 0, 0, 1, 1],
               [0, 0, 0, 0, 1]]

    sa = State(s1_grid)
    # test printing state
    print(sa)

    print("*" * 40)
    print("letter_to_cell() Tests: ")
    check("Input: 'A'", (0, 0), sa.letter_to_cell("A"))
    check("Input: 'M'", (2, 2), sa.letter_to_cell("M"))
    check("Input: 'Z'", (5, 0), sa.letter_to_cell("Z"))
    check("Input: '4'", None, sa.letter_to_cell("4"))

    print("*" * 40)
    print("move() Tests:")
    sa.move("A")
    check("Input: 'A', (0, 0) changes from 1 -> 0", 0, sa.grid[0][0])
    print(sa)
    sa.move("M")
    check("Input: 'M', (2, 2) changes from 1 -> 0", 0, sa.grid[2][2])
    print(sa)
    try:
        sa.move("X")
        error_caught = False
    except ValueError:
        error_caught = True
    check("Input: 'X', ValueError caught", True, error_caught)

    print("*" * 40)
    # reassign state for testing purposes
    sa = State(s1_grid)
    print("successors() test")
    successors = list(sa.successors())
    check("11 different states showing all possible moves", 11, len(successors))
    for option in successors:
        print("Possible move:")
        print(option)

    print("*" * 40)
    print("numRegions() test")
    check("Number of regions", 2, sa.numRegions())
    sa.move("M")
    check("Number of regions after performing move (2,2)", 3, sa.numRegions())

    print("*" * 40)
    # reassign state for testing purposes
    sa = State(s1_grid)
    print("numHingers() test")
    check("Number of hingers", 2, sa.numHingers())
    sa.move("T")
    check("Number of hingers after performing move (3,4)", 3, sa.numHingers())

if __name__ == "__main__":
    tester()

# TODO 1.7 Add utility and helper functions wwhere needed
