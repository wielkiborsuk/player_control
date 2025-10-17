from .mpris import MprisController

class SpotifyController(MprisController):
    name = 'spotify'
    __dbus_name = 'org.mpris.MediaPlayer2.spotify'

    def __init__(self):
        super().__init__(self.__dbus_name)
