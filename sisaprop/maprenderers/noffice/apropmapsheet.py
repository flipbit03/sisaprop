from .nofficeexc import *
#import sisaprop.maprenderers.noffice.aproptemplates as tpl
from . import aproptemplates as tpl


class ApropMapSheet(object):
    sheettype = "Folha de Rosto"

    def __init__(self, especialidade="ESPECIALIDADE", turno="001", nome="NOME DO APONTAD"):
        # Save data
        self.especialidade = str(especialidade)
        self.turno = str(turno)
        self.apropnome  = str(nome)
        
        # Create area for (employee number, name) tuples
        self.workers = []
        
        # Define max workers:
        self.maxworkers = 12
        
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
        out.append(tpl.ap_cabec(espec=str(self.especialidade), turno=str(self.turno), nome=str(self.apropnome)))
        
        # Loop three times
        
        for _x_ in range(4):
            # pop 3 entries from 'w'
            n1 = w.pop()
            n2 = w.pop()
            n3 = w.pop()
            
            # 2 - "3 Names" Header
            out.append(tpl.apq_cabec(matr1=n1[0], nome1=n1[1], matr2=n2[0], nome2=n2[1], matr3=n3[0], nome3=n3[1]))
            
            # 3 - "Pedido" Header
            out.append(tpl.apq_cabec2())
            
            # 4 - 8 "annotation lines"
            for _y_ in range(8):
                out.append(tpl.apq_linha())
                
            # 5 - '+==+' Separator
            out.append(tpl.apq_sep())
        
        
        return '\n'.join(out)
        
   
