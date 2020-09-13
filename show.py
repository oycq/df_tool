import cv2
capture = cv2.VideoCapture('ss.mp4')
while(1):
    ret,frame=capture.read()
    if ret==False:
        print("Bad frame")
        break
    cv2.imshow('display',frame)
    ret=cv2.waitKey(10)
    if ret==27: #esc
        break

