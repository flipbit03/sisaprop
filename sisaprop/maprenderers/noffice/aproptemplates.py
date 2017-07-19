# -*- coding: cp1252 -*-
# Funções de geração de Folha de Apropriação de Mão-De-Obra

# Funções gerais

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

#---------------------------------------------------------------------------
#
# Apropriação
#
#---------------------------------------------------------------------------


#---------------------------------------------------------------------------
# MODELO: Cabeçalho do arquivo para o n'Office
#---------------------------------------------------------------------------

m_nofficecabec = """.op
.po4
.mt0
.mb2"""

def nofficecabec():
    return m_nofficecabec


#---------------------------------------------------------------------------
# MODELO: Cabeçalho da folha de Apropriação
#---------------------------------------------------------------------------

#==========================================================================
#|    IPC            APROPRIACAO DE MAO DE OBRA            DATA:   /   /  |
#|------------------------------------------------------------------------|
#| XXXXXXXXXXXX  TURNO YYY / ZZZZZZZZZZZ  MATR. RESPONSAVEL: __|__|__|__  |
#+========================================================================+

# X (12L) -->  Especialidade (TRAT. TERMIC / SOLDA / ...)
# Y (3L)  -->  Turno ( MAN / ADM / NOI )
# Z (11L) -->  Nome do Apontador

m_ap_cabec = \
"""==========================================================================
|    IPC            APROPRIACAO DE MAO DE OBRA            DATA:   /   /  |
|------------------------------------------------------------------------|
| {0}  TURNO {1} / {2}  MATR. RESPONSAVEL: __|__|__|__  |
+========================================================================+"""

def ap_cabec(espec="ESPECIALIDADE", turno="001", nome="NOME DO APONTAD"):
    return m_ap_cabec.format(fl(12,espec), \
                             fl(3,turno), \
                             fl(11, nome))


                             
#---------------------------------------------------------------------------                             
# MODELO: Quadro de apropriação // Cabecalho
#---------------------------------------------------------------------------

#|               MATRICULA                  | 370     | 375     | 1043    |
#|                 NOME                     |GONCALVES|RANGEL   | JAIR    |
#|------------------------------------------|---------|---------|---------|

m_apq_cabec = \
"""|               MATRICULA                  |{0}|{2}|{4}|
|                 NOME                     |{1}|{3}|{5}|
|------------------------------------------|---------|---------|---------|"""

def apq_cabec(matr1="", nome1="", matr2="", nome2="", matr3="", nome3=""):
    return m_apq_cabec.format(fc(9,str(matr1)), fc(9, nome1), \
                       fc(9,str(matr2)), fc(9, nome2), \
                       fc(9,str(matr3)), fc(9, nome3) )



#---------------------------------------------------------------------------                       
# MODELO: Quadro de apropriação // Cabecalho2
#---------------------------------------------------------------------------

#|      PEDIDO       |   FA    |  OF   |ATIV| HN | HE | HN | HE | HN | HE |
#|-------------------|---------|-------|----|----|----|----|----|----|----|

m_apq_cabec2 = \
"""|      PEDIDO       |   FA    |  OF   |ATIV| HN | HE | HN | HE | HN | HE |
|-------------------|---------|-------|----|----|----|----|----|----|----|"""

def apq_cabec2():
    return m_apq_cabec2


#---------------------------------------------------------------------------    
# MODELO: Quadro de apropriação // Linha de Anotação
#---------------------------------------------------------------------------


#|      PEDIDO       |   FA    |  OF   |ATIV| HN | HE | HN | HE | HN | HE |
#|-------------------|---------|-------|----|----|----|----|----|----|----|

m_apq_linha = \
"""|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|_|____|____|____|____|____|____|____|"""

def apq_linha():
    return m_apq_linha

    
#---------------------------------------------------------------------------
# MODELO: Separador   
#---------------------------------------------------------------------------
    
m_apq_sep = "+========================================================================+"

def apq_sep():
    return m_apq_sep
    
#---------------------------------------------------------------------------    
# MODELO: Quadro de apropriação completo
#---------------------------------------------------------------------------

def quadro(data={3461:'TESTE'},qtdl=8):
    ldata = data.keys()
    ldata.sort()
    if not len(ldata) == 3:
           for times in range(3-(len(ldata)%3)):
               print "append..."
               ldata.append('')

    data[''] = ''

    out = []
    if len(ldata) != 3:
        return "quadro(): Erro: Mais de 3 pares matr/nome (%d)!" % (len(ldata))
    else:
        matr1 = ldata[0]
        nome1 = data[ldata[0]]
        matr2 = ldata[1]
        nome2 = data[ldata[1]]
        matr3 = ldata[2]
        nome3 = data[ldata[2]]
        out.append(apq_cabec(matr1,nome1,matr2,nome2,matr3,nome3))
        out.append(apq_cabec2())
        for times in range(qtdl):
                   out.append(apq_linha())


    return '\n'.join(out)

    
#---------------------------------------------------------------------------
#
# Rascunho!
#
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
# MODELO: Cabeçalho
#---------------------------------------------------------------------------

#=======================================================================+
#                        DISTRIBUICAO DE MAO DE OBRA                     |
#                                                                        |
#  TRACAGEM        TURNO 001 / APONTADOR                  DATA:         |
#========================================================================+

m_apr_cabec = \
"""+========================================================================+
|                        DISTRIBUICAO DE MAO DE OBRA                     |
|                                                                        |
| {0}     TURNO {1} / {2}                 DATA:         |
+========================================================================+
| MATR.|   NOME     |   ORDEM DE SERVICO                |   FA      | OP |
|______|____________|___________________________________|___________|____|"""

def apr_cabec(espec="ESPECIALIDADE", turno="001", nome="NOME DO APONTAD"):
    return m_apr_cabec.format(fl(12,espec), \
                             fl(3,turno), \
                             fl(11, nome))
                             
#---------------------------------------------------------------------------
# MODELO: Linhas para anotações
#---------------------------------------------------------------------------

#     |            |                                   |           |    |
#23456|123456789012|                                   |           |    |
#_____|____________|___________________________________|___________|____|

m_apr_linha = \
"""|      |            |                                   |           |    |
|{0}|{1}|                                   |           |    |
|______|____________|___________________________________|___________|____|"""

def apr_linha(matr="1234", nome="NOME FUNCIONARIO"):
    return m_apr_linha.format(fc(6,str(matr)), \
                             fc(12, str(nome)))
                             
                             
#---------------------------------------------------------------------------
# MODELO: Linha separadora final +==+
#---------------------------------------------------------------------------                           
                             
#+========================================================================+

m_apr_sep = "+========================================================================+"

def apr_sep():
    return m_apr_sep