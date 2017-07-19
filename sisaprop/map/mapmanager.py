# -*- coding: utf8 -*-
__author__ = 'carlos.coelho'

import os

from sisaprop.map.map import Map

import logging
l = logging.getLogger("mapmanager")

class MapManager(object):
    def __init__(self, mappath):
        # Save mappath
        self.mappath = mappath

        # Populate valid map dict with instances of APROPMap
        self.validmaps = self.__getvalidmaps()

    def __getvalidmaps(self):
        # This is the return list.
        validmaplist = {}

        # List .csv files in MAPPATH
        dirlst = os.listdir(unicode(self.mappath))
        mapfilenamelist = [os.path.join(self.mappath, fn) for fn in dirlst]

        # Iterate over each .csv file trying to import valid ones.
        for mapfn in mapfilenamelist:
            mapname = os.path.basename(mapfn)

            l.debug(u"Carregando mapa %s..." % (mapfn,))
            newmap = Map(mapname, _mapfn=mapfn)

            if not newmap.invalid:
                l.debug(u"Mapa \"%s\" é válido!" % (newmap.name,))
                validmaplist[mapname] = newmap
            else:
                l.debug(u"Mapa \"%s\" não é válido!" % (newmap.name,))

        return validmaplist

    def getvalidmapnames(self):
        return self.validmaps.keys()

    def getmap(self, _mapname):
        return self.validmaps[_mapname]