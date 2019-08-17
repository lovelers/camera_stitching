import cv2
import numpy as np

if __name__ == '__main__':
    img_path    ='./output/030.jpg'
    img         = cv2.imread(img_path)
    rows, cols = np.where(img[:,:,0] !=0)
    min_row, max_row = min(rows), max(rows) +1
    min_col, max_col = min(cols), max(cols) +1
    print(max_row, max_col)
    max_col    = max_col - 20
    result = img[min_row:max_row,min_col:max_col,:]#去除黑色无用部分
    cv2.imwrite('left1.jpg',result)



