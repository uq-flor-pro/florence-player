'''
Python module for Florence Player tags.
'''

__all__ = (
    'PlayPause',
    'Play',
    'Pause',
    'Stop',
    'PreviousTrack',
    'NextTrack',
    'Shutdown',
    'Tracklist',
    'ToggleShuffle',
    'Volume',
)

from .playback import PlayPause, Play, Pause, Stop, PreviousTrack, NextTrack
from .shutdown import Shutdown
from .tracklist import Tracklist, ToggleShuffle
from .volume import Volume

ACTIONS = {}
for action in __all__:
    ACTIONS[action] = globals()[action].__doc__.strip()
