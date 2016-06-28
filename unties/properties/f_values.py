"""F-Values for LMTD method for solving heat exchangers with multiple passes
s - shell side
t - tube side
i - in
o - out
"""

from numpy import log10

def _Rf(Tsi, Tso, Tti, Tto):
    return (Tsi - Tso) / (Tto - Tti)

def _Pf(Tsi, Tti, Tto):
    return (Tto - Tti) / (Tsi - Tti)

def F1s2t(Tsi, Tso, Tti, Tto):
    """F for 1 shell and 2 tubes"""
    Rf = _Rf(Tsi, Tso, Tti, Tto)
    Pf = _Pf(Tsi, Tti, Tto)
    sqrt = (Rf**2 + 1)**0.5
    log = log10((2 / Pf - 1 - Rf + sqrt) / (2 / Pf - 1 - Rf - sqrt))
    if Rf == 1:
        return sqrt * Pf / (2.3 * (1 - Pf) * log)
    else:
        return sqrt / (Rf - 1) * log10((1 - Pf) / (1 - Pf * Rf)) / log

def F2s4t(Tsi, Tso, Tti, Tto):
    """F for 2 shells and 4 tubes"""
    Rf = _Rf(Tsi, Tso, Tti, Tto)
    Pf = _Pf(Tsi, Tti, Tto)
    sqrt = (Rf**2 + 1)**0.5
    first = 2 / Pf - 1 - Rf + 2 / Pf * ((1 - Pf) * (1 - Pf * Rf))**0.5
    log = log10((first + sqrt) / (first - sqrt))
    if Rf == 1:
        return sqrt * Pf / (4.6 * (1 - Pf) * log)
    else:
        return sqrt * log10((1 - Pf) / (1 - Pf * Rf)) / (2 * (Rf - 1) * log)
