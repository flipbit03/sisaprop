__author__ = 'carlos.coelho'

import logging
import os
import zipfile

from .autoapropxlsx.autoapropmaptypes import AutoApropModeloSemanal, AutoApropModeloDiario, \
    AutoApropModeloDiarioAdministrativo, AutoApropException

from sisaprop.map.map import Map
from .maprendererbase import MapRendererBase


l = logging.getLogger("AutoApropXlsxMapRenderer")

class AutoApropXlsxMapRenderer(MapRendererBase):
    def realrender(self, _map: Map, _path):

        l.debug("Map is [{0}]".format(_map))
        l.debug("RenderPath is [{0}]".format(_path))

        _map.get_statistics()

        # Split maps by "nome_planilha"
        submaps = _map.getsplitmapdata(keysorting='nome_planilha')

        l.debug("{0} submap(s) to render from map...".format(len(submaps)))
        for submapname in submaps:
            rendersubmapname = submapname.split(u'/')[-1].lower()
            assert isinstance(rendersubmapname, str)
            rendersubmapname = rendersubmapname.replace(u'.',u'') + u'.xlsx'

            # Get filename from rendersubmapname
            renderfilename = os.path.join(_path, rendersubmapname.upper())

            # Generate each map.
            print("  Renderizando mapa {0} ({1})...".format(submapname, rendersubmapname))
            l.debug("Rendering submap \"{0}\".".format(submapname))
            self.rendereachmap(submaps[submapname], rendersubmapname, renderfilename)
            l.debug(" ")

    def rendereachmap(self, _map : Map, _mapname, _renderfilepath):
        assert isinstance(_map, Map)

        bigemployeelist = _map.get_all_funcionarios()

        for slice in bigemployeelist:
            employees, params = tuple(slice)
            apropriador_com_matr, nome_setor_planilha, turno = params

            nome_apropriador, matr_apropriador = apropriador_com_matr

            nome_setor, nome_planilha = nome_setor_planilha

            l.debug("    [slice] > {0:s} {1:s} {2:s}".format(nome_apropriador, nome_setor, turno))

            # Build Dict for renderer
            renderdict = {}

            renderdict["##NOMESETOR##"]  = nome_setor
            renderdict["##NOMEPLANILHA##"] = nome_planilha

            renderdict["##NOMERESP##"] = nome_apropriador
            renderdict["##MATRRESP##"] = matr_apropriador

            renderdict["##EMPCOUNT##"] = len(employees)

            for emp, empcount in zip(employees, range(1,len(employees)+1)):
                _empmatr, _nome, _apelido, _flags = emp

                # Nome OR Apelido
                _empnome = _apelido if _apelido else _nome

                renderdict["##NOME{}##".format(empcount)] = _empnome
                renderdict["##MATR{}##".format(empcount)] = _empmatr

            # Get flags for this submap
            flags = _map.get_flags_for(nome_planilha=nome_planilha)

            # Choose model from employeecount
            xlsxtemplate = AutoApropModeloSemanal
            if len(employees) > 6:
                xlsxtemplate = AutoApropModeloDiario

            try:
                # Render
                xlsxtemplate.render(_renderdict=renderdict, _outputxlsxpath=_renderfilepath)
            except AutoApropException as e:
                l.error("Erro renderizando XLSX[{}]: Pulando render de {}".format(xlsxtemplate, _renderfilepath))
                print(e)