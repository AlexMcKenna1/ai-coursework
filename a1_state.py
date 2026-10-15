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

        if len(grid) != ROWS: # catches invalid row length
            raise ValueError("Invalid Grid Size")

        for row in grid: # catches invalid col length
            if len(row) != COLS:
                raise ValueError("Invalid Grid Size")

        self.grid = [row[:] for row in grid] # copying each row


    def __str__(self): # returns the grid as rows of numbers separated by spaces

        lines = []

        for row in self.grid:
            cells = []
            for cell in row:
                cells.append(str(cell))
            lines.append(" ".join(cells))

        return "\n".join(lines)
    

    def letter_to_cell(self, letter): # converts move letter to (row, col)
        index = ord(letter) - ord('A') # gets index as number code 'A' is just zero
        row = index // COLS
        col = index % COLS
        return (row, col)


    def move(self, letter): # removes one from the cell named by letter

        if len(letter) != 1 or letter not in "ABCDEFGHIJKLMNOPQRSTUVWXY": # checks for valid letter, no Z thats index 25 off board
            raise ValueError("Invalid Move")
        
        row, col = self.letter_to_cell(letter)

        if not self.grid[row][col]: # empty cell check
            raise ValueError("Invalid Grid Cell")

        self.grid[row][col] -= 1


    def successors(self): # yields all states reachable in one move

        for row in range(ROWS):
            for col in range(COLS):
                if self.grid[row][col] > 0: # only active cells check
                    child = State(self.grid) # its own copy
                    child.grid[row][col] -= 1
                    yield child
        
