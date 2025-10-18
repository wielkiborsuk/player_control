from .base import Controller
from .delegating_controller import DelegatingController
from .cmus import CmusController
from .spotify import SpotifyController
from .browser import ChromiumController, FirefoxController

__all__ = [
    "Controller",
    "DelegatingController",
    "CmusController",
    "SpotifyController",
    "ChromiumController",
    "FirefoxController",
]
