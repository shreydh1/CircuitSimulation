
import re
from PIL import Image, ImageFont, ImageDraw, ImageTk
import os,fnmatch
import numpy as np
import glob
import shutil
import sys
import re

class merge():
	def __init__(self):
		self=[]
		pass
	counter = 0




	def oper(self, mylist):
		nlist = mylist[0]
		j=len(nlist)
		sym_list=[]
		inst_list=[]
		for i in range(0,j):
			x = nlist[i]
			s= x[x.find("[")+1:x.find("]")]				#item between the square brackets
			inst_list.append(s)							#this list is for instructions to be printed
			if x.startswith('('):
				sym_list.append(x[1:4])					#extracting symbols like XIC and XIO
			else:
				sym_list.append(x[0:3])					#everything else like OTE,AND,OR,TON


		nsym_list = sym_list.pop(0)					#removal of the first element 'rung'
		s_list = sym_list
		#print s_list
		s_list1 = s_list[0::2]						#this is for zipping and printing
		i_list=inst_list[1::2]						##this is for zipping and printing
		
		z = zip(s_list1,i_list)
		self.drawOn(s_list1, i_list)
		self.horMerge(s_list)							


	def drawOn(self, my_list, my_list1):					#method to write the addresses on symbols
		imgs =[]
		print"%d" %(self.counter),my_list
		#print"my list is", len(my_list)
		path = os.getcwd()+ '/otdir/Rungs/'+ 'Rung%s' %(self.counter)
		if not os.path.exists(path):
			os.makedirs(path)

		for x in range(len(my_list)):
			var = os.getcwd() + '/symbols/'+ my_list[x]+'.jpg'
			img = Image.open('%s'%(var), "r")

			
			size = width, height = img.size
			draw = ImageDraw.Draw(img)
		
			fonts_path = '/library/Fonts/Comic Sans MS.ttf'
			font = ImageFont.truetype(fonts_path, 22)
			
			if my_list[x].startswith('O'):
				draw.text((100, 60), my_list1[x] ,(0,0,0),font=font)
			else:
				draw.text((100, 16), my_list1[x] ,(0,0,0),font=font)
			
			imgs.append(img)

			#make new directory for every rung

			img.save( path +'/Test%s' %(x) + '.jpg' )
		
		self.counter+=1

	def horMerge(self, m_list):
		r_list=[]

		for i in range(0,len(m_list)):
			if m_list[i] == 'AND':
				m_list[i] = 'horline.jpg'
			if m_list[i] =='-->':
				m_list[i] = 'horline.jpg'
				#m_list.remove('OR')
			if m_list[i]=='OR':
				r_list=m_list
				
		#print "counter is ", self.counter
		c = self.counter -1
		

		if len(r_list)==0:
			
			img_list =[]
			for k in range (0, self.counter):
				path = os.getcwd()+'/otdir/Rungs/' + 'Rung%s'%(k)

				for f in fnmatch.filter(os.listdir(path),'*.jpg'):
					img_list.append(Image.open(os.path.join(path,f)))
				min_shape = (380,240)
				imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in img_list ) )

				# save the picture horizontally
				imgs_comb = Image.fromarray( imgs_comb)
				path2= os.getcwd()+'/otdir/Rungs/TestHores/'
				if not os.path.exists(path2):
					os.makedirs(path2)

				imgs_comb.save( path2+ 'Testhor%s' %(k) + '.jpg')

				imgs_comb=[]    
				img_list=[]

		else:
			new_list = filter(lambda x: x != 'horline.jpg', r_list)
			self.makeRect(new_list,c)

	_nsre = re.compile('([0-9]+)')

	def natural_sort_key(s):
    		return [int(text) if text.isdigit() else text.lower()
            	for text in re.split(_nsre, s)]   



	
	def verticalMerge(self):
		img_list =[]
		path=os.getcwd()+'/otdir/Rungs/TestHores/'
		a=0
		for x in fnmatch.filter(os.listdir(path),'*.jpg'):
			x=Image.open(os.path.join(path,x))
			size = width, height = x.size
			draw = ImageDraw.Draw(x)
		
			fonts_path = '/library/Fonts/Comic Sans MS.ttf'
			font = ImageFont.truetype(fonts_path, 18)
	
			draw.text((0,10), "Rung%s"%(a) ,(0,0,0),font=font)
			img_list.append(x)
			a+=1

		img_list.sort(key=self.natural_sort_key())
		print img_list


		min_shape =(600,200)  											
		#sorted( [(np.sum(i.size), i.size ) for i in img_list])[0][1]	#
		imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in img_list ) )
		imgs_comb = Image.fromarray(imgs_comb)
		path2=os.getcwd()+'/otdir/Rungs/OutputPic/'
		if not os.path.exists(path2):
			os.makedirs(path2)
		imgs_comb.save( path2 +'Test.jpg' )
		#print"Vertical Merge"



	def makeRect(self, r_list,c):
		#print 'list for rectangle',r_list
		
		image_list = []
		yourpath= os.getcwd()+"/otdir/Rungs/"+"Rung%s/"%(c)
		for filename in glob.glob(yourpath+'*.jpg'): #assuming jpg
		    im=Image.open(filename)
		    image_list.append(im)
		length_im=len(image_list)			
		im = Image.open("Rect.jpg")
		im=im.resize((400,200),Image.ANTIALIAS)
		rin = r_list.index('OR')
		

		#print "rin is ",rin

		#taking the index of OR and extracting the symbols
		
		list1=image_list[0:rin]
		list2=image_list[rin:(len(r_list)-2)]
		
		#print"list1 is:",len(list1)
		#print "list2 is:",len(list2)
		#the following code to paste the symbols to the rectangle
		
		l=105

		for i in range(0,len(list1)):
			k=list1[i]
			k=k.resize((70,70),Image.ANTIALIAS)
			d=im.paste(k,(l,7))
			l+=100


		
		l=105
		for j in range(0,len(list2)):
			k=list2[j]
			k=k.resize((70,70),Image.ANTIALIAS)
			d=im.paste(k, (l,120))
			l+=100	

		im.save("testMerge.jpg")
		t=image_list[length_im-1]
		t.save("zlast.jpg")						#output Rung image at the end 
		images = map(Image.open, ['testmerge.jpg','zlast.jpg'])
		widths, heights = zip(*(i.size for i in images))
		total_width = sum(widths)
		max_height = max(heights)



		new_im = Image.new('RGB', (total_width, max_height))
		x_offset = 0
		for im2 in images:

			  min_shape= (320,160)

			  im2 = im2.resize(min_shape)
			  new_im.paste(im2, (x_offset,0))
			  x_offset += im2.size[0]

		path =os.getcwd()+'/otdir/Rungs/Testhores/Test/'
		if not os.path.exists(path):
			os.makedirs(path)
		new_im.save( path +'Testhor%s' %(c) + '.jpg' )





