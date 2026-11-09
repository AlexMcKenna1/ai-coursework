"""
Hinger Project
Coursework 001 for: CMP-6058A Artificial Intelligence

Includes a Agent class for Task 2

@author: <group number> (<your ID>, <partner ID>, <partner ID>, <partner ID>)
@date:   22/10/2026
"""

from a1_state import State 
import time

class Agent: 

    def __init__(self, name="A9"): 
        self.name = name
        self.modes = ["minimax", "alphabeta"]
        self.nodes = 0  #counts how many boards the agent looks at

    def __str__(self): #What print(agent) will show
        return f"Agent {self.name} | modes: {', '.join(self.modes)}"

    def _legal_moves(self, state): # returns a list of every leter allowed to play
        moves = []

        for row in range(5): #go down the rows 
            for col in range(5): #in each row, go across the coloums
                if state.grid[row][col] > 0:
                    letter = chr(ord("A") + row * 5 + col) #turns the sqaure into its letter 
                    moves.append(letter) 

        return moves 
    
    def _move_cost(self, state, letter):
        row, col = state.letter_to_cell(letter)
        cost = 0

        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r = row + dr
                c = col + dc
                if 0 <= r < 5 and 0 <= c < 5 and state.grid[r][c] > 0:
                    cost += 1


        return cost

    def _is_hinger(self, state, letter): 
        row, col = state.letter_to_cell(letter)

        if state.grid[row][col] != 1:   # hingers must have exactly 1 counter
            return False

        test_board = State(state.grid)  #photocopy the board (a1_state copies the grid)
        test_board.grid[row][col] = 0   

        return test_board.numRegions() > state.numRegions()  
    
    def _points(self, state, letter):  #how many points this move earns (it can be negative)
        bonus = 100 if self._is_hinger(state, letter) else 0   
        return bonus - self._move_cost(state, letter)         

    def _play(self, state, letter):  # makes the move on a COPY and returns the new board
        new_board = State(state.grid)  
        new_board.move(letter)         
        return new_board


    def _minimax(self, state, depth, my_turn, gap):  # returns the best gap reachable from this point
        self.nodes += 1  
        moves = self._legal_moves(state)

        if depth == 0 or not moves:  
            return gap

        if my_turn:  
            best = float("-inf")  # start at minus infinity
            for letter in moves:
                new_gap = gap + self._points(state, letter)  
                result = self._minimax(self._play(state, letter), depth - 1, False, new_gap)
                best = max(best, result)  
            return best

        else:  
            best = float("inf")   #start at plus infinity
            for letter in moves:
                new_gap = gap - self._points(state, letter)  
                result = self._minimax(self._play(state, letter), depth - 1, True, new_gap)
                best = min(best, result)  
            return best

    def _best_move_minimax(self, state, depth):  
        best_letter = None
        best_score = float("-inf")

        for letter in self._legal_moves(state):
            first_points = self._points(state, letter)  
            score = self._minimax(self._play(state, letter), depth - 1, False, first_points)  
            if score > best_score:  
                best_score = score
                best_letter = letter

        return best_letter

    def next_move(self, state, mode="alphabeta", depth=3):  
        if mode not in self.modes:  
            raise ValueError("Unknown mode: " + str(mode))

        if not self._legal_moves(state):  # empty board means no move possible
            return None

        if mode == "minimax":
            return self._best_move_minimax(state, depth)
        
        return self._best_move_alphabeta(state, depth)  

    def _alphabeta(self, state, depth, my_turn, gap, alpha, beta):  
        self.nodes += 1  
        moves = self._legal_moves(state)

        if depth == 0 or not moves: 
            return gap

        if my_turn:  
            best = float("-inf")
            for letter in moves:
                new_gap = gap + self._points(state, letter)
                result = self._alphabeta(self._play(state, letter), depth - 1, False, new_gap, alpha, beta)
                best = max(best, result)
                alpha = max(alpha, best)  
                if alpha >= beta:       
                    break                 
            return best

        else:  
            best = float("inf")
            for letter in moves:
                new_gap = gap - self._points(state, letter)
                result = self._alphabeta(self._play(state, letter), depth - 1, True, new_gap, alpha, beta)
                best = min(best, result)
                beta = min(beta, best)    
                if alpha >= beta:         
                    break                 
            return best

    def _best_move_alphabeta(self, state, depth):  
        best_letter = None
        best_score = float("-inf")
        alpha = float("-inf")  
        beta = float("inf")   

        for letter in self._legal_moves(state):
            first_points = self._points(state, letter)
            score = self._alphabeta(self._play(state, letter), depth - 1, False, first_points, alpha, beta)
            if score > best_score:
                best_score = score
                best_letter = letter
            alpha = max(alpha, best_score)  

        return best_letter


    

    
#Testing method
if __name__ == "__main__": #runs only when this file(a2_agent) is run directly
    agent = Agent()
    print(agent)

        # State s1 from Figure 1.1 in the spec
    s1 = State([[1, 1, 0, 0, 1],
                [1, 1, 0, 0, 0],
                [0, 0, 1, 1, 1],
                [0, 0, 0, 1, 1],
                [0, 0, 0, 0, 1]])
    print(agent._legal_moves(s1))

        #Alice plays Y on s1 , cost 2, not a hinger
    print("Y cost:", agent._move_cost(s1, "Y"), "| hinger:", agent._is_hinger(s1, "Y"))

    # Make s2 by playing Y on a copy of s1
    s2 = State(s1.grid)
    s2.move("Y")

    #Bob plays M on s2 , cost 3, IS a hinger
    print("M cost:", agent._move_cost(s2, "M"), "| hinger:", agent._is_hinger(s2, "M")) 


    print("Minimax move on s1:", agent.next_move(s1, "minimax"))
    print("Empty board:", agent.next_move(State([[0]*5 for _ in range(5)]), "minimax"))

    print("Alphabeta move on s1:", agent.next_move(s1, "alphabeta"))

    # Efficiency comparison: same answer
    for mode in agent.modes:
        agent.nodes = 0
        start = time.perf_counter()
        move = agent.next_move(s1, mode, depth=5)
        took = time.perf_counter() - start
        print(f"{mode:10} | move {move} | boards checked {agent.nodes:6} | {took:.3f}s")