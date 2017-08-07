#!/usr/bin/python3
# -*- coding: utf-8 -*-

import copy

from gi.repository import Gtk

UI_FILE = __name__ + ".ui"


class GUI:
    def __init__(self, state, *image_file_path):
        print(image_file_path)
        # global app state
        self.globState = state
        # local config
        self.config = copy.deepcopy(state['config'])

        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_FILE)
        self.builder.connect_signals(self)

        self.window = self.builder.get_object(__name__ + '_dialog')
        self.window.show_all()

        if image_file_path:
           self.image = self.builder.get_object('image')
           self.image.set_from_file(image_file_path[0])
        
