import numpy as np

def DownSamplingVertical(U0, U1):
    if(len(U0) == 1):
        return U0, U1
    
    V0 = U0[::2, :]
    V1 = U1[1::2, :]
    
    return V0, V1
