import numpy as np
import imutils
import cv2
import common

ret             = True
frame_count     = 1
while(ret):
    path    = common.rotate_dir + 'video_%d.jpg'%frame_count
    img     = cv2.imread(path)
    if type(img) == type(None):
        ret = False
        break
    else:
        dst         = imutils.rotate(img, common.rotate_angle)
        cv2.imwrite(path, dst)
        frame_count = frame_count+1
        print('rotation for: %d'%frame_count)


