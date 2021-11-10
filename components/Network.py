import json
import pandas as pd

from components import Node
from components import Line
from components import SignalInformation
import math
import matplotlib.pyplot as plt


class Network:
    def __init__(self, nodes):
        self._nodes = nodes
        self._lines = {}
        self._weighted_paths = None

        for node in self._nodes.values():
            for connectedNode in node.connected_node:
                label = node.label + connectedNode
                nodeConnected = self._nodes[connectedNode]
                y1 = node.position[1]
                y0 = nodeConnected.position[1]
                x1 = node.position[0]
                x0 = nodeConnected.position[0]
                dist = math.hypot(y1 - y0, x1 - x0)
                newLine = Line.Line(label, dist)
                self._lines[newLine.label] = newLine

    @property
    def nodes(self):
        return self._nodes

    @property
    def lines(self):
        return self._lines

    @property
    def weighted_paths(self):
        return self._weighted_paths

    def computeWeightedPaths(self):
        totalPaths = []
        for startingNode in self._nodes.values:
            for endingNode in self._nodes.values:
                paths = self.find_paths(startingNode, endingNode)
                for path in paths:
                    formattedPath = ""
                    for node in path:
                        formattedPath = formattedPath + node + " -> "
                    formattedPath = formattedPath[:-3]
                    signalPropagated = self.propagate(SignalInformation.SignalInformation(0.001, path))
                    if signalPropagated.noise_power > 0:
                        noise_ratio = 10 * math.log(0.001 / signalPropagated.noise_power, 10)
                    else:
                        noise_ratio = 0
                    totalPaths.append(
                        [formattedPath, signalPropagated.latency, signalPropagated.noise_power, noise_ratio])

        self._weighted_paths = pd.DataFrame(totalPaths, columns=["Path", "latency", "signal_noise", "noise_ratio"])
        print(self._weighted_paths)

    # each node must have a dict of lines and each line must have a dictionary of a node
    def connect(self):
        for nodeLabel, node in self._nodes.items():
            for lineLabel, line in self._lines.items():
                if lineLabel.startswith(nodeLabel):
                    node.successive[lineLabel] = line

        for lineLabel, line in self._lines.items():
            for letter in line.label:
                line.successive[letter] = self._nodes[letter]

    def propagate(self, signal_information):
        while len(signal_information.path) > 1:
            start_node = self._nodes[signal_information.path[0]]
            line = self._lines[signal_information.path[0] + signal_information.path[1]]
            signal_information = start_node.propagate(signal_information, line)
        return signal_information

    def draw(self):
        figure, axes = plt.subplots()
        plt.xlim(-800000, 800000)
        plt.ylim(-800000, 800000)
        for node in self._nodes.values():
            print(node.position[0], node.position[1])
            draw_circle = plt.Circle((node.position[0], node.position[1]), 30000, color='r')
            axes.add_artist(draw_circle)

        for line in self._lines.values():
            labelA = line.label[0]
            labelB = line.label[1]
            nodeA = self._nodes[labelA]
            nodeB = self._nodes[labelB]
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
        if start not in graph.keys():
            print("Node not in chart")
            return []
        paths = []
        for node in graph[start].connected_node:
            if node not in path:
                newpaths = self.find_paths(node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def find_best_snr(self, nodeA, nodeB):
        paths = self.find_paths(nodeA, nodeB)
        bestPath = paths[0]
        firstPathSignal = self.propagate(SignalInformation.SignalInformation(0.01, paths[0]))
        if firstPathSignal.noise_power == 0:
            bestSNR = 0
        else:
            bestSNR = 10 * math.log(0.001 / firstPathSignal.noise_power, 10)
        for path in paths[1:]:
            tempPath = path.copy()
            pathSignal = self.propagate(SignalInformation.SignalInformation(0.01, tempPath))
            if pathSignal.noise_power != 0:
                snr = 10 * math.log(0.001 / pathSignal.noise_power, 10)
                if snr > bestSNR:
                    bestSNR = snr
                    bestPath = path
        return bestPath

    def find_best_latency(self, nodeA, nodeB):
        paths = self.find_paths(nodeA, nodeB)
        bestPath = paths[0]
        firstPathSignal = self.propagate(SignalInformation.SignalInformation(0.01, paths[0]))
        bestLatency = firstPathSignal.latency
        for path in paths[1:]:
            tempPath = path.copy()
            pathSignal = self.propagate(SignalInformation.SignalInformation(0.01, tempPath))
            if pathSignal.latency < bestLatency:
                bestLatency = pathSignal.latency
                bestPath = path
        return bestPath

    def stream(self, connections, label="latency"):
        for connection in connections:
            if label == "latency":
                path = self.find_best_latency(connection.input.label, connection.output.label)
            else:
                path = self.find_best_snr(connection.input.label, connection.output.label)
            pathSignal = self.propagate(SignalInformation.SignalInformation(0.01, path))
            connection.latency = pathSignal.latency
            if pathSignal.noise_power != 0:
                connection.snr = 10 * math.log(0.001 / pathSignal.noise_power, 10)
            else:
                connection.snr = 0

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
#             signalPropagated = net.propagate(SignalInformation(0.001, path))
#             if signalPropagated.noise_power > 0:
#                 noise_ratio = 10 * math.log(0.001 / signalPropagated.noise_power, 10)
#             else:
#                 noise_ratio = 0
#             totalPaths.append([formattedPath, signalPropagated.latency, signalPropagated.noise_power, noise_ratio])
#
# data = pd.DataFrame(totalPaths, columns=["Path", "latency", "signal_noise", "noise_ratio"])
# print(data)
