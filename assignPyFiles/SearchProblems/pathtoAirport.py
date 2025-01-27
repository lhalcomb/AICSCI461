"""
Create a Python implementation of A*. Run the program on the airport graph below.
Your output should list the nodes in the shortest path in order of traversal, as well as
the total cost of the path

"""


class Node: 
    def __init__(self, state: str, parent: None, actions: None, cost: int):
        self.state = state
        self.parent = parent
        self.actions = actions
        self.cost = cost