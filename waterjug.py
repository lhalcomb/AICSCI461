
import numpy as np
from collections import deque
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
    def __init__(self, state: tuple, parent: None, actions: None, cost: int):
        self.state = state
        self.parent = parent
        self.actions = actions
        self.cost = cost


    def is_goal(self):
        """Check to see if we have reached the goal state"""
        return 1 in self.state

    def is_valid(self, state):
        """Check if the state is valid"""
        if len(self.state) != len(CAPACITIES):
            return False
        for i in range(len(self.state)):
            if self.state[i] < 0 or self.state[i] > CAPACITIES[i]:
                return False
        return True


    def generate_states(self):
        # Generate all possible next states
        next_states = []
        x, y, z = self.state
        capacities = CAPACITIES
        #Fill a jug
        for i in range(len(self.state)): #initial = (0, 0, 0) capacities = (12, 8, 3)
            if (self.state[i] < capacities[i]) and self.is_valid(self.state): #if the jug is not full
                new_state = list(self.state) #copy the state -> new_state = [0, 0, 0]
                new_state[i] = capacities[i] #fill the jug -> new_state = [12, 0, 0]
                next_states.append((tuple(new_state), f"Fill jug {i + 1}")) #add the new state to the list of next states
        #Empty a jug
        for i in range(len(self.state)):
            if self.state[i] > 0 and self.is_valid(self.state): #if the jug is not empty
                new_state = list(self.state)
                new_state[i] = 0
                next_states.append((tuple(new_state), f"Empty jug {i+1}"))
        
        #Pour from one jug to another
        for i in range(len(self.state)):
            for j in range(len(self.state)):
                if i != j and self.is_valid(self.state): #avoid transferring into the same jug 
                    new_state = list(self.state) #copy the state
                    transfer_amount = min(self.state[i], capacities[j] - self.state[j]) #calculate the amount to transfer
                    new_state[i] -= transfer_amount
                    new_state[j] += transfer_amount
                    next_states.append((tuple(new_state), f"Pour from jug {i+1} to jug {j+1}"))
        return next_states
def reconstructPath(node):
    path = []
    while node:
        path.append(node)
        node = node.parent
    return path[::-1]


def bfsSolve(node):
    queue = deque([node]) #initialize the queue with the initial node for bfs searching
    visited = set() #tracking the visited states
    while queue:
        current_node = queue.popleft()
        if current_node.is_goal():
            return reconstructPath(current_node)
        next_states = current_node.generate_states()
        visited.add(current_node.state)
        for state, action in next_states:
            if state not in visited:
                new_node = Node(state, current_node, action, current_node.cost + 1)
                queue.append(new_node)
    return None

def dfsSolve(node):
    stack = [node]
    visited = set()
    while stack:
        current_node = stack.pop()
        if current_node.is_goal():
            return reconstructPath(current_node)
        next_states = current_node.generate_states()
        visited.add(current_node.state)
        for state, action in next_states:
            if state not in visited:
                new_node = Node(state, current_node, action, current_node.cost + 1)
                stack.append(new_node)
    return None



node = Node((0, 8, 0), None, None, 0)

def test1():
    print(node.is_valid((-1, 0, 0)))  # False
    print(node.is_valid((0, 0, 1)))  # True
    print(node.is_valid((-1, 0, 4)))  # False

def test2():
    # print(generate_states((12, 0, 0)))
    next_states = node.generate_states()
    statesOnly = [state for state, action in next_states]
    stateString = [f"{state} -> {action}" for state, action in next_states]
    print(np.matrix(statesOnly))
    print(np.matrix(stateString))
    # print(generate_states((0, 0, 3)))
    # print(generate_states((12, 8, 3)))

if __name__ == "__main__":
   

    print("BFS Solution")
    initial_state = (0, 0, 0)
    node = Node(initial_state, None, None, 0)

    path = bfsSolve(node)
    if path:
        for node in path:
            print(f"State : {node.state}, Action: {node.actions}, State Amount: {node.cost}")
    else:
            print("No solution found")

    print("\n \n \n")

    print("DFS Solution")
    node2 = Node(initial_state, None, None, 0)
    path2 = dfsSolve(node2)
    if path2:
        for node in path2:
            print(f"State : {node.state}, Action: {node.actions}, State Amount: {node.cost}")
    else:
        print("No solution found")
