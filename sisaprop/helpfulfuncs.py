# -*- coding: utf8 -*-
__author__ = 'carlos.coelho'

def reportfatalerror(_exc):
    print u""
    print u"-----------------------------------"
    print u"ERRO FATAL: [%s] %s" % (_exc.__class__.__name__,_exc.message)
    print u"<Encerrando SISAPROP>"
    print u"-----------------------------------"
    print u""
    exit(1)

def chooseoption(optionitems, prompt):
    optionpicker = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ".upper()
    if len(optionitems) > len(optionpicker):
        raise Exception("chooseoption() error: too many options (max %d)" % (len(optionpicker)))

    print prompt+'\n'

    optdict = {}
    slicedoptionpicker = optionpicker[0:len(optionitems)]
    for opt, optionitem in zip(slicedoptionpicker, optionitems):
        optdict[opt] = optionitem
        print "  %s: \"%s\"" % (opt, optionitem)

    opt = ""
    while not opt:
        chosenoption = raw_input("\n[%s-%s or / to cancel]: " % (slicedoptionpicker[0], slicedoptionpicker[-1]))
        if chosenoption in slicedoptionpicker+'/':
            opt = chosenoption

    if opt == "/":
        return ""

    return optdict[opt]

