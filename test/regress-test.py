import sys
sys.path.append('../src')

import regress

datsrc="../data/src/"
# regression test according the data from page:
# https://www.immagic.com/eLibrary/ARCHIVES/GENERAL/WIKIPEDI/W120619S.pdf

vx = []
vy = []
for line in open(datsrc + "regression-test.dat"):
    if not line.startswith("#"):
        split = line.split()
        x = float(split[0])
        y = float(split[1])
        vx.append(x)
        vy.append(y)
for x in vx:
    print("%5.2f" % x ,end=" ")
print()
for y in vy:
    print("%5.2f" % y ,end=" ")
print()

reg = regress.Regress(vx,vy)
print(reg.fit())
print(reg.fiterr())
reg.details_xmgrace()

