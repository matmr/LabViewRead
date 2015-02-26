'''
Created on 21. mar. 2013

@author: Matjaz
'''
import locale

import numpy as np

def lvm_read(fname, MAX_DATA=50000):
    '''A simple function for getting the contents
    of a labview measurement file. Returns a tuple
    of second header and measurement values dictionaries.
    
    Returns
    --------
    (h1, h2, meas)
    h1    : Header (1) dictionary.
    h2    : Header (2) dictionary.
    meas  : Measured quantities.
    
    Note
    --------
    Check LabView documentation and/or LabView measurement
    file for dictionary keys.
    '''
    
    # .. The header delimiter.
    EOH = 'End_of_Header'
    
    f = open(fname, 'rt')
    
    # .. Read in the first header.
    h1 = {}
    for entry in f:
        if EOH in entry:
            break
        kv = entry.split()
        h1[kv[0]] = kv[1]
                
    # .. Read in the second header.
    # .. NOTE: Be careful, first header is followed
    #    by an empty line, while second header is not!
    h2 = {}
    for entry in f:
        if EOH in entry:
            break
        kv = entry.strip().split('\t')
        try:
            h2[kv[0]] = list(map(float, kv[1:]))
        except ValueError:
            h2[kv[0]] = kv[1:]

    # .. Parse the measured data.
    chnr = int(h2['Channels'][0])
    # .. Interpret table heading first.
    mdatal = next(f).strip()
    names = mdatal.split('\t')
    
    # .. Get numbers of rows and columns.
    rarr = next(f).strip().split('\t')
    ncols = len(rarr)

    # .. Check if X_val (time) is written. As
    #    this is written it expects the comment
    #    column to be always present. Otherwise
    #    it breaks.
    #
    # TODO: More general approach is needed here.
    if ncols < (len(names)-1):
        names = names[1:]
        xch = 0
    else:
        xch = 1
    
    # .. Build a dictionary of arrays for measured values.
    meas = {}
    for name in names[:-1]:
        meas[name] = np.empty(MAX_DATA)

    # .. Finally populate the arrays.    
    for j in range(chnr+xch):
        meas[names[j]][0] = float(rarr[j].replace(',','.'))

    # .. Read the remaining lines.
    i = 1
    for line in f:
        rarr = line.strip().split()
        for j in range(chnr+xch):
            meas[names[j]][i] = float(rarr[j].replace(',','.'))
        i += 1
    
    # .. Trim the arrays.
    for n in range(chnr+xch):
        meas[names[n]] = meas[names[n]][:i]
    
    f.close()
    
    return h1, h2, meas