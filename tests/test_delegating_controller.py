from unittest.mock import MagicMock, patch
from player_control.controllers.delegating_controller import DelegatingController


class MockController:
    def __init__(self, name, is_active=False, is_valid=True):
        self.name = name
        self._is_active = is_active
        self._is_valid = is_valid

    def is_active(self):
        return self._is_active

    def is_valid(self):
        return self._is_valid

    def status(self):
        return "mock status"

    def toggle(self):
        pass

    def next(self):
        pass


@patch("player_control.controllers.delegating_controller.MocpController")
@patch("player_control.controllers.delegating_controller.CmusController")
@patch("player_control.controllers.delegating_controller.SpotifyController")
@patch("player_control.controllers.delegating_controller.ChromiumController")
@patch("player_control.controllers.delegating_controller.FirefoxController")
def test_scan_no_active_player(
    MockFirefox, MockChromium, MockSpotify, MockCmus, MockMocp
):
    MockMocp.return_value = MockController("mocp")
    MockCmus.return_value = MockController("cmus")
    MockSpotify.return_value = MockController("spotify")
    MockChromium.return_value = MockController("chromium")
    MockFirefox.return_value = MockController("firefox")

    controller = DelegatingController()
    assert controller.current.name == "mocp"


@patch("player_control.controllers.delegating_controller.MocpController")
@patch("player_control.controllers.delegating_controller.CmusController")
@patch("player_control.controllers.delegating_controller.SpotifyController")
@patch("player_control.controllers.delegating_controller.ChromiumController")
@patch("player_control.controllers.delegating_controller.FirefoxController")
def test_scan_with_active_player(
    MockFirefox, MockChromium, MockSpotify, MockCmus, MockMocp
):
    MockMocp.return_value = MockController("mocp")
    MockCmus.return_value = MockController("cmus", is_active=True)
    MockSpotify.return_value = MockController("spotify")
    MockChromium.return_value = MockController("chromium")
    MockFirefox.return_value = MockController("firefox")

    controller = DelegatingController()
    assert controller.current.name == "cmus"


@patch("player_control.controllers.delegating_controller.os.path.exists")
@patch("player_control.controllers.delegating_controller.configparser.ConfigParser")
def test_load_default_controller_name(MockConfigParser, mock_exists):
    mock_exists.return_value = True
    mock_config = MagicMock()
    mock_config.get.return_value = "spotify"
    MockConfigParser.return_value = mock_config

    controller = DelegatingController()
    assert controller.default_controller_name == "spotify"
