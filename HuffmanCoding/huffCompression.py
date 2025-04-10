import heapq 

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

#TODO: Implement the build_huffman_tree function to create the Huffman tree from the nodes list.
def build_huffman_tree(freq_dict):
    pass

#TODO: Implement the generate_codes function to generate the Huffman codes for each character.
def generate_codes(node, prefix="", code_dict={}):
    pass

#TODO: Print the Huffman tree in a readable format. For visualizing the tree.
def print_tree(node, prefix=""):
    pass

def test():
    data = "hello world"
    freq = {}
    calc_freq(data, freq)
    print("Frequency of characters in the data:")
    for char, freq in freq.items():
        print(f"{char}: {freq}")


if __name__ == "__main__":
    
    test()

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
