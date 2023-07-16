import numpy as np

def upsampleHorizontalLP(img):
    rows, cols = img.shape
    new_cols = 2 * cols

    result = np.zeros((rows, new_cols))
    result[:, ::2] = img

    return result

def upsampleHorizontalHP(img):
    rows, cols = img.shape
    new_cols = 2 * cols

    result = np.zeros((rows, new_cols))
    result[:, 1::2] = img

    return result