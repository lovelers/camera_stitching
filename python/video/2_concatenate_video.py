import cv2
import numpy as np
import os
import common

#delta 11
index_left      = common.concatenate_left
index_right     = common.concatenate_right
index_output    = 1

retval = True

output  = common.concatenate_output
if not os.path.isdir(output):
    os.mkdir(output)

while(retval):
    img_left    = cv2.imread(common.concatenate_input1 + 'video_%d.jpg'%index_left)
    img_right   = cv2.imread(common.concatenate_input2 + 'video_%d.jpg'%index_right)
    if type(img_left) == type(None) or type(img_right) == type(None):
        print('concatenate done')
        retval  = False
    else:
        dst = np.concatenate((img_left, img_right), axis = 1)
        cv2.imwrite(output + 'video_%d.jpg'%index_output, dst)
        index_left      = index_left+1
        index_right     = index_right+1
        index_output    = index_output+1
        print(index_left, index_right, index_output)

