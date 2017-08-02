__author__ = 'carlos.coelho'

import logging
import os

from . import noffice

from sisaprop.map.map import Map
from .maprendererbase import MapRendererBase

l = logging.getLogger("NofficeMapRenderer")

class NofficeMapRenderer(MapRendererBase):
    def realrender(self, _map: Map, _path):

        l.debug("Map is [{0}]".format(_map))
        l.debug("RenderPath is [{0}]".format(_path))

        _map.get_statistics()

        # Split maps by default keysorting
        submaps = _map.getsplitmapdata()

        # Create dict for render stats gathering.
        renderstats = {}

        l.debug("{0} submap(s) to render from map...".format(len(submaps)))
        for submapname in submaps:
            rendersubmapname = submapname.split(u'/')[-1].lower()
            assert isinstance(rendersubmapname, str)
            rendersubmapname = rendersubmapname.replace(u'.',u'') + u'.txt'

            # Get filename from rendersubmapname
            renderfilename = os.path.join(_path, rendersubmapname)

            # Generate each map.
            print("  Renderizando mapa {0} ({1})...".format(submapname, rendersubmapname))
            l.debug("Rendering submap \"{0}\".".format(submapname))
            renderstats[rendersubmapname] = self.rendereachmap(submaps[submapname], rendersubmapname, renderfilename)
            l.debug(" ")

        # TODO: Statistics
        # Brinca
        #x=_map.get_statistics()
        #print "brinca"
        #from code import interact
        #interact(local=locals())


    def rendereachmap(self, _map : Map, _mapname, _renderfilepath):
        assert isinstance(_map, Map)

        # Create a list to populate statistics (page number, etc)
        renderstatistics = []

        # Create a new NOffice Document
        nod = noffice.NOfficeDoc(docname=_mapname)

        # Get the full list of employees separated by params (nome_apropriador, especialidade, turno)
        # [ ((matr, nome, nickname)[1..n], (nome_apropriador, especialidade, turno))
        bigemployeelist = _map.get_all_funcionarios()

        l.debug("  [sub] map {0} has {1} slice(s).".format(_mapname, len(bigemployeelist)))

        # "sheets" array -- this will hold all apropmapsheets
        output_apropsheets = []
        sheetpgno = 1

        # "drafts" array -- this will hold all propmapdrafts
        output_apropdrafts = []
        draftpgno = 1

        for slice in bigemployeelist:
            employees, params = tuple(slice)
            apropriador_com_matr, especialidade, nome_planilha , turno = params

            nome_apropriador, matr_apropriador = apropriador_com_matr

            especialidade = especialidade.replace("\n","")

            l.debug("    [slice] > {0:s} {1:s} {2:s}".format(nome_apropriador, especialidade, turno))

            # Helper functions
            def append_sheet():
                output_apropsheets.append(
                    (noffice.ApropMapSheet(especialidade=especialidade, turno=turno, nome=nome_apropriador),
                     []))

            def append_draft():
                output_apropdrafts.append(
                    (noffice.ApropMapDraft(especialidade=especialidade, turno=turno, nome=nome_apropriador),
                     []))

            def allocworker_sheet(_matr, _workername):
                _sheet, _stats = output_apropsheets[-1]
                # Add worker to sheet
                _sheet.addworker(_matr, _workername)
                # Add worker stats
                _stats.append((_matr, _workername))

            def allocworker_draft(_matr, _workername):
                _sheet, _stats = output_apropdrafts[-1]
                # Add worker to sheet
                _sheet.addworker(_matr, _workername)
                # Add worker stats
                _stats.append((_matr, _workername))

            # Create initial pages
            append_sheet()
            append_draft()

            # Start allocating employees (popping from a copy)
            employees_copy = list(employees)
            while employees_copy:
                matr, name, nickname, FLAGS = employees_copy.pop(0)
                workersheetname = name
                if nickname:
                    workersheetname = nickname

                # Sheet
                try:
                    # Add the worker
                    allocworker_sheet(matr, workersheetname)
                except noffice.EFull:
                    # Generate a new ApropMapSheet
                    append_sheet()

                    # Add the worker to the new page
                    allocworker_sheet(matr, workersheetname)

                # Draft
                try:
                    # Add the worker
                    allocworker_draft(matr, workersheetname)
                except noffice.EFull:
                    # Generate a new ApropMapSheet
                    append_draft()

                    # Add the worker to the new page
                    allocworker_draft(matr, workersheetname)

        # Add all content to a list of nofficepages.
        allpages = output_apropsheets + output_apropdrafts
        pagenumbers = range(1,len(allpages)+1)
        for (content, pageno) in zip(allpages, pagenumbers):
            sheet, stats = content
            # Populate statistics, now that we know the page numbers
            for employee_stat in stats:
                _matr , _empname = employee_stat
                renderstatistics.append( (_mapname, sheet.sheettype, sheet.especialidade, sheet.turno, sheet.apropnome,
                                          _matr, _empname, pageno))

            nod.addpage()
            nod.getlastpage().addcontent(str(sheet))

        # Render NofficeDocument to a TXT
        text = nod.rendertotext()
        with open(_renderfilepath, 'wb') as f:
            f.write(bytes(text, "ascii"))

        return renderstatistics
