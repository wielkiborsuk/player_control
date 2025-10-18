class Controller(object):
    def format_time(self, seconds: int) -> str:
        return "{:02d}:{:02d}".format(seconds // 60, seconds % 60)

    def json_escape(self, text: str) -> str:
        return text.replace('"', '\\"')

    def is_valid(self) -> bool:
        return True
