from scipy.optimize import fsolve
from numpy import tan, pi
from scipy.special import jv

def Eplane_wall(n, Bi):
    def f(xg, small, big):
        if xg < small:
            return (small * tan(small) - Bi) * (small - xg)
        elif xg > big:
            return (big * tan(big) - Bi) * (xg - big)
        return xg * tan(xg) - Bi
    if n == 1:
        small = 0
        big = pi / 2
        return fsolve(f, (small + big) / 2, args=(small, big))[0]
    else:
        small = (2 * n - 1) * pi / 2 - pi * 0.9999
        big = (2 * n - 1) * pi / 2 * 0.9999
        return fsolve(f, (small + big) / 2, args=(small, big))[0]

def Ecylinder(n, Bi):
    def f(xg, small, big):
        if xg < small:
            return (small * jv(1, small) / jv(0, small) - Bi) * (small - xg)
        elif xg > big:
            return (big * jv(1, big) / jv(0, big) - Bi) * (xg - big)
        return xg * jv(1, xg) / jv(0, xg) - Bi
    if n == 1:
        small = 0
        big = 2.4
        return fsolve(f, (small + big) / 2, args=(small, big))[0]
    else:
        small = 0.005 + (n - 1) * pi
        big = 2.35 + (n - 1) * pi
        return fsolve(f, (small + big) / 2, args=(small, big))[0]

def Esphere(n, Bi):
    def f(xg, small, big):
        if xg < small:
            return (1 - small / tan(small) - Bi) * (small - xg)
        elif xg > big:
            return (1 - big / tan(big) - Bi) * (xg - big)
        return 1 - xg / tan(xg) - Bi
    small = n * pi - 0.9999 * pi
    big = n * pi * 0.9999
    return fsolve(f, (small + big) / 2, args=(small, big))[0]
