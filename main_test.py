import unittest

import main
import tkinter as tk
from tkinter import *

import os
from matplotlib import pyplot as plt
import numpy as np

class TestStringMethods(unittest.TestCase):

    def test_org_fill(self):
        alpha = []

        main.org_fill(alpha)

        if alpha == []:
            unittest.fail("should not be empty")
        else:
            pass

    def test_get_font(self):
        alpha=[]
        main.org_fill(alpha)
        main.get_font('5', alpha)

    def test_get_label(self):
        alpha = []
        main.org_fill(alpha)
        display = Label(text="test")
        label = Label(text="")
        main.get_label(5, display, label, alpha)

    def test_Cursor(self):
        x, y = [], []
        file = open(os.path.join("output_graphs","lower_a.txt"), "r")
        for line in file:
            x.append(float(line.split(" ")[0]))
            y.append(float(line.split(" ")[1]))
        file.close()
        fig = plt.figure()
        ax = fig.add_subplot(111)


        main.Cursor( ax, x, y)



    def test_Curosr_location(self):
        main.nodes=[[0,0]]
        main.org=['ABeeZee-italic']
        display = Label(text="test")
        label = Label(text="")
        x, y = [], []
        file = open(os.path.join("output_graphs","lower_a.txt"), "r")
        for line in file:
            x.append(float(line.split(" ")[0]))
            y.append(float(line.split(" ")[1]))
        file.close()
        fig = plt.figure()
        ax = fig.add_subplot(111)

        self.lx = ax.axhline(color='k')  # the horiz line
        self.ly = ax.axvline(color='k')  # the vert line

        main.Cursor(ax, x, y)

        main.Cursor.set_location(self, 0, label, display, fig)

    def test_Curosor_mouse(self):
        main.nodes = [[0, 0]]
        main.org = ['ABeeZee-italic']
        display = Label(text="test")
        label = Label(text="")
        x, y = [], []
        file = open(os.path.join("output_graphs", "lower_a.txt"), "r")
        for line in file:
            x.append(float(line.split(" ")[0]))
            y.append(float(line.split(" ")[1]))
        file.close()
        fig = plt.figure()
        ax = fig.add_subplot(111)

        self.lx = ax.axhline(color='k')  # the horiz line
        self.ly = ax.axvline(color='k')  # the vert line

        main.Cursor(ax, x, y)
        main.font_box=Listbox(exportselection=0)
        main.font_box.insert(END, main.org[0])
        main.font_box.select_set(0)

        class event(object):
            xdata=0
            ydata=0
            inaxes=True

        main.Cursor.mouse_move(self, event, fig, label, display)

    def test_plotter(self):
        main.nodes = [[0, 0]]
        main.org = ['ABeeZee-italic']
        display = Label(text="test")
        label = Label(text="")
        x, y = [], []
        file = open(os.path.join("output_graphs", "lower_a.txt"), "r")
        for line in file:
            x.append(float(line.split(" ")[0]))
            y.append(float(line.split(" ")[1]))
        file.close()
        fig = plt.figure()
        ax = fig.add_subplot(111)

        self.lx = ax.axhline(color='k')  # the horiz line
        self.ly = ax.axvline(color='k')  # the vert line

        main.Cursor(ax, x, y)
        root = tk.Tk()
        main.App.plotter(self, root, label, display, True)



if __name__ == '__main__':
    unittest.main()

