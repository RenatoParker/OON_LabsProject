
from components import Network
from components import Node
from pathlib import Path
import matplotlib.pyplot as plt

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
            nodeData["transceiver"] = "flex_rate"
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
    simulationResults = []

    for m in range(1, 50):
        traffic_matrix = []
        for indexRow, valueRow in enumerate(nodes_not_full):
            row = []
            for indexCol, valueCol in enumerate(nodes_not_full):
                if indexRow == indexCol:
                    row.append(0)
                else:
                    row.append(100 * m)
            traffic_matrix.append(row)
        print(traffic_matrix)
        simulationResults.append(net.createAndManageConnections(traffic_matrix, "latency"))

    avgBitrateAllocated = 0
    avgAllocatedConnections = 0
    avgBlockingEvent = 0

    GSNRavgs = []
    bitrateAllocated = []
    allocatedConnections = []
    blockingEvent = []

    for res in simulationResults:
        print(res)
        avgBitrateAllocated += res["bitrateAllocated"]
        avgAllocatedConnections += res["allocatedConnections"]
        avgBlockingEvent += res["blockingEvent"]

        GSNRavgs.append(res["GSNRavg"])
        bitrateAllocated.append(res["bitrateAllocated"])
        allocatedConnections.append(res["allocatedConnections"])
        blockingEvent.append(res["blockingEvent"])

    avgBitrateAllocated /= len(simulationResults)
    avgAllocatedConnections /= len(simulationResults)
    avgBlockingEvent /= len(simulationResults)

    print(avgBitrateAllocated)
    print(avgAllocatedConnections)
    print(avgBlockingEvent)

    plt.bar(range(1, 50), bitrateAllocated)
    plt.yscale('symlog')
    plt.show()
    plt.bar(range(1, 50), allocatedConnections)
    plt.yscale('log')
    plt.show()
    plt.bar(range(1, 50), blockingEvent)
    plt.show()
    print(GSNRavgs)
    print(type(GSNRavgs))
    plt.bar(range(1, 50), GSNRavgs)
    plt.show()


    # print(simulationResults)
