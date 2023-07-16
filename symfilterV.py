import numpy as np

def symfilterV(X, H, k):
    k_temp = k//2
    result = np.zeros_like(X, dtype=float)
    
    for row, data in enumerate(X):
        data = data.tolist()
        for num in range(0, k_temp):
            data.insert(0, X[row][num+1])
            data.append(X[row][len(X[row])-(num+2)])
        data = np.array(data, dtype=float)
        for col in range(len(data) - (k-1)):
            value = np.dot(data[col:col+k], H)
            result[row][col] = value
    
    return result