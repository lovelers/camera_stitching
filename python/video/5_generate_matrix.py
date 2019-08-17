import cv2
import numpy as np
import os
import common

left_points     = common.left_points
right_points    = common.right_points
index_left      = common.concatenate_left
index_right     = common.concatenate_right
index_output    = 1

min_row         = common.perspective_min_row
max_row         = common.perspective_max_row
min_col         = common.perspective_min_col
max_col         = common.perspective_max_col

output          = common.perspective_output
overlap_output  = common.overlap_output

if not os.path.isdir(output):
    os.mkdir(output)

if not os.path.isdir(overlap_output):
    os.mkdir(overlap_output)

if len(left_points) == len(right_points):
    #warpR = cv2.getPerspectiveTransform(np.float32(left_points), np.float32(right_points))
    M, mask   = cv2.findHomography(np.float32(right_points).reshape(-1,1,2),
            np.float32(left_points).reshape(-1,1,2),
            cv2.RANSAC, 5.0)
else:
    print('calibration failed, due to match the corner point failed')
print('left_points', left_points, 'right_points', right_points)
print('M', M)


points          = np.array([[[0, 0], [0, common.video_size[1]-1]]],dtype='float32')
new_points      = cv2.perspectiveTransform(points, M)
print(new_points)
new_min_col     = min(new_points[0][0][0], new_points[0][1][0])
new_width       = int((new_min_col + (common.black_width - new_min_col) / 2) * 2)
new_hegiht      = common.video_size[1]

overlap_min_row = 0
overlap_max_row = common.video_size[1]
overlap_min_col = int(new_min_col)
overlap_max_col = common.black_width

retval = True
while (retval):
    img1_path   = common.perspective_input1 + 'video_%d.jpg'%index_left
    img2_path   = common.perspective_input2 + 'video_%d.jpg'%index_right

    img1        = cv2.imread(img1_path)
    img2        = cv2.imread(img2_path)

    if type(img1) == type(None) or type(img2) == type(None):
        print('process done')
        retval = False
    else:
        wrap            = cv2.warpPerspective(img2, M, (new_width , new_hegiht))
        overlap_left    = img1[overlap_min_row:overlap_max_row, overlap_min_col:overlap_max_col,:]
        overlap_right   = wrap[overlap_min_row:overlap_max_row, overlap_min_col:overlap_max_col,:]
        cv2.imwrite(overlap_output +'left_%d.jpg'%index_output, overlap_left)
        cv2.imwrite(overlap_output +'right_%d.jpg'%index_output, overlap_right)

        wrap[0:img1.shape[0], 0:img1.shape[1]] = img1
        result = wrap[min_row:max_row,min_col:max_col,:]#去除黑色无用部分
        cv2.imwrite(output + 'video_%d.jpg'%index_output,result)
        print('process left:%d'%index_left, 'right:%d'%index_right, 'output:%d'%index_output)
        index_left      = index_left+1
        index_right     = index_right+1
        index_output    = index_output+1
print('overlap:', overlap_min_row, overlap_max_row, overlap_min_col, overlap_max_col)
