'''
Florence Player Python module.
'''

import os
import pkg_resources
import mopidy

from logging import getLogger
from .frontend import FlorencePlayerFrontend
from .web import LatestHandler, RegistryHandler, RegisterHandler, UnregisterHandler, \
    ActionClassesHandler, RegisterStationHandler, UploadFile


LOGGER = getLogger(__name__)
__version__ = pkg_resources.get_distribution('Florence-Player').version

def app_factory(config, core):  # pylint: disable=unused-argument
    '''
    App factory for the web apps.

    :param mopidy.config config: The mopidy config
    :param mopidy.core.Core: The mopidy core

    :return: The registered app request handlers
    :rtype: list
    '''
    return [
        ('/latest/', LatestHandler),
        ('/registry/', RegistryHandler),
        ('/register/', RegisterHandler),
        ('/registerstations/', RegisterStationHandler),
        ('/unregister/', UnregisterHandler),
        ('/action-classes/', ActionClassesHandler),
        ('/upload/file', UploadFile),
    ]


class Extension(mopidy.ext.Extension):
    '''
    Florence Player extension.
    '''

    dist_name = 'Florence-Player'
    ext_name = 'florence'
    version = __version__

    def get_default_config(self):  # pylint: disable=no-self-use
        '''
        Return the default config.

        :return: The default config
        '''
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return mopidy.config.read(conf_file)

    def get_config_schema(self):
        '''
        Return the config schema.

        :return: The config schema
        '''
        schema = super(Extension, self).get_config_schema()
        return schema

    def setup(self, registry):
        '''
        Setup the extension.

        :param mopidy.ext.Registry: The mopidy registry
        '''
        registry.add('frontend', FlorencePlayerFrontend)

        registry.add('http:static', {
            'name': self.ext_name,
            'path': os.path.join(os.path.dirname(__file__), 'webui'),
        })

        LOGGER.info(
            registry.add('http:app', {
                'name': self.ext_name,
                'factory': app_factory,
            })
        )
