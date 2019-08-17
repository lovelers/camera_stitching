import cv2 as cv
import numpy as np

filename = 'chart.jpg'

bw_rows = 9;
bw_col  = 5;

bw_step = 100;

width   = bw_step * bw_col;
height  = bw_step * bw_rows;

img = np.zeros((width, height, 3), np.uint8)

print(width, 'x', height, ',step:', bw_step)
for h in range(height):
    flag_h  = int(h / bw_step)
    for w in range(width):
        flag_w  = int(w / bw_step)
        if flag_h % 2 == 0:
            if flag_w % 2 == 0:
                img[w][h] = [0, 0, 0]
            else:
                img[w][h] = [255, 255, 255]
        else:
            if flag_w % 2 == 0:
                img[w][h] = [255, 255, 255]
            else:
                img[w][h] = [0, 0, 0]

cv.imwrite(filename, img)





