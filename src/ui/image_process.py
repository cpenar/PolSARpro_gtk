#!/usr/bin/python3
# -*- coding: utf-8 -*-

import copy
import os

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

#from scipy import misc

import matplotlib
matplotlib.use('GTK3Agg')
import matplotlib.pyplot as plt

#from PIL.Image import open as imload
from matplotlib.image import imread as imload

from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as GtkFigureCanvas
#from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as GtkFigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as MplNavBar
#from matplotlib.backends.backend_gtk3agg import NavigationToolbar2GTK3agg as MplNavBar

from matplotlib.patches import Polygon


UI_FILE = __name__ + ".ui"

default_image_path = 'Images/PSPyoda.gif'
#default_image_path = '/home/nemosyne/work/PolSARpro/doc_n_data_set/SAN_FRANCISCO_ALOS/T3/PauliRGB.bmp'


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
        width, height, _ = self.image.shape
    
        fig, ax = plt.subplots()
        ax.imshow(self.image, origin='lower')
        #ax.get_xaxis().set_visible(False)
        #ax.get_yaxis().set_visible(False)
        #ax.set_axis_off()
        #ax.set_frame_on(False)
        #ax.set_xticks([]); ax.set_yticks([])
        #plt.axis('off')

        canvas = GtkFigureCanvas(fig)
        self.GtkSw.add_with_viewport(canvas)

        if width > max_width or height > max_height:
            # resize to max allowed size
            self.window.resize(max_width, max_height)
        else:
            self.window.resize(width, height)
            

        # MplNavBar

        toolbar = MplNavBar(canvas, self.window)
        box = self.builder.get_object('box1')
        box.pack_start(toolbar, False, True, 0)

        # window
        
        self.window.show_all()
        self.window.move(max_width + 200, 130)

        # testing polygon

        absices = np.random.random_integers(width, size=(5,))
        ordonnees = np.random.random_integers(height, size=(5,))
        points = np.stack((absices, ordonnees), axis=-1)

        Polygon(points)

        
        

    def on_rect_selection_button_clicked(self, widget, *args):
        pass
