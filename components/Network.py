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
    def nodes(self):
        return self._nodes

    @property
    def lines(self):
        return self._lines

    # each node must have a dict of lines and each line must have a dictionary of a node
    def connect(self):
        for nodeLabel, node in self._nodes.items():
            for lineLabel,line in self._lines.items():
                if lineLabel.startswith(nodeLabel):
                    node.successive[lineLabel] = line

        for lineLabel, line in self._lines.items():
            for letter in line.label:
                line.successive[letter] = self._nodes[letter]

    def propagate(self, signal_information):
        while len(signal_information.path) > 1:
            start_node = self._nodes[signal_information.path[0]]
            line = self._lines[signal_information.path[0] + signal_information.path[1]]
            # nextNodeLabel = signal_information.path[1]
            # line = next((x for x in self._lineList if x.label == signal_information.path[0] + nextNodeLabel))
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
            print("non in chart")
            return []
        paths = []
        for node in graph[start].connected_node:
            if node not in path:
                newpaths = self.find_paths(node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def stream(self, connections, label="latency"):
        for connection in connections:
            connectionPaths = self.find_paths(connection.input.label, connection.output.label)
            print(connectionPaths, connectionPaths[0])
            firstPath = self.propagate(SignalInformation.SignalInformation(0.01, connectionPaths[0]))
            bestLatency = firstPath.latency
            bestPath = connectionPaths[0]
            if firstPath.noise_power == 0:
                bestSNR = 0
            else:
                bestSNR = 10 * math.log(0.001 / firstPath.noise_power, 10)
            for streamPath in connectionPaths:
                print("STREAM PATH", streamPath)
                streamSignalProgagated = self.propagate(SignalInformation.SignalInformation(0.01, streamPath))
                latency = streamSignalProgagated.latency
                print(latency, streamPath)
                if streamSignalProgagated.noise_power == 0:
                    snr = 0
                else:
                    snr = 10 * math.log(0.001 / streamSignalProgagated.noise_power, 10)
                if (label == "latency") & (latency < bestLatency) & (latency != 0.0):
                    bestPath = streamPath
                    bestLatency = latency
                    bestSNR = snr
                else:
                    if (label == "snr") & (snr > bestSNR):
                        bestPath = streamPath
                        bestLatency = latency
                        bestSNR = snr
                connection.latency = bestLatency
                connection.snr = bestSNR



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
