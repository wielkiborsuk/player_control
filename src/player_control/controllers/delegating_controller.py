import os
import configparser
from .base import Controller
from .cmus import CmusController
from .spotify import SpotifyController
from .browser import ChromiumController, FirefoxController
from .mocp import MocpController

class DelegatingController(Controller):
    def __init__(self, debug=False):
        self.__debug = debug
        self.current = None
        self.controllers = [ c for c in [
            MocpController(),
            CmusController(),
            SpotifyController(),
            ChromiumController(),
            FirefoxController()
        ] if c.is_valid() ]
        self.default_controller_name = self.__load_default_controller_name()
        self.scan()

    def _get_config_file_path(self):
        xdg_config_home = os.environ.get('XDG_CONFIG_HOME', os.path.join(os.path.expanduser('~'), '.config'))
        config_dir = os.path.join(xdg_config_home, 'player_control')
        return os.path.join(config_dir, 'config.ini')

    def __load_default_controller_name(self):
        config = configparser.ConfigParser()
        config_path = self._get_config_file_path()
        if os.path.exists(config_path):
            try:
                config.read(config_path)
                return config.get('general', 'default_controller', fallback=None)
            except (configparser.Error, IOError):
                return None
        return None

    def _get_state_file_path(self):
        xdg_runtime_dir = os.environ.get('XDG_RUNTIME_DIR')
        if xdg_runtime_dir:
            state_dir = os.path.join(xdg_runtime_dir, 'player_control')
            os.makedirs(state_dir, exist_ok=True)
            return os.path.join(state_dir, 'current_player')
        return '/tmp/player_control_current'

    def focus(self, name):
        for controller in self.controllers:
            if controller.name == name:
                self.current = controller
                self.__save_focus(name)
                return

    def scan(self):
        # 1. Check for active player
        for controller in self.controllers:
            try:
                if controller.is_active():
                    self.focus(controller.name)
                    return
            except Exception:
                if self.__debug:
                    print(f'controller {controller.name} not responding')

        # 2. Check for last used player
        last_used_name = self.__load_focus()
        if last_used_name:
            self.focus(last_used_name)
            return

        # 3. Check for default player in config
        if self.default_controller_name:
            self.focus(self.default_controller_name)
            return

        # 4. Fallback to first available player
        if self.controllers:
            self.current = self.controllers[0]
        else:
            self.current = None

    def status(self):
        if not self.current: return ''
        try:
            return self.json_escape(self.current.status())
        except Exception:
            self.__save_focus(None)
            return ''

    def toggle(self):
        if not self.current: return
        return self.current.toggle()

    def next(self):
        if not self.current: return
        return self.current.next()

    def __save_focus(self, name):
        if not name:
            return
        state_file = self._get_state_file_path()
        with open(state_file, 'w') as state:
            state.write(name)

    def __load_focus(self):
        state_file = self._get_state_file_path()
        try:
            with open(state_file, 'r') as state:
                return state.read()
        except (FileNotFoundError, IOError):
            return None
