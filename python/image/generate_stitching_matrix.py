import calculate_stitching_fov as csf
import find_corner_points as fcp
import cv2
import numpy as np

def calcPerspectiveTransform(left_image, right_image, fov_ratio):

    #left_points     = fcp.getCornerPoints(left_image, fov_ratio, 0)
    #right_points    = fcp.getCornerPoints(right_image, fov_ratio, 1)
    left_points     = np.array([[3195, 852], [3826, 845], [3238,3063], [3839, 3106]])
    right_points    = np.array([[300,  675], [1233, 785], [ 412,3321], [1285, 3157]])



    if len(left_points) == len(right_points):
        H, mask   = cv2.findHomography(np.float32(right_points).reshape(-1,1,2),
                np.float32(left_points).reshape(-1,1,2),
                cv2.RANSAC, 5.0)
    else:
        print('calibration failed, due to match the corner point failed')
    print('left_points', left_points, 'right_points', right_points)

    return H, mask


if __name__ == '__main__':
    left_image      = 'left.jpg'
    right_image     = 'right.jpg'

    fov_ratio       = csf.calcFov()
    H,mask          = calcPerspectiveTransform(left_image, right_image, fov_ratio)
    print("matrix", H)
