import scipy.constants
import numpy as np
import math

from scipy.constants import pi as pi
from scipy.constants import e as e


# todo non importare tutta libreria ma solo le funzioni/costanti che ti servono

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
        self._launch_power = 10
        print("New line created:", "\t", "Label: ", self._label, "\t", "Length:", self._length)

        self._constant = {
            "aDb": 0.2,
            "B2": 2.13e-26,  # ps2/km;
            "GAMMA": 1.27,  # (Wm)−1;
            "A": 0.2 / (10 * (math.log(math.e, 10)))
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

    @property
    def launch_power(self):
        return self._launch_power

    @launch_power.setter
    def launch_power(self, launch_power):
        self._launch_power = launch_power

    def latency_generation(self):
        return float(self._length / (scipy.constants.speed_of_light * (2 / 3)))

    def noise_generation(self, signal_power):
        # todo 9.1
        # todo la lunghezza nelle slide è messa in km, quindi qua che ci va?
        loss = 10 ** (-self._constant["aDb"] * (self._length) / 10)
        Bn = 12.5e9
        Pnli = self.nli_generation(signal_power) * signal_power ** 3 * loss * self._gain * Bn
        GSNR = signal_power / (self.ase_generation() + Pnli)
        # print("GSNR:", GSNR)
        return abs(GSNR)

    # Define a propagate method that updates the signal information modifying its
    # noise power and its latency and call the successive element propagate method,
    # accordingly to the specified path.
    def propagate(self, signal_information):
        signal_information.increment_latency(self.latency_generation())
        signal_information.increment_noise(self.noise_generation(signal_information.signal_power, 10))
        return signal_information

    def ase_generation(self):
        f = 193.414e12
        Bn = 12.5e9
        ase = self._n_amplifiers * (
                scipy.constants.Planck * f
                * Bn * self._noise_figure * (self._gain - 1)
        )

        return ase

    def nli_generation(self, signal_power):
        # RS = 32 GHz
        nli = signal_power ** 3 * self.etaNLI() * (self._n_amplifiers - 1)
        # print("nli generated:", nli)
        return nli

    def etaNLI(self):
        channel = 10
        Rs = 32e9
        etaNLI = ((16 / (27 * pi)) * math.log(
            (pi ** 2) *
            self._constant["B2"] *
            Rs ** 2 * (channel ** (2 * Rs / 50e9)) / (2 * self._constant["A"] * 1e-3)) *
                  (self._constant["GAMMA"] ** 2) * (self._length ** 2) / (
                              4 * self._constant["A"] * (self._constant["B2"] * Rs ** 3)))
        # print("etaNLI: ", etaNLI)
        return etaNLI

    def optimized_launch_power(self, signal_power):
        # todo slide 32 - check
        # da questo devo far ritornare la potenza, non l'GSRN
        Bn = 12.5e9
        opt_pwr = (
            (self.noise_figure * self.length * signal_power) /
            (2 * Bn) * self.etaNLI()
        ) ** (1/3)
        # opt_pwr = ((self._length / 1000) * self._noise_figure * self._launch_power / (
        #             2 * self._constant["B2"] * self.etaNLI())) ** (1 / 3)
        # print("computer optimal power: ", opt_pwr)
        return opt_pwr
