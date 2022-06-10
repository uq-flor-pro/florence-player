'''
Python module for the dedicated Florence Player threads.
'''

__all__ = (
    'GPIOHandler',
)

from threading import Thread
from logging import getLogger
from time import time, sleep

import RPi.GPIO as GPIO

from mopidy_florence_player.actions import Play, Pause, NextTrack, Shutdown
from mopidy_florence_player.stations.stations import PlayStationOne, PlayStationTwo, PlayStationThree,  PlayStationFour
from mopidy_florence_player.sound import play_sound

LOGGER = getLogger(__name__)


class GPIOHandler(Thread):
    '''
    Thread which handles the GPIO ports, which basically means activating the
    LED when it's started and then reacting to button presses.
    '''
    button_pins = {
        16: Play,
        13: Pause,
        23: NextTrack,
        20: PlayStationOne,
        6: PlayStationTwo,
        5: PlayStationThree,
        22: PlayStationFour,
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

        now             = time()
        self.timestamps = {x: now for x in self.button_pins}

    # pylint: disable=no-member
    def run(self):
        '''
        Run the thread.
        '''

        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()

        for pin in self.button_pins:
            success = False
            while not success:
                try:
                    LOGGER.info('Setting up pin %s as button pin', pin)
                    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                    GPIO.add_event_detect(pin, GPIO.RISING, callback=lambda pin: self.button_push(pin))  # pylint: disable=unnecessary-lambda
                    LOGGER.info('Setup pin %s as button pin', pin)
                    success = True
                except Exception as ex:
                    sleep(1)
                    LOGGER.info(str(ex))

        play_sound('boot.wav')
        self.stop_event.wait()
        LOGGER.debug('Cleaning up GPIO')
        GPIO.cleanup()
        LOGGER.debug('Cleaned up GPIO')

    def button_push(self, pin):
        '''
        Callback method when a button is pushed.

        :param int pin: Pin number
        '''
        now    = time()
        before = self.timestamps[pin]

        if (GPIO.input(pin) == GPIO.LOW) and (now - before > 0.25):
            LOGGER.debug('Button at pin %s was pushed', pin)
            play_sound('success.wav')
            self.button_pins[pin].execute(self.core)
            self.timestamps[pin] = now
