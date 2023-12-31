import numpy as np
from utils.exceptions import FileFormatError
import sys
import os
"""
Module containing functions ``frextract()`` and ``reswrite()``, which serve as I/O from the program to the local directories.
"""

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def frextract(filepath, var, qqrng):
    """
    Extracts the fractions and Q^2 values from the given file for all channels, putting them in a single numpy array.

    :param filepath: Filepath of the column file from which to extract the fractions.
    :type filepath: str
    :param var: Variable of which to exctract fractions. Allowed values are ``'pi'`` and ``'mu'`` for ``QQpipi`` and ``QQmumu`` respectively.
    :type var: str
    :param qqrng: Two element tuple containing the left and right ends of the Q^2 range (in GeV^2) to extract from the file.
    :type qqrng: tuple(float)
    :return: 9 column 2D numpy array containing the Q^2 values in the first column, and in the following columns respectively the fractions and errors: ppg, dppg, mmg, dmmg, eeg, deeg, ppp, dppp.
    :rtype: numpy.array(float)

    """
    QQstring = 'QQ' + var + var
    list_fracs = [[], [], [], [], [], [], [], [], []]
    filename = os.path.basename(filepath)
    err = 1 # To check if there are no valid headers
    try:
        with open(filepath, 'r') as buf:
            flg = 0 # To make sure only the data columns after the first valid header are recorded
            head = 0 # To make sure only the first header is used to determine which column belongs to which fraction
            cols = [QQstring,'ppg','dppg','mmg','dmmg','eeg','deeg','ppp','dppp']
            posdict = {}
            for line in buf:
                line = line.replace(' ','')
                line.strip('\t')
                linlist = line.split('\t')
                linlist[-1] = linlist[-1].replace('\n','') # Removes spurious \n at the end of the last linlist element
                if flg:
                    temp = {}
                    try:  
                        for sublist,name in zip(list_fracs,cols):
                            if float(qqrng[0]) <= float(linlist[posdict[QQstring]]) <= float(qqrng[1]):
                                temp[name] = float(linlist[posdict[name]])
                    except ValueError:
                        if linlist != ['']: flg = 0
                    except IndexError:
                        raise FileFormatError(f"In file {filename} there incomplete data rows for variable '{QQstring}'!")
                    else: 
                        if temp:
                            for sublist,name in zip(list_fracs,cols): sublist.append(temp[name])

                if QQstring in linlist and not head:
                    head = 1
                    flg = 1
                    err = 0
                    try:
                        for name in cols:
                            posdict[name] = linlist.index(name) # Record the meaning of the different columns
                    except ValueError:
                        raise FileFormatError(f"In file {filename} the header with '{QQstring}' does not contain '{name}'!")

                if len(linlist) < 5:
                    continue
    except FileNotFoundError:
        print(f"File {filepath} does not exist! Aborting...\n")
        sys.exit(1)


    if err: raise FileFormatError(f"File {filename} does not contain a header with {QQstring}!")
    if not list_fracs[0]: raise FileFormatError(f"File {filename} does not contain data for {QQstring} in the specified range!")

    return np.transpose(np.array(list_fracs))

def reswrite(fracts, resids, dresids, filename1, filename2, variable, filepath):
    """
    Writes the given residuals, along with their errors, to the given filepath.

    :param fracts: 2D numpy array containing in its first column the Q^2 values as a function of which the residuals have been calculated. The rest of the array is not used in this function and therefore is arbitrary.
    :type fracts: numpy.array(float)
    :param resids: 4 column 2D numpy array containing in its columns respectively the residuals for: ppg, mmg, eeg, ppp.
    :type resids: numpy.array(float)
    :param dresids: 4 column 2D numpy array containing in its columns respectively the errors of the residuals for: ppg, mmg, eeg, ppp.
    :type dresids: numpy.array(float)
    :param filename1: Name of file 1 from which the residuals have been calculated, to be inserted in the header of the output file.
    :type filename1: str
    :param filename1: Name of file 2 from which the residuals have been calculated, to be inserted in the header of the output file.
    :type filename1: str
    :param variable: Name of variable as a function of which the given residuals have been calculated, to be inserted in the header of the output file.
    :type variable: str
    :param filepath: Filepath of the output column file containing the residuals.
    :type filepath: str

    """
    QQstring = 'QQ' + variable + variable
    try:
        with open(filepath, encoding='utf-8', mode='w') as buf:

            buf.write("\nResiduals generated by the frac-comp program\n\n"
                    f"Calculated as difference between {filename1} and {filename2} in {QQstring}\n"
                    "---------------------------------------------------------------------------- \n\n"
                    f"{QQstring}     res(ppg)       dres(ppg)      res(mmg)       dres(mmg)      res(eeg)       dres(eeg)      res(ppp)       dres(ppp)\n"
                    "\n")
            for i in range(resids.shape[0]):
                buf.write(f"{fracts[i][0]:9.2f}      {resids[i][0]:9.2e}      {dresids[i][0]:9.2e}      {resids[i][1]:9.2e}      {dresids[i][1]:9.2e}      {resids[i][2]:9.2e}      {dresids[i][2]:9.2e}      {resids[i][3]:9.2e}      {dresids[i][3]:9.2e}\n".lstrip())
    except FileNotFoundError:
        print("Residuals were not saved due to invalid -svdr,--savedir directory!")


                

if __name__ == '__main__':
    frextract('fracfile.txt','pi')#,(0.58,0.62))

