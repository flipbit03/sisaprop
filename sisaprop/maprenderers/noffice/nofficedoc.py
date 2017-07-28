from .nofficesheet import NOfficeSheet

class NOfficeDoc(object):
    """Class structured to define a full NOfficeDoc Document, spanning several pages"""
    def __init__(self, docname="nofficedoc"):

        # Page storage - each item is a NOfficeSheet instance
        self.__pages = []

    def pagecount(self):
        return len(self.__pages)

    def addpage(self):
        self.__pages.append(NOfficeSheet(pageno=self.pagecount()+1))

    def getlastpage(self):
        return self.__pages[-1] if self.__pages else None

    def getpage(self, pageno):
        return self.__pages[pageno]

    def rendertotext(self):
        return '\n'.join([str(page) for page in self.__pages])