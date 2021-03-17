#!/usr/bin/env python3
import os
from pathlib import Path
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '/')

def getinputdict(loglineareqs = True):
    inputdict = {}

    inputdict['paramssdict'] = {'GAMMA': 1, 'BETA': 0.95, 'ETA': 2, 'ALPHA': 0.3, 'RHO_A': 0.95, 'Abar': 1}
    inputdict['states'] = ['A']
    inputdict['controls'] = ['C', 'L', 'Rp', 'W', 'Y']
    inputdict['shocks'] = ['epsilon_A']

    # equations:{{{
    inputdict['equations'] = []

    # household
    if loglineareqs is True:
        inputdict['equations'].append('-GAMMA * C = Rp - GAMMA * C_p')
    else:
        inputdict['equations'].append('C^(-GAMMA) = BETA*Rp*C_p^(-GAMMA)')
    if loglineareqs is True:
        inputdict['equations'].append('W - GAMMA * C = ETA * L')
    else:
        inputdict['equations'].append('W*C^(-GAMMA) = L^(ETA)')

    # firms
    if loglineareqs is True:
        inputdict['equations'].append('W = A')
    else:
        inputdict['equations'].append('W = A')
    if loglineareqs is True:
        inputdict['equations'].append('Y = A + L')
    else:
        inputdict['equations'].append('Y = A * L')

    # exogenous process
    if loglineareqs is True:
        inputdict['equations'].append('A_p = RHO_A * A + epsilon_A')
    else:
        inputdict['equations'].append('log(A_p) = RHO_A*log(A) + (1 - RHO_A) * log(Abar) + epsilon_A')

    # resource
    if loglineareqs is True:
        inputdict['equations'].append('C = Y')
    else:
        inputdict['equations'].append('C = Y')
        
    # equations:}}}

    p = inputdict['paramssdict']
    p['A'] = p['Abar']
    p['W'] = p['A']
    p['Rp'] = 1/p['BETA']

    p['L'] = p['A'] ** ((1 - p['GAMMA']) / (p['ETA'] + p['GAMMA']))
    p['Y'] = p['A'] * p['L']
    p['C'] = p['Y']

    if loglineareqs is True:
        inputdict['loglineareqs'] = True
    else:
        inputdict['logvars'] = inputdict['states'] + inputdict['controls']
    inputdict['irfshocks'] = ['epsilon_A']

    # save stuff
    inputdict['savefolder'] = __projectdir__ / Path('temp/')

    return(inputdict)


def check():
    inputdict_loglin = getinputdict(loglineareqs = True)
    inputdict_log = getinputdict(loglineareqs = False)
    sys.path.append(str(__projectdir__ / Path('submodules/dsge-perturbation/')))
    from dsgediff_func import checksame_inputdict
    checksame_inputdict(inputdict_loglin, inputdict_log)
    

def dsgefull():
    inputdict = getinputdict()
    sys.path.append(str(__projectdir__ / Path('submodules/dsge-perturbation/')))
    from dsge_bkdiscrete_func import discretelineardsgefull
    discretelineardsgefull(inputdict)


# Run:{{{1
check()
dsgefull()
