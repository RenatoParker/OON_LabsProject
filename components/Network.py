import pandas as pd
import random

from components import Line
from components import SignalInformation
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import erfcinv
from enum import Enum
from components import Connection


# todo """
#  le matrici che hanno i path mi danno un tot di problemi perchè sto unsando delle liste
#  la cosa corretta da fare è non passare i path come liste, ma fargli una pulita e passarle come stringhe.
#  In realtà esiste un metrodo molto più ottimizzato: dovrei fare il traslato di quella matrice: i path dovrebbero
#  essere le colonne di quella matrice (una colonna per ogni path) e nelle colonne metto i valori relativi a tale path
#  questo di fatto è il modo più veloce per lavorare con gli hash su quella matrice """

class Network:
    def __init__(self, nodes):
        self._nodes = nodes
        self._lines = {}
        self._weighted_paths = None
        self._switching_matrix = {}  # todo: non devo metterla nel costruttore?
        self._route_space = pd.DataFrame(None, columns=["Path", "Status"])

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
        # sto modificando in modo da avere una sola riga per ogni path
        data = []
        for startingNode in self._nodes:
            for endNode in self._nodes:
                if startingNode != endNode:
                    paths = self.find_paths(startingNode, endNode)
                    availability = np.array([0] * 10, int)
                    for path in paths:
                        for channel in range(10):
                            tempPath = path.copy()
                            while len(tempPath) > 1:
                                availability[channel] = self._lines[tempPath[0] + tempPath[1]].state[channel]
                                tempPath.pop(0)
                        data.append([path, availability])
        self._route_space = pd.DataFrame(data, columns=["Path", "Status"])
        pd.set_option('display.max_rows', 30)
        print(self._route_space)

    def computeWeightedPaths(self):
        data = []
        allPaths = []
        for startingNode in self._nodes:
            for endNode in self._nodes:
                if startingNode != endNode:
                    allPaths = self.find_paths(startingNode, endNode)
                for path in allPaths:
                    signalPropagated = self.probe(SignalInformation.SignalInformation(10, path.copy()))
                    if signalPropagated.noise_power > 0:
                        print("ASD",signalPropagated.noise_power)
                        noise_ratio = 10 * math.log(10 / signalPropagated.noise_power, 10)
                    else:
                        noise_ratio = 0
                    data.append(
                        [path, signalPropagated.latency, signalPropagated.noise_power, noise_ratio])

        self._weighted_paths = pd.DataFrame(data, columns=["Path", "latency", "signal_noise", "noise_ratio"])
        print("Weightpath")
        print(self._weighted_paths)

    # each node must have a dict of lines and each line must have a dictionary of a node
    def connect(self):
        for nodeLabel, node in self._nodes.items():
            self._switching_matrix[nodeLabel] = node.switching_matrix
        print(self._switching_matrix)

    def findPathUsingLine(self, pathList, A, B):
        if A in pathList:
            if pathList.index(A) < (len(pathList) - 1):
                if pathList[pathList.index(A) + 1] == B:
                    return True
                else:
                    return False

    def isSubPath(self, pathExt, pathInt):
        isSubPath = False
        if len(pathExt) < len(pathInt):
            return isSubPath
        else:
            if pathInt[0] not in pathExt:
                return isSubPath
            index = pathExt.index(pathInt[0])
            for i in pathInt:
                if index > (len(pathExt) - 1):
                    return isSubPath
                if pathExt[index] == i:
                    index += 1
                else:
                    return isSubPath
            isSubPath = True
            return isSubPath

    def calculate_bit_rate(self, path, transceiver):
        # todo Modify the method calculate bit rate of the class Network to have as input a light-path instead of the
        #  path in order to retrieve the specific symbol rate Rs.

        index = self._weighted_paths.index[
            self._weighted_paths.Path.apply(lambda x: x == path)].tolist()

        GSNR = self._weighted_paths.at[index[0], "signal_noise"]
        print("GSNR ", GSNR)
        print(transceiver)
        if transceiver == "fixed_rate":
            if GSNR >= 2 * erfcinv(2 * 1 * 10e-3) ** 2 * 32 * 10e9 / (12.5 * 10e9):
                return 100 * 10e9
            else:
                return 0
        if transceiver == "flex_rate":
            if GSNR < 2 * erfcinv(2 * 1e-3) ** 2 * 32e9 / 12.5e9:
                return 0
            if (GSNR >= 2 * erfcinv(2 * 1 * 10e-3) ** 2 * 32 * 10e9 / (12.5 * 10e9)) & (
                    GSNR < (14 / 3) * erfcinv((3 / 2) * 1 * 10e-3) ** 2 * 32 * 10e9 / (12.5 * 10e9)):
                return 100 * 10e9
            if (GSNR >= (14 / 3) * erfcinv((3 / 2) * 1 * 10e-3) ** 2 * 32 * 10e9 / (12.5 * 10e9)) & (
                    GSNR < 10 * erfcinv((8 / 3) * 1 * 10e-3) ** 2 * 32 * 10e9 / (12.5 * 10e9)):
                return 200 * 10e9
            if GSNR > 10 * erfcinv((8 / 3) * 1 * 10e-3) ** 2 * 32 * 10e9 / (12.5 * 10e9):
                return 400 * 10e9

        if transceiver == "shannon":
            return 2 * 32 * 10e9 * math.log((1 + GSNR * (32 * 10e9 / 12.5 * 10e9)), 2) * 10e9

    def updateRouteSpace(self, path):
        prev = path[0]
        for next in path[1:]:
            line = [prev, next]
            prev = next
            allIndex = self._route_space.index[
                self._route_space.Path.apply(lambda x: self.isSubPath(x, line))].tolist()
        for index in allIndex:
            path = self._route_space.at[index, "Path"]
            start = path[0]
            rs_update = np.array([1] * 10, int)
            for i in range(len(path) - 1):
                next = path[i + 1]
                lineObj = self._lines[start + next]
                if (i != 0) & (i != len(path)):
                    # lab 7: sto modificando la matrice che viene usata da quella del network a quella del nodo
                    # matrix = self._switching_matrix[start][path[i-1]][next]
                    matrix = self._nodes[start].switching_matrix[path[i - 1]][next]
                else:
                    matrix = np.array([1] * 10, int)
                start = next
                rs_update *= matrix * lineObj.state
            self._route_space.at[index, "Status"] = rs_update
        # print(self._route_space)

    def propagate(self, signal_information, channel):
        totalPath = signal_information.path.copy()
        while len(signal_information.path) > 1:
            start_node = self._nodes[signal_information.path[0]]
            line = self._lines[signal_information.path[0] + signal_information.path[1]]
            line.state[channel] = 0
            signal_information = start_node.propagate(signal_information, line, channel, totalPath)
        for node in totalPath:
            self._nodes[node].switching_matrix = self._switching_matrix[node]
        return signal_information

    def probe(self, signal_information):
        while len(signal_information.path) > 1:
            start_node = self._nodes[signal_information.path[0]]
            line = self._lines[signal_information.path[0] + signal_information.path[1]]
            signal_information = start_node.propagate(signal_information, line, None, None)
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

    def getFreeChannelsOnPath(self, path):
        channelsStatus = self._route_space[(self._route_space["Path"].isin([path]))]["Status"].values
        # print("Query:\n", channelsStatus)
        if len(channelsStatus) == 0:
            return None
        else:
            # print(path, channelsStatus)
            return channelsStatus[0]

    def find_best_snr(self, nodeA, nodeB):
        if nodeA == nodeB:
            return None
        paths = self.find_paths(nodeA, nodeB)
        data = []
        weightedPaths = pd.DataFrame(data, columns=["Path", "latency", "signal_noise", "noise_ratio"])
        for path in paths:
            subData = self._weighted_paths.loc[self._weighted_paths.Path.apply(lambda x: x == path)]
            weightedPaths = pd.concat([weightedPaths, subData])
        while not weightedPaths.empty:
            max = weightedPaths.loc[weightedPaths["noise_ratio"] == weightedPaths["noise_ratio"].max()]
            pathOfMax = max.iloc[0].Path
            freeChannels = self.getFreeChannelsOnPath(pathOfMax)

            if freeChannels is None:
                print("ERROR")
            else:
                # devo cercare il primo libero
                for index, i in enumerate(freeChannels):
                    # print(i, index)
                    if i == 1:
                        return pathOfMax, index
            # se non lo trovo devo passare al prossimo path
            weightedPaths = weightedPaths.drop([weightedPaths["noise_ratio"].idxmax()])

    def find_best_latency(self, nodeA, nodeB):
        if nodeA == nodeB:
            return None
        paths = self.find_paths(nodeA, nodeB)
        data = []
        weightedPaths = pd.DataFrame(data, columns=["Path", "latency", "signal_noise", "noise_ratio"])
        for path in paths:
            subData = self._weighted_paths.loc[self._weighted_paths.Path.apply(lambda x: x == path)]
            weightedPaths = pd.concat([weightedPaths, subData])
        while not weightedPaths.empty:
            max = weightedPaths.loc[weightedPaths["latency"] == weightedPaths["latency"].min()]
            pathOfMax = max.iloc[0].Path
            freeChannels = self.getFreeChannelsOnPath(pathOfMax)

            if freeChannels is None:
                print("ERROR")
            else:
                # devo cercare il primo libero
                for index, i in enumerate(freeChannels):
                    # print(i, index)
                    if i == 1:
                        return pathOfMax, index
            # se non lo trovo devo passare al prossimo path
            weightedPaths = weightedPaths.drop([weightedPaths["latency"].idxmin()])

    def stream(self, connections, label="latency"):
        for connection in connections:
            if label == "latency":
                pathAndChannel = self.find_best_latency(connection.input.label, connection.output.label)
            else:
                pathAndChannel = self.find_best_snr(connection.input.label, connection.output.label)
            if pathAndChannel is None:
                print("No free channel found for connection:", connection.input.label, connection.output.label)
            else:
                if len(pathAndChannel[0]) == 0:
                    print("No available path found")
                    connection.snr = 0
                    connection.latency = None
                else:
                    print(pathAndChannel)
                    bit_rate = self.calculate_bit_rate(pathAndChannel[0], self._nodes[pathAndChannel[0][0]].transceiver)
                    print(" bit rate", bit_rate)
                    if bit_rate < 0:
                        print("this path do not support minimum BitRate")
                        return
                    connection.bit_rate = bit_rate
                    pathSignal = self.propagate(SignalInformation.SignalInformation(0.01, pathAndChannel[0].copy()),
                                                pathAndChannel[1])
                    print("New path occupied:", pathAndChannel[0], "with channel: ", pathAndChannel[1])
                    self.updateRouteSpace(pathAndChannel[0])
                    connection.latency = pathSignal.latency
                    if pathSignal.noise_power != 0:
                        connection.snr = 10 * math.log(0.001 / pathSignal.noise_power, 10)
                    else:
                        connection.snr = 0
                    return bit_rate

    def createAndManageConnections(self, trafficMatrix, label):
        connectionsList = []
        connectionsList.append(
            Connection.Connection(
                self._nodes[chr(65 + random.randint(0, len(trafficMatrix[0]) - 1))],
                self._nodes[chr(65 + random.randint(0, len(trafficMatrix[0]) - 1))],
                1))

        bit_rate = self.stream(connectionsList, label)
        print("Bit Rate: ", bit_rate)
        return 0
