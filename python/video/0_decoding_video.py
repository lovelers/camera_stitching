import cv2 as cv
import os
import common


if not os.path.isdir(common.video_output_left):
    os.mkdir(common.video_output_left)
if not os.path.isdir(common.video_output_right):
    os.mkdir(common.video_output_right)
#decode the left.mp4
cap0        = cv.VideoCapture(common.video_left)
print(cap0.isOpened())
success     = True
frame_count = 1
while(success):
    success, frame  = cap0.read()
    print ('read new frame, frame_count:', frame_count)
    if success == False:
        break

    params  =   []
    params.append(cv.IMWRITE_PXM_BINARY)
    cv.imwrite(common.video_output_left + 'video_%d.jpg'%frame_count, frame, params)
    frame_count = frame_count+1
cap0.release()

#decode the right.mp4
cap1        = cv.VideoCapture(common.video_right)
print(cap1.isOpened())
success     = True
frame_count = 1
while(success):
    success, frame  = cap1.read()
    print ('read new frame, frame_count:', frame_count)
    if success == False:
        break

    params  =   []
    params.append(cv.IMWRITE_PXM_BINARY)
    cv.imwrite(common.video_output_right + 'video_%d.jpg'%frame_count, frame, params)
    frame_count = frame_count+1


cap1.release()
