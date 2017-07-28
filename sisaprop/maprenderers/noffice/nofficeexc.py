class NOfficeException(Exception):
    pass

class EWontFit(NOfficeException):
    pass
    
class EFull(NOfficeException):
    pass
    
class EDupWorker(NOfficeException):
    pass