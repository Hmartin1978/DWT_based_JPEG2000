import matplotlib.pyplot as plt
import numpy as np
from PSNR import PSNR
import time
from Encoder import Encode
from Decoder import Decode


def main(k, StepSize):
    lena = np.fromfile('image1.512', dtype=np.uint8)
    lena = lena.reshape(512, 512)
    X = lena.copy().astype(np.float32)
    X0 = X

    start = time.time()

    Encode(X0, k, StepSize)
    result = Decode(k, StepSize)

    end = time.time()

    print("Total time is {:.5f}s".format(end - start))
    # plt.subplot(121), plt.imshow(X, 'gray', vmin=0, vmax=255), plt.xticks([]), plt.yticks([])
    # plt.subplot(122), plt.imshow(result, 'gray', vmin=0, vmax=255), plt.xticks([]), plt.yticks([])
    # plt.show()
    return PSNR(X, result)
    
    

if __name__ == "__main__":
    psnr1 = main(5, 8)
    print("PSNR = {:.5f}".format(psnr1))
    # psnr2 = main(5, 5)
    # psnr3 = main(5, 10)
    # psnr4 = main(5, 15)
    # psnr5 = main(5, 20)

    # x = [1, 5, 10, 15, 20]
    # y = [psnr1, psnr2, psnr3, psnr4, psnr5]
    # fig, ax = plt.subplots()
    # ax.plot(x,y)
    # ax.set_title("q-D")
    # ax.set_xlabel("q")
    # ax.set_ylabel("PSNR")

    # plt.show()
