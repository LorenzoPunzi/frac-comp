import numpy as np
import os
import sys

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def frextract(filepath, var, qqrng):
    novar = 'mu' if var == 'pi' else 'pi'
    QQstring = 'QQ' + var + var
    noQQstring = 'QQ' + novar + novar
    list_fracs = [[], [], [], [], [], [], [], [], []]
    with open(filepath, 'r') as buf:
        flg = 0
        err = 0 # To check for correct formatting
        cols = [QQstring,'ppg','dppg','mmg','dmmg','eeg','deeg','ppp','dppp']
        posdict = {}
        for line in buf:
            line = line.replace(' ','')
            line.strip('\t')
            linlist = line.split('\t')
            linlist[-1] = linlist[-1].replace('\n','')

            if QQstring in linlist:
                flg = 1
                for name in cols:
                    posdict[name] = linlist.index(name)
                
            if noQQstring in linlist:
                flg = 0

            if len(linlist) < 5:
                continue

            if not False in map(is_float,linlist) and flg:
                for sublist,name in zip(list_fracs,cols):
                    if qqrng[0] <= float(linlist[posdict[QQstring]]) <= qqrng[1]:
                        sublist.append(float(linlist[posdict[name]]))

    return np.array(list_fracs)

'''
# Error handling for when the file is wrongly formatted (not all chanels or QQ, channel repeated twice,...) !!!!

            for name in cols:
                if line.find(f'\t{name}') < 0:
                    pass
'''
            

                

if __name__ == '__main__':
    frextract('fracfile.txt','pi')#,(0.58,0.62))

