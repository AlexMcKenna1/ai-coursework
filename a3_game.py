#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hinger Project
Coursework 001 for: CMP-6058A Artificial Intelligence

Includes the game loop for Task 3

@author: <B07> (100475742, 100174060, 100464504, 100481021)
@date:   11/11/2026
"""


from a1_state import State, ROWS, COLS
from a2_agent import Agent


def get_move(player, state): # gets a move letter from a human or agent
    if player is None:
        user_input = (input("Your move (A-Y, or Z to quit): ")).strip().upper()
        return user_input
    else:
        return player.next_move(state)


def valid(r, c): # checks (r, c) is actually on the board
    return 0 <= r < ROWS and 0 <= c < COLS


def is_legal(state, letter): # returns true if passed letter is legitimate move for passed state
    # if not a character, return false
    if len(letter) != 1:
        return False

    # must be a valid alphabetical character
    if not ('A' <= letter <= 'Y'):
        return False

    # return true if cell has a counter
    row, col = state.letter_to_cell(letter)
    return state.grid[row][col] > 0


def move_points(state, letter): # points for a move +100 if hinger
    row, col = state.letter_to_cell(letter)
    cost = 0
    for dr in (-1, 0, 1): # count active cells in the 8 squares around it
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0: # skip the cell itself
                continue
            r = row + dr
            c = col + dc
            if valid(r, c) and state.grid[r][c] > 0:
                cost += 1

    bonus = 0
    if state.grid[row][col] == 1:
        test = State(state.grid)
        test.grid[row][col] = 0
        if test.numRegions() > state.numRegions():
            bonus = 100

    return bonus - cost


def board_empty(state): # True once every counter is gone
    for row in state.grid:
        for cell in row:
            if cell > 0:
                return False
    return True


def play(state, agentA, agentB): # runs a full game, returns winner name and score
    state = State(state.grid) # copy so original board isn't changed
    players = [agentA, agentB]

    names = []
    for player in players:
        if player is None:
            names.append("Human")
        else:
            names.append(player.name)

    scores = [100,100] # both start on 100
    turn = 0 # agentA = 0, agentB = 1
    while not board_empty(state):
        print(state)
        letter = get_move(players[turn], state)

        if letter == "Z": # lose immediately
            winner = 1 - turn
            print(names[turn], "played Z and loses!", names[winner], "wins.")
            return (names[winner], scores[winner])

        # handle illegal moves
        if not is_legal(state, letter):
            winner = 1 - turn
            print(names[turn], "played an illegal move and loses!", names[winner], "wins.")
            return (names[winner], scores[winner])

        points = move_points(state, letter)
        state.move(letter)
        scores[turn] += points

        turn = 1 - turn # swap players

    print(state)
    print("Final scores:", names[0], scores[0], "|", names[1], scores[1])

    if scores[0] > scores[1]:
        print(names[0], "wins!")
        return (names[0], scores[0])

    elif scores[0] < scores[1]:
        print(names[1], "wins!")
        return (names[1], scores[1])

    else:
        print("It's a draw!")
        return None


def tester(): # main test harness

    # class to simulate a player inputting moves
    class ScriptedPlayer:
        def __init__(self, name, moves):
            self.name = name
            # converts string of chars into list of moves
            self.moves = list(moves)

        # return newest move
        def next_move(self, state):
            return self.moves.pop(0)

    # helper function to provide test results
    def check(label, expected, result):
        if expected == result:
            status = "PASS"
        else:
            status = "FAIL"
        print("{} | {}: expected {}, got {}".format(status, label, expected, result))

    s1_grid = [[1, 1, 0, 0, 1],
              [1, 1, 0, 0, 0],
              [0, 0, 1, 1, 1],
              [0, 0, 0, 1, 1],
              [0, 0, 0, 0, 1]]

    # grid to simulate a draw
    draw_grid = [[1, 0, 0, 0, 1],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]]

    # grid to simulate a win
    win_grid = [[1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]]

    s1 = State(s1_grid)
    print("*" * 40)
    print("is_legal() Tests:")
    check("Input: 'A' ", True, is_legal(s1, "A"))
    check("Input: 'X' ", False, is_legal(s1, "X"))
    check("Input: 'Z' ", False, is_legal(s1, "Z"))
    check("Input: '' ", False, is_legal(s1, ""))
    check("Input: '3' ", False, is_legal(s1, "3"))

    print("*" * 40)
    print("move_points() Tests (taken from 1.1 example):")
    check("Alice performs move Y, cost of 2, bonus of 0", -2, move_points(s1, "Y"))
    s1.move("Y")
    check("Bob performs move M, cost of 3, bonus of 100", 97, move_points(s1, "M"))

    print("*" * 40)
    print("play() Tests:")
    draw_grid = State(draw_grid)
    # test draw
    result = play(draw_grid, ScriptedPlayer("P1", "A"), ScriptedPlayer("P2", "E"))
    check("Equal scores give a draw", None, result)
    # test win
    win_grid = State(win_grid)
    result = play(win_grid, ScriptedPlayer("P1", "BC"), ScriptedPlayer("P2", "A"))
    check("P1 Wins on points", ("P1", 198), result)


if __name__ == "__main__":
    tester()
