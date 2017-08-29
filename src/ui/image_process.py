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
    
        fig, ax = plt.subplots(subplotpars=params)

        ax.set_axis_off()
        #ax.xaxis.set_visible(False)
        #ax.yaxis.set_visible(False)
        ax.imshow(self.image, origin='lower')

        # Trying to add a polygon with alpha

        polycoords = [(360, 1610),
                (425, 1226),
                (724, 944),
                (1124, 1409)
                ]

        polygon = Polygon(polycoords, True, alpha=0.4)

        ax.add_patch(polygon)

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

        from gi.repository import GLib
        def del_poly():
            polygon.remove()

        GLib.timeout_add(1000, del_poly)


    def on_rect_selection_button_clicked(self, widget, *args):
        pass
