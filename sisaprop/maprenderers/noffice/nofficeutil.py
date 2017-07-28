import os

def f(size, align, what):
    pdata = str(what)
    align = str(align)
    if len(pdata) > size:
        pdata = pdata[0:size]
    fstring = '{0:%s%s}' % (align, str(size))
    return fstring.format(pdata)
    
def fc(size, what):
    return f(size, '^', what)

def fl(size, what):
    return f(size, '<', what)

def fr(size, what):
    return f(size, '>', what)

# FAIL
def exitr(reason, code=0):
    print("ERRO: %s\n" % (reason))
    input("-- press enter --")
    exit(int(code))

    
# MAP open utils
__mapfolder = os.path.join(os.getcwd(), 'maps')

def getmap(mapname):
    mapfname = mapname + '.csv'
    f = open(os.path.join(__mapfolder, mapfname), 'rb')
    fd = f.read()
    f.close()
    return fd
    
    
    