#!/usr/bin/python3
# -*- coding: utf-8 -*-

import copy
import os

from gi.repository import Gtk, Gdk

from scipy import misc

import matplotlib.pyplot as plt

from PIL.Image import open as pilload

from matplotlib.image import imread as pltimread

#from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as GtkFigureCanvas
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as GtkFigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar

#from lib.convimage import ConvImage as CIm

UI_FILE = __name__ + ".ui"

#default_image_path = 'Images/PSPyoda.gif'
default_image_path = '/home/nemosyne/work/PolSARpro/doc_n_data_set/SAN_FRANCISCO_ALOS/T3/PauliRGB.bmp'


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

        self.image = pilload(self.image_file_path)
        
        max_width = Gdk.Screen.width() / 2 - 100
        max_height = Gdk.Screen.height() / 2 - 100

        #self.window.set_size_request(max_width, max_height)

        # Setting Gtk image
        
        self.GtkSw = self.builder.get_object('scrolledwindow_image')
        width, height = self.image.size
    
        fig, ax = plt.subplots()
        ax.imshow(self.image, origin='upper')

        canvas = GtkFigureCanvas(fig)
        self.GtkSw.add_with_viewport(canvas)

        if width > max_width or height > max_height:
            # resize to max allowed size
            self.window.resize(max_width, max_height)
        else:
            self.window.resize(width, height)
            
        self.window.show_all()

    def on_rect_selection_button_clicked(self, widget, *args):
        pass
