import json
from Node import Node
from Line import Line
import math

class Network:
    def __init__(self):
        nodeList = list()
        lineList = list()
        with open("../Resource/nodes.json", "r") as read_file:
            self._nodes = json.load(read_file)
            # print(self._nodes)
            for nodeKey, nodeValue in self._nodes.items():
                nodeData = nodeValue
                nodeData["label"] = nodeKey
                new_node = Node(nodeData)
                nodeList.append(new_node)

            for node in nodeList:
                for connectedNode in node.connected_node:
                    label = node.label + connectedNode
                    nodeConnected = next((x for x in nodeList if x.label == connectedNode))
                    y1 = node.position[1]
                    y0 = nodeConnected.position[1]
                    x1 = node.position[0]
                    x0 = nodeConnected.position[0]
                    dist = math.hypot(y1 - y0, x1 - x0)
                    newLine = Line(label, dist)
                    lineList.append(newLine)



net = Network()
