#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging

# Importa Gerenciador de Mapas
from sisaprop.map.mapmanager import MapManager
from sisaprop.map.map import Map

# Importa Gerenciador de Renderização
from sisaprop.maprenderers.maprendermanager import MapRenderManager

l = logging.getLogger("SISAPROP_Runner")

class SISAPROP_Runner(object):
    def __init__(self, _mapsfolder, _tools: dict, _outputsfolder, _mapname, _rendermethod):
        # A partir deste ponto, possuimos:
        # (2) rootfolder / mapsfolder / outputsfolder reais e válidos
        #
        # (3) MapManager ativo (self.mapmanager) apontando para a pasta de mapas
        # (3) Nome de mapa existente e válido (self.realmapname)
        #
        # (4) Método de renderização definido (self.realrendermethod).
        #
        # Podemos então gerar as saídas desejadas.

        self.mapsfolder = _mapsfolder

        self.tools = _tools

        self.outputsfolder = _outputsfolder
        self.mapname = _mapname
        self.rendermethod = _rendermethod

    def run(self):
        l.debug(u"Map name = {0}".format(self.mapname))

        # Init MapManager
        mapmanager = MapManager(self.mapsfolder, tools=self.tools)

        # Get Worker Map
        workermap = mapmanager.getmap(self.mapname)
        assert isinstance(workermap, Map)

        # Init Render Manager
        maprendermanager = MapRenderManager()

        # Generate Output Path from Map Name and Render Method
        renderoutputpath = os.path.join(self.outputsfolder, workermap.name, self.rendermethod)
        l.debug(u"Output path = {0}".format(renderoutputpath))

        print(u"\nO mapa será renderizado na pasta \"{0}\"...".format(renderoutputpath))

        # Render!
        l.debug(u"[Calling MapRenderManager.Render]")
        maprendermanager.render(workermap, renderoutputpath, self.rendermethod)

# print "CAIU"
# from code import interact
# interact(local=locals())