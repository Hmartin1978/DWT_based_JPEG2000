#coding=gbk
import numpy as np
from symfilterV import symfilterV
from symfilterH import symfilterH
from DownSamplingHorizontal import DownSamplingHorizontal
from DownSamplingVertical import DownSamplingVertical
import Quantizer
from collections import defaultdict
from RLEEncoder import RLE
from HuffmanEncode import HuffmanEncode
import package

H0 = [-1/8, 1/4, 3/4, 1/4, -1/8]
H1 = [-1/2, 1, -1/2]


def Encode(X0, k, StepSize):
    subBands = defaultdict(list)
    RootNode = defaultdict(list)
    Scale_Huffman = defaultdict(list)
    LenofHuffman = defaultdict(list)
    Scale_Binary = defaultdict(list)
    LenofBinary = defaultdict(list)

    ### 1.DWT
    for i in range(k):
        U0 = symfilterV(X0, H0, 5)
        U1 = symfilterV(X0, H1, 3)
        V0, V1 = DownSamplingHorizontal(U0, U1)
        B1 = symfilterH(V0, H0, 5)
        B2 = symfilterH(V0, H1, 3)
        B3 = symfilterH(V1, H0, 5)
        B4 = symfilterH(V1, H1, 3)

        LL, LH = DownSamplingVertical(B1, B2) 
        HL, HH = DownSamplingVertical(B3, B4) 

        X0 = LL
        subBands["HL"].insert(0, HL)
        subBands["LH"].insert(0, LH)
        subBands["HH"].insert(0, HH)

    ### 2.Quantization
    # for LL
    LL_Quantized = Quantizer.Quantization(LL, StepSize)
    # for subbands
    for direction in subBands.keys():
        for i in range(k):
            subBands[direction][i] = Quantizer.Quantization(subBands[direction][i], StepSize)
            # zero_cnt = np.where(subBands[direction][i], 0, 1)
            # print("percent of zero of {}'s {} scale is {:.1f}%".format(direction, i+1, 100 * np.sum(zero_cnt) / subBands[direction][i].size))

    ### 3.Encode(RLE&Huffman)
    # for LL
    LL_Symbol_seq, LL_Binary_seq = RLE(LL_Quantized, subBands, "LL", k) # img->RLE
    LL_HuffmanEncodedStream, RootNode["LL"] = HuffmanEncode(LL_Symbol_seq)
    LL_tobeTransmit = [LL_HuffmanEncodedStream, LL_Binary_seq] # ***noneed to transmit codebook(Root_Node)***
    # for subbands
    for direction in subBands.keys():
        Scale_Huffman[direction], RootNode[direction], LenofHuffman[direction], Scale_Binary[direction], LenofBinary[direction] = RLE(subBands[direction][0], subBands, direction, k)

    ### 4.Packing
    LLHuffmanLen, LLBinaryLen = package.PackingLL(LL_tobeTransmit)
    HuffmansubBandsLen, BinarysubBandsLen= package.PackingSubBands(Scale_Huffman, Scale_Binary, k)
    package.PackingRoot(RootNode)
    package.PackingLen(LenofHuffman, LenofBinary, LLHuffmanLen, LLBinaryLen, HuffmansubBandsLen, BinarysubBandsLen)