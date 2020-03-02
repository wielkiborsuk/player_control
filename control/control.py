from subprocess import check_output, DEVNULL
import dbus
import re


class Controller(object):
    def format_time(self, seconds):
        return '{:02d}:{:02d}'.format(seconds // 60, seconds % 60)

    def json_escape(self, text):
        return text.replace('"', '\\"')


class DelegatingController(Controller):
    tmp_file = '/tmp/player_control_current'

    def __init__(self, debug=False):
        self.__debug = debug
        self.current = None
        self.controllers = [
            CmusController(),
            SpotifyController(),
            BrowserController()
        ]
        self.focus(self.__load_focus())
        self.scan()

    def focus(self, name):
        for controller in self.controllers:
            if controller.name == name:
                self.current = controller
                self.__save_focus(name)

    def scan(self):
        for controller in self.controllers:
            try:
                if controller.is_active():
                    self.focus(controller.name)
            except Exception:
                if self.__debug:
                    print('controller {} not responding'
                          .format(controller.name))

    def get_controler(self):
        return self.current or self.controllers[0]

    def status(self):
        return self.json_escape(self.get_controler().status())

    def toggle(self):
        return self.get_controler().toggle()

    def next(self):
        return self.get_controler().next()

    def __save_focus(self, name):
        with open(self.tmp_file, 'w') as state:
            state.write(name)

    def __load_focus(self):
        try:
            with open(self.tmp_file, 'r') as state:
                return state.read()
        except Exception:
            return None


class CmusController(Controller):
    name = 'cmus'

    def status(self):
        try:
            status = self.__cmus_status()
            file_name = self.__parse_file(
                self.__find_in_status(status, 'file'))
            duration = self.__parse_number(
                self.__find_in_status(status, 'duration'))
            position = self.__parse_number(
                self.__find_in_status(status, 'position'))
            status_message = '{} {}/{}'.format(file_name,
                                               self.format_time(position),
                                               self.format_time(duration))
            return status_message
        except Exception:
            return ''

    def is_active(self):
        return 'playing' in self.__cmus_status()[0]

    def toggle(self):
        self.__ensure_cmus_present()
        check_output(['cmus-remote', '-u'])

    def next(self):
        self.__ensure_cmus_present()
        check_output(['cmus-remote', '-n'])

    def __parse_file(self, file_line):
        return file_line.split()[1].split('/')[-1]

    def __parse_number(self, time_line):
        return int(time_line.split()[1])

    def __find_in_status(self, status, name):
        return next((line for line in status if line.startswith(name)), None)

    def __cmus_status(self):
        output = check_output(['cmus-remote', '-Q'], stderr=DEVNULL)
        output = output.decode('utf-8').split('\n')
        return output

    def __ensure_cmus_present(self):
        try:
            check_output(['pgrep', 'cmus'])
        except Exception:
            check_output(['playback_toggle'])


class MprisController(Controller):
    __dbus_player = 'org.mpris.MediaPlayer2.Player'
    __dbus_path = '/org/mpris/MediaPlayer2'
    __dbus_properties = 'org.freedesktop.DBus.Properties'
    __bus = dbus.SessionBus()

    def __init__(self, dbus_name):
        self.__dbus_name = dbus_name

    def toggle(self):
        return self.__player_interface.PlayPause()

    def next(self):
        return self.__player_interface.Next()

    def is_active(self):
        status = self.__mpris_playback_status()
        return status == 'Playing'

    def status(self):
        status = self.mpris_metadata()
        title = status['xesam:title']
        duration = int(status.get('mpris:length', '0'))
        status_message = '{} {}/{}'.format(
            title,
            self.format_time(self.mpris_position()),
            self.format_time(duration//1000000))
        return status_message

    def mpris_metadata(self):
        return self.__player_properties.Get(self.__dbus_player,
                                            'Metadata')

    def mpris_position(self):
        return self.__player_properties.Get(self.__dbus_player,
                                            'Position')

    def __mpris_playback_status(self):
        return self.__player_properties.Get(self.__dbus_player,
                                            'PlaybackStatus')

    def __get_player_object(self):
        return self.__bus.get_object(self.__dbus_name, self.__dbus_path)

    @property
    def __player_properties(self):
        return dbus.Interface(
            self.__get_player_object(),
            dbus_interface=self.__dbus_properties)

    @property
    def __player_interface(self):
        return dbus.Interface(
            self.__get_player_object(),
            dbus_interface=self.__dbus_player)

    def find_instance(self, query):
        obj = self.__bus.get_object("org.freedesktop.DBus",
                                    "/org/freedesktop/DBus")
        result = [str(name) for name in obj.ListNames() if query in name]
        return result


class SpotifyController(MprisController):
    name = 'spotify'
    __dbus_name = 'org.mpris.MediaPlayer2.spotify'

    def __init__(self):
        super().__init__(self.__dbus_name)


class BrowserController(MprisController):
    name = 'chromium'

    def __init__(self):
        instances = self.find_instance(self.name)
        dbus_name = self.__select_instance_by_cmd(instances, 'chromium')
        super().__init__(dbus_name)

    def __select_instance_by_cmd(self, instances, cmd_part):
        for instance in instances:
            pid = re.match('.+instance(\\d+)', instance).group(1)
            cmd = check_output(['ps', '-o', 'cmd=', pid]).decode('utf-8')
            if cmd_part in cmd:
                return instance
        return None
