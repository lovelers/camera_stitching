import os
import cv2
import numpy as np
import common


video   = cv2.VideoWriter(common.video_output_path,
        common.video_fourcc,
        common.video_framerate,
        common.video_output_size)
retval			= True
output_index	= 1
while(retval):
    img = cv2.imread(common.video_output_src + 'video_%d.jpg'%output_index)
    if(type(img) == type(None)):
        break
    else:
        video.write(img)
        output_index    = output_index + 1
        print('encoding : %d'%output_index)

    #if output_index == 441:
    #    break;

video.release()
cv2.destroyAllWindows()
print('endocing done:' + common.video_output_path)
