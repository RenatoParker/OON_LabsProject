from components import SignalInformation


class Lightpath(SignalInformation.SignalInformation):
    def __init__(self, channel, signal_power, path):
        super().__init__(signal_power, path)
        self._channel = channel
        self._rs = 32e9 # the signal symbol rate
        self._df = 50e9 # frequency spacing between two consecutive channels 50Ghz??
        # print(SignalInformation.SignalInformation.path)

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, channel):
        self._channel = channel

    @property
    def rs(self):
        return self._rs

    @rs.setter
    def rs(self, rs):
        self._rs = rs

    @property
    def df(self):
        return self._df

    @df.setter
    def df(self, df):
        self._df = df
