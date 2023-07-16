import numpy as np
from symfilterV import symfilterV
from symfilterH import symfilterH
import upsamleHorizontal
import upsamleVertical
import Quantizer
from RLEDecoder import RLEDecode
from HuffmanEncode import HuffmanDecode
import package

G0 = [1/2, 1, 1/2]
G1 = [-1/8, -1/4, 3/4, -1/4, -1/8]

def Decode(k, StepSize):
   ### 1.UnPacking
    DeRoot = package.UnPacking("HuffmanRoot.bin")
    DeLen = package.UnPacking("Len.bin")
    BisubBandsHuffman = package.UnPackingDecimal2Bin("SubBandsHuffman.bin", DeLen[4])
    BisubBandsBinary = package.UnPackingDecimal2Bin("SubBandsBitStream.bin", DeLen[5])
    DesubBands = package.UnPackingSubBands(BisubBandsHuffman, DeLen[0], k)
    DesubBandsBinary = package.UnPackingSubBands(BisubBandsBinary, DeLen[1], k)
    DeLLHuffman = package.UnPackingDecimal2Bin("LLHuffman.bin", DeLen[2])
    DeLLBinary = package.UnPackingDecimal2Bin("LLBinary.bin", DeLen[3])

    ### 2.Decode(Huffman&RLE)
    # for LL
    size = 512 // np.power(2, k)
    LLHuffmanDecodeStream = HuffmanDecode(DeLLHuffman, DeRoot["LL"]) # HuffmanBitStream->SymbolStream
    LL_Decode_Symbol = RLEDecode(LLHuffmanDecodeStream, DeLLBinary) # RLE->OneDimList
    DC_prediction = np.int32(LL_Decode_Symbol[0])
    LL_Decode_Symbol[1:] += DC_prediction
    LL_Decode_Symbol = np.array(LL_Decode_Symbol, dtype=np.float32).reshape(size, size) # OneDimList->img
    # for subands
    for direction in DesubBands.keys():
        size = 512 // np.power(2, k)
        for i in range(k):
            DesubBands[direction][i] = HuffmanDecode(DesubBands[direction][i], DeRoot[direction][i])
            DesubBands[direction][i] = RLEDecode(DesubBands[direction][i], DesubBandsBinary[direction][i])
            DesubBands[direction][i] = np.array(DesubBands[direction][i], dtype=np.float32).reshape(size,size)
            size *= 2

    ### 3.DeQuantization
    # for LL
    LL = Quantizer.DeQuantization(LL_Decode_Symbol, StepSize)
    # for subBands
    for direction in DesubBands.keys():
        for i in range(k):
            DesubBands[direction][i] = Quantizer.DeQuantization(DesubBands[direction][i], StepSize)

    ### 4.IDWT
    for i in range(k):
        D1 = upsamleVertical.upsampleVerticalLP(LL) 
        D2 = upsamleVertical.upsampleVerticalHP(DesubBands["LH"][i])
        D3 = upsamleVertical.upsampleVerticalLP(DesubBands["HL"][i]) 
        D4 = upsamleVertical.upsampleVerticalHP(DesubBands["HH"][i]) 
        C1 = symfilterH(D1, G0, 3)
        C2 = symfilterH(D2, G1, 5)
        C3 = symfilterH(D3, G0, 3)
        C4 = symfilterH(D4, G1, 5)

        W0 = upsamleHorizontal.upsampleHorizontalLP(C1+C2)
        W1 = upsamleHorizontal.upsampleHorizontalHP(C3+C4)

        Y0 = symfilterV(W0, G0, 3)
        Y1 = symfilterV(W1, G1, 5)
        Y = Y0 + Y1

        LL = Y

    return Y