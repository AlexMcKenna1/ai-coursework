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

def get_move(player, state): # gets a move letter from a human or agent
    if player is None:
        user_input = (input("Your move (A-Y, or Z to quit): ")).strip().upper()
        return user_input
    else:
        return player.next_move(state)

    

def valid(r, c): # checks (r, c) is actually on the board
    return 0 <= r < ROWS and 0 <= c < COLS

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