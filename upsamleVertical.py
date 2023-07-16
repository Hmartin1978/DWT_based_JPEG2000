import numpy as np

def upsampleVerticalLP(X):
    if(len(X) == 1): return X

    rows, cols = X.shape
    new_rows = 2 * rows 

    result = np.zeros((new_rows, cols))
    result[::2] = X

    return result

def upsampleVerticalHP(X):
    if(len(X) == 1): return X

    rows, cols = X.shape
    new_rows = 2 * rows 

    result = np.zeros((new_rows, cols))
    result[1::2] = X

    return result