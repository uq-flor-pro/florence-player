'''
Python module for Florence Player frontend.
'''

__all__ = (
    'FlorencePlayerFrontend',
)

from threading import Event
from logging import getLogger
import subprocess

import pykka
from mopidy import core as mopidy_core
import RPi.GPIO as GPIO

from .threads import GPIOHandler, TagReader, MCPWatcher


LOGGER = getLogger(__name__)


class FlorencePlayerFrontend(pykka.ThreadingActor, mopidy_core.CoreListener):
    '''
    Frontend which basically reacts to GPIO button pushes and touches
    of RFID tags.
    '''

    def __init__(self, config, core):  # pylint: disable=unused-argument
        super().__init__()
        self.core         = core
        # set volume at 85%
        subprocess.run(['amixer', 'set', 'PCM', '85%'])
        self.stop_event   = Event()
        self.gpio_handler = GPIOHandler(core=core, stop_event=self.stop_event)
        # turn off tag reader
        # self.tag_reader   = TagReader(core=core, stop_event=self.stop_event)
        self.mcp_watcher  = MCPWatcher(core=core, stop_event=self.stop_event)

    def on_start(self):
        '''
        Start GPIO handler & tag reader threads.
        '''

        GPIO.setmode(GPIO.BCM)
        self.gpio_handler.start()
        # turn off tag reader
        # self.tag_reader.start()
        self.mcp_watcher.start()

    def on_stop(self):
        '''
        Set threading stop event to tell GPIO handler & tag reader threads to
        stop their operations.
        '''
        self.stop_event.set()
