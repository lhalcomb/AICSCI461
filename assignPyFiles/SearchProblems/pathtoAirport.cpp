#include <iostream> 
#include <vector>
#include <algorithm>
#include <queue>
#include <climits>
#include <string>
#include <unordered_map>
#include <cstdint>

using namespace std;

struct Node {
    string name;
    vector<pair<Node*, int>> neighbors; // pair<node, distance> neighbors to the specified node
    double distance = INT_MAX; //distance between each node and it's neighbor
    Node* prev = nullptr; //pointer to the previous node

};


// Custom hash function for a pair of strings
struct pair_hash {
    template <class T1, class T2>
    std::size_t operator()(const std::pair<T1, T2>& p) const {
        auto h1 = std::hash<T1>{}(p.first);
        auto h2 = std::hash<T2>{}(p.second);
        return h1 ^ (h2 << 1); // Combine the two hash values
    }
};






int main(){
    unordered_map<pair<string, string>, double, pair_hash> nodeConnections = {
        {{"1", "10"}, 0.7}, {{"1", "9"}, 1.3},
        {{"2", "3"}, 1.5}, {{"3", "4"}, 2.4}, {{"3", "2"}, 1.5},
        {{"3", "7"}, 2.3}, {{"3", "13"}, 4.0}, {{"4", "5"}, 4.0},
        {{"4", "7"}, 0.7}, {{"4", "3"}, 2.4}, {{"5", "6"}, 2.1},
        {{"5", "8"}, 0.8}, {{"5", "4"}, 4.0}, {{"6", "12"}, 1.8},
        {{"7", "9"}, 1.9}, {{"7", "8"}, 4.7}, {{"7", "3"}, 2.3},
        {{"8", "11"}, 1.8}, {{"8", "7"}, 4.7}, {{"9", "14"}, 2.3},
        {{"10", "11"}, 0.8}, {{"10", "15"}, 2.2}, {{"11", "12"}, 2.7},
        {{"11", "16"}, 2.3}, {{"11", "17"}, 4.3}, {{"12", "17"}, 3.0},
        {{"13", "14"}, 1.5}, {{"14", "15"}, 2.3}, {{"15", "16"}, 0.8},
        {{"15", "19"}, 1.7}, {{"16", "17"}, 2.9}, {{"16", "20"}, 1.5},
        {{"17", "21"}, 1.6}, {{"18", "14"}, 1.5}, {{"18", "19"}, 2.1},
        {{"19", "20"}, 0.9}, {{"20", "21"}, 2.1}
    };

    unordered_map<string, Node> nodes;

    //populate the nodes
    for (const auto& connections: nodeConnections){
        string from = connections.first.first;
        string to = connections.first.second;
        double distance = connections.second;

        if (nodes.find(from) == nodes.end()){ // if find() == end() then the node is not in the map
            nodes[from] = Node{from}; // nodes[from] adds node to the map, Node{from} initializes the node from pointer above
        }
        if (nodes.find(to) == nodes.end()){
            nodes[to] = Node{to};
        }

        nodes[from].neighbors.emplace_back(&nodes[to], distance); // add the from neighbor to the nodes map 
    }; 

    //print the graph 
    for (const auto& node: nodes){
        cout << "Node: " <<node.first << endl;
        for (const auto& neighbor: node.second.neighbors){
            cout << "Neighbor: " << neighbor.first->name << " Distance: " << neighbor.second << endl;
        }
    };


    
};

