"""
Hinger Project
Coursework 001 for: CMP-6058A Artificial Intelligence

Includes a Agent class for Task 2

@author: <group number> (<your ID>, <partner ID>, <partner ID>, <partner ID>)
@date:   22/10/2026
"""

from a1_state import State 
import time
import math
import random

class _MCTSNode:
    """One position in the Monte Carlo search tree."""

    def __init__(self, state, moves, player_to_move, score_gap,
                 parent=None, move=None):
        self.state = state
        self.untried_moves = moves
        self.player_to_move = player_to_move  # 0: agent, 1: opponent
        self.score_gap = score_gap            # agent points minus opponent points
        self.parent = parent
        self.move = move                      # move leading from parent to this node
        self.children = []
        self.visits = 0
        self.total_reward = 0.0
        
class Agent: 

    def __init__(self, name="A9"): 
        self.name = name
        self.modes = ["minimax", "alphabeta", "mcts"]
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

    def next_move(self, state, mode="alphabeta", depth=3, iterations=300):  
        if mode not in self.modes:  
            raise ValueError("Unknown mode: " + str(mode))

        if not self._legal_moves(state):  # empty board means no move possible
            return None

        if mode == "minimax":
            return self._best_move_minimax(state, depth)
        if mode == "mcts":
            return self._best_move_mcts(state, iterations)

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

    def _best_move_mcts(self, state, iterations):
        """Choose a move using UCT-based Monte Carlo Tree Search.

        Each rollout returns +1 for winning on points, -1 for losing,
        and 0 for a draw, evaluated from this agent's perspective.
        """
        if not isinstance(iterations, int) or iterations < 1:
            raise ValueError("MCTS iterations must be a positive integer")

        legal_moves = self._legal_moves(state)
        if not legal_moves:
            return None
        if len(legal_moves) == 1:
            return legal_moves[0]

        root = _MCTSNode(State(state.grid), legal_moves, player_to_move=0,
                         score_gap=0)

        for _ in range(iterations):
            node = root

            # 1. Selection: follow promising fully expanded branches.
            while not node.untried_moves and node.children:
                # At opponent nodes, prefer lower rewards for the agent.
                direction = 1 if node.player_to_move == 0 else -1
                node = max(
                    node.children,
                    key=lambda child: (
                        direction * (child.total_reward / child.visits)
                        + math.sqrt(2 * math.log(node.visits) / child.visits)
                    ),
                )

            # 2. Expansion: add one previously unexplored legal move.
            if node.untried_moves:
                move = random.choice(node.untried_moves)
                node.untried_moves.remove(move)
                points = self._points(node.state, move)
                new_state = self._play(node.state, move)
                new_gap = node.score_gap + (points if node.player_to_move == 0 else -points)
                child = _MCTSNode(new_state, self._legal_moves(new_state),
                                  1 - node.player_to_move, new_gap,
                                  parent=node, move=move)
                node.children.append(child)
                node = child
                self.nodes += 1

            # 3. Simulation: complete a game with random legal moves.
            rollout_state = State(node.state.grid)
            gap = node.score_gap
            turn = node.player_to_move
            while True:
                moves = self._legal_moves(rollout_state)
                if not moves:
                    break
                move = random.choice(moves)
                points = self._points(rollout_state, move)
                rollout_state.move(move)
                gap += points if turn == 0 else -points
                turn = 1 - turn
                self.nodes += 1

            # The game starts at 100-100, so final score difference is gap.
            reward = 1.0 if gap > 0 else (-1.0 if gap < 0 else 0.0)

            # 4. Backpropagation: update every ancestor in this path.
            while node is not None:
                node.visits += 1
                node.total_reward += reward
                node = node.parent

        # Most-visited root move is the best recommendation.
        return max(root.children, key=lambda child: child.visits).move

