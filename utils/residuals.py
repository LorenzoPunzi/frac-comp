import numpy as np
"""
Module containing functions ``makeresids()`` and ``fitconst()``, which serve manipulate arrays to find the fractions' residuals and fit them with a constant.
"""

def makeresids(fracts1, fracts2):
    """
    Makes two numpy arrays containing residuals and their errors from the given fraction arrays.

    :param fracts1: 9 column 2D numpy array containing arbitrary values in the first column, and in the following columns respectively the fractions and errors (from file 1): ppg, dppg, mmg, dmmg, eeg, deeg, ppp, dppp.
    :type fracts1: numpy.array(float)
    :param fracts2: 9 column 2D numpy array containing arbitrary values in the first column, and in the following columns respectively the fractions and errors (from file 2): ppg, dppg, mmg, dmmg, eeg, deeg, ppp, dppp.
    :type fracts2: numpy.array[float]
    :return: Two element tuple containing respectively a 4 column 2D numpy array of the residuals (column order: ppg, mmg, eeg, ppp) and a 4 column 2D numpy array of the the residual's errors in same column order.
    :rtype: tuple(numpy.array(float))

    """

    resids = fracts1-fracts2
    resids = resids[:,1::2]
    dresids = np.sqrt(fracts1**2+fracts2**2)
    dresids = dresids[:,2::2]
    return resids , dresids

def fitconst(resids, dresids):
    """
    Fits the residuals with a constant and returns the best fit constant, along with the chi square of the fit.

    :param resids: 4 column 2D numpy array containing in its columns respectively the residuals for: ppg, mmg, eeg, ppp.
    :type resids: numpy.array(float)
    :param dresids: 4 column 2D numpy array containing in its columns respectively the errors of the residuals for: ppg, mmg, eeg, ppp.
    :type dresids: numpy.array(float)
    :return: Three element tuple containing respectively the best fit constant, its error and the chi square of the fit.
    :rtype: tuple(float)

    """

    dresids[dresids != 0] = 1 / dresids[dresids != 0]
    w_i = dresids**2
    dresids[dresids != 0] = 1 / dresids[dresids != 0] # revert to original residual errors so as to not change them in __main__

    r_i_w_i = resids*w_i

    num = np.sum(r_i_w_i, axis=0)
    denom = np.sum(w_i, axis=0)
    
    q = num/denom
    dq = np.sqrt(1/denom)
    chisq = np.divide(resids-q, dresids, out=np.zeros_like(resids), where=dresids!=0)
    chisq = chisq**2
    chisq = np.sum(chisq, axis=0)

    return q, dq, chisq

