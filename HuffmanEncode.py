#coding=gbk
import numpy as np
from queue import PriorityQueue
from collections import Counter

Huffman_Codebook = {} # 全局变量哈夫曼编码字典{key:code}

# 哈夫曼树的节点类
class HuffmanNode(object):
    def __init__(self, weight, key=None, symbol='', left_Child=None, right_Child=None):
        # 哈夫曼树的节点的初始化
        
        self.weight = weight # weight：权值，即频率
        self.key = key # key：叶子节点的元素
        self.left_Child = left_Child # left_Child：左子节点
        self.right_Child = right_Child # right_Child：右子节点
        if symbol != '':
            return False
        else:
            self.symbol = symbol # symbol：叶子节点的哈夫曼编码，初始化为空字符串


    def __ge__(self, other) -> bool:
        # 比较前一个HuffmanNode的weight值是否大于等于后一个
        return self.weight >= other.weight

    def __lt__(self, other) -> bool:
        # 比较前一个HuffmanNode的weight值是否小于后一个
        return self.weight < other.weight

def CreateHuffmanTree(file : dict) -> HuffmanNode:
    # 自底向上构建哈夫曼树
    # file：输入字典文件
    # HuffmanNode：哈夫曼树的root节点

    # 使用优先级队列方便进行频率权值的排序
    q = PriorityQueue()

    # 根据传入的键&值创建哈夫曼节点并存入队列
    for key, value in file: 
        # 存入哈夫曼树的叶子节点
        q.put(HuffmanNode(weight=value, key=key))

    # 进行判断，看当前队列是否到达root节点
    while q.qsize() > 1:
        # 取出队列中最小的两个节点(左子节点权值<右子节点权值)，同时将这两个节点从队列中剔除
        l_Node , r_Node = q.get(), q.get()
        # 由两个子节点创建父节点，对于父节点不赋予元素值
        Node = HuffmanNode(weight=l_Node.weight + r_Node.weight, left_Child=l_Node, right_Child=r_Node)
        # 然后将父节点存入队列，循环往复直至构建整个哈夫曼树
        q.put(Node)

    # 若当前队列只剩下root节点，则进行返回操作
    return q.get()

def TreeTraversal(root_Node, symbol=''):
    # 遍历哈夫曼树，获取每个叶子节点元素的哈夫曼编码，并进行保存
    # root_Node：哈夫曼树的根节点
    # symbol：对哈夫曼树进行递归时对其上所有节点进行编码，为'0'或'1'

    global Huffman_Codebook

    # 判断节点是否为HuffmanNode，因为叶子节点的子节点是None
    # "isinstance(a,b)"：若object a是class b的实例或子类的实例，返回True，否则为False
    if isinstance(root_Node, HuffmanNode):
        # 进行编码操作，改变每个子树根节点的哈夫曼编码
        root_Node.symbol += symbol
        # 判断是否到达叶子节点
        if root_Node.key != None:
            # 记录叶子节点的编码
            Huffman_Codebook[root_Node.key] = root_Node.symbol

        # 访问左子树，并在根节点基础上赋'0'
        TreeTraversal(root_Node.left_Child, symbol=root_Node.symbol + '0')
        # 访问右子树，并在根节点基础上赋'1'
        TreeTraversal(root_Node.right_Child, symbol=root_Node.symbol + '1')

def encoder(encoded_file:np.ndarray, codebook:dict):
    # endoded_file：原始文件数据
    # codebook：编码字典，dict={key:code}

    file_encode = ''
    for key in encoded_file:
        file_encode += codebook[key]
    return file_encode

def decoder(bitStream_encode:str, huffman_tree_root:HuffmanNode):
    # img_encode：哈夫曼编码数据，只包含"0"&"1"
    # huffman_tree_root：哈夫曼树根节点
    # return 原图像数据展开的向量
    bitStream_decode = []
    root_node = huffman_tree_root

    for code in bitStream_encode:
        # if current code is "0", go left tree
        if code == "0":
            root_node = root_node.left_Child
        # if current code is "1", go right tree
        elif code == "1":
            root_node = root_node.right_Child
        # only leaf's key is not None, determine whether current node is leaf
        if root_node.key != None:
            bitStream_decode.append(root_node.key) # if current node is leaf, record the key
            root_node = huffman_tree_root # access the leaf node, next iteration should start from root of tree

    bitStream_decode = "".join(bitStream_decode)
    return bitStream_decode

### Encoding
def HuffmanEncode(original_seq:str):
    # load file(SymbolStream)
    frequency_dict = Counter(original_seq).items()
    Huffman_root_Node = CreateHuffmanTree(frequency_dict)
    TreeTraversal(Huffman_root_Node)

    # SymbolStream -> HuffmanBitStream
    HuffmanBitStream = encoder(original_seq, Huffman_Codebook)

    return HuffmanBitStream, Huffman_root_Node
    
### Decoding
def HuffmanDecode(EncodedBitStream:str, Huffman_Root:HuffmanNode):
    HuffmanDecodeStream = decoder(EncodedBitStream, Huffman_Root)
    return HuffmanDecodeStream