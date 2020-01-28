from subprocess import check_output


class Controller(object):
    pass


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
        return self.__cmus_status()

    def is_active(self):
        return 'playing' in self.__cmus_status()[0]

    def toggle(self):
        check_output(['cmus-remote', '-u'])

    def next(self):
        check_output(['cmus-remote', '-n'])

    def __cmus_status(self):
        output = check_output(['cmus-remote', '-Q'])
        output = output.decode('utf-8').split('\n')
        return output


class SpotifyController(Controller):
    name = 'spotify'

    def status(self):
        return 'spotify'

    def is_active(self):
        return 'spotify'


class BrowserController(Controller):
    name = 'browser'

    def status(self):
        return 'browser'
