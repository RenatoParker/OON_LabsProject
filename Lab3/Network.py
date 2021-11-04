import json
import pandas as pd

from Node import Node
from Line import Line
from SignalInformation import SignalInformation
import math
import matplotlib.pyplot as plt


class Network:
    def __init__(self):
        self._nodeList = list()
        self._lineList = list()
        with open("../Resource/nodes.json", "r") as read_file:
            self._nodes = json.load(read_file)
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

    @property
    def nodeList(self):
        return self._nodeList

    @property
    def nodes(self):
        return self._nodes

    @property
    def lineList(self):
        return self._lineList

    # each node must have a dict of lines and each line must have a dictionary of a node
    def connect(self):
        for node in self._nodeList:
            for line in self._lineList:
                if line.label.startswith(node.label):
                    node.successive[line.label] = line

        for line in self._lineList:
            for label in line.label:
                node = next((x for x in self._nodeList if x.label == label))
                line.successive[label] = node


    def propagate(self, signal_information):
        print(self._nodeList)
        start_node = next((x for x in self._nodeList if x.label == signal_information.path[0]))
        propagated_signal_information = start_node.propagate(signal_information)
        return propagated_signal_information


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




    def find_paths(self, start, end, path=[]):
        graph = self._nodes
        path = path + [start]
        if start == end:
            return [path]
        if start not in graph:
            return []
        paths = []
        for node in graph[start].get("connected_nodes"):
            if node not in path:
                newpaths = self.find_paths(node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths



net = Network()
net.connect()
# net.draw()
paths = net.find_paths("A", "F")
signalInfo = SignalInformation(10, paths[0])
net.propagate(signalInfo)
print(paths)

totalPaths = []


for startingNode in net.nodes:
    for endingNode in net.nodes:
        paths = net.find_paths(startingNode, endingNode)
        for path in paths:
            formattedPath = ""
            for node in path:
                formattedPath = formattedPath + node + " -> "
            formattedPath = formattedPath[:-3]
            totalPaths.append([formattedPath, 0 , 0 , 0])


data = pd.DataFrame(totalPaths, columns=["Path","latency" ,"signal_noise" , "noiseAt1mW"])
print(data)


