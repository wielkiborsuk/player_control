from .base import Controller
from .cmus import CmusController
from .spotify import SpotifyController
from .browser import BrowserController
from .firefox import FirefoxController

class DelegatingController(Controller):
    tmp_file = '/tmp/player_control_current'

    def __init__(self, debug=False):
        self.__debug = debug
        self.current = None
        self.controllers = [ c for c in [
            CmusController(),
            SpotifyController(),
            BrowserController(),
            FirefoxController()
        ] if c.is_valid() ]
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
        try:
            return self.json_escape(self.get_controler().status())
        except Exception:
            self.__save_focus(None)
            return ''

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
