import cv2
import sys
import os
import numpy as np
import skvideo.io

mouse_x = 0
mouse_y = 0
rect_w = 40
rect_h = 40
name = 'output'

GENERATE = 1

def MouseEvent(event, x, y, flags, param):
    global mouse_x,mouse_y
    mouse_x,mouse_y = x,y

cap = cv2.VideoCapture(name + '.mp4')
if not GENERATE:
    cv2.namedWindow('show')
outputfile = 'output_final.mp4'
writer = skvideo.io.FFmpegWriter(outputfile, outputdict={
  '-r': str(cap.get(cv2.CAP_PROP_FPS)),
  '-vcodec': 'libx264',  #use the h.264 codec
  '-crf': '0',           #set the constant rate factor to 0, which is lossless
  '-preset':'veryslow'   #the slower the better compression, in princple, try 
                         #other options see https://trac.ffmpeg.org/wiki/Encode/H.264
}) 

video_frames = []
while(1):
    _, raw_image = cap.read()
    if not _:
        break
    video_frames.append(raw_image)
record = np.load(name+'.npy')

i = 0
if not GENERATE:
    while(1):
        img = video_frames[i].copy()
        p1,p2,p3,p4 = record[i]
        if (p1 + p2 + p3 + p4) > 0:
            try:
                img[p2:p4,p1:p3] = cv2.imread('merged/%s_%d.png'%(name,i+100000))
            except:
                pass
        cv2.imshow('show',img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            np.save(name+'.npy', record)
            sys.exit(0)
        if key == ord('a'):
            i -= 1
            if i < 0:
                i = 0
        if key == ord('d'):
            i += 1
            if i > len(video_frames)-2:
                i = len(video_frames)-2
        if key == ord('j'):
            i -= 10
            if i < 0:
                i = 0
        if key == ord('l'):
            i += 10
            if i > len(video_frames)-2:
                i = len(video_frames)-2
if GENERATE:
    for i in range(len(video_frames)):
        img = video_frames[i]
        p1,p2,p3,p4 = record[i]
        try:
            img[p2:p4,p1:p3] = cv2.imread('merged/%s_%d.png'%(name,i+100000))
        except:
            pass
        writer.writeFrame(img[:,:,::-1])
        if i % 50 == 0:
            print('%7.2f%%'%(i*100.0/len(video_frames)))
writer.close() 
