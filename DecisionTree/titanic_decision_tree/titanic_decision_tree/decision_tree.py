# Skeleton code for the decision tree structure

# helper class for decision tree nodes
import copy

import numpy as np
from math import e, log
class DecisionNode:

    def __init__(self):
        self.test_attributes = None
        self.test_value = None
        self.child_nodes = {}
        self.action = None 


# class implementing an ID3 decision tree
class DecisionTree:
    
    def __init__(self):
        self.root = DecisionNode()
        self.ATTRIBUTE_VALUE = "survived" # the attribute we are interested in
        

    # TODO: implement
    def train(self, training_set, attributes):
        print ("Training...")

        # Indirection allows us to shield caller from DecisionNode details
        self.make_tree(training_set, attributes, self.root)

    def classify(self, example):
        current = self.root
        
        # traverse the tree to find the action
        while current.action is None:
            test_attr = current.test_attributes

            if test_attr is None:
                print("Test attribute is None")
                return None
            
            try:
                attribute_value = example[test_attr]
                if attribute_value in current.child_nodes:
                    current = current.child_nodes[attribute_value]
                else:
                    print(f"Attribute value {attribute_value} not found in child nodes")
                    return None
                
            except KeyError:
                print(f"KeyError: {test_attr} not found in example")
                return None
            
        return  current.action
            
    # TODO: implement
    def test (self, test_set):
        print ("Testing...")
        correct = 0
        incorrect = 0
        set_size = len(test_set)
        print(f"Testing on {set_size} examples")

        example_testcount = 0

        for example in test_set:
            actual_value = example[self.ATTRIBUTE_VALUE]
            example_testcount += 1

            if example_testcount % 100 == 0:
                print (f"Testing example {example_testcount} of {set_size}")
            

            # traverse the tree to find the action
            predicted_value = self.classify(example)
            print(f"Testing example {example_testcount} completed")


            if predicted_value == actual_value:
                correct += 1
            else:  
                incorrect += 1
                print (f"Incorrect prediction for {example} predicted {predicted_value} actual {actual_value}")
            
        percent = (correct / set_size) * 100
        print (f"Correct: {correct} Incorrect: {incorrect} Percent correct: {percent:.2f}%")

        return percent


    # Recursively buid the tree based on maximum information gain
    def make_tree (self, examples, attributes, decision_node):
        # Calculate initial entropy
        initial_entropy = self.entropy(examples)

        # if entropy is 0, nothing else to do
        # let's talk about single points of entry and exit in class
        if initial_entropy == 0.0:
            # set the action of this node to the value of the attribute we are interested in
            decision_node.action = examples[0][self.ATTRIBUTE_VALUE]
            return
        # if there are no more attributes to split on, set the action to the most common value
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
            print(f"Best attribute: {best_split_attribute} with information gain: {best_information_gain}")
            # remove the best attribute from the set we will pass down the tree
            new_attributes = copy.deepcopy(list(attributes))
            
            if best_split_attribute in new_attributes:
                new_attributes.remove(best_split_attribute)


            # TODO: create the child nodes
            for subset_key, subset_examples in best_sets.items():
                # create a new child node
                child_node = DecisionNode()
                # add the child node to the decision node
                decision_node.child_nodes[subset_key] = child_node

                # recursively call make_tree on the child node with the subset of examples and attributes
                self.make_tree(subset_examples , new_attributes, child_node)
            
            decision_node.test_attributes = best_split_attribute
            

    

    # Calculate the information entropy of an example set
    # TODO: implement
    def entropy(self, examples: list[dict]) -> float:
        """Calculate the entropy at a given node(attribute). """
        # Count the number of examples in each class
        examples_count = len(examples) #get the number of examples
        attribute_counts = {} # dictionary to hold the frequencies of each attribute value

        if examples_count == 0: # if there are no examples, there is no entropy
            return 0.0
        
        for example in examples: #for each example in the set
            # get the value of the attribute we are interested in
            value = example[self.ATTRIBUTE_VALUE]
            # if the value is not in the dictionary, add it
            if value not in attribute_counts:
                attribute_counts[value] = 1
            else:
                # if the value is in the dictionary, increment the count
                attribute_counts[value] += 1
        
        entropy = 0.0
        # Calculate the entropy
        for value, count in attribute_counts.items():
            # Calculate the probability of this value
            probability = count / examples_count
            # Calculate the entropy using the formula: -p * log2(p) for every value 
            if probability > 0:
                entropy -= probability * log(probability, 2)
            # print (f"Entropy for {value} = {entropy}")
            # print (f"Probability for {value} = {probability}")

        return entropy

    # Divide a set of examples based on an attribute value
    # TODO: implement
    def split_by_attribute(self, examples: list, attribute: str) ->  dict:
        print ("Splitting on " + attribute)
        sets = {}

        for example in examples:
            values = example[attribute]
            # if the value is not in the dictionary, add it
            if values not in sets:
                sets[values] = []

            sets[values].append(example)
        
        return sets



    # Find the entropy of a list of sets
    # TODO: implement
    def entropy_of_sets(self, sets, count):
        overall_entropy = 0.0

        for subset in sets.values():
            subset_entropy = self.entropy(subset)
            subset_count = len(subset)
            overall_entropy += (subset_count / count) * subset_entropy

        return overall_entropy
    
    def print_tree(self, node: DecisionNode, indent: str = ""):
        """Print the tree structure."""
        if node.test_attributes:
            for val, child in node.child_nodes.items():
                print(f"{indent}{node.test_attributes} = {val}")
                self.print_tree(child, indent + "  ")
        else:
            print(f"{indent}Action: {node.action}")
            return

    
if __name__ == '__main__':
    
    pass
    