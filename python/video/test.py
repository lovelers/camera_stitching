import cv2
video_full_path="test1.mp4"
cap  = cv2.VideoCapture(video_full_path)
print(cap.isOpened())
frame_count = 1
success = True
while(success):
    success, frame = cap.read()
    print ('Read a new frame: ', success)

    params  = []
    params.append(cv2.IMWRITE_PXM_BINARY)
    cv2.imwrite("video" + "_%d.jpg" % frame_count, frame, params)
    frame_count = frame_count + 1

