class Node:
    def __init__(self, data):
        self._label = data["label"]
        self._position = data["position"]
        self._connected_node = data["connected_nodes"]
        self._successive = dict()
        self._switching_matrix = data["switching_matrix"]
        if "transceiver" in data:
            self._transceiver = data["transceiver"]
        else:
            self._transceiver = "fixed_rate"
        print("New node created:", "\t",
              "Label: ", self._label, "\t",
              "Position:", self._position, "\t",
              "Connected Node: ", self._connected_node, "\t",
              "Transceiver: ", self._transceiver, "\t",
              "Switching Matrix:", self._switching_matrix)

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        self._label = label

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    @property
    def connected_node(self):
        return self._connected_node

    @connected_node.setter
    def connected_node(self, connected_node):
        self._connected_node = connected_node

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self, successive):
        self._successive = successive

    @property
    def switching_matrix(self):
        return self._switching_matrix

    @switching_matrix.setter
    def switching_matrix(self, switching_matrix):
        self._switching_matrix = switching_matrix

    @property
    def transceiver(self):
        return self._transceiver

    @transceiver.setter
    def transceiver(self, transceiver):
        self._transceiver = transceiver

    def propagate(self, signal_information, line, channel, totalPath):
        if len(signal_information.path) > 1:
            signal_information.path.pop(0)
            latency = line.latency_generation()
            launch_power = line.optimized_launch_power()
            line.launch_power = launch_power
            noise = line.noise_generation(launch_power)
            signal_information.increment_latency(latency)
            signal_information.noise_power = noise

            if (totalPath is not None) & (channel is not None):
                index = totalPath.index(self._label)
                if (index != 0) & (index != len(totalPath)):
                    if channel == 0:
                        for key in self._switching_matrix:
                            self._switching_matrix[key][channel] = 0
                            self._switching_matrix[key][channel + 1] = 0
                    else:
                        if channel == 9:
                            for key in self._switching_matrix:
                                self._switching_matrix[key][channel] = 0
                                self._switching_matrix[key][channel - 1] = 0
                        else:
                            for key in self._switching_matrix:
                                self._switching_matrix[key][channel] = 0
                                self._switching_matrix[key][channel + 1] = 0
                                self._switching_matrix[key][channel - 1] = 0
            return signal_information

    def closeConnection(self, path, channel, totalPath):
        if len(path) > 1:
            path.pop(0)
            if (totalPath is not None) & (channel is not None):
                index = totalPath.index(self._label)
                if (index != 0) & (index != len(totalPath)):
                    for key in self._switching_matrix:
                        self._switching_matrix[key][channel] = 1
            return path
