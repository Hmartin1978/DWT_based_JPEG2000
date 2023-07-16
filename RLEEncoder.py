import numpy as np
import HuffmanEncode

# get the size of each element in list
def get_size(val:int):
    if(val <= -512 or val >= 512): return "j" #10
    if(val <= -256 or val >= 256): return "i" #9
    if(val <= -128 or val >= 128): return "h" #8
    if(val <= -64 or val >= 64): return "g" #7
    if(val <= -32 or val >= 32): return "f" #6
    if(val <= -16 or val >= 16): return "e" #5
    if(val <= -8 or val >= 8): return "d" #4
    if(val <= -4 or val >= 4): return "c" #3
    if(val <= -2 or val >= 2): return "b" #2
    if(val == -1 or val == 1): return "a" #1
# get the element index in corresponding size
def size_idx(val:int, size:str):
    power = ord(size) - ord("a") + 1
    len = np.power(2, power)
    init_val = -1 * len + 1 if val < 0 else len - 1
    idx = val - init_val if val < 0 else len - (init_val - val) - 1
    return bin(idx)[2:].zfill(power)

## do EZW operation
def EZW(currentPixel:int, scale:int, scaleIdx:int, subBands:list, direction:str, stage:int):
    row = currentPixel // scale # get the row of current element
    col = currentPixel % scale # get the col of current element
    multiplier = 2
    for idx in range(scaleIdx,stage):
        ZTR = np.sum(np.where(subBands[direction][idx][row*multiplier:(row+1)*multiplier, col*multiplier:(col+1)*multiplier], 1, 0)) # small block -> big blcok
        if ZTR == 0: # current block all equal to 0, go down
            multiplier *= 2
            continue
        else: # current block exist non-zero element->isolated zero
            return "k" # 0
    return "l" # ZTR

# RLE Encoding
def RLE(img:np.ndarray, subBands:list, flag:str, stage:int):
    encoded_seq = [] # encoded bit stream
    Binary_seq = [] # Amplitude bit stream
    Scale_Huffman = []
    Scale_Binary = []
    Scale_Huffman_Root = []
    LenofHuffman = []
    LenofBinary = []

    if flag == "LL":
        img_OneDim = img.flatten() 
        # DC prediction:
        img_OneDim[1:] = img_OneDim[1:] - img_OneDim[0]
        for i in range(len(img_OneDim)):
            if img_OneDim[i] != 0 : # NZ
                current_size = get_size(img_OneDim[i])
                encoded_seq.append(current_size)
                Binary_seq.append(size_idx(img_OneDim[i], current_size))
            else: # Zero
                encoded_seq.append("k")

        encoded_seq = "".join(encoded_seq)
        Binary_seq = "".join(Binary_seq)
        return encoded_seq, Binary_seq
    else: # 2.subbands
        for scaleIdx in range(stage): # children in the same direction
            encoded_seq = [] 
            Binary_seq = []
            scale = img.shape[0]
            img_OneDim = img.flatten()
            for i in range(len(img_OneDim)):
                if img_OneDim[i] != 0: # NZ
                    current_size = get_size(img_OneDim[i])
                    encoded_seq.append(current_size)
                    Binary_seq.append(size_idx(img_OneDim[i], current_size))
                else: # accur zero, judge ZTR
                    if scaleIdx != stage-1:
                        symbol = EZW(i, scale, scaleIdx+1, subBands, flag, stage)
                        encoded_seq.append(symbol)
                    else: encoded_seq.append("k")
            # parent image is scaned, go to children image
            if scaleIdx != stage-1 : img = subBands[flag][scaleIdx+1]

            temp_scale_huffman, temp_scale_root = HuffmanEncode.HuffmanEncode(encoded_seq)
            Scale_Huffman.append(temp_scale_huffman), Scale_Huffman_Root.append(temp_scale_root)
            Scale_Huffman[scaleIdx] = "".join(Scale_Huffman[scaleIdx])
            LenofHuffman.append(len(Scale_Huffman[scaleIdx]))
            Binary_seq = "".join(Binary_seq)
            Scale_Binary.append(Binary_seq)
            LenofBinary.append(len(Binary_seq))

        return Scale_Huffman, Scale_Huffman_Root, LenofHuffman, Scale_Binary, LenofBinary