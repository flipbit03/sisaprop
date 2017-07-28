#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging

# Importa Gerenciador de Mapas
from sisaprop.map.mapmanager import MapManager

# Importa Gerenciador de Renderização
from sisaprop.maprenderers.maprendermanager import MapRenderManager

# Importa exceções necessárias SISAPROP
from .appexceptions import SISAPROPEFolderDoesNotExist, SISAPROPNoWorkableMap, SISAPROPNoRenderMethod

# Importa Runner
from .runner import SISAPROP_Runner

# Importa funções úteis
from . import helpfulfuncs

l = logging.getLogger("SISAPROP_CmdLineApp")

# -----------------------------------
# Classe SISAPROP_CmdLineApp
# Interface Linha de Comando para o APP, suporta validação interativa de opções.
# -----------------------------------
class SISAPROP_CmdLineApp(object):
    def __init__(self, args):

        # Salva pasta para a possível pasta-raiz
        self.possiblerootfolder = args.rootpath

        # Nome do mapa desejado [desejado --> real]
        self.desiredmapname = args.m
        self.realmapname = ""

        # Método de Renderização [desejado --> real]
        self.desiredrendermethod = args.r
        self.realrendermethod = ""

        # --
        # Begin Processing Flow.
        # --

        # (1) -- program banner
        # Print Application Banner
        self.imprime_banner()

        # (2) -- folders
        # Generate 3 of the main app variables.
        # self.rootfolder       =   root-folder from where maps are searched and output is written
        #                           also derived from "self.possiblerootfolder"
        # self.mapsfolder       =   folder which contains the employee maps.
        # self.outputsfolder    =   folder that will house generated files.
        self.rootfolder, self.mapsfolder, self.outputsfolder = self.verifica_rootfolder(self.possiblerootfolder)
        # Exclui "possiblerootfolder", pois não é mais necessário.
        del self.possiblerootfolder

        # (3) -- map file
        # Verifica se o mapa desejado existe e pode ser usado.
        self.realmapname = self.verifica_mapadesejado(self.desiredmapname)
        # Exclui "desiredmapname", pois não é mais necessário.
        del self.desiredmapname
        if not self.realmapname:
            raise SISAPROPNoWorkableMap(u"Não foi escolhido um mapa para processar ou foi escolhido um mapa inválido.")

        # (4) -- render method
        # Escolher método de renderização.
        self.realrendermethod = self.verifica_rendermethod(self.realmapname, self.desiredrendermethod)
        del self.desiredrendermethod
        if not self.realrendermethod:
            raise SISAPROPNoRenderMethod(u"Não foi escolhido um método para renderizar o mapa selecionado.")

        # A partir deste ponto, possuimos:
        # (2) rootfolder / mapsfolder / outputsfolder reais e válidos
        #
        # (3) MapManager ativo (self.mapmanager) apontando para a pasta de mapas
        # (3) Nome de mapa existente e válido (self.realmapname)
        #
        # (4) Método de renderização definido (self.realrendermethod).
        #
        # Podemos então gerar as saídas desejadas.
        sisaproprunner = SISAPROP_Runner(self.mapsfolder, self.outputsfolder, self.realmapname, self.realrendermethod)
        sisaproprunner.run()

    def imprime_banner(self):
        print()
        print(u"-----------------------------------------------")
        print(u"-SISAPROP--------------------------------------")
        print(u"-Sistema de Preparação de Mapas de Apropriação-")
        print(u"-----------------------------------------------")
        print()

    def verifica_rootfolder(self, rootfolder, mapsfoldername=u"maps", outputsfoldername=u"outputs"):
        if not os.path.exists(rootfolder):
            raise SISAPROPEFolderDoesNotExist(u"Pasta %s não existe" % (rootfolder,))

        # A pasta existe. Salvar no self.rootfolder.
        l.debug(u"A pasta-raiz é \"%s\"...\n" % (os.path.abspath(rootfolder),))
        absrootfolder = os.path.abspath(rootfolder)

        # Verifica se existe a pasta_raiz/maps
        maps_folder = os.path.join(absrootfolder, mapsfoldername)
        if not os.path.exists(maps_folder):
            l.debug(u"Criando pasta \"%s\"..." % (mapsfoldername,))
            os.mkdir(maps_folder)

        outputs_folder = os.path.join(absrootfolder, outputsfoldername)
        if not os.path.exists(outputs_folder):
            l.debug(u"Criando pasta \"%s\"..." % (outputsfoldername,))
            os.mkdir(outputs_folder)

        # Retorna tupla (absrootfolder, maps_folder, outputs_folder)
        return (absrootfolder, maps_folder, outputs_folder)

    def verifica_mapadesejado(self, wantedmapname=u""):

        print(u"Pasta dos mapas --> {0:s}\n".format(self.mapsfolder, ))

        # Cria gerenciador de mapas, usado para listar ou buscar mapas.
        mapmanager = MapManager(self.mapsfolder)

        validmaps = mapmanager.getvalidmapnames()
        quotedvalidmaps = [u'\"{0}\"'.format(mn) for mn in validmaps]

        if not validmaps:
            raise SISAPROPNoWorkableMap("Não existem mapas válidos a serem escolhidos.")
        else:
            l.info("Mapas encontrados: %s" % (' '.join(quotedvalidmaps)))

        if not wantedmapname:
            # Listar mapas disponiveis.
            chosenmapname = helpfulfuncs.chooseoption(validmaps, u"Escolha um Mapa:")
            return chosenmapname
        elif wantedmapname in validmaps:
            print(u"O nome do mapa é \"{0}\"".format(wantedmapname))
            return wantedmapname
        else:
            print(u"O mapa de nome \"{0}\" não foi encontrado.".format(wantedmapname))
            return ""

    def verifica_rendermethod(self, _mapname, desiredrendermethod):
        print()
        mprompt = u"Escolha o metodo de renderização para o mapa \"%s" % (_mapname)

        # Cria gerenciador de renderização.
        maprendermanager = MapRenderManager()
        rendermethods = maprendermanager.getrendermethods()

        chosenrendermethod = ""
        if not (desiredrendermethod in rendermethods):
            chosenrendermethod = helpfulfuncs.chooseoption(rendermethods, mprompt)
        else:
            chosenrendermethod = desiredrendermethod

        print(u"O mapa será renderizado utilizando o plugin \"{0}\".".format(chosenrendermethod))

        return chosenrendermethod


