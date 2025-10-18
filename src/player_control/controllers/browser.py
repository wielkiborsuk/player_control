import re
from subprocess import check_output
from .mpris import MprisController


class GenericBrowserController(MprisController):
    def __init__(self, name):
        instances = self.find_instance(name)
        dbus_name = self.__select_instance_by_cmd(instances, name)
        super().__init__(dbus_name)

    def __select_instance_by_cmd(self, instances, cmd_part):
        if len(instances) == 1:
            return instances[0]
        for instance in instances:
            try:
                pid_match = re.match(".+instance([\\d_]+)", instance)
                if not pid_match:
                    continue
                pid = pid_match.group(1)
                cmd = check_output(["ps", "-o", "cmd=", pid]).decode("utf-8")
                if cmd_part in cmd:
                    return instance
            except (AttributeError, FileNotFoundError):
                continue
        if instances:
            return instances[0]
        return None


class ChromiumController(GenericBrowserController):
    name = "chromium"

    def __init__(self):
        super().__init__(self.name)


class FirefoxController(GenericBrowserController):
    name = "firefox"

    def __init__(self):
        super().__init__(self.name)
