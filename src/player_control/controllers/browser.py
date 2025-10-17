import re
from subprocess import check_output
from .mpris import MprisController


class BrowserController(MprisController):
    name = 'chromium'

    def __init__(self):
        instances = self.find_instance(self.name)
        dbus_name = self.__select_instance_by_cmd(instances, 'chromium')
        super().__init__(dbus_name)

    def __select_instance_by_cmd(self, instances, cmd_part):
        if len(instances) == 1:
            return instances[0]
        for instance in instances:
            pid = re.match('.+instance(\d+)', instance).group(1)
            cmd = check_output(['ps', '-o', 'cmd=', pid]).decode('utf-8')
            if cmd_part in cmd:
                return instance
        return None
