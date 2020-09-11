import cv2
import sys
import os
import numpy as np

mouse_x = 0
mouse_y = 0
rect_w = 50
rect_h = 50
name = '2'

GENERATE = 1

def MouseEvent(event, x, y, flags, param):
    global mouse_x,mouse_y
    mouse_x,mouse_y = x,y

cap = cv2.VideoCapture(name + '.mp4')
cv2.namedWindow('show')
cv2.setMouseCallback('show', MouseEvent)  

video_frames = []
while(1):
    _, raw_image = cap.read()
    if not _:
        break
    video_frames.append(raw_image)
if not os.path.isfile(name+'.npy'):
    record = np.zeros((len(video_frames),4),int)
    np.save(name+'.npy', record)
record = np.load(name+'.npy')


if GENERATE == 0:
    i = 0
    while(1):
        img = video_frames[i].copy()
        p1,p2,p3,p4 = record[i]
        cv2.rectangle(img, (p1,p2), (p3,p4), (0,255,0), 2)
        x,y = mouse_x - rect_w // 2, mouse_y - rect_h // 2
        cv2.rectangle(img, (x,y), (x+rect_w,y+rect_h), (255,0,0), 2)
        cv2.imshow('show',img)
        key = cv2.waitKey(1)
        if ord('0') < key <= ord('9'):
            rect_w = (key - ord('0')) * 50
            rect_h = (key - ord('0')) * 50
        if key == ord('q'):
            np.save(name+'.npy', record)
            sys.exit(0)
        if key == ord('k'):
            record[i] = 0,0,0,0
            i += 1
        if key == ord(' '):
            record[i] = x,y,x+rect_w,y+rect_h
            i += 1
        if key == ord('a'):
            i -= 1
            if i < 0:
                i = 0
        if key == ord('d'):
            i += 1
            if i > len(video_frames)-2:
                i = len(video_frames)-2

if GENERATE == 1:
    for i in range(len(video_frames)):
        img = video_frames[i]
        p1,p2,p3,p4 = record[i]
        if p1 + p2 + p3 + p4 == 0:
            continue
        p1 = max(0,p1)
        p2 = max(0,p2)
        face = img[p2:p4,p1:p3]
        cv2.imwrite('output/%s_%d.jpg'%(name,i+100000),face)
        if i % 200 == 0:
            print('%7.2f%%'%(i*100.0/len(video_frames)))
