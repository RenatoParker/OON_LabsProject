from components import Line


class Lightpath(Line):
    def __init__(self, channel):
        self._channel = channel
        # todo come lo calcolo?
        self._rs = None # the signal symbol rate
        #todo 50ghz?
        self._df = 50e9 # frequency spacing between two consecutive channels 50Ghz??

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, channel):
        self._channel = channel
