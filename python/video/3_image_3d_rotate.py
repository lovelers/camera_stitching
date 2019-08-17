from image_transformer import ImageTransformer
from util import save_image
import sys
import os
import common
import numpy as np
import cv2

# Usage:
#     Change main function with ideal arguments
#     then
#     python demo.py [name of the image] [degree to rotate] ([ideal width] [ideal height])
#     e.g.,
#     python demo.py images/000001.jpg 360
#     python demo.py images/000001.jpg 45 500 700
#
# Parameters:
#     img_path  : the path of image that you want rotated
#     shape     : the ideal shape of input image, None for original size.
#     theta     : the rotation around the x axis
#     phi       : the rotation around the y axis
#     gamma     : the rotation around the z axis (basically a 2D rotation)
#     dx        : translation along the x axis
#     dy        : translation along the y axis
#     dz        : translation along the z axis (distance to the image)
#
# Output:
#     image     : the rotated image


# Input image path
img_root_path = common.rotate_3d_src

# Rotation range
rot_range = int(common.rotate_3d_angle)

# Make output dir
output  = common.rotate_3d_output

if not os.path.isdir(output):
    os.mkdir(output)


retval  = True
index   = 1

min_col = 0
min_row = 0
max_col = 0
max_row = 0
print(output)
while(retval):
    img_path    = img_root_path + 'video_%d.jpg'%index
    if os.path.isfile(img_path):
        it = ImageTransformer(img_path, None)
        rotated_img = it.rotate_along_axis(phi = rot_range, dx = 5)
        if index == 1:
            mat             = it.getTransfrom()
            width, height   = it.getImageSize()
            points          = np.array([[[width-1, 0], [width-1, height-1]]],dtype='float32')
            new_points      = cv2.perspectiveTransform(points, mat)
            print(new_points)
            min_col         = 0
            min_row         = new_points[0][0][1]
            max_col         = min(new_points[0][0][0], new_points[0][1][0])
            max_row         = new_points[0][1][1]

        save_image(output+'/video_%d.jpg'%index, rotated_img)
        print('save_image:%d'%index)
        index = index+1
    else:
        retval  = False

print('final crop region: ', min_col, min_row, max_col, max_row)
