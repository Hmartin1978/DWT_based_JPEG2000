import numpy as np

def inverse_idx(idx:int, power:int):
    lenOfSize = np.power(2, power)
    if idx >= lenOfSize // 2:
        return idx
    else: return idx + 1 - lenOfSize

def RLEDecode(SymbolStream:str, BitStream:str):
    Decoded_img = []
    currentIdx = 0
    for char in SymbolStream:
        if char == "k" or char == "l" : 
            Decoded_img.append(0)
            continue
        
        size = ord(char) - ord("a") + 1
        idx = int(BitStream[currentIdx:currentIdx+size], 2) # binary->decimal
        Decoded_img.append(inverse_idx(idx, size))
        currentIdx += size

    return Decoded_img