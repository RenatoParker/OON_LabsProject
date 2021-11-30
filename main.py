import random

from components import Network
from components import Node
from components import Connection
from pathlib import Path

import json


if __name__ == '__main__':
    # root = Path(__file__).parent
    # with open("Resource/nodes.json", "r") as read_file:
    #     nodesJson = json.load(read_file)
    #     nodes = {}
    #     for nodeKey, nodeValue in nodesJson.items():
    #         nodeData = nodeValue
    #         nodeData["label"] = nodeKey
    #         new_node = Node.Node(nodeData)
    #         nodes[nodeKey] = new_node

    root = Path(__file__).parent
    with open("Resource/nodes_full.json", "r") as read_file:
        nodesJson = json.load(read_file)
        nodes_full = {}
        for nodeKey, nodeValue in nodesJson.items():
            nodeData = nodeValue
            nodeData["label"] = nodeKey
            new_node = Node.Node(nodeData)
            nodes_full[nodeKey] = new_node

    with open("Resource/nodes_not_full.json", "r") as read_file:
        nodesJson = json.load(read_file)
        nodes_not_full = {}
        for nodeKey, nodeValue in nodesJson.items():
            nodeData = nodeValue
            nodeData["label"] = nodeKey
            new_node = Node.Node(nodeData)
            nodes_not_full[nodeKey] = new_node

    net = Network.Network(nodes_not_full)
    net.connect()
    # net.draw()
    # net.find_best_snr("A", "F")
    # net.find_best_latency("A", "F")
    net.initRouteSpace()
    net.computeWeightedPaths()
    # net.checkIfPathIsFree(["A", "B"])

    connectionsList = []
    for i in range(100):
        connectionsList.append(Connection.Connection(random.choice(list(net.nodes.values())), random.choice(list(net.nodes.values())), 1))
    # connectionsList.append( Connection.Connection( nodes["A"], nodes["B"], 1))
    net.stream(connectionsList, "snr")
    # net.stream(connectionsList, "latency")

