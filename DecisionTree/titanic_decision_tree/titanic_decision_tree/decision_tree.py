# Skeleton code for the decision tree structure

# helper class for decision tree nodes
import copy

import numpy as np
from math import e, log
class DecisionNode:

    def __init__(self):
        self.test_value = None
        self.child_nodes = []


# class implementing an ID3 decision tree
class DecisionTree:

    def __init__(self):
        self.root = DecisionNode()

    # TODO: implement
    def train(self, training_set, attributes):
        print ("Training...")

        # Indirection allows us to shield caller from DecisionNode details
        self.make_tree(training_set, attributes, self.root)


    # TODO: implement
    def test (self, test_set):
        print ("Testing...")

    # Recursively buid the tree based on maximum information gain
    def make_tree (self, examples, attributes, decision_node):
        # Calculate initial entropy
        initial_entropy = self.entropy(examples)

        # if entropy is 0, nothing else to do
        # let's talk about single points of entry and exit in class
        if initial_entropy > 0.0:
            example_count = len(examples)

            # keep the best result
            best_information_gain =  0
            best_split_attribute = None
            best_sets = None

            # calculate information gain for each attribute
            for attr in attributes:
                sets = self.split_by_attribute(examples, attr)
                overall_entropy = self.entropy_of_sets(sets, example_count)
                information_gain = initial_entropy - overall_entropy

                # if this one is better, keep it
                if information_gain > best_information_gain:
                    best_information_gain = information_gain
                    best_split_attribute = attr
                    best_sets = sets

            # set the decision node to this attribute
            decision_node.test_value = best_split_attribute

            # remove the best attribute from the set we will pass down the tree
            new_attributes = copy.deepcopy(attributes)
            new_attributes -= best_split_attribute


            # TODO: create the child nodes
            for subset_key, subset_examples in best_sets.items():
                # create a new child node
                child_node = DecisionNode()
                # add the child node to the decision node
                decision_node.child_nodes.append((subset_key, child_node))
                # recursively call make_tree on the child node with the subset of examples and attributes
                self.make_tree(subset_examples , new_attributes, child_node)

    # Calculate the information entropy of an example set
    # TODO: implement
    def entropy(self, examples: list[dict]) -> float:

        n_examples: int = len(examples)

        if n_examples <= 1:
            return 0.0
        
        value, counts = np.unique(examples, return_counts=True) 
        probabilities = counts / n_examples
        n_classes = np.count_nonzero(probabilities)
        if n_classes <= 1:
            return 0.0
        entropy = 0.0
        base = e
        for i in probabilities:
            entropy -= i * log(i, base)

        return entropy

    # Divide a set of examples based on an attribute value
    # TODO: implement
    def split_by_attribute(self, examples: list, attribute) ->  dict:
        print ("Splitting on " + attribute)

        sets = {}
        for example in examples:

            key = example[attribute]


            if key not in sets:
                sets[key] = []
            # add the example to the set for this attribute value
            sets[key].append(example)
        
        #return list(sets.values())
        return sets



    # Find the entropy of a list of sets
    # TODO: implement
    def entropy_of_sets(self, sets, count):
        overall_entropy = 0.0

        for subset in sets:
            subset_entropy = self.entropy(subset)
            subset_count = len(subset)
            overall_entropy += (subset_count / count) * subset_entropy

        return overall_entropy

    


if __name__ == '__main__':
    

    #test entropy function
    dt = DecisionTree()
    test_set = [1, 0, 1, 1, 0, 0]
    print(dt.entropy(test_set))

    