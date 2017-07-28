# -*- coding: utf8

import logging
import csv
from sisaprop.map.mapdataloader import MapDataLoader


class MapException(Exception):
    """ Exceção simples utilizada apenas dentro da classe Map
        Não é uma excessão de aplicativo, e não é propagada para fora da classe Map.
    """
    def __init__(self, reason : list, ln=0):
        self.reason = reason
        self.linenumber = ln


class Map(object):
    """ Load a Map, either from a list (_mapdata) or from a filename (_mapfn)
    """
    def __init__(self, _mapname, _mapdata=[], _mapfn=u""):

        # Create logger entry for this map
        self.logger = logging.getLogger("map(%s)" % (_mapname,))

        # Save map name
        self.name = _mapname

        # Invalid Attribute.
        self.invalid = False

        # Data source? _mapdata OR _mapfn (via Loader)
        if not (bool(_mapdata) or bool(_mapfn)):
            raise MapException("No data to generate map! [_mapdata and _mapfn are null]")

        if _mapdata:
            self.mapdata = _mapdata
        else:
            # Instantiate MapDataLoader to fetch us the map data.
            mdl = MapDataLoader(_mapfn)
            self.mapdata = mdl.load()

        # DATASTORE: This is where the real loaded and validated map data will be saved.
        self.__map = []

        # Validate map data to check if we have a valid map.
        self.__validatemapdata()

    def __repr__(self):
        return "<SISAPROP.Map \"{0}\">".format(self.name)

    def __validatemapdata(self):
        l = self.logger

        def validate_line(_linenumber, _linedata):

            # Valid Shifts
            validshifts = ("ADM", "2TN", "1TN")

            mapline_s = [str(val).strip() for val in _linedata]
            retval = [True, mapline_s]

            # This is used to validate the first line.
            first_line = ['matr_func', 'nome_func', 'apelido', 'nome_apropriador',
                          'especialidade', 'turno', 'suplentes']

            try:
                try:
                    matr_func, nome_func, apelido_func, nome_apropriador, especialidade, turno, suplentes = mapline_s
                except ValueError as e:
                    raise MapException((u"Número de Campos Incorreto [{}]".format(e),), _linenumber)

                # First line Validation
                problems = []
                if _linenumber == 1:
                    if _linedata != first_line:
                        problems.append(u"Primeira linha com formato incorreto [Formato: [%s]]"
                                        % (','.join(first_line)))

                        problems.append("piru")
                else:

                    if not matr_func:
                        problems.append(u"Matr em branco")

                    if not (bool(nome_func) or bool(apelido_func)):
                        problems.append(u"Sem nome e sem apelido")

                    if not nome_apropriador:
                        problems.append(u"Sem nome de apropriador")

                    if not especialidade:
                        problems.append(u"Campo \"especialidade\" em branco.")

                    if turno not in validshifts:
                        problems.append(u"Campo \"turno\" com valor inválido.")
                        problems.append(u"(Turnos válidos = %s)" % ('/'.join(validshifts)))

                # Raise exception if any problems found.
                if problems:
                    raise MapException(problems, _linenumber)

            except MapException as e:
                # Exception .reason will be a LIST of problems.
                for problem in e.reason:
                    l.debug(u"Erro na linha %d: %s" % (e.linenumber, problem))
                self.invalid = True

        # Commence Validation
        try:
            lmd = len(self.mapdata)
            if not self.mapdata:
                raise MapException(u"Sem dados para validar no mapa \"{0}\"!".format(self.name))
            for linenumber, mapline in zip(range(1,lmd+1), self.mapdata):
                validate_line(linenumber, mapline)

            # Set MAP from MAPDATA, strip header
            self.__map = self.mapdata[1:]
        except MapException as e:
            l.debug("Erro: %s" % (e.reason))
            self.__map = []
            self.invalid = True

    def getmapdata(self):
        # Return a COPY of __map using list()
        return list(self.__map)

    def getsplitmapdata(self, keysorting=3):
        if keysorting not in (3,4,5):
            raise MapException("Invalid SplitMapData Key={0} (Valid Keys=3/4/5)".format(keysorting))

        # Map COPY
        md = self.getmapdata()

        # Get a list of deduplicated values from md[keysorting], then sort it.
        kvalues = list(set(map(lambda x: x[keysorting],md)))
        kvalues.sort()

        splitmd = {}
        for k in kvalues:
            # Create a sub-Map()
            submapname = self.name + u'/' + str(k)
            # Create submapdata by adding "header" from __mapdata and then filtering the rest of the data.
            submapdata = [self.mapdata[0]] + [d for d in md if d[keysorting] == k]
            splitmd[k] = Map(submapname,_mapdata=submapdata)

        return splitmd

    def get_apropriadores(self):
        return sorted(list(set([x[3] for x in self.getmapdata() if not self.invalid])))

    def get_especialidades(self):
        return sorted(list(set([x[4] for x in self.getmapdata() if not self.invalid])))

    def get_turnos(self):
        return sorted(list(set([x[5] for x in self.getmapdata() if not self.invalid])))

    def get_combinedvalues(self):
        return self.get_apropriadores(), self.get_especialidades(), self.get_turnos()

    def get_funcionarios(self, _apropriador="", _especialidade="", _turno=""):

        # Copy of the map data list.
        md = self.getmapdata()

        if _apropriador:
            md = [e for e in md if e[3] == _apropriador]

        if _especialidade:
            md = [e for e in md if e[4] == _especialidade]

        if _turno:
            md = [e for e in md if e[5] == _turno]

        # Strip additional data, deliver only matr/nome/apelido
        md = [e[0:3] for e in md]

        # Convert <matr> to integer, for sorting
        md = [(int(x[0]), x[1], x[2]) for x in md]


        # Get list and split it in "workers" and "apprentices" and "machines"
        # apprentices = "*" character in name.
        # machinesces = "-" character in name.

        md_workers = [x for x in md if (x[1].find("*") == -1 and x[1].find("-") == -1)]
        md_apprentices = [x for x in md if x[1].find("*") != -1]
        md_machines = [x for x in md if x[1].find("-") != -1]

        # Sort each list by <matr>
        md_workers_sorted = sorted(md_workers, key= lambda x: x[0])
        md_apprentices_sorted = sorted(md_apprentices, key= lambda x: x[0])
        md_machines_sorted = sorted(md_machines, key= lambda x: x[0])

        joinedlist = md_workers_sorted + md_apprentices_sorted + md_machines_sorted

        # Convert <matr> back to String
        joinedlist = [(str(x[0]), x[1], x[2]) for x in joinedlist]

        return joinedlist

    def get_all_funcionarios(self):

        apropriadores, especialidades, turnos = self.get_combinedvalues()

        return [(self.get_funcionarios(apropriador, especialidade, turno), (apropriador, especialidade, turno))
            for turno in turnos
            for especialidade in especialidades
            for apropriador in apropriadores]

    def get_suplentes(self, _key=('apropriador','especialidade','turno')):

        # Explode fields
        _a, _e, _t = _key

        # Copy of the map data list.
        md = self.getmapdata()

        # Filter
        filteredmd = [e[6] for e in md if (e[3] == _a and
                                        e[4] == _e and
                                        e[5] == _t and
                                        # suplente is not null
                                        bool(e[6].strip()))]

        # No results? Return empty string.
        if not filteredmd:
            return u''

        # Results? Sort and return the first element, ignore the rest.
        sortedmd = sorted(filteredmd)
        return sortedmd[0]

    def get_statistics(self):
        data = self.get_all_funcionarios()
        stats = [(entry[1], len(entry[0]), self.get_suplentes(_key=entry[1])) for entry in data if len(entry[0]) > 0]
        return stats
