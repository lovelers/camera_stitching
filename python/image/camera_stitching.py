import calculate_stitching_fov as csf
import generate_stitching_matrix as gsm
import cv2
import numpy as np

if __name__ == '__main__':
    img1_path   = './left1.jpg'
    img2_path   = './right.jpg'
    fovr        = csf.calcFov()
    M, mask     = gsm.calcPerspectiveTransform(img1_path, img2_path, fovr)
    img1        = cv2.imread(img1_path)
    img2        = cv2.imread(img2_path)
    print('M', M)
    wrap        = cv2.warpPerspective(img2, M, (img1.shape[1] * 2 , img2.shape[0] * 2))
    wrap[0:img1.shape[0], 0:img1.shape[1]] = img1
    rows, cols = np.where(wrap[:,:,0] !=0)
    min_row, max_row = min(rows), max(rows) +1
    min_col, max_col = min(cols), max(cols) +1
    min_row = 290
    max_row = 3160
    result = wrap[min_row:max_row,min_col:max_col,:]#去除黑色无用部分

    cv2.imwrite('result.jpg',result)



