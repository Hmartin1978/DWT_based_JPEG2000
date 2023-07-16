import numpy as np

def Quantization(X, q):
    X = np.where((X / q) <= 0 , np.round(X / q), np.floor(X / q))
    return X.astype(int)

def DeQuantization(X, q):
    X = np.where((X * q) <= 0, np.round(X * q),  np.floor(X * q))
    return X.astype(np.float32)