class Line:
    def __init__(self, label, length):
        self._label = label
        self._length = length
        self._successive = ""
        print("New line created:", "\t", "Label: ", self._label, "\t", "Length:", self._length)


    def latency_generation(self): float(self._length/(3.33564e-9*(2/3)))

    def noise_generation(self, signal_power): 1e-9 * signal_power * self._length

# Define a propagate method that updates the signal information modifying its
    # noise power and its latency and call the successive element propagate method,
    # accordingly to the specified path.
    def propagate(self, signal_information):
        signal_information.increment_latency(self.latency_generation())
        signal_information.increment_noise(self.noise_generation())

        return signal_information
