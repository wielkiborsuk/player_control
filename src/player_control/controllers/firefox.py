import re
from subprocess import check_output
from .mpris import MprisController


class FirefoxController(MprisController):
    name = 'firefox'

    def __init__(self):
        instances = self.find_instance(self.name)
        dbus_name = self.__select_instance_by_cmd(instances, 'firefox')
        super().__init__(dbus_name)

    def __select_instance_by_cmd(self, instances, cmd_part):
        if len(instances) == 1:
            return instances[0]
        for instance in instances:
            return instance
            pid = re.match('.+instance([_\d]+)', instance).group(1)
            cmd = check_output(['ps', '-o', 'cmd=', pid]).decode('utf-8')
            if cmd_part in cmd:
                return instance
        return None
