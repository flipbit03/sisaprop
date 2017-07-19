from nofficeexc import *
from nofficeutil import *

class NOfficeSheet(object):
    # maxlines without the HEADER which is always 1 line long
    def __init__(self, maxlines=63, maxlinelen=75, pageno=1):
        
        # if we want X lines, then it's really X-1 newline characters
        self.maxnewlines = maxlines - 1
        
        self.maxlinelen = maxlinelen
        self.pageno = int(pageno)
        self.content = []
        
    def clearcontent(self):
        self.content = []
        
    def getcontentsize(self):
        if not self.content:
            return 0
        else:
            return '\n'.join(self.content).count('\n')
            
    def getcontent(self):
        if not self.content:
            return ''
        else:
            return '\n'.join(self.content)

    def _canaddcontent(self, addcontent):
        sco = addcontent.strip()
        scolen = 1 + sco.count('\n')
        
        if scolen + self.getcontentsize() > self.maxnewlines:
            return False
        else:
            return True
        
    def addcontent(self, content):
        sco = content.replace('\r\n','\n')
        sco = sco.strip()

        if self._canaddcontent(sco):
            for _line in sco.split('\n'):
                self.content.append(_line)
        else:
            raise EWontFit
            
    def __str__(self):
        out  = []

        nl2add = ((self.maxnewlines) - self.getcontentsize())/2

        # add top white lines
        for i in range(int(nl2add)):
            out.append('')
        
        # add content
        out.append(self.getcontent())
        
        # calculate and add bottom white lines
        bottomnl2add = self.maxnewlines - '\n'.join(out).count('\n')
        for i in range(bottomnl2add):
            out.append('')
        
        # Add page number
        out.append(fc(self.maxlinelen, 'PAG %02d' % (self.pageno)))
        
        # If this is the first page, add some custom N'office headers
        if self.pageno == 1:
            out.insert(0, ".op\n.po4\n.mt0\n.mb2")

        # Iterate over returnval, outputting to a new list. this list will be fixed by self.maxlinelen
        returnval = []
        for line in '\n'.join(out).split('\n'):
            returnval.append(fl(self.maxlinelen, line))

        # Returnval now is ready and can be \n-joined to create the real page.
        return '\n'.join(returnval)