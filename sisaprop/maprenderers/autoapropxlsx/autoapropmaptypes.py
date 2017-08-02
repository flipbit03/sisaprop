from sisaprop.map.map import Map

import logging
import os
import zipfile
import re
templatepath = os.path.join(os.getcwd(), "sisaprop", "data")

l = logging.getLogger("AutoApropMaps")

class AutoApropException(Exception):
    pass

class AutoApropMapBase():
    def __repr__(self):
        return "<{}:{}:capacity={}>".format(self.__class__.__name__, self.name, self.amount)

    def __init__(self, name, original_template : str, amount : int):
        self.name = name
        self.original_template = original_template
        self.amount = amount

    def render(self, _renderdict: dict, _outputxlsxpath: str):

        # Adjust Render Dict
        adjusted_renderdict = self._adjust_renderdict(_renderdict)

        # Open Template
        templatezf = zipfile.ZipFile(self.original_template, 'r')

        # Open Output File
        outputzf = zipfile.ZipFile(_outputxlsxpath, 'w')

        # For each file inside the Template XLSX
        for zi in templatezf.infolist():

            # Read the file's contents as bytes
            template_filedata = templatezf.read(zi)

            # Substitute all variables
            replaced_filedata = self._rendertext_from_renderdict(template_filedata, adjusted_renderdict)

            # Detect if something changed
            if template_filedata != replaced_filedata:
                pass

            # Write the new file to the output .zip (XLSX)
            outputzf.writestr(zi, replaced_filedata)

        # Close the output zip file and the template
        outputzf.close()
        templatezf.close()

    def _adjust_renderdict(self, _renderdict: dict) -> dict:

        # Make a copy of the renderdict
        rv = dict(_renderdict)

        # Less than the amount this dict holds
        #namecount = len(list(filter(lambda x: re.search("##NOME[0-9]", x), _renderdict.keys())))
        namecount = _renderdict["##EMPCOUNT##"]

        if namecount <= self.amount:
            for i in range(1, self.amount+1):
                namekey = "##NOME{}##".format(i)
                if not namekey in rv:
                    rv["##NOME{}##".format(i)] = " "
                    rv["##MATR{}##".format(i)] = " "
        else:
            raise AutoApropException("Grupo não cabe nesta folha (grupo[{}] > folha[{}])".format(namecount, self.amount))

        return rv

    def _rendertext_from_renderdict(self, _text: bytes, _renderdict: dict) -> bytes:

        # Make a copy of the original text.
        outputtext = bytes(_text)

        for key in _renderdict:
            key_bytes = key.encode("utf8")

            try:
                value_bytes = _renderdict[key].encode("utf8")
            except:
                # integer
                value_bytes = bytes(_renderdict[key])

            replacecount = 0
            while outputtext.find(key_bytes) != -1:
                replacecount = replacecount + 1
                outputtext = outputtext.replace(key_bytes, value_bytes, 1)

        return outputtext

# Modelo Semanal
modelosemanal_path = os.path.join(templatepath, "msemanal.xlsx")
AutoApropModeloSemanal = AutoApropMapBase("Modelo Semanal", modelosemanal_path, 6)

# Modelo Diário - Somente Turno Administrativo
modelodiarioadm_path = os.path.join(templatepath, "mdiario_adm.xlsx")
AutoApropModeloDiarioAdministrativo = AutoApropMapBase("Modelo Diário Administrativo", modelodiarioadm_path, 30)

# Modelo Diário
modelodiario_path = os.path.join(templatepath, "mdiario.xlsx")
AutoApropModeloDiario = AutoApropMapBase("Modelo Diário", modelodiario_path, 30)

