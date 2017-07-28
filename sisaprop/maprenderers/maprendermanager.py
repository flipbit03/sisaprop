__author__ = 'carlos.coelho'

import logging
from .nofficemaprenderer import NofficeMapRenderer
from sisaprop.appexceptions import MapRenderManagerException

l = logging.getLogger("MapRenderManager")

class MapRenderManager(object):
    def __init__(self):
        self.rendermethods = {
            "noffice" : NofficeMapRenderer
        }

    def getrendermethods(self):
        return self.rendermethods.keys()

    def render(self, _map, _path, _rendermethod="noffice"):

        if not _rendermethod in self.getrendermethods():
            raise MapRenderManagerException("No such rendermethod=\"{0}\"".format(_rendermethod))

        l.debug("Initializing renderer=\"{0}\"...".format(_rendermethod))
        renderer = self.rendermethods[_rendermethod](_map, _path)

        l.debug("Rendering...")
        renderer.render()