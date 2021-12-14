import scipy.constants
import numpy as np
import math
#todo non importare tutta libreria ma solo le funzioni/costanti che ti servono

class Line:
    def __init__(self, label, length):
        self._label = label
        self._length = length
        self._successive = dict()
        # True means that the line is in state free
        self._state = np.array([1] * 10, int)
        self._n_amplifiers = int(length // (80 * 1000))
        self._gain = 16
        self._noise_figure = 3
        print("New line created:", "\t", "Label: ", self._label, "\t", "Length:", self._length)

        self._constant = {
            "aDb": 0.2,
            "B2": 2.13e-26,  # ps2/km;
            "GAMMA": 1.27,  # (Wm)−1;
            "A": 0.2 / (10 * (math.log(scipy.constants.e, 10)))
        }

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

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    @property
    def n_amplifiers(self):
        return self._n_amplifiers

    @n_amplifiers.setter
    def n_amplifiers(self, n_amplifiers):
        self._n_amplifiers = n_amplifiers

    @property
    def gain(self):
        return self._gain

    @gain.setter
    def gain(self, gain):
        self._gain = gain

    @property
    def noise_figure(self):
        return self._noise_figure

    @noise_figure.setter
    def noise_figure(self, noise_figure):
        self._noise_figure = noise_figure

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

    def ase_generation(self):
        return self._n_amplifiers * (scipy.constants.Planck * (193.414 * 1e12) * (
                    12.5 * 1e9) * self._n_amplifiers * self._noise_figure * (self._gain - 1))

    def nli_generation(self, signal_power, channel):
        # RS = 32 GHz
        # todo controlla questa funzione, aggiusta le costanti e definisci variabili invece di mettere i numeri
        return signal_power * channel**3 * ((16/(27*scipy.constants.pi)) * math.log((scipy.constants.pi**2) * self._constant["B2"] * 32e18 * channel**(2*32e9/50e9)*2*self._constant["A"]) * self._constant["GAMMA"]/(4*self._constant["A"]*self._constant["B2"]*32e9)) * self._n_amplifiers
