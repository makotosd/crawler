# -*- coding: utf-8 -*-
import sys

OLDFILE = sys.argv[1]
NEWFILE = sys.argv[2]

NEWENTRYFILE = sys.argv[3]   # "appear.json"
DISAPPEARFILE = sys.argv[4]  # "disappear.json"

a = open(OLDFILE, 'r').read().split('\n')
b = open(NEWFILE, 'r').read().split('\n')
c = open(NEWENTRYFILE, 'w')
d = open(DISAPPEARFILE, 'w')
c.write('\n'.join([comm for comm in b if not (comm in a)]))
c.close()
d.write('\n'.join([comm for comm in a if not (comm in b)]))
d.close()
