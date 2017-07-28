from .nofficeexc import *
from . import aproptemplates as tpl


class ApropMapDraft(object):
    sheettype = "Rascunho"

    def __init__(self, especialidade="ESPECIALIDADE", turno="001", nome="NOME DO APONTAD"):
        # Save data
        self.especialidade = str(especialidade)
        self.turno = str(turno)
        self.apropnome  = str(nome)
        
        # Create area for (employee number, name) tuples
        self.workers = []
        
        # Define max workers:
        self.maxworkers = 18
        
    def sortworkers(self):
        """ Re-sorts workers using employee number """
        if self.workers:
            self.workers = sorted(self.workers, key= lambda x: x[0])
        
    def addworker(self, matr, name):
        if len(self.workers) < self.maxworkers:
            self.workers.append((int(matr), str(name)))
        else:
            raise EFull
            
    # Generate sheet from data
    def __str__(self):

        # Fill blanks to make sure we'll have 'maxworkers' slots
        w = ( self.workers + [(' ',' '),]*self.maxworkers )[:self.maxworkers]
        
        # Invert w, because we are going to 'pop' items from it
        w = w[::-1]
        
        # Output var
        out = []
        
        # 1 - Header
        out.append(tpl.apr_cabec(espec=str(self.especialidade), turno=str(self.turno), nome=str(self.apropnome)))
        
        # Loop 'maxworkers' times - 1 worker per line
        
        for _x_ in range(len(w)):
            # pop 1 entries from 'w'
            n1 = w.pop()
            
            # 2 - "Draft Annotation" Line 
            out.append(tpl.apr_linha(matr=n1[0], nome=n1[1]))
            

        # 5 - '+==+' Separator
        out.append(tpl.apr_sep())


        return '\n'.join(out)     
