#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hinger Project
Coursework 001 for: CMP-6058A Artificial Intelligence

Includes the game loop for Task 3, as well as a tkinter GUI for playing the game

@author: <B07> (100475742, 100174060, 100464504, 100481021)
@date:   11/11/2026
"""


from a1_state import State, ROWS, COLS
from a2_agent import Agent
import tkinter as tk


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

    # test illegal moves
    result = play(win_grid, ScriptedPlayer("P1", "X"), ScriptedPlayer("P2", ""))
    check("P1 plays empty cell X, P2 wins", ("P2", 100), result)
    result = play(win_grid, ScriptedPlayer("P1", "B"), ScriptedPlayer("P2", "B"))
    check("P2 plays B after P1 emptied it, P1 wins", ("P1", 198), result)
    result = play(win_grid, ScriptedPlayer("P1", "A"), ScriptedPlayer("P2", "?"))
    check("P2 plays non-letter '?', P1 wins", ("P1", 99), result)
    result = play(win_grid, ScriptedPlayer("P1", ["AB"]), ScriptedPlayer("P2", ""))
    check("P1 plays two letters 'AB', P2 wins", ("P2", 100), result)
    result = play(win_grid, ScriptedPlayer("P1", [""]), ScriptedPlayer("P2", ""))
    check("P1 plays nothing, P2 wins", ("P2", 100), result)


class HingerGui:
    """Class to create a gui that allows the hinger game to be played.
       Requires board state, list of players/agents and root window to be passed."""

    background_colour = "light blue"
    frame_colour = "light blue"
    title_font = ("Calibri", 25)
    main_font = ("Calibri", 20)

    def __init__(self, state, players: list, root):
        self.state = State(state.grid)
        # store starting state to allow for resetting of board
        self.start_state = State(state.grid)
        self.players = players
        self.root = root

        # game variables
        self.names = []
        self.modes = []
        # initialise player names
        for i in range(0, 2):
            if self.players[i] is None:
                self.names.append("Human " + str(i + 1))
                self.modes.append(None)
            else:
                self.names.append(players[i].name)
                self.modes.append("alphabeta")
        self.scores = [100, 100]
        self.turn = 0
        self.result = None
        self.buttons = []

        # agent variables
        # ms delay between move to allow for visual clarity
        self.agent_delay = 1500
        # pending agent move, allows it to be cancelled on new game
        self.after_id = None

        # gui initialise
        root.title("Hinger Game")
        root.config(bg=self.background_colour)
        root.geometry("1000x700")
        self.initialise_root()
        self.refresh()
        self.schedule_agent()

    # initialise root window with main layout
    def initialise_root(self):
        title_frame = tk.Frame(self.root, bg=self.frame_colour)
        title_frame.pack(padx=5, pady=5, fill="x")
        self.title_text = tk.Label(title_frame, text="Hinger Game", font=self.title_font)
        self.title_text.pack(padx=5, pady=5, fill="x")

        main_frame = tk.Frame(self.root, bg=self.frame_colour)
        main_frame.pack(padx=5, pady=5)
        button_frame = tk.Frame(main_frame, bg=self.frame_colour)
        button_frame.grid(row=0, column=1, padx=10)
        self.player1_text = tk.Label(main_frame, text="Player 1: ", font=self.main_font, width=18)
        self.player1_text.grid(row=0, column=0, padx=10)
        self.player2_text = tk.Label(main_frame, text="Player 2: ", font=self.main_font, width=18)
        self.player2_text.grid(row=0, column=2, padx=10)

        # resign buttons layout
        self.resign_button_1 = tk.Button(main_frame, text="Resign (Z)", font=self.main_font, command=
        lambda: self.handle_move("Z"))
        self.resign_button_1.grid(row=1, column=0, padx=5, pady=5)
        self.resign_button_2 = tk.Button(main_frame, text="Resign (Z)", font=self.main_font, command=
        lambda: self.handle_move("Z"))
        self.resign_button_2.grid(row=1, column=2, padx=5, pady=5)
        # create list for ease of iteration
        self.resign_buttons = [self.resign_button_1, self.resign_button_2]

        # button grid layout
        for row in range(ROWS):
            row_buttons = []
            for column in range(COLS):
                # calculate letter at pos (row, column)
                letter = "ABCDEFGHIJKLMNOPQRSTUVWXY"[row * COLS + column]
                # create button
                button = tk.Button(button_frame, width=4, height=2, font=self.main_font, command=
                                   lambda move=letter: self.handle_move(move))
                button.grid(row=row, column=column, padx=2, pady=2)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        # player dropdowns
        options = ["Human"]
        # append agent options dynamically
        for mode in Agent().modes:
            options.append("Bot ({})".format(mode))

        # create dropdown and fill with player choices
        self.player_choices = []
        for i in range(2):
            if self.players[i] is None:
                choice = tk.StringVar(value="Human")
            else:
                choice = tk.StringVar(value="Bot ({})".format(self.modes[i]))
            # create dropdown
            dropdown = tk.OptionMenu(main_frame, choice, *options,
                                     command=lambda selected, i=i: self.set_player(i, selected))
            dropdown.config(font=self.main_font)
            if i == 0:
                dropdown.grid(row=2, column=0, padx=5, pady=5)
            else:
                dropdown.grid(row=2, column=2, padx=5, pady=5)
            self.player_choices.append(choice)

        # new game button
        new_game_button = tk.Button(main_frame, text="New Game", font=self.main_font, command=self.new_game)
        new_game_button.grid(row=1, column=1, padx=5, pady=5)

    # handle dropdown swapping player, start new game
    def set_player(self, i, selected):
        if selected == "Human":
            self.players[i] = None
            self.modes[i] = None
            self.names[i] = "Human " + str(i + 1)
        else:
            mode = selected[5:-1]  # "Bot (minimax)" -> "minimax"
            self.players[i] = Agent("Bot {} ({})".format(i + 1, mode))
            self.modes[i] = mode
            self.names[i] = self.players[i].name
        self.new_game()

    # refresh button grid from current state
    def refresh(self):
        for row in range(ROWS):
            for column in range(COLS):
                letter = "ABCDEFGHIJKLMNOPQRSTUVWXY"[row * COLS + column]
                count = self.state.grid[row][column]
                # colour available cells in white
                colour = "white" if count > 0 else "gray"
                self.buttons[row][column].config(text="{}\n{}".format(letter, count), bg=colour)

        # update player scores
        self.player1_text.config(text="{}: {}".format(self.names[0], self.scores[0]))
        self.player2_text.config(text="{}: {}".format(self.names[1], self.scores[1]))

        # disable resign buttons based off turn
        for i in range(2):
            if i == self.turn and self.players[i] is None:
                self.resign_buttons[i].config(state="normal")
            else:
                self.resign_buttons[i].config(state="disabled")

        # update text to show whose turn it is
        self.title_text.config(text="{}'s turn".format(self.names[self.turn]))

    # reset the game back to the starting board as well as scores
    def new_game(self):

        # cancel any agent move still waiting from the old game
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        # reset state and scores
        self.state = State(self.start_state.grid)
        self.scores = [100, 100]
        self.turn = 0
        self.result = None

        # update title
        self.title_text.config(text="New Game Starting! Resetting...")

        # enable the board
        for row in self.buttons:
            for button in row:
                button.config(state="normal")

        self.refresh()
        self.schedule_agent()

    # handle human turn
    def handle_move(self, letter):
        # if game has ended or not player's turn, return
        if self.result is not None or self.players[self.turn] is not None:
            return
        self.apply_move(letter)

    # retrieve move from agent and plays it
    def agent_turn(self):
        # clear pending moves
        self.after_id = None
        if self.result is not None:
            return
        letter = self.players[self.turn].next_move(self.state, self.modes[self.turn])
        self.apply_move(letter)

    # schedule next agent move before turn
    def schedule_agent(self):
        # if game has not ended and is agent's turn
        if self.result is None and self.players[self.turn] is not None:
            # load next move to keep track
            self.after_id = self.root.after(self.agent_delay, self.agent_turn)

    # play a single move for current player
    def apply_move(self, letter):
        # identify player and opponent
        player = self.names[self.turn]
        opponent = 1 - self.turn

        # handle Z being played
        if letter == "Z":
            self.end_game("{} resigned, {} wins!".format(player, self.names[opponent]),
                          (self.names[opponent], self.scores[opponent]))
            return

        # handle illegal move
        if not is_legal(self.state, letter):
            self.end_game("{} played an illegal move. {} wins!".format(player, self.names[opponent]),
                          (self.names[opponent], self.scores[opponent]))
            return

        # score move being made
        points = move_points(self.state, letter)
        self.state.move(letter)
        self.scores[self.turn] += points

        # swap turns
        self.turn = opponent
        # update board
        self.refresh()

        # handle board being empty and end game
        if board_empty(self.state):
            # win conditions
            if self.scores[0] > self.scores[1]:
                self.end_game("{} wins!".format(self.names[0]), (self.names[0], self.scores[0]))
            elif self.scores[1] > self.scores[0]:
                self.end_game("{} wins!".format(self.names[1]), (self.names[1], self.scores[1]))
            # draw
            else:
                self.end_game("It's a draw!", "draw")
            return
        self.schedule_agent()

    def end_game(self, message, result):
        self.result = result

        # disable board
        for row in self.buttons:
            for button in row:
                button.config(state="disabled")
        for button in self.resign_buttons:
            button.config(state="disabled")

        # update title text with result
        self.title_text.config(text=message)


if __name__ == "__main__":
    # tester()
    root = tk.Tk()
    start_state = State([[1, 1, 0, 0, 1],
                         [1, 1, 0, 0, 0],
                         [0, 0, 1, 1, 1],
                         [0, 0, 0, 1, 1],
                         [0, 0, 0, 0, 1]])
    gui = HingerGui(start_state, [None, Agent("Bot")], root)
    root.mainloop()
