#!/usr/bin/env python
# -*- coding: utf-8

class SISAAPROPAppException(Exception):
    pass

# Erros do APP
class SISAPROPEFolderDoesNotExist(SISAAPROPAppException):
    pass

class SISAPROPNoWorkableMap(SISAAPROPAppException):
    pass

class SISAPROPNoRenderMethod(SISAAPROPAppException):
    pass


# Exceções internas
class MapRendererException(SISAAPROPAppException):
    pass

class MapRenderManagerException(SISAAPROPAppException):
    pass

