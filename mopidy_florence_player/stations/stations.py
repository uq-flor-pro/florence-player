'''
Python module for Florence Player.
Plays the given station.
'''

__all__ = (
    'PlayStationOne',
    'PlayStationTwo',
    'PlayStationThree',
    'PlayStationFour',
)

from logging import getLogger

from mopidy_florence_player.actions.base import Action

from mopidy_florence_player.registry import REGISTRY

from mopidy_florence_player.sound import play_sound

LOGGER = getLogger(__name__)


class PlayStation(Action):
    '''
    Base class for playing a station
    '''

    @classmethod
    def execute(cls, core, station):
        '''
        Replace tracklist and play.

        :param mopidy.core.Core core: The mopidy core instance
        '''
        try:
            action = REGISTRY[str(station)]
            action(core)
            play_sound('success.wav')
        except Exception as ex:
            LOGGER.info("Can't fetch parameter. Maybe there's no tracklist assigned to this station yet. Exception: %s", str(ex))
            play_sound('fail.wav')
            return

class PlayStationOne(PlayStation):
    '''
    Play station number 1
    '''
    @classmethod
    def execute(cls, core):
        # each station is stored as a tag in the db
        station = 'station_1'

        super().execute(core, station)

class PlayStationTwo(PlayStation):
    '''
    Play station number 2
    '''
    @classmethod
    def execute(cls, core):
        station = 'station_2'

        super().execute(core, station)

class PlayStationThree(PlayStation):
    '''
    Play station number 3
    '''
    @classmethod
    def execute(cls, core):
        station = 'station_3'

        super().execute(core, station)

class PlayStationFour(PlayStation):
    '''
    Play station number 4
    '''
    @classmethod
    def execute(cls, core):
        station = 'station_4'

        super().execute(core, station) 