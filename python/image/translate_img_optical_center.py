import cv2
import numpy as np

def getCorrectionImage(img, src_points, dst_point, width, height):
    matrix          = cv2.getPerspectiveTransform(src_points, dst_point)
    width,height    = img.shape[0:2]
    return cv2.warpPerspective(img, matrix, (height * 2, width * 2))

if __name__ == '__main__':
    img             = cv2.imread('left.jpg')
    width, height   = img.shape[0:2]
    src_points      = np.array([[0,0], [width-1, 0], [0, height-1], [width-1, height-1]], np.float32)
    #src_points      = np.array([[0,0], [height - 1, 0], [height-1, width-1], [0, width -1], np.float32)

    x_offset = -600
    y_offset = x_offset * 4 / 3;
    dst_points      = np.array([[x_offset, y_offset], [width-1, 0], [x_offset, height-1 -y_offset], [width-1, height-1]], np.float32)
    #dst_points      = np.array([y_offset, x_offset, [height -1 - y_offset,  x_offset
    new_img         = getCorrectionImage(img, src_points, dst_points, width - 2* x_offset, height - 2 * y_offset);
    print(len(new_img), len(new_img[0]))

    rows, cols = np.where(new_img[:,:,0] !=0)
    min_row, max_row = min(rows), max(rows) +1
    min_col, max_col = min(cols), max(cols) +1
    result = new_img[min_row:max_row,min_col:max_col,:]#去除黑色无用部分


    cv2.imwrite('left1.jpg', result)
