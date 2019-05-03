# -*- coding: utf8

from typing import List, Tuple, AnyStr
import logging
import csv
from .mapdataloader import MapDataLoader
from .mapdatarow import ApropDataRow

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
    def __init__(self, _mapname, _mapdata=[], _mapfn=u"", _tools: dict = None):

        # Create logger entry for this map
        self.logger = logging.getLogger("map(%s)" % (_mapname,))

        # Save tools
        self.tools = _tools

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
            mdl = MapDataLoader(_mapfn, _tools=self.tools)
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

            mapline_s = ApropDataRow(*[str(val).strip() for val in _linedata])
            retval = [True, mapline_s]

            # This is used to validate the first line.
            first_line = ApropDataRow(*['matr_func', 'nome_func', 'apelido', 'nome_apropriador', 'matr_apropriador',
                                        'nome_responsavel', 'matr_responsavel', 'nome_setor', 'nome_planilha', 'turno',
                                        'suplentes', 'flags'])

            try:
                try:
                    matr_func, nome_func, apelido_func, nome_apropriador, matr_apropriador, \
                    nome_responsavel, matr_responsavel, \
                    nome_setor, nome_planilha, turno, suplentes, flags = mapline_s
                except ValueError as e:
                    raise MapException((u"Número de Campos Incorreto [{}]".format(e),), _linenumber)

                # First line Validation
                problems = []
                if _linenumber == 1:
                    if _linedata != first_line:
                        problems.append(u"Primeira linha com formato incorreto [Formato: [%s]]"
                                        % (','.join(first_line)))

                else:

                    if not matr_func:
                        problems.append(u"Matr em branco")

                    if not (bool(nome_func) or bool(apelido_func)):
                        problems.append(u"Sem nome e sem apelido")

                    if not nome_apropriador:
                        problems.append(u"Sem nome de apropriador")

                    if not nome_setor:
                        problems.append(u"Campo \"nome_setor\" em branco.")

                    if turno not in validshifts:
                        problems.append(u"Campo \"turno\" com valor inválido.")
                        problems.append(u"(Turnos válidos = %s)" % ('/'.join(validshifts)))

                    if nome_planilha.find("\n") != -1:
                        problems.append("Tem newline no nome da planilha...")

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

    def getmapdata(self) -> List[ApropDataRow]:
        return self.__map

    def getsplitmapdata(self, keysorting='nome_apropriador'):
        valid_keysort_values = [
            'nome_apropriador',
            'nome_planilha'
        ]

        if keysorting not in valid_keysort_values:
            raise MapException("Invalid SplitMapData Key={} (Valid Keys={})".format(keysorting, valid_keysort_values))

        # Map COPY
        md = self.getmapdata()

        # Get a list of deduplicated values from md[keysorting], then sort it.
        kvalues = list(set(map(lambda x: getattr(x, keysorting), md)))
        kvalues.sort()

        splitmd = {}
        for k in kvalues:
            # Create a sub-Map()
            submapname = self.name + u'/' + str(k)
            # Create submapdata by adding "header" from __mapdata and then filtering the rest of the data.
            submapdata = [self.mapdata[0]] + [d for d in md if getattr(d, keysorting) == k]
            splitmd[k] = Map(submapname, _mapdata=submapdata)

        return splitmd

    def get_responsaveis_matr(self):
        return sorted(list(set([(x.nome_responsavel, x.matr_responsavel) for x in self.getmapdata()
                                if not self.invalid])))

    def get_nomesetores(self):
        return sorted(list(set([x.nome_setor for x in self.getmapdata() if not self.invalid])))

    def get_nomeplanilhas(self):
        return sorted(list(set([x.nome_planilha for x in self.getmapdata() if not self.invalid])))

    def get_nomesetores_nomeplanilha(self):
        return sorted(list(set([(x.nome_setor, x.nome_planilha) for x in self.getmapdata() if not self.invalid])))

    def get_turnos(self):
        return sorted(list(set([x.turno for x in self.getmapdata() if not self.invalid])))

    def get_funcionarios(self, _responsavel_matr=None, _nomesetor=None, _nome_planilha=None, _turno=None):

        # Copy of the map data list.
        md = self.getmapdata()

        if _responsavel_matr:
            md = [e for e in md if (e.nome_responsavel == _responsavel_matr[0] and
                                    e.matr_responsavel == _responsavel_matr[1])]

        if _nomesetor:
            md = [e for e in md if e.nome_setor == _nomesetor]

        if _nome_planilha:
            md = [e for e in md if e.nome_planilha == _nome_planilha]

        if _turno:
            md = [e for e in md if e.turno == _turno]

        # Strip additional data, deliver only matr/nome/apelido
        md = [(e.matr_func, e.nome_func, e.apelido, e.flags) for e in md]

        # Convert <matr> to integer, for sorting
        md = [(int(x[0]), x[1], x[2], x[3]) for x in md]

        md_workers = [x for x in md if (x[1].find("*") == -1 and x[1].find("-") == -1)]
        md_apprentices = [x for x in md if x[1].find("*") != -1]
        md_machines = [x for x in md if x[1].find("-") != -1]

        # Sort each list by <matr>
        md_workers_sorted = sorted(md_workers, key= lambda x: x[0])
        md_apprentices_sorted = sorted(md_apprentices, key= lambda x: x[0])
        md_machines_sorted = sorted(md_machines, key= lambda x: x[0])

        joinedlist = md_workers_sorted + md_apprentices_sorted + md_machines_sorted

        # Convert <matr> back to String
        joinedlist = [(str(x[0]), x[1], x[2], x[3]) for x in joinedlist]

        return joinedlist

    def get_all_funcionarios(self) -> [List[Tuple[AnyStr]], [AnyStr, AnyStr, AnyStr]]:

        return [(self.get_funcionarios(_apr_matr, _nomesetor, _nomeplanilha, _turno),
                 (_apr_matr, _nomesetor, _nomeplanilha, _turno))
            for _apr_matr in self.get_responsaveis_matr()
            for _nomesetor in self.get_nomesetores()
            for _nomeplanilha in self.get_nomeplanilhas()
            for _turno in self.get_turnos()]

    def get_suplentes(self, _key=('apropriador', 'nome_setor', 'nome_planilha', 'turno')):

        # Explode fields
        _a, _ns, _np, _t = _key

        # Copy of the map data list.
        md = self.getmapdata()

        # Filter
        filteredmd = [e.suplentes for e in md if (e.nome_apropriador == _a[0] and
                                                  e.nome_setor == _ns and
                                                  e.turno == _t and
                                                  bool(e.suplentes.strip()))] # suplentes "is not null"

        # No results? Return empty string.
        if not filteredmd:
            return ''

        # Results? Sort and return the first element, ignore the rest.
        sortedmd = sorted(filteredmd)
        return sortedmd[0]

    def get_statistics(self):
        data = self.get_all_funcionarios()
        stats = [(entry[1], len(entry[0]), self.get_suplentes(_key=entry[1])) for entry in data if len(entry[0]) > 0]
        return stats

    def get_flags_for(self, nome_planilha: str=""):

        flaglist = list(set(filter(None, [x[3] for x in self.get_funcionarios(_nome_planilha=nome_planilha)])))

        # Return the list of all flags from this _nome_planilha
        return flaglist
