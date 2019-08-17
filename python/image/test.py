import cv2
import numpy as np

#left.jpg
img = cv2.imread('left.jpg')
img = cv2.copyMakeBorder(img, 800, 800, 800, 800, cv2.BORDER_CONSTANT, 0)
w,h = img.shape[0:2]

w_offset = -800
h_offset = -800
print('w',w, 'h', h)
org = np.array([[0, 0],[w, 0],[0, h],[w, h]], np.float32)
dst = np.array([[w_offset, h_offset], [w, 0],[w_offset, h - h_offset], [w, h]], np.float32)


warpR = cv2.getPerspectiveTransform(org, dst)

print('warpR', warpR)

result = cv2.warpPerspective(img, warpR, (h, w))
cv2.imwrite('left_1.jpg', result)



#right.jpg
img = cv2.imread('right.jpg')
img = cv2.copyMakeBorder(img, 1400, 1400, 1400, 1400, cv2.BORDER_CONSTANT, 0)
w,h = img.shape[0:2]

w_end = w+1400
h_end = h+1400
print('w',w, 'h', h)
org = np.array([[0, 0],[w, 0],[0, h],[w, h]], np.float32)
dst = np.array([[0, 0], [w_end, -1400],[0, h], [w_end, h_end]], np.float32)


warpR = cv2.getPerspectiveTransform(org, dst)

print('warpR', warpR)

result = cv2.warpPerspective(img, warpR, (h, w))
cv2.imwrite('right_1.jpg', result)

###
img1=cv2.imread('left_1.jpg')
img2=cv2.imread('right_1.jpg')

gray1=cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
gray2=cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
orb=cv2.ORB_create()
kp1,des1=orb.detectAndCompute(gray1,None)
kp2,des2=orb.detectAndCompute(gray2,None)
bf=cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)
matches=bf.match(des1,des2)
matches=sorted(matches,key=lambda x:x.distance)
img3=cv2.drawMatches(gray1,kp1,gray2,kp2,matches[:23],gray2,flags=2)
cv2.imwrite('stitching.jpg', img3)

