class Node:
    def __init__(self, data):
        self._label = data["label"]
        self._position = data["position"]
        self._connected_node = data["connected_nodes"]
        self._successive = dict()
        print("New node created:", "\t", "Label: ", self._label, "\t", "Position:", self._position, "\t", "Connected Node: ", self._connected_node)



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

    def propagate(self, signal_information,line):
        if len(signal_information.path) > 1:
            signal_information.path.pop(0)
            latency = line.latency_generation()
            noise = line.noise_generation(signal_information.signal_power)
            signal_information.increment_latency(latency)
            signal_information.increment_noise(noise)
            # print("Propagate:", signal_information.path, "Latency:\t", latency, "Noise:\t", noise)
            return signal_information

