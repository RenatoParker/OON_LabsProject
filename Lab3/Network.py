import json
from Node import Node
from Line import Line
import math
import matplotlib.pyplot as plt


class Network:
    def __init__(self):
        self._nodeList = list()
        self._lineList = list()
        with open("../Resource/nodes.json", "r") as read_file:
            self._nodes = json.load(read_file)
            # print(self._nodes)
            for nodeKey, nodeValue in self._nodes.items():
                nodeData = nodeValue
                nodeData["label"] = nodeKey
                new_node = Node(nodeData)
                self._nodeList.append(new_node)

            for node in self._nodeList:
                for connectedNode in node.connected_node:
                    label = node.label + connectedNode
                    nodeConnected = next((x for x in self._nodeList if x.label == connectedNode))
                    y1 = node.position[1]
                    y0 = nodeConnected.position[1]
                    x1 = node.position[0]
                    x0 = nodeConnected.position[0]
                    dist = math.hypot(y1 - y0, x1 - x0)
                    newLine = Line(label, dist)
                    self._lineList.append(newLine)

    # each node must have a dict of lines and each line must have a dictionary of a node
    def connect(self):
        for node in self._nodeList:
           for line in self._lineList:
               if line.label.startswith(node.label):
                   node.successive[line.label]=line

        for line in self._lineList:
            for label in line.label:
                node = next((x for x in self._nodeList if x.label == label))
                line.successive[label] = node


    def find_paths(self, labelA, labelB):
        nodes = self._nodeList.copy()
        paths = list()
        while len(nodes) > 0:
            path = []
            crossed = list()
            nodeA = next((x for x in self._nodeList if x.label == labelA))
            nodes.remove(nodeA)
            path.append(nodeA.label)
            neighbors = nodeA.successive.keys()
            for neighbor in neighbors:
                self.find_paths(neighbor.label, labelB)

    def recursive_find_paths(self , labelA, labelB, crossed):
        return
        # while len(nodes)> 1:


    def propagate(self, signal_information):
        return

    def draw(self):
        figure, axes = plt.subplots()
        plt.xlim(-800000, 800000)
        plt.ylim(-800000, 800000)
        for node in self._nodeList:
            print(node.position[0], node.position[1])
            draw_circle = plt.Circle((node.position[0], node.position[1]), 30000, color='r')
            axes.add_artist(draw_circle)

        for line in self._lineList:
            labelA = line.label[0]
            labelB = line.label[1]
            nodeA = next((x for x in self._nodeList if x.label == labelA))
            nodeB = next((x for x in self._nodeList if x.label == labelB))
            point1 = [nodeA.position[0], nodeA.position[1]]
            point2 = [nodeB.position[0], nodeB.position[1]]
            x_values = [point1[0], point2[0]]
            y_values = [point1[1], point2[1]]
            plt.plot(x_values, y_values, color="b")
        plt.show()

net = Network()
net.connect()
net.draw()
