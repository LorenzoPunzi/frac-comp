import numpy as np

def makeresids(fracts1, fracts2):

    resids = fracts1-fracts2
    resids = resids[:,1::2]
    dresids = np.sqrt(fracts1**2+fracts2**2)
    dresids = dresids[:,2::2]
    return resids , dresids

def fitconst(resids, dresids):

    dresids[dresids != 0] = 1 / dresids[dresids != 0]
    w_i = dresids**2
    dresids[dresids != 0] = 1 / dresids[dresids != 0] # revert to original residual errors so as to not change them in __main__

    r_i_w_i = resids*w_i

    num = np.sum(r_i_w_i, axis=0)
    denom = np.sum(w_i, axis=0)

    q = num/denom
    dq = np.sqrt(1/denom)
    chisq = (resids-q)/dresids
    chisq = chisq**2
    chisq = np.sum(chisq, axis=0)

    return q, dq, chisq

