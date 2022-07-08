'''
Python module for Florence Player registry.
'''

__all__ = (
    'RegistryDict',
    'REGISTRY',
)

import os
import json
from logging import getLogger

from mopidy_florence_player import actions


LOGGER = getLogger(__name__)


class RegistryDict(dict):
    '''
    Class which can be used to retreive and write RFID tags to the registry.
    '''

    registry_path = '/var/lib/mopidy/florenceplayer/tags.json'

    def __init__(self):
        '''
        Constructor.

        Automatically reads the registry if it exists.
        '''
        super().__init__()

        if os.path.exists(self.registry_path):
            self.read()
        else:
            LOGGER.warning('Registry not existing yet on "%s"', self.registry_path)

    @classmethod
    def unserialize_item(cls, item):
        '''
        Unserialize an item from the persistent storage on filesystem to a
        native action.

        :param tuple item: The item

        :return: The action
        :rtype: actions.Action
        '''
        if 'tag_class' in item:
            item['action_class'] = item.pop('tag_class')

        return item['uid'], cls.init_action(**item)

    @classmethod
    def init_action(cls, action_class, uid, alias=None, parameter=None,
                    is_rfid=True):
        '''
        Initialise a new action instance.

        :param str action_class: The action class
        :param str uid: The RFID UID
        :param str alias: The alias
        :param str parameter: The parameter
        :param bool is_rfid: Is the entry for a RFID tag (true) or a station
        (false)?
        :return: The action instance
        :rtype: actions.Action
        '''
        uid          = str(uid).strip()
        action_class = getattr(actions, action_class)

        return action_class(uid, alias, parameter, is_rfid)

    def read(self):
        '''
        Read registry from disk.

        :raises IOError: When registry file on disk is missing
        '''
        LOGGER.debug('Reading registry from %s', self.registry_path)

        with open(self.registry_path) as f:
            data = json.load(f)
            self.clear()
            self.update((self.unserialize_item(item) for item in data))

    def write(self):
        '''
        Write registry to disk.
        '''
        LOGGER.debug('Writing registry to %s', self.registry_path)

        config    = self.registry_path
        directory = os.path.dirname(config)

        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(config, 'w') as f:
            json.dump([action.as_dict() for action in self.values()], f, indent=4)

    def register(self, action_class, uid, alias=None, parameter=None,
                 is_rfid=True):
        '''
        Register a new tag in the registry.

        :param str action_class: The action class
        :param str uid: The UID
        :param str alias: The alias
        :param str parameter: The parameter (optional)
        :param bool is_rfid: is the tag being registered a rfid tag? else a
        station.

        :return: The action
        :rtype: actions.Action
        '''
        LOGGER.info('Registering %s tag %s with parameter "%s"', action_class, uid, parameter)

        action = self.init_action(
            action_class=action_class,
            uid=uid,
            alias=alias,
            parameter=parameter,
            is_rfid=is_rfid,
        )

        action.validate()

        self[uid] = action
        self.write()

        return action

    def unregister(self, uid):
        '''
        Unregister a tag from the registry.

        :param str uid: The UID
        '''
        LOGGER.info('Unregistering tag %s', uid)

        del self[uid]
        self.write()


REGISTRY = RegistryDict()
