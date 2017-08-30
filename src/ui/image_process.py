#!/usr/bin/python3
# -*- coding: utf-8 -*-

import copy
import os

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

#from scipy import misc

import matplotlib as mpl
mpl.use('GTK3Agg')
import matplotlib.pyplot as plt

from PIL.Image import open as imload
#from matplotlib.image import imread as imload

from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as GtkFigureCanvas
#from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as GtkFigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as MplNavBar
#from matplotlib.backends.backend_gtk3agg import NavigationToolbar2GTK3agg as MplNavBar

from matplotlib.patches import Polygon


UI_FILE = __name__ + ".ui"

#default_image_path = 'Images/PSPyoda.gif'
#default_image_path = '/home/nemosyne/work/PolSARpro/doc_n_data_set/SAN_FRANCISCO_ALOS/T3/PauliRGB.bmp'
default_image_path = '/home/cpenar/work/PolSARpro/doc_n_data_set/SAN_FRANCISCO_ALOS/T3/PauliRGB.bmp'


class GUI:
    def __init__(self, state, image_file_path=None):
        # global app state
        self.globState = state
        # local config
        self.config = copy.deepcopy(state['config'])

        self.builder = state['GtkBuilder']
        self.builder.add_from_file(UI_FILE)
        self.builder.connect_signals(self)

        self.window = self.builder.get_object(__name__ + '_dialog')
        self.window.show_all()

        self.image_file_path = image_file_path
        self.init_image()

        self.polycollection = []
        self.currentpoly = []

    def init_image(self):

        imBox = self.builder.get_object('dialog-vbox1')
        if self.image_file_path is None:
            self.image_file_path = \
                default_image_path
                #self.config['localDir'] + '/' + default_image_path

        self.image = imload(self.image_file_path)
        
        max_width = Gdk.Screen.width() / 2 - 100
        max_height = Gdk.Screen.height() - 250

        #self.window.set_size_request(max_width, max_height)

        # Setting Gtk image
        
        self.GtkSw = self.builder.get_object('scrolledwindow_image')
        width, height = self.image.size

        params = mpl.figure.SubplotParams(left=0, bottom=0, right=1, top=1, wspace=0.1, hspace=0.1)
    
        self.fig, self.ax = plt.subplots(subplotpars=params)

        self.ax.set_axis_off()
        self.ax.imshow(self.image)

        self.canvas = GtkFigureCanvas(self.fig)
        self.GtkSw.add_with_viewport(self.canvas)

        if width > max_width or height > max_height:
            # resize to max allowed size
            self.window.resize(max_width, max_height)
        else:
            self.window.resize(width, height)
            

        # MplNavBar

        toolbar = MplNavBar(self.canvas, self.window)
        box = self.builder.get_object('box1')
        box.pack_start(toolbar, False, True, 0)

        # window
        
        self.window.show_all()
        self.window.move(max_width + 200, 130)

    def on_polygon_selection_button_clicked(self, widget, *args):
        self.cid = self.fig.canvas.mpl_connect(
            'button_press_event', 
            self.next_poly_coord)

    def next_poly_coord(self, event):
        if event.button!=1: return
        if (event.xdata is None): return

        print(event.xdata, event.ydata)
        print()
        self.currentpoly.append((event.xdata, event.ydata))

        if len(self.currentpoly) > 1:
            self.draw_poly_segment(self.currentpoly[-1], self.currentpoly[-2])

        if len(self.currentpoly) == 4:
            # we assume polygon is 4 points and segments
            # draw the last segment
            self.draw_poly_segment(self.currentpoly[-1], self.currentpoly[0])
            # disconnect event handler
            self.fig.canvas.mpl_disconnect(self.cid)
            # reset currentpoly
            self.currentpoly = []

    def draw_poly_segment(self, pt1, pt2):
        self.ax.plot([pt1[0], pt2[0]], [pt1[1], pt2[1]], linestyle='-', color='k')
        self.canvas.draw()

