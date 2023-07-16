import numpy as np

def DownSamplingHorizontal(U0, U1):
    V0 = U0[:, ::2]
    V1 = U1[:, 1::2]
    
    return V0, V1