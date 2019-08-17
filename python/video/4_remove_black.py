import cv2
import numpy as np
import os
import common

retval          = True
index           = 1

output  = common.black_dir_output
if not os.path.isdir(output):
    os.mkdir(output)


while (True):
    img_path    = common.black_dir_src + 'video_%d.jpg'%index
    img = cv2.imread(img_path)
    if (type(img) == type(None)):
        break
    cv2.imwrite(output + '/video_%d.jpg'%index, img[0:common.black_height, 0:common.black_width, :])
    index = index+1
    print('save non_black. video_%d.jpg'%index)

