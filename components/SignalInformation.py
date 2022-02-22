class SignalInformation:
    def __init__(self, signal_power, path):
        self._signal_power = signal_power
        self._noise_power = 0.0
        self._latency = 0.0
        self._path = path
        # print("New Signal Information created: \t Power:", self._signal_power, "\t Path:", self._path)

    @property
    def signal_power(self):
        return self._signal_power

    @signal_power.setter
    def signal_power(self, signal_power):
        self._signal_power = signal_power

    @property
    def noise_power(self):
        return self._noise_power

    @noise_power.setter
    def noise_power(self, noise_power):
        self._noise_power = noise_power

    @property
    def latency(self):
        return self._latency

    @latency.setter
    def latency(self, latency):
        self._latency = latency

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

    def increment_power(self, increment):
        self._signal_power += increment

    def increment_latency(self, increment):
        self._latency = self._latency + increment

    def increment_noise(self, increment):
        self._noise_power = self.noise_power + increment

    def add_path(self, new_element):
        self._path.append(new_element)
