#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, GdkPixbuf, Gdk
import os, sys, copy

UI_FILE = "single_data_set.ui"

# importing lib tools
from lib.colorMap import windowFromFile

class GUI:
    def __init__(self, state):
        # global app state
        self.globSt = state
        # local config
        self.config = copy.deepcopy(state['config'])

        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_FILE)
        self.builder.connect_signals(self)

        self.window = self.builder.get_object('single_data_set_window')
        self.window.show_all()

        fileChooser = self.builder.get_object('input_dir_file_chooser')
        fileChooser.set_current_folder(self.config['inputDir'])

    def selection_changed(self, widget, *args):
        self.config['inputDir'] = widget.get_filename()

    def supColorMap16(self, *args):
        mapFile = os.path.dirname(__file__) + '/ColorMap/Supervised_ColorMap16.pal'
        windowFromFile(mapFile, self)

    def save_and_exit(self, widget, *args):
        self.globSt['config'].update(self.config)
        self.window.destroy()

