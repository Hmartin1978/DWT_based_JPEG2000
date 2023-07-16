#coding=gbk
import numpy as np
import pickle
import struct
from collections import defaultdict

LLHuffman_path = "LLHuffman.bin"
LLBinary_path = "LLBinary.bin"

HuffmanStream_path = "SubBandsHuffman.bin"
BitStream_path = "SubBandsBitStream.bin"

Root_path = "HuffmanRoot.bin"
Len_path = "Len.bin"


def PackingLL(LLtobeTransmit:list):
    LLHuffman = LLtobeTransmit[0]
    LLBinary = LLtobeTransmit[1]
    LLHuffmanLen = len(LLHuffman)
    LLBinaryLen = len(LLBinary)

    with open(LLHuffman_path, 'wb') as f1:
    # 每8个bit组成一个byte
        for i in range(0, len(LLHuffman), 8):
            # 把这一个字节的数据根据二进制翻译为十进制的数字
            img_encode_dec = int(LLHuffman[i:i + 8], 2)
            # 把这一个字节的十进制数据打包为一个unsigned char
            img_encode_bin = struct.pack('>B', img_encode_dec)
            # 写入这一个字节数据
            f1.write(img_encode_bin)

    with open(LLBinary_path, 'wb') as f2:
        for i in range(0, len(LLBinary), 8):
            img_encode_dec = int(LLBinary[i:i + 8], 2)
            img_encode_bin = struct.pack('>B', img_encode_dec)
            f2.write(img_encode_bin)

    return LLHuffmanLen, LLBinaryLen

def PackingSubBands(scale_Huffman, scale_Binary, k):
    HuffmanToBeTransmit = []
    BinaryToBeTransmit = []
    
    for direction in scale_Huffman.keys():
        for i in range(k):
            HuffmanToBeTransmit += scale_Huffman[direction][i]
            BinaryToBeTransmit += scale_Binary[direction][i]

    HuffmanToBeTransmit = "".join(HuffmanToBeTransmit)
    BinaryToBeTransmit = "".join(BinaryToBeTransmit)
    LenSubBandHuffman = len(HuffmanToBeTransmit)
    LenSubBandBinary = len(BinaryToBeTransmit)

    with open(HuffmanStream_path, 'wb') as f1:
        for i in range(0, len(HuffmanToBeTransmit), 8):
            img_encode_dec = int(HuffmanToBeTransmit[i:i + 8], 2)
            img_encode_bin = struct.pack('>B', img_encode_dec)
            f1.write(img_encode_bin)

    with open(BitStream_path, 'wb') as f2:
        for i in range(0, len(BinaryToBeTransmit), 8):
            img_encode_dec = int(BinaryToBeTransmit[i:i + 8], 2)
            img_encode_bin = struct.pack('>B', img_encode_dec)
            f2.write(img_encode_bin)

    return LenSubBandHuffman, LenSubBandBinary

def PackingRoot(RootNode):
    with open(Root_path, "wb") as f:
        pickle.dump(RootNode, f)

def PackingLen(LenofHuffman, LenofBinary, LLHuffman, LLBinary, subBandsHuffman, subBandsBinary):
    data = (LenofHuffman, LenofBinary, LLHuffman, LLBinary, subBandsHuffman, subBandsBinary)
    with open(Len_path, "wb") as f:
        pickle.dump(data, f)


def UnPackingDecimal2Bin(BinFile:str, EncodeLen:int):
    '''
    从二进制的编码文件读取数据，得到原来的编码信息，为只包含'0'和'1'的字符串
    :param huffman_file: 保存的编码文件
    :param img_encode_len: 原始编码的长度，必须要给出，否则最后一个字节对不上
    :return: str, 只包含'0'和'1'的编码字符串
    '''
    code_bin_str = ""
    with open(BinFile, 'rb') as f:
        # 从文件读取二进制数据
        content = f.read()
        # 从二进制数据解包到十进制数据，所有数据组成的是tuple
        code_dec_tuple = struct.unpack('>' + 'B' * len(content), content)
        for code_dec in code_dec_tuple:
            # 通过bin把解压的十进制数据翻译为二进制的字符串，并填充为8位，否则会丢失高位的0
            # 0 -> bin() -> '0b0' -> [2:] -> '0' -> zfill(8) -> '00000000'
            code_bin_str += bin(code_dec)[2:].zfill(8)
        # 由于原始的编码最后可能不足8位，保存到一个字节的时候会在高位自动填充0，读取的时候需要去掉填充的0，否则读取出的编码会比原来的编码长
        # 计算读取的编码字符串与原始编码字符串长度的差，差出现在读取的编码字符串的最后一个字节，去掉高位的相应数量的0就可以
        len_diff = len(code_bin_str) - EncodeLen
        # 在读取的编码字符串最后8位去掉高位的多余的0
        code_bin_str = code_bin_str[:-8] + code_bin_str[-(8 - len_diff):]
    return code_bin_str

def UnPackingSubBands(LongHuffmanCode, Len, k):
    SubBands = defaultdict(list)
    start = 0
    for direction in Len.keys():
        for i in range(k):
            length = Len[direction][i]
            SubBands[direction].append(LongHuffmanCode[start:start+length])
            start = start+length

    return SubBands

def UnPacking(file_path):
    with open(file_path, "rb") as file:
        load_Data = pickle.load(file)

    return load_Data