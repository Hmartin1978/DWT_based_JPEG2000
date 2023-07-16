import numpy as np

def PSNR(img1, img2):
    mse = np.sum((img1 - img2) ** 2) / (float(img1.shape[1] * img1.shape[0]))
    # print("MSE = ",mse)
    if mse < 0.01:
        return 99
    psnr = 10 * np.log10(255 ** 2 / mse)

    return psnr