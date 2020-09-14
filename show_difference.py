import cv2
capture = cv2.VideoCapture('ma.mp4')
capture2 = cv2.VideoCapture('./aaa.mp4')
while(1):
    ret,frame=capture.read()
    ret2,frame2=capture2.read()
    if ret==False or ret2 == False:
        print("Bad frame")
        break
    cv2.imshow('display',frame)
    cv2.imshow('display2',frame2)
    ret=cv2.waitKey(0)
    if ret==ord('q'): #esc
        break

