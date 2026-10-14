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