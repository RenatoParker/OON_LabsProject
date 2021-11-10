from components import Network
from components import Node

import json


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

