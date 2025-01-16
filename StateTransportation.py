"""
Farmer, Fox, Goose, & Grain state transportation problem 
=====================================================

Using BFS Search algorithm to determine the optimal path and a tuple of integers to detect state

01/15/2025  --- Layden H.

====================================================

Process ----- 

States - Farmer, Fox, Goose, Grain = (1, 0, 0, 0) 

Constraints (inValidStates): 

- the fox cannot be alone with the goose
- the goose cannot be alone with the grain 

Search Algo - BFS

is_validState(), possibleMoves(), BFS() 
"""

from queue import Queue

#state = (1, 1, 1, 1) -> start state 
def is_validState(state: tuple) -> bool: 
    farmer, fox, goose, grain = state 

    #fox w/ goose - NO
    if fox == goose != farmer: #(fox = 1 == goose = 1) != farmer = 0 -> True != False -> True 
        return False
    #goose w/ grain - NO
    if goose == grain != farmer: # (goose = 1 == grain = 1) != farmer = 0 -> True != False -> True 
        return False
    
    return True

def possibleMoves(state: tuple) -> list: 
    farmer, fox, goose, grain = state
    current_states = []

    #farmer crossed alone
    farmerCrossing = 1 - farmer
    moves = [(farmerCrossing, fox, goose, grain)]

    #farmer takes fox
    if farmer == fox:
        moves.append((farmerCrossing, farmerCrossing, goose, grain))
    #farmer takes goose
    if farmer == goose:
        moves.append((farmerCrossing, fox, farmerCrossing, grain))

    #farmer takes grain
    if farmer == grain:
        moves.append((farmerCrossing, fox, goose, farmerCrossing))

    for move in moves:
        current_states.append(move)
    

    return current_states  

def BFS(state: tuple, goal: tuple) -> None:
    queue =  Queue()
    
    queue.put((state, [state]))
    visited = set([state])
    visited.add(state)
    while not queue.empty():
        current_state, current_path = queue.get()
        if current_state == goal:
            return current_path
        for next_state in possibleMoves(current_state):
            if is_validState(next_state) and next_state not in visited:
                queue.put((next_state, current_path + [next_state]))
                visited.add(next_state)
    
    return None

def printMember(step: tuple) -> str:
    sides = ["left", "right"]
    farmer, fox, goose, grain = step
    left_side = []
    right_side = []
    items = [("Farmer", farmer), ("Fox", fox), ("Goose", goose), ("Grain", grain)]
    for name, position in items:
        if position == 0:
            left_side.append(name)
        else: 
            right_side.append(name)

    left = ", ".join(left_side) if left_side else "None"
    right = ", ".join(right_side) if right_side else "None"

    return f"Left Bank: {left} | Right Bank: {right}"




if __name__ == "__main__":

    #initial state
    state = (0, 0, 0, 0)

    goal = (1, 1, 1, 1)

    solution = BFS(state, goal)
    if solution:
        for step in solution:
            print(step, printMember(step))
    else: 
        print("No solution exists")