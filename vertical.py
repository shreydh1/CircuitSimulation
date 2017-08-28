from PIL import Image, ImageFont, ImageDraw, ImageTk
import os,fnmatch
import numpy as np
from resizeimage import resizeimage

import re

def convert(str):
    return int("".join(re.findall("\d*", str)))

img_list =[]
path=os.getcwd()+'/TestHor/'
for f in fnmatch.filter(os.listdir(path),'*.jpg'):
	print f
	img_list.append(f)
img_list.sort(key=convert)
print img_list
img_list2=[]

for x in img_list:
	img_list2.append(Image.open(os.path.join(path,x)))



min_shape = (600,200)   #sorted( [(np.sum(i.size), i.size ) for i in img_list])[0][1]
imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in img_list2 ) )
imgs_comb = Image.fromarray( imgs_comb)
imgs_comb.save( os.getcwd()+'/Test/Testyo.jpg' )
imgs_comb.show
print"Vertical Merge"

		
