import dbus
from .base import Controller


class MprisController(Controller):
    __dbus_player = "org.mpris.MediaPlayer2.Player"
    __dbus_path = "/org/mpris/MediaPlayer2"
    __dbus_properties = "org.freedesktop.DBus.Properties"
    __bus = dbus.SessionBus()

    def __init__(self, dbus_name):
        self.__dbus_name = dbus_name

    def toggle(self):
        return self.__player_interface.PlayPause()

    def next(self):
        return self.__player_interface.Next()

    def is_active(self):
        status = self.__mpris_playback_status()
        return status == "Playing"

    def is_valid(self) -> bool:
        return bool(self.__dbus_name)

    def status(self):
        status = self.mpris_metadata()
        title = status["xesam:title"]
        duration = int(status.get("mpris:length", "0"))
        status_message = "{} {}/{}".format(
            title,
            self.format_time(self.mpris_position() // 1000000),
            self.format_time(duration // 1000000),
        )
        if not title or not status_message:
            raise RuntimeError("mpris service didn't respond")
        return status_message

    def mpris_metadata(self):
        return self.__player_properties.Get(self.__dbus_player, "Metadata")

    def mpris_position(self):
        try:
            return self.__player_properties.Get(self.__dbus_player, "Position")
        except Exception:
            return 0

    def __mpris_playback_status(self):
        return self.__player_properties.Get(self.__dbus_player, "PlaybackStatus")

    def __get_player_object(self):
        return self.__bus.get_object(self.__dbus_name, self.__dbus_path)

    @property
    def __player_properties(self):
        return dbus.Interface(
            self.__get_player_object(), dbus_interface=self.__dbus_properties
        )

    @property
    def __player_interface(self):
        return dbus.Interface(
            self.__get_player_object(), dbus_interface=self.__dbus_player
        )

    def find_instance(self, query):
        obj = self.__bus.get_object("org.freedesktop.DBus", "/org/freedesktop/DBus")
        result = [
            str(name) for name in obj.ListNames() if query in name and "mpris" in name
        ]
        return result
