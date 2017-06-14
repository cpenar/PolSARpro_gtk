#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, GdkPixbuf, Gdk
import os, sys

#Comment the first line and uncomment the second before installing
#or making the tarball (alternatively, use project variables)
UI_FILE = "single_data_set.ui"
#UI_FILE = "/usr/local/share/example_use_glade_anjuta/ui/example_use_glade_anjuta.ui"

# importing lib tools
from lib.colorMap import windowFromFile

def openChild(root):
    root.builder.add_from_file(UI_FILE)
    window = root.builder.get_object('single_data_set_window')
    window.show_all()

class GUI:
    def __init__(self, root):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_FILE)
        self.builder.connect_signals(self)
        window = self.builder.get_object('single_data_set_window')
        window.show_all()

    def supColorMap16(self, *args):
        mapFile = os.path.dirname(__file__) + '/ColorMap/Supervised_ColorMap16.pal'
        windowFromFile(mapFile, self)

