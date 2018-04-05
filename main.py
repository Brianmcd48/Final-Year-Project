import tkinter as tk
from tkinter import *
from tkinter.ttk import Style

from PIL import ImageFont, ImageDraw, Image,  ImageTk

import matplotlib as mpl
mpl.use("TkAgg")
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np
import os
import sys
import string
import pickle
import textwrap
import time



org = []
nodes=[]
current_select=0
fig=0
font_box=0

cursor=0
letter = 'a'
case="lower"
current_graph="output_graphs", case + "_" + letter + ".txt"



class Methods:
    def org_fill(self):
        global org

        for root, dirs, files in os.walk('test_data'):

            for file in files:

                if file.endswith(chr(97) + '.png'):

                    org.append(file[0:file.__len__() - 12])

            org.sort(key=str.lower)

    def get_font(self,value):
        font = ImageFont.truetype(os.path.join('fonts', org[int(value)] + '.ttf'), 100)
        W, H=700,200

        im = Image.new("RGBA", (W, H), (255, 255, 255))
        draw = ImageDraw.Draw(im)
        w,h = draw.textsize('Aa,Bb,Cc,Dd')

        draw.text((5, 0), 'Aa,Bb,Cc,Dd', (0, 0, 0), font=font,)

        return im

    def get_label(self, value, display, label):
        photo = ImageTk.PhotoImage(self.get_font(value))
        display.configure(text=org[value] + ":")
        label.configure(image=photo)
        label.image = photo



class Cursor:

    def __init__(self, ax, x, y):
        global nodes
        self.ax = ax
        self.lx = ax.axhline(color='k')  # the horiz line
        self.ly = ax.axvline(color='k')  # the vert line
        self.x = x
        self.y = y


    def set_location(self, value, label, display, fig):
        global current_select, nodes

        self.lx.set_ydata(nodes[value][1])
        self.ly.set_xdata(nodes[value][0])

        fig.canvas.draw()

        Methods.get_label(value, display, label)

        current_select=value

    def mouse_move(self, event, fig, label, display):
        global nodes, font_box

        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata

        nodes = np.asarray(nodes)

        dist_2 = np.sum((nodes - [x, y]) ** 2, axis=1)

        vector= dist_2[0]
        position=[nodes[0][0],nodes[0][1]]
        tracker=0

        for i in range(1, nodes.__len__()):
            if(vector>dist_2[i]):
                vector=dist_2[i]
                position=[nodes[i][0],nodes[i][1]]
                tracker=i

        self.lx.set_ydata(position[1])
        self.ly.set_xdata(position[0])

        fig.canvas.draw()

        font_box.select_set(tracker)

        font_box.yview(tracker)
        Methods.get_label(tracker, display, label)

######################################################################################
######################################################################################

class App:
    def __init__(self, master):
        global nodes, cursor, fig, font_box

        self.master=master
        self.master.title("Font Select")

        frame = tk.Frame(self.master)
        frame.grid(row=0, column=0)

        Methods.org_fill()



        ###########################################

        # displays font
        display = Label(master, text=org[0]+":")
        display.grid(row=1, column=3, sticky=S+W)
        photo = ImageTk.PhotoImage(Methods.get_font(0))
        label = Label(master, image=photo)
        label.image = photo
        label.grid(row=2, column=3, rowspan=1, columnspan=2, sticky=N + S + W)

        ###########################################

        #create and plot canvas
        self.plotter(master, label, display, True)

        ###########################################
        #creates box for selecting letter
        alpha = list(string.ascii_lowercase) + list(string.ascii_uppercase)

        Label(master, text="Select Letter:").grid(row=1, column=1, sticky=E)
        letter_box = Listbox(master, exportselection=0)
        letter_box.config(width=10, justify='center')

        for item in alpha:
            letter_box.insert(END, item)

        letter_box.select_set(0)

        letter_check = lambda e: self.update_letter(letter_box.get(letter_box.curselection()), master, label, display)
        letter_box.bind('<<ListboxSelect>>', letter_check)

        letter_box.grid(row=2, column=1, sticky=N + E)

        ###########################################

        # creates box for selecting font
        Label(master, text="Select Font:").grid(row=1, column=2)
        font_box = Listbox(master, exportselection=0)

        for item in org:
            font_box.insert(END, item)
        font_box.select_set(0)



        font_check = lambda e: cursor.set_location(int(font_box.curselection()[0]), label, display, fig)
        font_box.bind('<<ListboxSelect>>', font_check)

        font_box.grid(row=2, column=2, sticky=N)
        print(font_box)
######################################################################################
######################################################################################

    def plotter(self, master, label, display, start):

        global current_graph, nodes,cursor, fig
        if start is False:
            plt.close('all')

        fig = plt.figure()

        ax = fig.add_subplot(111)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        current_graph = "output_graphs", case + "_" + letter + ".txt"
        file = open(os.path.join("output_graphs", case + "_" + letter + ".txt"), "r")

        x, y = [], []
        for line in file:
            x.append(float(line.split(" ")[0]))
            y.append(float(line.split(" ")[1]))

        nodes = np.column_stack((x, y))

        colors = cm.rainbow(np.linspace(0, 1, len(y)))
        ax.scatter(x, y, s=3, c=colors)
        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.figure = fig
        canvas.draw()
        cursor = Cursor(ax, x, y)

        canvas.get_tk_widget().grid(row=0, column=0, columnspan=4, sticky=N + S + E + W)
        canvas.mpl_connect('button_press_event', lambda event, arg=cursor: cursor.mouse_move(event, fig, label, display))

        cursor.set_location(current_select, label, display, fig)



    def update_letter(self, value, master, label, display):

        global case, letter

        letter = value

        if ord(letter) >= 97:
            case = 'lower'
        else:
            case = 'upper'
        self.plotter( master, label, display,False)



def main():
    root= tk.Tk()
    #root.geometry("800x1000")
   # root.overrideredirect(True)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_columnconfigure(3, weight=1)
    root.grid_rowconfigure(0, weight=10)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=6)

    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.focus_set()  # <-- move focus to this widget
    root.bind("<Escape>", lambda e: root.quit())
  #  root.minsize(root.winfo_screenwidth(), root.winfo_screenheight()-int(root.winfo_screenheight()/10))
    App(root)
    root.protocol("WM_DELETE_WINDOW", lambda: root.quit())
    root.mainloop()

if __name__ == '__main__':
    main()
