"""
Solution to the bridge and torch river crossing problem.
Adapted by Chris Branton January 21, 2023
Original solution by Carol Browning and Sarah Lester
January 24, 2020
"""
"""
Problem description: Four people come to a river at night. There is a narrow
bridge, but it can only hold two people at a time. They have one torch and,
because it's night, the torch has to be used when crossing the bridge.
Person A can cross the bridge in 1 minute, B in 2 minutes, C in 5 minutes,
and D in 8 minutes. When two people cross the bridge together,
they must move at the slower person's pace. The question is, can they all
get across the bridge if the torch lasts only 15 minutes?
"""
""" Define constants """

east = 1   #to change sides, multiply current side by -1
west = -1
torch = 0
a=1   #state list will be a list of sides (east or west) in the order
b=2   #torch, person a, person b, person c, person d
c=3
d=4

""" Define the Node class"""

class Node:
    def __init__(self,state: list, parent, action: list, cost: int):
        self.state = state   # a state is a list of four values, each either east or west
        self.parent = parent # this is the pointer to the previous state
        self.action = action # what action is performed on parent to get this state
        self.cost = cost     # length of path from initial state to this one

""" Given a state, generate a list of the possible actions """

#an action is a list of items to move.  
def actionList(state): 

    currentSide = state[torch]
    mylist = [] 

    for item in [a,b,c]:

        if state[item] == currentSide:
            mylist.append([torch,item])

            for item2 in range(item+1, d+1):

              if state[item2] == currentSide:
                mylist.append([torch, item, item2])

    return mylist

""" Check to see whether or not the given state is valid. """

def isValid(node):
  return node.cost <= 15

""" Given a current state and an action, determine the next state """

def makeNewState(currentState, action):
    if action == []: return currentState
    newState = []
    direction = currentState[torch]

    for state in currentState:
        newState.append(state)

    if direction == west:
      newDirection = east
    else:
      newDirection = west

    newState[torch] = newDirection 
    for person in action: 
        newState[person] = newDirection
    
    return newState

"""get action cost"""
def getActionCost(action):
  # gets the action that costs the most and returns the cost associated with that
    actionCosts = {1: 1, 2: 2, 3: 5, 4: 8}
    people = action[1:] 

    if people == []: return 0

    return max(actionCosts[person] for person in people)

""" findAnswer is the main algorithm for searching the space for a solution
    Returns a tuple of final node and number of nodes visited.
    Returns None if no solution found.
"""

def findAnswer():
    initial = [west,west,west,west,west]
    goal = [east,east,east,east,east]
    initialNode = Node(initial,None,None,0)

    openNodes = [initialNode]
    exploredStates = []

    while openNodes:
        currentNode = openNodes.pop(0)
        
        exploredStates.append(currentNode.state)

        if currentNode.state == goal:
            
            return currentNode, len(exploredStates)

        actions = actionList(currentNode.state)
        for action in actions:
            newState = makeNewState(currentNode.state, action)
            newCost = currentNode.cost + getActionCost(action)
            newNode = Node(newState, currentNode, action, newCost)

            if isValid(newNode) and newState not in exploredStates:
                openNodes.append(newNode)
    

    return None


"""get items in action"""
def getItems(action):
  items = ["Torch", "Person A", "Person B", "Person C", "Person D"]

  # return [items[i] for i in action]
  return items[action]

""" Print the path from the initial node to the given node """

def printAnswer(node):
    #if parent is None, we are done.  Otherwise, print the previous step then print this one.
    if node.parent != None:

        #print the path to the previous step
        printAnswer(node.parent)
        # #now print the action to get to this step
        message = " move "
        i = 0
        length = len(node.action)
        while(i < length):
          message += getItems(node.action[i])
          if i < length-1:
            message += ", "
          i+=1
        if node.state[0]== east: message = message + " west to east"
        else: message = message + " east to west"
        print(node.action,node.state, message)


        
    else: #We have recursed back to the initial state
        print(node.state, "Everyone is on the west bank.")


    if node.state == [east,east,east,east,east]:
        print(node.state, "Everyone is on the east bank.")

""" Main program. Find the answer and print the answer and the analysis
     complete the solution
"""

def test1():
  #testing MakeNewState
    currentState = [west, west, west, west, west]
    action = [torch, b, c]
    print(makeNewState(currentState, action))

def test2():
  #testing actionList
    currentState = [west, west, west, west, west]
    print(actionList(currentState))
    return actionList(currentState)

def test3():
  actions = [[torch, a], [torch, b], [torch, c], [torch, d], [torch, a, b], [torch, a, c], [torch, a, d], [torch, b, c], [torch, b, d], [torch, c, d]]
  for action in actions:
    print(f"Action: {action}, Cost: {getActionCost(action)}")

def test4():
  #testing getItems
  actions = test2()
  for action in actions:
    print(getItems(action))

if __name__ == "__main__":
    finalNode,numExploredStates = findAnswer()
    printAnswer(finalNode)
    print("Number of minutes spent = ",finalNode.cost)
    print("Number of explored states = ",numExploredStates)

    #test4()

    