# Testing method
def tester():
    
    # Helper function to check test results
    def check(label, expected, result):
        if expected == result:
            print(f"PASS | {label}: expected {expected}, got {result}")
        else:
            print(f"FAIL | {label}: expected {expected}, got {result}")
            raise AssertionError(f"Test failed: {label}")

    agent = Agent()
    print(agent)

    print("*" * 40)
    print("Agent initialisation tests:")
    check("Agent name is a string", True, isinstance(agent.name, str))
    check("Minimax mode exists", True, "minimax" in agent.modes)
    check("Alphabeta mode exists", True, "alphabeta" in agent.modes)
    check("MCTS mode exists", True, "mcts" in agent.modes)

    # State s1 from Figure 1.1 in the spec
    s1 = State([[1, 1, 0, 0, 1],
                [1, 1, 0, 0, 0],
                [0, 0, 1, 1, 1],
                [0, 0, 0, 1, 1],
                [0, 0, 0, 0, 1]])

    print("*" * 40)
    print("Legal moves tests:")
    legal_moves = agent._legal_moves(s1)
    print("Legal moves:", legal_moves)
    check("Number of legal moves", 11, len(legal_moves))
    check("Move A is legal", True, "A" in legal_moves)
    check("Move X is illegal", False, "X" in legal_moves)

    print("*" * 40)
    print("Move cost and hinger tests:")

    # Alice plays Y on s1, cost 2, not a hinger
    check("Move Y cost", 2, agent._move_cost(s1, "Y"))
    check("Move Y is not a hinger", False, agent._is_hinger(s1, "Y"))
    check("Move Y points", -2, agent._points(s1, "Y"))

    # Make s2 by playing Y on a copy of s1
    s2 = State(s1.grid)
    s2.move("Y")

    # Bob plays M on s2, cost 3, is a hinger
    check("Move M cost", 3, agent._move_cost(s2, "M"))
    check("Move M is a hinger", True, agent._is_hinger(s2, "M"))
    check("Move M points", 97, agent._points(s2, "M"))

    print("*" * 40)
    print("Minimax, alphabeta and mtcs tests:")

    # Both strategies should return legitimate moves
    for mode in agent.modes:
        move = agent.next_move(s1, mode)
        check(f"{mode} returns a legal move",
              True, move in agent._legal_moves(s1))
        print(f"{mode} selected move: {move}")

    # Check expected move on s1
    check("Minimax best move", "M",
          agent.next_move(s1, "minimax"))
    check("Alphabeta best move", "M",
          agent.next_move(s1, "alphabeta"))
    check("MCTS best move", "M",
          agent.next_move(s1, "mcts"))

    # Test default strategy
    check("Default strategy move", "M",
          agent.next_move(s1))

    print("*" * 40)
    print("Empty board tests:")

    empty = State([[0] * 5 for _ in range(5)])

    for mode in agent.modes:
        check(f"{mode} on empty board", None,
              agent.next_move(empty, mode))

    print("*" * 40)
    print("Single legal move tests:")

    single = State([[1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0]])

    for mode in agent.modes:
        check(f"{mode} with one legal move", "A",
              agent.next_move(single, mode))

    print("*" * 40)
    print("Invalid mode test:")

    try:
        agent.next_move(s1, "invalid")
        error_caught = False
    except ValueError:
        error_caught = True

    check("Invalid mode raises ValueError", True, error_caught)

    print("*" * 40)
    print("Original state unchanged test:")

    original_grid = [row[:] for row in s1.grid]
    agent.next_move(s1, "alphabeta")
    check("Original state unchanged", original_grid, s1.grid)
    
    print("*" * 40)
    print("Minimax vs Alphabeta vs mcts efficiency comparison:")

    results = {}

    for mode in agent.modes:
        agent.nodes = 0
        start = time.perf_counter()

        move = agent.next_move(s1, mode, depth=5)

        took = time.perf_counter() - start
        results[mode] = (move, agent.nodes)

        print(f"{mode:10} | move {move} | "
              f"boards checked {agent.nodes:6} | {took:.3f}s")

    # Both strategies should produce the same best move
    check("Both strategies select the same move",
          results["minimax"][0],
          results["alphabeta"][0])

    # Alpha-beta should explore fewer or equal nodes
    check("Alphabeta explores fewer or equal nodes",
          True,
          results["alphabeta"][1] <= results["minimax"][1])

    print("*" * 40)
    print("All Agent tests passed!")
        
if __name__ == "__main__":
    tester()