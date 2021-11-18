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
        self._route_space = pd.DataFrame(None, columns=["Path", "Channel", "Status"])

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

    @property
    def route_space(self):
        return self._route_space

    @route_space.setter
    def route_space(self, route_space):
        self._route_space = route_space

    def initRouteSpace(self):
        data = []
        for startingNode in self._nodes:
            for endNode in self._nodes:
                if startingNode != endNode:
                    paths = self.find_paths(startingNode, endNode)
                    availability = False
                    for path in paths:
                        for channel in range(10):
                            tempPath = path.copy()
                            while len(tempPath) > 1:
                                availability = self._lines[tempPath[0] + tempPath[1]].state[channel]
                                tempPath.pop(0)
                            data.append([path, channel, availability])
        self._route_space = pd.DataFrame(data, columns=["Path", "Channel", "Status"])
        pd.set_option('display.max_rows', 30)
        print(self._route_space)

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
                    signalPropagated = self.probe(SignalInformation.SignalInformation(0.001, path.copy()))

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

    def check(self, list, A, B):
        if (A in list):
            if (list.index(A) < (len(list)-1) ):
                if list[ list.index(A) + 1 ] == B:
                    return True
                else:
                    return False


    def propagate(self, signal_information, channel):
        while len(signal_information.path) > 1:
            start_node = self._nodes[signal_information.path[0]]
            line = self._lines[signal_information.path[0] + signal_information.path[1]]
            line.state[channel] = False
            self._route_space.loc[(self._route_space["Channel"] == channel) & (self._route_space.Path.apply(lambda x: self.check(x, line.label[0] , line.label[1]) ) ) , ["Status"]] = False
            signal_information = start_node.propagate(signal_information, line)
        return signal_information

    def probe(self, signal_information):
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

    def getFreeChannelOnPath(self, path):
        query = self._route_space[(self._route_space["Path"].isin([path]))]
        # print("Query:\n", query)
        status = query[query["Status"] == True]
        # print("status:\n", status)
        firstChannelFree = status["Channel"].head(1).values
        if len(firstChannelFree) > 0:
            # print("Channel found:", firstChannelFree[0], " for path: ", path)
            return firstChannelFree[0]
        else:
            # print("no free channel found for path:", path)
            return None

    def find_best_snr(self, nodeA, nodeB):
        paths = self.find_paths(nodeA, nodeB)
        bestPath = []
        bestSNR = 0
        channel = None
        for path in paths:
            pathSignal = self.probe(SignalInformation.SignalInformation(0.01, path.copy()))
            if pathSignal.noise_power != 0:
                snr = 10 * math.log(0.001 / pathSignal.noise_power, 10)
                freeChannel = self.getFreeChannelOnPath(path)
                if (snr > bestSNR) & (freeChannel is not None):
                    bestSNR = snr
                    bestPath = path
                    channel = freeChannel
        return bestPath, channel

    def find_best_latency(self, nodeA, nodeB):
        paths = self.find_paths(nodeA, nodeB)
        bestLatency = float("inf")
        bestPath = []
        channel = None
        for path in paths:
            pathSignal = self.probe(SignalInformation.SignalInformation(0.01, path.copy()))
            # snr = 10 * math.log(0.001 / pathSignal.noise_power, 10)
            freeChannel = self.getFreeChannelOnPath(path)
            if (pathSignal.latency < bestLatency) & (freeChannel is not None):
                bestLatency = pathSignal.latency
                bestPath = path
                channel = freeChannel
        return bestPath, channel

    def stream(self, connections, label="latency"):
        for connection in connections:
            if label == "latency":
                pathAndChannel = self.find_best_latency(connection.input.label, connection.output.label)
            else:
                pathAndChannel = self.find_best_snr(connection.input.label, connection.output.label)
            pathSignal = self.propagate(SignalInformation.SignalInformation(0.01, pathAndChannel[0].copy()),pathAndChannel[1] )
            if len(pathAndChannel[0]) == 0:
                print("No available path found")
                connection.snr = 0
                connection.latency = None
            else:
                print("New path occupied:", pathAndChannel[0], "with channel: ", pathAndChannel[1])
                connection.latency = pathSignal.latency
                if pathSignal.noise_power != 0:
                    connection.snr = 10 * math.log(0.001 / pathSignal.noise_power, 10)
                else:
                    connection.snr = 0
