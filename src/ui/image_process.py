#!/usr/bin/python3
# -*- coding: utf-8 -*-

import copy
import os

from gi.repository import Gtk, Gdk
from PIL import Image

UI_FILE = __name__ + ".ui"

default_image = 'Images/PSPyoda.gif'


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
        # will use a pil thumbnail for the GtkImage

        # Setting pillow image
        if self.image_file_path is None:
            self.image_file_path = \
                self.config['localDir'] + '/' + default_image

        self.image =  Image.open(self.image_file_path)
        
        max_width = Gdk.Screen.width() / 2 - 100
        max_height = Gdk.Screen.height() / 2 - 100

        # Setting Gtk image

        self.GtkImage = self.builder.get_object('main_image')
        self.GtkImage_width, self.GtkImage_height = self.image.size
    
        self.thumb_path = self.config['tempDir'] + \
            os.path.basename(self.image_file_path)

        self.thumb = self.image.copy()

        if self.GtkImage_width > max_width and \
            self.GtkImage_height > max_height:

            # resize to max allowed size
            self.thumb.thumbnail(max_width, max_height)
    
        self.thumb.save(self.thumb_path)

        self.GtkImage.set_from_file(self.thumb_path)
        
    def on_rect_selection_button_clicked(self, widget, *args):
        pass
