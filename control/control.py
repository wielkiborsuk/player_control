from subprocess import check_output
import dbus


class Controller(object):
    def format_time(self, seconds):
        return '{:02d}:{:02d}'.format(seconds // 60, seconds % 60)


class DelegatingController(Controller):
    def __init__(self):
        self.current = None
        self.controllers = [
            CmusController(),
            SpotifyController(),
            BrowserController()
        ]

    def focus(self, name):
        for controller in self.controllers:
            if controller.name == name:
                self.current = controller

    def get_controler(self):
        return self.current or self.controllers[0]

    def status(self):
        return self.get_controler().status()

    def toggle(self):
        return self.get_controler().toggle()

    def next(self):
        return self.get_controler().next()


class CmusController(Controller):
    name = 'cmus'

    def status(self):
        status = self.__cmus_status()
        file_name = self.__parse_file(self.__find_in_status(status, 'file'))
        duration = self.__parse_number(
            self.__find_in_status(status, 'duration'))
        position = self.__parse_number(
            self.__find_in_status(status, 'position'))
        status_message = '{} {}/{}'.format(file_name,
                                           self.format_time(position),
                                           self.format_time(duration))
        return status_message

    def is_active(self):
        return 'playing' in self.__cmus_status()[0]

    def toggle(self):
        check_output(['cmus-remote', '-u'])

    def next(self):
        check_output(['cmus-remote', '-n'])

    def __parse_file(self, file_line):
        return file_line.split()[1].split('/')[-1]

    def __parse_number(self, time_line):
        return int(time_line.split()[1])

    def __find_in_status(self, status, name):
        return next((line for line in status if line.startswith(name)), None)

    def __cmus_status(self):
        output = check_output(['cmus-remote', '-Q'])
        output = output.decode('utf-8').split('\n')
        return output


class SpotifyController(Controller):
    name = 'spotify'
    __dbus_name = 'org.mpris.MediaPlayer2.spotify'
    __dbus_player = 'org.mpris.MediaPlayer2.Player'
    __dbus_path = '/org/mpris/MediaPlayer2'
    __dbus_properties = 'org.freedesktop.DBus.Properties'
    __bus = dbus.SessionBus()
    __player_object = __bus.get_object(__dbus_name, __dbus_path)
    __player_properties = dbus.Interface(__player_object,
                                         dbus_interface=__dbus_properties)
    __player_interface = dbus.Interface(__player_object,
                                        dbus_interface=__dbus_player)

    def status(self):
        status = self.__spotify_metadata()
        title = status['xesam:title']
        duration = int(status['mpris:length'])
        status_message = '{} {}/{}'.format(
            title,
            self.format_time(self.__spotify_position()),
            self.format_time(duration//1000000))
        return status_message

    def toggle(self):
        return self.__player_interface.PlayPause()

    def next(self):
        return self.__player_interface.Next()

    def is_active(self):
        status = self.__spotify_playback_status()
        return status == 'Playing'

    def __spotify_metadata(self):
        return self.__player_properties.Get(self.__dbus_player,
                                            'Metadata')

    def __spotify_playback_status(self):
        return self.__player_properties.Get(self.__dbus_player,
                                            'PlaybackStatus')

    def __spotify_position(self):
        return self.__player_properties.Get(self.__dbus_player,
                                            'Position')


class BrowserController(Controller):
    name = 'browser'

    def status(self):
        return 'browser'
