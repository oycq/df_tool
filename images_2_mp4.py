import cv2
import glob
import skvideo.io
images_names = glob.glob('output/*.png')
images_names.sort()
images_list = []
outputfile = 'output.mp4'
writer = skvideo.io.FFmpegWriter(outputfile, outputdict={

  '-vcodec': 'libx264',  #use the h.264 codec
  '-crf': '0',           #set the constant rate factor to 0, which is lossless
  '-preset':'veryslow'   #the slower the better compression, in princple, try 
                         #other options see https://trac.ffmpeg.org/wiki/Encode/H.264
}) 
for item in images_names:
    item = cv2.imread(item)
    images_list.append(item)
max_shape = 100
for img in images_list:
    if img.shape[0] > max_shape:
        max_shape = img.shape[0]
for i in range(len(images_list)):
    images_list[i] = cv2.resize(images_list[i],(max_shape,max_shape))
    frame = images_list[i][:,:,::-1]
    writer.writeFrame(frame)

writer.close() 

