from components import Line


class Lightpath(Line):
    def __init__(self, channel):
        self._channel = channel
        self._rs = None # the signal symbol ratw
        #todo 50ghz?
        self._df = None # frequency spacing between two consecutive channels 50Ghz??

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, channel):
        self._channel = channel
