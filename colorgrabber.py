import webcolors
import cv2
import numpy as np
from sklearn.cluster import KMeans
from tkinter import *
from tkinter import filedialog
import tempfile
import base64, zlib
import os
from PyInstaller.utils.hooks import collect_submodules

ICON = zlib.decompress(base64.b64decode('eJxjYGAEQgEBBiDJwZDBy'
    'sAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc='))

_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)

def color_grab(filename):
	img = cv2.imread(filename)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

	img = img.reshape((img.shape[0] * img.shape[1], 3))


	n_clusters = 5
	kmeans = KMeans(n_clusters)
	kmeans.fit(img)
	colors = kmeans.cluster_centers_
	labels = kmeans.labels_

	def closest_color(color):
	    min_colors = {}
	    for key, name in webcolors.css3_hex_to_names.items():
	        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
	        rd = (r_c - color[0]) ** 2
	        gd = (g_c - color[1]) ** 2
	        bd = (b_c - color[2]) ** 2
	        min_colors[(rd + gd + bd)] = name
	    return min_colors[min(min_colors.keys())]
			
	def get_color(color):
		try:
			closest_name = actual_name = webcolors.rgb_to_name(color)
		except:
			closest_name = closest_color(color)
			actual_name = None
		return actual_name, closest_name

	label_count = [0 for i in range(n_clusters)]
	for ele in labels:
		label_count[ele] += 1
	index_color = label_count.index(max(label_count))
	'''
	print
	for index, ele in enumerate(label_count):
		print(str(ele) + 'labels with pixel value ')
		print(colors[index])
		print('Percentage ' + str(float(ele)/len(labels)*100))
		print()
	'''
	#actual_name, closest_name = get_color(colors[index_color])

	color = (int(colors[index_color][0]), int(colors[index_color][1]), int(colors[index_color][2]))
	actual_name, closest_name = get_color(color)
	#print(f"Actual Name: {actual_name}\nClosest Name: {closest_name}")

	r = colors[index_color][0]
	g = colors[index_color][1]
	b = colors[index_color][2]

	image = np.zeros((100,100,3),np.uint8)
	for x in range(100):
		for y in range(100):
			image[x,y] = [b,g,r]

	cv2.imwrite('result.png', image)

	return closest_name

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)                 
        self.master = master
        self.init_window()

    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget      
        self.master.title("ColorGrabber")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating a button instance
        browseButton = Button(self, text="Choose Image", command=self.browse_files)

        # placing the button on my window
        browseButton.place(x=120, y=320)

    def browse_files(self): 
    	filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("PNG files", "*.png*"), ("all files", "*.*"))) 
    	color = color_grab(filename)
    	colorInfoLabel = Label(root, text=f"Closest name: {color}")
    	colorInfoLabel.place(x=100,y=220)
    	colorPhoto = PhotoImage(file="result.png")
    	os.remove("result.png")
    	colorPhotoLabel = Label(root,image=colorPhoto)
    	colorPhotoLabel.colorPhoto = colorPhoto
    	colorPhotoLabel.place(x=115,y=100)

root = Tk()
root.iconbitmap(default=ICON_PATH)
root.geometry("350x350")
app = Window(root)
root.mainloop()