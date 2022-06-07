'''
Watches the MCP3008 for volume signal
'''

__all__ = (
    'MCPWatcher',
)

from threading import Thread
from logging import getLogger
import time

LOGGER = getLogger(__name__)

from gpiozero import MCP3008

from mopidy_florence_player.actions import Volume

class ReadError(Exception):
    '''
    
    '''


class MCPWatcher(Thread):
    '''
    Outputs the volume potentiometer as it changes
    '''
    daemon = True
    latest = None
    
    pins = {
        'clock': 11,
        'mosi': 10,
        'miso': 9,
        'select': 8,
    }

    def __init__(self, core, stop_event):
        '''
        Class constructor.

        :param mopidy.core.Core core: The mopidy core instance
        :param threading.Event stop_event: The stop event
        '''
        super().__init__()
        self.core       = core
        self.stop_event = stop_event
        
        self.mcp = MCP3008(channel=0, clock_pin=self.pins['clock'], mosi_pin=self.pins['mosi'], miso_pin=self.pins['miso'], select_pin=self.pins['select'])
        self.mcp_previous_value = -1

        Volume.execute(self.core, self.mcp.value * 30)

        LOGGER.info("Setting up MCP3008")

    def run(self):
        '''
        Volume reading loop
        '''

        while not self.stop_event.is_set():
            if abs(self.mcp.value - self.mcp_previous_value) > 0.1:
                LOGGER.info(str(self.mcp.value))
                Volume.execute(self.core, self.mcp.value * 30)
                self.mcp_previous_value = self.mcp.value
            time.sleep(0.0001)
