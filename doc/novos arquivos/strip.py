import sys
import os

a = open(sys.argv[1],'rb').readlines()

b = open(os.path.join(os.getcwd(),'out.out'),'wb')

for i in a:
    b.write(i.rstrip()+'\n')

b.close()
