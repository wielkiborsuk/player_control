from .base import Controller
from .delegating_controller import DelegatingController
from .cmus import CmusController
from .spotify import SpotifyController
from .browser import BrowserController
from .firefox import FirefoxController

__all__ = [
    'Controller',
    'DelegatingController',
    'CmusController',
    'SpotifyController',
    'BrowserController',
    'FirefoxController',
]
