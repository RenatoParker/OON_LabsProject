from components import Line


class Lightpath(Line):
    def __init__(self, channel):
        self._channel = channel

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, channel):
        self._channel = channel
