import os
import zlib
import base64
import tempfile
import numpy as np
import webcolors
from sklearn.cluster import KMeans
import cv2
from PIL import Image, ImageTk, ImageGrab
from tkinter import Tk, Frame, Label, Button, BOTH, SUNKEN, filedialog

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb
    
def closest_color(color):
    min_colors = {}
    for hex_value, name in webcolors.names("css3").items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(hex_value)
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

def color_grab(filename):
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.reshape((img.shape[0] * img.shape[1], 3))

    n_clusters = 5
    kmeans = KMeans(n_clusters=n_clusters, n_init='auto')
    kmeans.fit(img)
    
    colors = kmeans.cluster_centers_
    labels = kmeans.labels_

    label_count = [0 for _ in range(n_clusters)]
    for ele in labels:
        label_count[ele] += 1
    
    dominant_idx = label_count.index(max(label_count))
    dominant_rgb = (int(colors[dominant_idx][0]), 
                    int(colors[dominant_idx][1]), 
                    int(colors[dominant_idx][2]))

    try:
        closest_name = webcolors.rgb_to_name(dominant_rgb)
    except ValueError:
        min_colors = {}
        for name in webcolors.names("css3"):
            hex_val = webcolors.name_to_hex(name)
            r_c, g_c, b_c = webcolors.hex_to_rgb(hex_val)
            
            rd = (r_c - dominant_rgb[0]) ** 2
            gd = (g_c - dominant_rgb[1]) ** 2
            bd = (b_c - dominant_rgb[2]) ** 2
            min_colors[(rd + gd + bd)] = name
            
        closest_name = min_colors[min(min_colors.keys())]

    return closest_name, dominant_rgb

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)                 
        self.master = master
        self.init_window()

    def init_window(self):     
        self.master.title("ColorGrabber")
        self.pack(fill=BOTH, expand=1)

        self.user_image_label = Label(self, text="No Image", bg="lightgrey")
        self.user_image_label.place(x=25, y=25, width=150, height=150)

        self.color_display_box = Frame(self, width=100, height=100, relief=SUNKEN, borderwidth=2)
        self.color_display_box.place(x=200, y=50)

        self.colorInfoLabel = Label(self, text="Select an image", font=("Arial", 10))
        self.colorInfoLabel.place(x=180, y=160)

        browseButton = Button(self, text="Choose Image", command=self.browse_files)
        browseButton.place(x=120, y=300)

    def browse_files(self): 
        filename = filedialog.askopenfilename(
            initialdir="/",
            title="Select a File",
            filetypes=(("Image files", "*.png *.jpg *.jpeg"), ("all files", "*.*"))
        ) 
        
        if filename:
            name, rgb = color_grab(filename)
            hex_color = '#%02x%02x%02x' % rgb
            
            img = Image.open(filename)
            img.thumbnail((150, 150))
            img_tk = ImageTk.PhotoImage(img)
            
            self.user_image_label.config(image=img_tk, text="")
            self.user_image_label.image = img_tk
            
            self.colorInfoLabel.config(text=f"Name: {name.capitalize()}\nHex: {hex_color.upper()}")
            self.color_display_box.config(bg=hex_color)

root = Tk()
root.geometry("350x350")
app = Window(root)
root.mainloop()