def main():
	m = merge()
	arg=sys.argv[1]
	z = open(arg,'r+') 
	linelist =[]
	for word in z.readlines():                			#listing the lines of text file
			line = [x.strip() for x in word.split(" ") if x!= '' ]
			linelist.append(line)
	j=len(linelist)

	print "value of j is",j

	for i in range (0,j-1 ):
		 mylist = [linelist[i]]							#accessing line by line

		 m.oper(mylist)
	

		# mylist=[]
	z.close()
	path =os.getcwd() + '/otdir/Rungs/TestHores' 
	if not os.path.exists(path):
			os.makedirs(path)
	source= path+'/Test'
	if not os.path.exists(source):
			os.makedirs(source)
	files = os.listdir(source)

	for f in files:
	    shutil.move(os.path.join(source, f), os.path.join(path, f))

	m.verticalMerge()
	
	#Display window
	'''window = tk.Tk()

	window.title("Join")
	window.geometry("600x2400")
	window.configure(background='grey')

	ipath = os.getcwd()+'/otdir/Rungs/OutputPic/RungPic.jpg'
	
	#Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
	
	img = ImageTk.PhotoImage(Image.open(ipath))

	#The Label widget is a standard Tkinter widget used to display a text or image on the screen.
	panel = tk.Label(window, image = img)

	#The Pack geometry manager packs widgets in rows or columns.
	panel.pack(side = "bottom", fill = "both", expand = "yes")

	#Start the GUI
	window.mainloop()'''

if __name__=='__main__':


	main()	