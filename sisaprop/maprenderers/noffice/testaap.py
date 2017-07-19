from nofficesheet import NOfficeSheet
from sisaprop.maprenderers.noffice.apropmapsheet import ApropMapSheet
from sisaprop.maprenderers.noffice.apropmapdraft import ApropMapDraft

a = NOfficeSheet(pageno=1)

b = ApropMapSheet('TRACAGEM','ADM','SERGIO')
b.addworker(3621, 'CARLOS EDUARDO')
b.addworker(2984, 'DIEGO COSTA PEREIRA')
b.addworker(3621, 'CARLOS EDUARDO')
b.addworker(2984, 'DIEGO COSTA PEREIRA')
b.addworker(3621, 'CARLOS EDUARDO')
b.addworker(2984, 'DIEGO COSTA PEREIRA')
b.addworker(3621, 'CARLOS EDUARDO')
b.addworker(2984, 'DIEGO COSTA PEREIRA')
b.addworker(3621, 'CARLOS EDUARDO')
b.addworker(2984, 'DIEGO COSTA PEREIRA')
b.addworker(3621, 'CARLOS EDUARDO')
b.addworker(2984, 'DIEGO COSTA PEREIRA')

a.addcontent(str(b))

b = ApropMapDraft('TRACAGEM','ADM','SERGIO')
b.addworker(3621, 'CARLOS EDUARDO')
b.addworker(2984, 'DIEGO COSTA PEREIRA')
b.addworker(3621, 'CARLOS EDUARDO')
b.addworker(2984, 'DIEGO COSTA PEREIRA')
b.addworker(3621, 'CARLOS EDUARDO')
b.addworker(2984, 'DIEGO COSTA PEREIRA')
b.addworker(3621, 'CARLOS EDUARDO')
b.addworker(2984, 'DIEGO COSTA PEREIRA')
b.addworker(3621, 'CARLOS EDUARDO')
b.addworker(2984, 'DIEGO COSTA PEREIRA')
b.addworker(3621, 'CARLOS EDUARDO')
b.addworker(2984, 'DIEGO COSTA PEREIRA')


a.addcontent(str(b))

print a