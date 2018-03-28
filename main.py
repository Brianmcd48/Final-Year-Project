import tkinter as tk
from tkinter import *
from tkinter.ttk import Style

from PIL import ImageFont, ImageDraw, Image,  ImageTk

import matplotlib as mpl
mpl.use("TkAgg")
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib.backend_bases import cursors
import matplotlib.backends.backend_tkagg as tkagg
import numpy as np
import os
import sys
import string
import pickle
import textwrap


ttf = []
org = []
letter = 'a'
case="lower"

alpha=list(string.ascii_lowercase) +list(string.ascii_uppercase)


def letter_picker():
    global ttf, org

    for root, dirs, files in os.walk('test_data'):

        for file in files:

            if file.endswith(chr(97) + '.png'):
                ttf.append(file[0:file.__len__() - 12])
                org.append(file[0:file.__len__() - 12])

        org.sort(key=str.lower)

def plotter(canvas):
        print('test')
        fig = plt.figure()
        ax = fig.add_subplot(111)

        file = open(os.path.join("output_graphs", case + "_" + letter + ".txt"), "r")
        x, y = [], []
        for line in file:
            x.append(float(line.split(" ")[0]))
            y.append(float(line.split(" ")[1]))
        colors = cm.rainbow(np.linspace(0, 1, len(y)))
        ax.scatter(x, y, s=3, c=colors)
        canvas.figure=fig
        canvas.draw()

        #canvas = ResizingCanvas(myframe, width=850, height=400, bg="red", highlightthickness

        #a.plot(float(line.split(" ")[0]), float(line.split(" ")[1]), ".")

class Cursor:

    def __init__(self, ax, x, y):
        self.ax = ax
        self.lx = ax.axhline(color='k')  # the horiz line
        self.ly = ax.axvline(color='k')  # the vert line
        self.x = x
        self.y = y
        # text location in axes coords
       # self.txt = ax.text(0.7, 0.9, '', transform=ax.transAxes)

    def mouse_move(self, event, fig):
       try:
            if not event.inaxes:
                return

            x, y = event.xdata, event.ydata

            indx = np.searchsorted(self.x, [x])[0]

            x = self.x[indx]
            print(x)
            y = self.y[indx]
            print(y)
            # update the line positions
            self.lx.set_ydata(y)
            self.ly.set_xdata(x)
            #self.ax.show()
            #self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
            #print('x=%1.2f, y=%1.2f' % (x, y))
            fig.canvas.draw()
       except IndexError:
           return

class App:
    def __init__(self, master):

        self.master=master
        self.master.title("Font Select")

        frame = tk.Frame(self.master)
        frame.grid(row=0, column=0)
        letter_picker()

        #fig = pickle.load(open('pickle_graphs/'+case+'_'+letter+'.pickle', 'rb'))

        #AxesSubplot(0.125,0.11;0.775x0.77)
        fig=plt.figure()
        ax=fig.add_subplot(111)


        file = open(os.path.join("output_graphs", case + "_" + letter + ".txt"), "r")

        x, y = [], []
        for line in file:

            x.append(float(line.split(" ")[0]))
            y.append(float(line.split(" ")[1]))

        colors = cm.rainbow(np.linspace(0, 1, len(y)))
        ax.scatter(x, y,s=3,  c=colors)

        cursor = Cursor(ax, x, y)
        move= lambda e:cursor.mouse_move

        printer=lambda self, event, e: cursor.mouse_move(self, event,)
        canvas = FigureCanvasTkAgg(fig, master=master)

        canvas.get_tk_widget().grid(row=0, column=0,  columnspan=3, sticky=N+S+E+W )
        canvas.mpl_connect('button_press_event', lambda event, arg=cursor: cursor.mouse_move(event, fig))

        # variable = StringVar(master)
        # variable.set(alpha[0])  # default value
        # om = tk.OptionMenu(master, variable, *alpha, command=lambda value, name=OptionMenu: update(value, canvas))
        # om.bind("<ButtonRelease-1>", lambda name=canvas: plotter(om, canvas) )
        # om.grid(row=1, column=0, sticky=W, padx= 200)


        Label(master, text="Select Letter:").grid(row=1, column=0, sticky=E)
        listbox = Listbox(master)
        listbox.config(width=10, justify='center')

        for item in alpha:
            listbox.insert(END, item)
        listbox.select_set(0)
        self.check=lambda e: update(listbox.get(listbox.curselection()), canvas)
        listbox.bind('<<ListboxSelect>>', self.check)
        listbox.grid(row=2, column=0, sticky=N + E)


        label_font = Label(master, text="Select Font:").grid(row=1, column=1, )
        listbox2 = Listbox(master)
        listbox2.grid(row=2, column=1, sticky=N, )
        for item in org:
            listbox2.insert(END, item)

        label=Label(master, text="TEST")
        photo = ImageTk.PhotoImage(get_font(0))

        label = Label(master, image=photo)
        label.image=photo
        label.grid(row=1, column=2, rowspan=2, sticky=N+S+W )

    def mouse_move(self, event):

        if not event.inaxes:
            print("test")
            return

        x, y = event.xdata, event.ydata

        indx = np.searchsorted(self.x, [x])[0]
        x = self.x[indx]
        y = self.y[indx]
        # update the line positions
        self.lx.set_ydata(y)
        self.ly.set_xdata(x)

        #self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
        print('x=%1.2f, y=%1.2f' % (x, y))
        plt.draw()


def get_font(value):
    font = ImageFont.truetype(os.path.join('fonts', org[int(value)] + '.ttf'), 100)
    im = Image.new("RGBA", (600, 200), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    draw.text((10, 10), 'Aa,Bb,Cc,Dd', (0, 0, 0), font=font,)



    return im

def update(value, canvas):

    global case,letter
    print(value)
    letter=value
    print(ord(letter))
    if ord(letter)>=97:
        case='lower'
    else:
        case='upper'
    plotter(canvas)
   # print(self.fig)

def main():
    root= tk.Tk()
    #root.geometry("800x1000")
   # root.overrideredirect(True)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_rowconfigure(0, weight=10)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=6)

    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.focus_set()  # <-- move focus to this widget
    root.bind("<Escape>", lambda e: root.quit())
    root.minsize(root.winfo_screenwidth(), root.winfo_screenheight()-int(root.winfo_screenheight()/10))
    App(root)

    root.mainloop()

if __name__ == '__main__':
    main()
    print('test')
   # sys.exit()
#fix window closing issue
#fix issue with random graph appearing