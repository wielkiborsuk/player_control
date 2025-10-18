import subprocess
from subprocess import check_output, DEVNULL
from .base import Controller


class MocpController(Controller):
    name = "mocp"

    def status(self):
        try:
            status_output = self.__mocp_status()
            state = self.__find_in_status(status_output, "State")
            if state not in ["PLAY", "PAUSE"]:
                return ""

            file_name = self.__find_in_status(status_output, "File")
            title = self.__find_in_status(status_output, "Title")
            total_time = self.__parse_number(
                self.__find_in_status(status_output, "TotalSec")
            )
            current_time = self.__find_in_status(status_output, "CurrentTime")

            display_title = (
                title if title else file_name.split("/")[-1] if file_name else ""
            )

            status_message = "{} {}/{}".format(
                display_title, current_time, self.format_time(total_time)
            )
            return status_message
        except (subprocess.CalledProcessError, AttributeError):
            return ""

    def is_active(self):
        try:
            status_output = self.__mocp_status()
            state = self.__find_in_status(status_output, "State")
            return state == "PLAY"
        except (subprocess.CalledProcessError, AttributeError):
            return False

    def is_valid(self) -> bool:
        try:
            check_output(["pgrep", "mocp"], stderr=DEVNULL)
            return True
        except subprocess.CalledProcessError:
            return False

    def toggle(self):
        check_output(["mocp", "-G"])

    def next(self):
        check_output(["mocp", "-f"])

    def __mocp_status(self):
        output = check_output(["mocp", "-i"], stderr=DEVNULL)
        return output.decode("utf-8").split("\n")

    def __find_in_status(self, status, name):
        line = next((line for line in status if line.startswith(name + ":")), None)
        if line:
            return line.split(":", 1)[1].strip()
        return None

    def __parse_number(self, time_line):
        if time_line:
            return int(time_line)
        return 0
