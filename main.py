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
    # paths = net.find_paths("A", "F")
    # print(paths)
    # signalInfo = SignalInformation.SignalInformation(10, paths[0])
    # net.propagate(signalInfo)
    #
    # totalPaths = []
    #
    # for startingNode in net.nodes:
    #     for endingNode in net.nodes:
    #         paths = net.find_paths(startingNode, endingNode)
    #         for path in paths:
    #             formattedPath = ""
    #             for node in path:
    #                 formattedPath = formattedPath + node + " -> "
    #             formattedPath = formattedPath[:-3]
    #             signalPropagated = net.propagate(SignalInformation.SignalInformation(0.001, path))
    #             if signalPropagated.noise_power > 0:
    #                 noise_ratio = 10 * math.log(0.001 / signalPropagated.noise_power, 10)
    #             else:
    #                 noise_ratio = 0
    #             totalPaths.append([formattedPath, signalPropagated.latency, signalPropagated.noise_power, noise_ratio])
    #
    # data = pd.DataFrame(totalPaths, columns=["Path", "latency", "signal_noise", "noise_ratio"])
    # print(data)

    connectionsList = []
    for i in range(100):
        connectionsList.append(Connection.Connection(random.choice(list(net.nodes.values())), random.choice(list(net.nodes.values())), 1))
    print(connectionsList[0].latency)
    net.stream(connectionsList, "latency")
    for i in connectionsList:
        print("Latency: ", i.latency, "SNR:", i.snr, i.input.label, i.output.label)

    net.stream(connectionsList, "snr")
    for i in connectionsList:
        print("Latency: ", i.latency, "SNR:", i.snr, i.input.label, i.output.label)

