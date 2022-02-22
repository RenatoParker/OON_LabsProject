
from components import Network
from components import Node
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
    # with open("Resource/nodes_full_flex_rate.json", "r") as read_file:
    #     nodesJson = json.load(read_file)
    #     nodes_full = {}
    #     for nodeKey, nodeValue in nodesJson.items():
    #         nodeData = nodeValue
    #         nodeData["label"] = nodeKey
    #         new_node = Node.Node(nodeData)
    #         nodes_full[nodeKey] = new_node

    with open("Resource/279186/full_network.json", "r") as read_file:
        nodesJson = json.load(read_file)
        nodes_full = {}
        for nodeKey, nodeValue in nodesJson.items():
            nodeData = nodeValue
            nodeData["label"] = nodeKey
            # il transceiver non è specificato nei file; in teoria c'è un default nel costruttore del nodo
            # nodeData["transceiver"] = "shannon"
            new_node = Node.Node(nodeData)
            nodes_full[nodeKey] = new_node

    with open("Resource/279186/not_full_network.json", "r") as read_file:
        nodesJson = json.load(read_file)
        nodes_not_full = {}
        for nodeKey, nodeValue in nodesJson.items():
            nodeData = nodeValue
            nodeData["label"] = nodeKey
            new_node = Node.Node(nodeData)
            nodes_not_full[nodeKey] = new_node

    # net = Network.Network(nodes_not_full)
    net = Network.Network(nodes_full)
    net.connect()
    # net.draw()
    net.initRouteSpace()
    net.computeWeightedPaths()

    # connectionsList = []
    # for i in range(100):
    #     connectionsList.append(
    #         Connection.Connection(random.choice(list(net.nodes.values())), random.choice(list(net.nodes.values())), 1))
    # # connectionsList.append( Connection.Connection( nodes_full["A"], nodes_full["F"], 1))
    # net.stream(connectionsList, "snr")
    # net.stream(connectionsList, "latency")

    traffic_matrix = []
    simulationResults = []

    for m in range(50):
        for indexRow, valueRow in enumerate(nodes_not_full):
            row = []
            for indexCol, valueCol in enumerate(nodes_not_full):
                if indexRow == indexCol:
                    row.append(0)
                else:
                    row.append((indexCol + 1) * (indexRow + 1) * 200)
            traffic_matrix.append(row)
        # print(traffic_matrix)
        simulationResults.append(net.createAndManageConnections(traffic_matrix, "snr"))

    print(simulationResults)
