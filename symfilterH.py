#coding=gbk
import numpy as np

def symfilterH(X, H, k):
    k_temp = k // 2 
    X_copy = X
    X_copy = np.transpose(X_copy)
    result = np.zeros_like(X_copy, dtype=np.float32)

    if(len(X) == 1): 
        return X
    else: 
        for row, data in enumerate(X_copy):
            # ��ֱ�����һ������Ϊnp��֯����������������֯����Ԫ�ؼ�����������Ҫ��ת�ã��൱��������ת��Ϊ������������������ʽ���˲������
            # ȡ��ת�ú��ÿһ�У�����Ԫ�ز�ֱ�Ӽ���
            data = data.tolist()
            for num in range(0, k_temp):
                data.insert(0, X[num+1][row])
                data.append(X[len(X)-(num+2)][row])
            data = np.array(data, dtype=float)
            for col in range(len(data) - (k-1)):
                value = np.dot(data[col:col+k], H)
                result[row][col] = value
        result = np.transpose(result)

        return result