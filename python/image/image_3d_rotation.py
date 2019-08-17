import numpy as np
import cv2
import math


def getM(alpha, beta, gamma):
    matrix = np.zeros((3,3), dtype=np.float32)

    matrix[0][0]    = math.cos(beta) * math.cos(gamma)
    matrix[0][1]    = math.cos(beta) * math.sin(gamma)
    matrix[0][2]    = -math.sin(beta)

    matrix[1][0]    = math.sin(alpha) * math.sin(beta) * math.cos(gamma) - math.cos(alpha) * math.sin(gamma)
    matrix[1][1]    = math.sin(alpha) * math.sin(beta) * math.sin(gamma) + math.cos(alpha) * math.cos(gamma)
    matrix[1][2]    = math.sin(alpha) * math.cos(beta)

    matrix[2][0]    = math.cos(alpha) * math.sin(beta) * math.cos(gamma) + math.sin(alpha) * math.sin(gamma)
    matrix[2][1]    = math.cos(alpha) * math.sin(beta) * math.sin(gamma) - math.sin(alpha) * math.cos(gamma)
    matrix[2][2]    = math.cos(alpha) * math.cos(beta)
    return matrix

if __name__ == '__main__':
    img_path    = 'left.jpg'

    alpha       = 0
    beta        = math.pi / 3
    gamma       = 0

    M                   = getM(alpha, beta, gamma)
    #M                   = np.float32(M).reshape(-1, 1, 2)
    retval, invertM     = cv2.invert(M, cv2.DECOMP_SVD)
    print("M", M, "invertM", invertM)

    img         = cv2.imread(img_path)

    result      = cv2.warpPerspective(img, invertM, (img.shape[1], img.shape[0]))

    cv2.imwrite('rotaion.jpg', result)




