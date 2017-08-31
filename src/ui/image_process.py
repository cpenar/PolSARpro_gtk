#!/usr/bin/python3
# -*- coding: utf-8 -*-

import copy
import os

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

import numpy as np

import matplotlib as mpl
mpl.use('GTK3Cairo')
import matplotlib.pyplot as plt

from PIL import Image, ImageDraw
#from PIL.Image import open as imload
from matplotlib.image import imread as imload

from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as GtkFigureCanvas
#from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as GtkFigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as MplNavBar
#from matplotlib.backends.backend_gtk3agg import NavigationToolbar2GTK3agg as MplNavBar

from matplotlib.patches import Polygon


UI_FILE = __name__ + ".ui"

#default_image_path = 'Images/PSPyoda.gif'
#default_image_path = '/home/nemosyne/work/PolSARpro/doc_n_data_set/SAN_FRANCISCO_ALOS/T3/PauliRGB.bmp'
default_image_path = '/home/cpenar/work/PolSARpro/doc_n_data_set/SAN_FRANCISCO_ALOS/T3/PauliRGB.bmp'
test_mask_image_path = '/home/cpenar/work/PolSARpro/doc_n_data_set/SAN_FRANCISCO_ALOS/T3/mask_valid_pixels.bmp'


class GUI:
    def __init__(self, state, image_file_path=None, image=None):
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
        self.image = image

        self.polycollection = []
        self.currentpoly = []
        self.connect_ids = []
        self.temp_segments = []
        self.synchronized_axes = []

        self.init_image()

    def init_image(self):

        imBox = self.builder.get_object('dialog-vbox1')
        if self.image is None:
            if self.image_file_path is None:
                self.image_file_path = \
                    default_image_path
                   #self.config['localDir'] + '/' + default_image_path
            self.image = imload(self.image_file_path)[::-1]
        
        max_width = Gdk.Screen.width() / 2 - 100
        max_height = Gdk.Screen.height() - 250

        #self.window.set_size_request(max_width, max_height)

        # Setting Gtk image
        
        self.GtkSw = self.builder.get_object('scrolledwindow_image')
        width, height = self.image.shape[:2]

        self.axparams = mpl.figure.SubplotParams(
                left=0.03, bottom=0.03, right=0.97, top=0.97, 
                wspace=0.1, hspace=0.1)
    
        #self.fig, self.ax = plt.subplots(subplotpars=self.axparams)
        self.fig = plt.figure(subplotpars=self.axparams)
        self.ax = self.fig.add_subplot(121)
        self.synchronized_axes.append(self.ax)

        self.ax.set_axis_off()
        self.ax.imshow(self.image)

        # setting mask_valid_pixels

        self.mask_image = imload(test_mask_image_path)[::-1]

        self.axmask = self.fig.add_subplot(122)
        self.axmask.set_axis_off()
        self.axmask.imshow(self.mask_image)

        self.synchronized_axes.append(self.axmask)
        # mpl canvas for Gtk
        self.canvas = GtkFigureCanvas(self.fig)
        self.GtkSw.add_with_viewport(self.canvas)

        if width > max_width or height > max_height:
            # resize to max allowed size
            self.window.resize(max_width, max_height)
        else:
            self.window.resize(width, height)
            

        # Notify Statusbar when mouse move
        self.fig.canvas.mpl_connect(
            'motion_notify_event',
            self.image_value_to_statusbar
            )
        # MplNavBar

        toolbar = MplNavBar(self.canvas, self.window)
        box = self.builder.get_object('box1')
        box.pack_start(toolbar, False, True, 0)

        # window
        
        self.window.show_all()
        self.window.move(max_width + 200, 130)

    def image_value_to_statusbar(self, event):
        if (event.xdata is None): return
        x, y = int(event.ydata), int(event.xdata)

        statusbar = self.builder.get_object('statusbar1')
        statusbar.push(1, ' x=' + str(x) + '     y=' + str(y)
                + '     image_value=' + str(self.image[x,y])
                + '     mask_value=' + str(self.mask_image[x,y]))


    def on_polygon_selection_button_clicked(self, widget, *args):
        self.connect_ids.append(self.fig.canvas.mpl_connect(
            'button_press_event', 
            self.next_poly_coord))

        self.connect_ids.append(self.fig.canvas.mpl_connect(
            'motion_notify_event',
            self.draw_temp_segment
            ))

    def next_poly_coord(self, event):
        if not event.button in (1, 3): return
        if (event.xdata is None): return

        self.currentpoly.append((event.xdata, event.ydata))

        if len(self.currentpoly) > 1:
            self.draw_poly_segment(self.currentpoly[-1], self.currentpoly[-2])

        if event.button == 3:
            # last segment
            self.polycollection.append(self.currentpoly)
            # draw the last segment
            self.draw_poly_segment(self.currentpoly[-1], self.currentpoly[0])
            # disconnect event handlers
            while self.connect_ids:
                self.fig.canvas.mpl_disconnect(self.connect_ids.pop())
            # reset currentpoly
            self.currentpoly = []
        # refresh canvas
        self.canvas.draw()

    def draw_poly_segment(self, pt1, pt2, color='k'):
        return self.ax.plot(
                [pt1[0], pt2[0]],
                [pt1[1], pt2[1]],
                linestyle='-',
                color=color)

    def draw_temp_segment(self, event):
        if not event.inaxes: return
        # if first point nothing to do
        if not self.currentpoly: return

        # remove previous temp_segments
        while self.temp_segments:
            #self.temp_segments.pop().remove()
            lines = self.temp_segments.pop()
            while lines:
                self.ax.lines.remove(lines.pop())

        x, y = event.xdata, event.ydata
        self.temp_segments.append(
                self.draw_poly_segment(self.currentpoly[-1], (x, y))
                )

        # can we draw a temp closing segment ?
        if len(self.currentpoly) > 1:
            self.temp_segments.append(
                    self.draw_poly_segment(self.currentpoly[0], (x,y), color='w')
                    )

        # refresh canvas
        self.canvas.draw()

    def on_extract_selection_clicked(self, widget, *args):
        import json
        if not self.polycollection: 
            print('Create selection polygons first')
            return

        # save self.polycollection
        print('saving polygon selection in ' + 
            self.config['tempDir'] + '/training.json')
        with open(self.config['tempDir'] + '/training.json', 'w') as fp:
            json.dump(self.polycollection, fp)

        # open polygons in new window

        result = np.zeros_like(self.image)
        imgarray = np.array(self.image)
        imgmask = Image.new('L', self.image.shape[:2][::-1], False)
        for poly in self.polycollection:
            ImageDraw.Draw(imgmask).polygon(poly, outline=1, fill=True)
        mask = np.array(imgmask)[::-1]
        
        for index, istrue in np.ndenumerate(mask):
            if istrue: result[index] = imgarray[index]

        GUI(self.globState, image=result)

    def on_open_new_clicked(self, widget, *args):
        pass
