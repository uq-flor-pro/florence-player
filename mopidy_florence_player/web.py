'''
Python module for Florence Player web classes.
'''

__all__ = (
    'LatestHandler',
    'RegistryHandler',
    'RegisterHandler',
    'RegisterStationHandler',
    'UnregisterHandler',
    'ActionClassesHandler',
    'UploadFile',
)

from json import dumps
from logging import getLogger

from tornado.web import RequestHandler

from mopidy_florence_player.registry import REGISTRY
from mopidy_florence_player.actions import ACTIONS
from mopidy_florence_player.threads import TagReader

import os

import subprocess

LOGGER = getLogger(__name__)


class LatestHandler(RequestHandler):  # pylint: disable=abstract-method
    '''
    Request handler which returns the latest scanned tag.
    '''

    def get(self, *args, **kwargs):  # pylint: disable=unused-argument
        '''
        Handle GET request.
        '''
        tag = TagReader.latest

        LOGGER.debug('Returning latest tag %s', tag)

        if tag is None:
            data = {
                'success': False,
                'message': 'No tag scanned yet'
            }

        else:
            data = {
                'success': True,
                'message': 'Scanned tag found',
            }

            data.update(tag.as_dict(include_scanned=True))

        self.set_header('Content-type', 'application/json')
        self.write(dumps(data))


class RegistryHandler(RequestHandler):  # pylint: disable=abstract-method
    '''
    Request handler which returns all registered tags.
    '''

    def get(self, *args, **kwargs):  # pylint: disable=unused-argument
        '''
        Handle GET request.
        '''
        tags_list = []

        for tag in REGISTRY.values():
            tags_list.append(tag.as_dict())

        data = {
            'success': True,
            'message': 'Registry successfully read',
            'tags': tags_list
        }

        self.set_header('Content-type', 'application/json')
        self.write(dumps(data))


class RegisterHandler(RequestHandler):  # pylint: disable=abstract-method
    '''
    Request handler which registers an RFID tag in the registry.
    '''

    def post(self, *args, **kwargs):  # pylint: disable=unused-argument
        '''
        Handle POST request.
        '''
        try:
            tag = REGISTRY.register(
                action_class=self.get_argument('action-class'),
                uid=self.get_argument('uid'),
                alias=self.get_argument('alias', None),
                parameter=self.get_argument('parameter', None),
            )

            data = {
                'success': True,
                'message': 'Tag successfully registered',
            }

            data.update(tag.as_dict())

        except ValueError as ex:
            self.set_status(400)
            data = {
                'success': False,
                'message': str(ex)
            }

        self.set_header('Content-type', 'application/json')
        self.write(dumps(data))

    def put(self, *args, **kwargs):  # pylint: disable=unused-argument
        '''
        Handle PUT request.
        '''
        self.post()

class RegisterStationHandler(RequestHandler):  # pylint: disable=abstract-method
    '''
    Request handler which registers stations in the registry.
    '''

    def post(self, *args, **kwargs):  # pylint: disable=unused-argument
        '''
        Handle POST request.
        '''

        data = {
                "station_1": False,
                "station_2": False,
                "station_3": False,
                "station_4": False,
        }

        try:
            for station in ['station_1', 'station_2', 'station_3', 'station_4']:
                alias = self.get_argument(station + "_alias", "")
                tracklist = self.get_argument(station + "_tracklist", "")

                if not alias and not tracklist:
                    data[station] = "skip"
                    continue
                if not alias or not tracklist:
                    data[station] = "error"
                    continue

                LOGGER.debug('Trying to add station')
                REGISTRY.register(
                    action_class="Tracklist",
                    uid=station,
                    alias=alias,
                    parameter=tracklist,
                    is_rfid=False,
                )

                data[station] = True

            data["success"] = True
            data["message"] = "No errors"

            # data.update(stations.as_dict())

        except ValueError as ex:
            LOGGER.debug('Error adding station:'  + station + ". Check there was"
                + "an alias and tracklist set for each updated station.")
            self.set_status(400)
            data["success"] = False
            data["message"] = str(ex)

        self.set_header('Content-type', 'application/json')
        self.write(dumps(data))

    def put(self, *args, **kwargs):  # pylint: disable=unused-argument
        '''
        Handle PUT request.
        '''
        self.post()

class UnregisterHandler(RequestHandler):  # pylint: disable=abstract-method
    '''
    Request handler which unregisters an RFID tag from the registry.
    '''

    def post(self, *args, **kwargs):  # pylint: disable=unused-argument
        '''
        Handle POST request.
        '''
        try:
            REGISTRY.unregister(uid=self.get_argument('uid'))

            data = {
                'success': True,
                'message': 'Tag successfully unregistered',
            }

        except ValueError as ex:
            self.set_status(400)
            data = {
                'success': False,
                'message': str(ex)
            }

        self.set_header('Content-type', 'application/json')
        self.write(dumps(data))

    def put(self, *args, **kwargs):  # pylint: disable=unused-argument
        '''
        Handle PUT request.
        '''
        self.post()


class ActionClassesHandler(RequestHandler):  # pylint: disable=abstract-method
    '''
    Request handler which returns all action classes.
    '''

    def get(self, *args, **kwargs):  # pylint: disable=unused-argument
        '''
        Handle GET request.
        '''
        data = {
            'success': True,
            'message': 'Action classes successfully retrieved',
            'action_classes': ACTIONS
        }

        self.set_header('Content-type', 'application/json')
        self.write(dumps(data))


class UploadFile(RequestHandler):
    '''
    Handles a file being POSTed. If it's a known audio file store it away, if
    it's a zip unzip and store it away. Else skip.

    Stores into /home/pi/music/webuploads/.
    '''
    def post(self):
        '''
        Handle POST request.
        '''
        store_dir = '/home/pi/music/webuploads/'

        file1 = self.request.files['file1'][0]
        LOGGER.info('Got request %s' % self.request)
        original_fname = file1['filename']
        ext = os.path.splitext(original_fname)[1]

        LOGGER.info(f'Adding file %s' % original_fname)

        if ext in ('.mp3', '.wav', '.flac'):
            with open(store_dir + original_fname, 'wb') as output_file:
                output_file.write(file1['body'])
            LOGGER.info('Successfully added new music')

        elif ext == ".zip":
            with open("/tmp/" + original_fname, 'wb') as output_file:
                output_file.write(file1['body'])

            subprocess.run(["unzip", "-d", store_dir, "/tmp/" +
                            original_fname, ], check=True)
            LOGGER.info('Successfully added new music')

        else:
            LOGGER.info('No valid file found')
            self.set_status(500)
            self.finish("Invalid file found.")

        self.finish("Upload successful")

    get = post
