import scipy.constants


class Line:
    def __init__(self, label, length):
        self._label = label
        self._length = length
        self._successive = dict()
        print("New line created:", "\t", "Label: ", self._label, "\t", "Length:", self._length)

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        self._label = label

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, length):
        self._length = length

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self, successive):
        self._successive = successive

    def latency_generation(self):
        return float(self._length / (scipy.constants.speed_of_light * (2 / 3)))

    def noise_generation(self, signal_power):
        return 1e-9 * signal_power * self._length

    # Define a propagate method that updates the signal information modifying its
    # noise power and its latency and call the successive element propagate method,
    # accordingly to the specified path.
    def propagate(self, signal_information):
        signal_information.increment_latency(self.latency_generation())
        signal_information.increment_noise(self.noise_generation())

        return signal_information
