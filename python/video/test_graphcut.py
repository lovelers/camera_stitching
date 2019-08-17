import cv2
import numpy as np
import common

img_left    = cv2.imread(common.overlap_output + 'left_1.jpg')
img_right   = cv2.imread(common.overlap_output + 'left_2.jpg')

print(type(img_left), type(img_right))

img_warped_f = []
img_warped_f.append(img_left.astype(np.float32))
img_warped_f.append(img_right.astype(np.float32))

corners = []
corners.append((10, 10))
corners.append((10, 10))

width       = img_left.shape[1]
height      = img_left.shape[0]
masks=[]
um=cv2.UMat(255*np.ones((img_left.shape[0],img_left.shape[1]),np.uint8))
masks.append(um)
um=cv2.UMat(255*np.ones((img_right.shape[0],img_right.shape[1]),np.uint8))
masks.append(um)

seam_finer  = cv2.detail_GraphCutSeamFinder("COST_COLOR")
seam_finer.find(img_warped_f, corners, masks)
cv2.imwrite("Mask1.jpg", masks[0])
cv2.imwrite("Mask2.jpg", masks[1])
