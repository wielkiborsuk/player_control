from subprocess import check_output, DEVNULL
from .base import Controller

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
        return file_line.split('/')[-1]

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