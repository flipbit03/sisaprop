#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import logging

from sisaprop import SISAPROP_CmdLineApp, SISAAPROPAppException
from sisaprop.helpfulfuncs import reportfatalerror

parser = argparse.ArgumentParser(description='SISAPROP',
epilog=u"Sistema de Preenchimento de Mapas de Apropriação")

parser.add_argument('rootpath', nargs="?", default=os.getcwd(), help=u"Pasta Raiz do SISAPROP")

# Arguments

# mapname = m
parser.add_argument('-m', nargs="?", default=u"", help=u"Nome do Mapa")
# loglevel = l
parser.add_argument('-l', nargs="?", default=u"INFO", help=u"Loglevel [INFO or DEBUG]")
# rendermethod = r
parser.add_argument('-r', nargs="?", default=u"", help=u"Método de Renderização (\"noffice\")")

args = parser.parse_args()

# Configure Logging
import logging
logFORMAT = "%(name)13s %(levelname)5s: %(message)s"
logging.basicConfig(format=logFORMAT, level=args.l)

# Start program

if __name__ == '__main__':
    try:
        app = SISAPROP_CmdLineApp(args)
    except SISAAPROPAppException as e:
        reportfatalerror(e)
