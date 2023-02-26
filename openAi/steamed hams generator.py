'''
Program to deconstruct video and reconstruct it with every image replaced by a variation of itself
'''
#importing a bunch of modules
import os
import openai
from PIL import Image
import requests
from io import BytesIO
import cv2
import time
import glob
import numpy as np
import imageio.v2 as imageio
import re

#set this to the api key for your open ai account
openai.api_key = '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'

#STAGE 1:   converts video to a png sequence
currentFrame = 0
frameRate = 15

cam = cv2.VideoCapture("./SteamedHams.mp4")

while True:
    for i in range(int(60/frameRate)):
        ret,frame = cam.read()
    
    if ret:# and currentFrame<250:
        name = "./images_orig/"+str(currentFrame)+".png"
        print("image no. " + str(currentFrame))
        #cv2.imwrite(name, frame) #uncomment this line to enable the desconstruction of the video (i only needed to do this once)
        currentFrame += 1
    else:
        break;
cam.release()
cv2.destroyAllWindows()

#STAGE 2:   sending each image to the API
imagesTot = currentFrame-1
for i in range(imagesTot):
    print("image gen: " + str(i))
    time.sleep(0.025) #just in case i overwhelmed the API and got timed out
    
    #OPENAI model call
    response = openai.Image.create_variation(
      image=open("./images_orig/"+str(i)+".png", "rb"),
      n=1,
      size="256x256"
    )
    image_url = response['data'][0]['url']
    imageData = requests.get(image_url)
    img = Image.open(BytesIO(imageData.content))
    img.save("./images_gen/img"+str(i)+".png","PNG")


#STAGE 3:   rewrite files to video
writer = imageio.get_writer('output.mp4', fps=frameRate/2)
files = glob.glob('./images_gen/*.png')
files.sort(key=lambda x:[int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x)])

for file in files:
    im = imageio.imread(file)
    writer.append_data(im)
writer.close()

