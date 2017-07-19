__author__ = 'carlos.coelho'

from sisaprop.appexceptions import MapRendererException

import logging
import os

class MapRendererBase(object):
    def __init__(self, _map, _path):
        # Map
        self.map = _map
        # Path
        self.path = _path
        # Logger
        self.l = logging.getLogger(self.__class__.__name__)

    def __repr__(self):
        return "<MapRenderer \"{0}\" at \"{1}\">".format(self.__class__.__name__,self.path)

    def checkpath(self):
        l=self.l

        if not (os.path.exists(self.path)):
            l.debug(u"Creating folder \"{0}\"".format(self.path))
            os.makedirs(self.path)
        elif not os.path.isdir(self.path):
            raise MapRendererException(u"Map render path \"{0}\" exists but is not a folder!".format(self.path))

    def render(self):
        # Check if path exists (creating if necessary)
        self.checkpath()
        # Do the actual render
        self.realrender(self.map, self.path)

    def realrender(self, _map, _path):
        print "{0}: Override __render() to actually do stuff!".format(self)



