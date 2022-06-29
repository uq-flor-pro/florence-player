'''
Python module to play sounds.
'''

__all__ = (
    'play_sound',
)

from os import path, system
import subprocess


def play_sound(sound):
    '''
    Play sound via aplay.

    :param str sound: The name of the sound file
    '''
    file_path = path.join(path.dirname(__file__), 'sounds', sound)
    # set volume 50%
    subprocess.run(['amixer', 'set', 'PCM', '50%'])
    subprocess.run(['aplay', file_path])
    # set volume 85%
    subprocess.run(['amixer', 'set', 'PCM', '85%'])
