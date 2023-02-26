'''
constructs the output video without any of the API calls etc
use this file when you make edits to any images
'''

import re

frameRate = 15 #play around with this, likely not accurate because i edited the speed in another software later anyway
import imageio.v2 as imageio
import glob

#rewrite files to video
writer = imageio.get_writer('output.mp4', fps=frameRate/4)
files = glob.glob('D:/openAi/images_gen/*.png')
files.sort(key=lambda x:[int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x)])

for i in range(len(files)):
    if i%2==0: #skips every other frame so it looks watchable
        im = imageio.imread(files[i])
        writer.append_data(im)
writer.close()
