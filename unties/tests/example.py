from unties import *
from unties.properties import air, water

# Example Problem From Lecture 20, used to test my code ########################
P = 1 * atm
Ts = deg_c(60)
Tinf = deg_c(20)
uinf = 5 * m / s
Lplate = 2 * m
Wplate = 1 * m
Aplate = Lplate * Wplate

Tf = (Ts + Tinf) / 2

ReLair = Lplate * uinf / air.kinematic_viscocity_one_atm(Tf)
ReLwater = Lplate * uinf / water.kinematic_viscocity(Tf)

print('ReLair: ', ReLair)       #=>   580604.9328822473
print('ReLwater: ', ReLwater)   #=> 14784102.506582394

Nuair = (0.037 * ReLair**(4/5) - 871) * air.Pr_one_atm(Tf)**(1/3)
Nuwater = (0.037 * ReLwater**(4/5) - 871) * water.Pr(Tf)**(1/3)

Cfair = 0.074 * ReLair**(-1/5) - 1742 * ReLair**-1
Cfwater = 0.074 * ReLwater**(-1/5) - 1742 * ReLwater**-1

hair = Nuair * air.k_v(Tf) / Lplate
hwater = Nuwater * water.k_l(Tf) / Lplate

qair = hair * Aplate * (Ts - Tinf)
qwater = hwater * Aplate * (Ts - Tinf)

print('qair: ', qair(W))        #=>    617.6629704277314 * W
print('qwater: ', qwater(W))    #=> 795162.4132944812 * W

# The printed values in comments have been certified to be correct. If the
# actual output has changed, then something is wrong with the air or water
# property files.

ReLair_correct = ReLair == 580604.9328822473
ReLwater_correct = ReLwater == 14784102.506582394
qair_correct = qair == 617.6629704277314 * W
qwater_correct = qwater == 795162.4132944812 * W

good = ReLair_correct and ReLwater_correct and qair_correct and qwater_correct

if good:
    print("All's good! :D")
else:
    print("Something's wrong!!! D:")
