"""
Create a Python implementation of A*. Run the program on the airport graph.
Your output should list the nodes in the shortest path in order of traversal, as well as
the total cost of the path

"""
import pygame 
import random, math, heapq

# Pygame setup
pygame.init()
width, height = 1080, 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("A* Pathfinding Visualization")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)


class Node: 
    def __init__(self, name: str, position: tuple):
        self.name = name
        self.position = position
        self.heuristic = 0
        self.parent = None
        self.cost = float("inf")
        self.neighbors = []
    
    def drawCircle(self, screen, color):
        pygame.draw.circle(screen, color, (self.position[0], self.position[1]), 20)

    def drawLine(self, screen, color, neighbor):
        pygame.draw.line(screen, color, (self.position[0], self.position[1]), (neighbor.position[0], neighbor.position[1]), 2)
    
    def addNeighbor(self, neighbor: list, cost: int): 
        self.neighbors.append((neighbor, cost))

    def drawConnections(self, screen):
        for neighbor, cost in self.neighbors:
            self.drawLine(screen, BLACK, neighbor)
            mid_x = (self.position[0] + neighbor.position[0]) // 2
            mid_y = (self.position[1] + neighbor.position[1]) // 2
            font=pygame.font.Font(None, 20)
            text = font.render(str(cost), True, BLACK)
            screen.blit(text, (mid_x, mid_y))
    
    def heuristicMan(self, goal) :
        x1, y1 = self.position
        x2, y2 = goal.position  # Access position from Node object
        return abs(x1 - x2) + abs(y1 - y2)


def generateNodes(coords: list[tuple]) -> dict:
    nodes = {}  # Dictionary to store nodes by name
    places = [str(place) for place in range(1, 22)]  

    for place in places:
        nodes[place] = Node(place, coords[int(place)-1])

    for (node1, node2), cost in nodeConnections.items():
        nodes[node1].addNeighbor(nodes[node2], cost)
        nodes[node2].addNeighbor(nodes[node1], cost)

    return nodes  # Return a dictionary instead of a list

def drawNodes(screen, nodes):
    font = pygame.font.SysFont(None, 24)  # Create a font object
    for node in nodes.values():  # Iterate over dictionary values
        node.drawCircle(screen, BLACK)
        node.drawConnections(screen)
        
        # Render the node name
        text = font.render(node.name, True, WHITE)
        text_rect = text.get_rect(center=(node.position[0], node.position[1]))
        screen.blit(text, text_rect)  # Draw the text at the node's position

def reconstructPath(current: Node):
    total_path = []
    while current.parent:
        total_path.append(current)
        current = current.parent
    total_path.append(current)
    return total_path[::-1]

def aStar(start: Node, end: Node):
    start.heuristic = start.heuristicMan(end)
    start.cost = 0
    
    openPath = []
    heapq.heappush(openPath, (start.heuristic, start))  # Use priority queue
    visited = set()

    while openPath:
        _, current = heapq.heappop(openPath)  # Get node with lowest f-score

        if current in visited:
            continue
        visited.add(current)

        if current == end:
            path = reconstructPath(current)
            print(f"Shortest Path: {[node.name for node in path]}")
            print(f"Total Cost: {current.cost}")
            return path

        for neighbor, cost in current.neighbors:
            temp_cost = current.cost + cost  # g(n)
            if temp_cost < neighbor.cost:  # Found a better path
                neighbor.parent = current
                neighbor.cost = temp_cost
                neighbor.heuristic = temp_cost + neighbor.heuristicMan(end)  # f(n) = g(n) + h(n)
                heapq.heappush(openPath, (neighbor.heuristic, neighbor))
                

    return None  # No path found

def drawPath(screen, path):
     for i in range(len(path) - 1):
            pygame.draw.line(screen, RED, path[i].position, path[i+1].position, 2)

if __name__ == "__main__":
    coords =  coords = [(50, 100), (200, 100), (200, 200), (350, 400), (400, 200), (500, 300), 
              (600, 200), (700, 300), (700, 100), (800, 100), (800, 200), (900, 300), 
              (1000, 200), (1000, 100), (200, 400), (300, 500), (400, 600), (450, 600), 
              (750, 800), (800, 900), (750, 750)]

    nodeConnections = {
    ("1", "10"): 0.7, 
    ("1", "9"): 1.3, 
    ("2", "3"): 1.5, 
    ("3", "4"): 2.4, 
    ("3", "2"): 1.5,
    ("3", "7"): 2.3,
    ("3", "13"): 4.0, 
    ("4", "5"): 4.0, 
    ("4", "7"): 0.7, 
    ("4", "3"): 2.4,
    ("5", "6"): 2.1, 
    ("5", "8"): 0.8, 
    ("5", "4"): 4.0,
    ("6", "12"): 1.8, 
    ("7", "9"): 1.9, 
    ("7", "8"): 4.7,
    ("7", "3"): 2.3, 
    ("8", "11"): 1.8, 
    ("8", "7"): 4.7,
    ("9", "14"): 2.3, 
    ("10", "11"): 0.8, 
    ("10", "15"): 2.2, 
    ("11", "12"): 2.7, 
    ("11", "16"): 2.3, 
    ("11", "17"): 4.3, 
    ("12", "17"): 3.0, 
    ("13", "14"): 1.5, 
    ("14", "15"): 2.3, 
    ("15", "16"): 0.8, 
    ("15", "19"): 1.7, 
    ("16", "17"): 2.9, 
    ("16", "20"): 1.5, 
    ("17", "21"): 1.6, 
    ("18", "14"): 1.5, 
    ("18", "19"): 2.1, 
    ("19", "20"): 0.9, 
    ("20", "21"): 2.1, 
}

    

    coords = createPlaceCoordinates(width, height)
    #print(coords)
    nodes = generateNodes(coords)

    start_name = "1"
    end_name = "2"

    nodes = generateNodes(coords)  # Generate the node dictionary
    start_node = nodes[start_name]  # Get the start node
    end_node = nodes[end_name]  # Get the end node

    print(f"Start Node: {start_node.name}, Position: {start_node.position}")
    print(f"End Node: {end_node.name}, Position: {end_node.position}")

    path = aStar(start_node, end_node)
    running = True
    while running:
        screen.fill(WHITE)
        drawNodes(screen, nodes)
        if path:
            drawPath(screen, path)

    
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        clock.tick(60)


    pygame.quit()
