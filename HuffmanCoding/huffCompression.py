import heapq 
from graphviz import Digraph
import os

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq
    
nodes = []


def calc_freq(data, freq):

    for char in data:
        if char not in freq:
            letterfreq = data.count(char)
            freq[char] = letterfreq
            nodes.append(Node(char, letterfreq))

#Implement the build_huffman_tree function to create the Huffman tree from the nodes list.
def build_huffman_tree(freq_dict):
    heap = [Node(char, freq) for char, freq in freq_dict.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, freq = left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    
    return heap[0]

#Implement the generate_codes function to generate the Huffman codes for each character.
def generate_huffman_codes(node, prefix="", code_dict={}):
    if node is None:
        return
    if node.char is not None:
        code_dict[node.char] = prefix

    generate_huffman_codes(node.left, prefix + "0", code_dict)
    generate_huffman_codes(node.right, prefix + "1", code_dict)

    return code_dict

#Print the Huffman tree in a readable format. For visualizing the tree.
def visualize_tree(node):
    dot = Digraph()

    def add_nodes_edges(node, label = ""):
        if node is None:
            return
        
        node_id = str(id(node))

        if node.char:
            dot.node(node_id, f"'{node.char}'\n {node.freq}")
        else:
            dot.node(node_id, f"{node.freq}")
        
        if node.left:
            left_id = str(id(node.left))
            dot.edge(node_id, left_id, label="0")
            add_nodes_edges(node.left)
        if node.right:
            right_id = str(id(node.right))
            dot.edge(node_id, right_id, label="1")
            add_nodes_edges(node.right)
    add_nodes_edges(node)
    
    return dot

def print_tree(root):
    dot = visualize_tree(root)
    dot.render("huffman_tree_rapgod", view=True, format="png", cleanup=True)


def print_small_tree(root, indent=""):
    if root is None:
        return
    
    if root.char:
        print(f"{indent} Leaf: '{root.char}' (freq: {root.freq})")
    else:
        print(f"{indent} Node (freq: {root.freq})")
    print_small_tree(root.left, indent + " |----")
    print_small_tree(root.right, indent + " |----")

def test():
    data = "hello world"
    freq = {}
    calc_freq(data, freq)
    print("Frequency of characters in the data:")
    for char, freq in freq.items():
        print(f"{char}: {freq}")

def huffman_encoding(data, freq_dict):
    
    calc_freq(data, freq_dict)
    huffman_tree = build_huffman_tree(freq_dict)
    huffman_codes = generate_huffman_codes(huffman_tree)
    
    encoded_data = "".join(huffman_codes[char] for char in data)
    
    return encoded_data, huffman_codes


if __name__ == "__main__":
    
    #test()

    # Top 8 letters and their frequencies
    freqs = {
        'E': 12.70,
        'T': 9.06,
        'A': 8.17,
        'O': 7.51,
        'I': 6.97,
        'N': 6.75,
        'S': 6.33,
        'H': 6.09
    }

    #debugging 
    
    print("Current working directory:", os.getcwd())
    

    # Example data

    data = open("HuffmanCoding/rapgod.txt", "r").read()

    
    # Huffman encoding
    freq_dict = {}

    #Rap god lyrics by Eminem
    calc_freq(data, freq_dict)
    root = build_huffman_tree(freq_dict)
    huffman_codes = generate_huffman_codes(root)
    encoded_data = "".join(huffman_codes[char] for char in data)

    print("Sorted Frequency of letters in the data:")
    freq_dict = dict(sorted(freq_dict.items(), key=lambda item: item[1], reverse=True))
    for char, freq in freq_dict.items():
        print(f"{char}: {freq}")
    
   

    #Most comonly used letters in english
    # root = build_huffman_tree(freqs)
    # huffman_codes = generate_huffman_codes(root)
    # print_small_tree(root)
    
    

    print("Huffman Codes:")
    for char, code in huffman_codes.items():
        print(f"{char}: {code}")
    #Print Huffman Tree 
    print_tree(root)
    
    

