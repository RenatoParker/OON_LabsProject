import random

from components import Network
from components import Node
from components import SignalInformation
from components import Connection

import json
import math
import pandas as pd


if __name__ == '__main__':
    with open("./Resource/nodes.json", "r") as read_file:
        nodesJson = json.load(read_file)
        nodes = {}
        for nodeKey, nodeValue in nodesJson.items():
            nodeData = nodeValue
            nodeData["label"] = nodeKey
            new_node = Node.Node(nodeData)
            nodes[nodeKey] = new_node

    net = Network.Network(nodes)
    net.connect()
    # net.draw()
    net.find_best_snr("A", "F")
    net.find_best_latency("A", "F")

    connectionsList = []
    for i in range(100):
        connectionsList.append(Connection.Connection(random.choice(list(net.nodes.values())), random.choice(list(net.nodes.values())), 1))
    net.stream(connectionsList, "latency")
    # for i in connectionsList:
    #     print("Latency: ", i.latency, "SNR:", i.snr, i.input.label, i.output.label)

    net.stream(connectionsList, "snr")
    # for i in connectionsList:
    #     print("Latency: ", i.latency, "SNR:", i.snr, i.input.label, i.output.label)

