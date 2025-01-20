
 
"""
/*
2. Give a complete formulation (state, initial state, actions, etc.) to the following problem. 

Choose a formulation that is precise enough to be implemented.

Problem: 
You have three jugs, measuring 12 gallons, 8 gallons, and 3 gallons, and a water faucet. 
You can fill the jugs from the faucet, or from one another, or pour their contents on the ground. 
The goal is to measure out (in a jug) exactly one gallon. 
"""

CAPACITIES = (12, 8, 3)

class Node:
    def __init__(self, state: tuple, parent, actions: list, cost: int):
        self.state = state
        self.parent = parent
        self.actions = actions
        self.cost = cost


def is_goal(state):
    return 1 in state

def is_valid():
    

def generate_states(state):
    # Generate all possible next states
    next_states = []
    


