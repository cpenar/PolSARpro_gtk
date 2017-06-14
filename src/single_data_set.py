#!/usr/bin/python3
# vim: set et ts=4 sw=4: #
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# main.py
# Copyright (C) 2017 Carlos Penaranda <cpenar@MR032028>
# 
# example_use_glade_anjuta is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# example_use_glade_anjuta is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with thiprogram.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk, GdkPixbuf, Gdk
import os, sys

#Comment the first line and uncomment the second before installing
#or making the tarball (alternatively, use project variables)
UI_FILE = "single_data_set.ui"
#UI_FILE = "/usr/local/share/example_use_glade_anjuta/ui/example_use_glade_anjuta.ui"

# importing lib tools
from lib.colorMap import windowFromFile

class GUI:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_FILE)
        self.builder.connect_signals(self)
        window = self.builder.get_object('single_data_set_window')
        window.show_all()

    def destroy(window, self):
        Gtk.main_quit()

    def supColorMap16(self, *args):
        mapFile = os.path.dirname(__file__) + '/ColorMap/Supervised_ColorMap16.pal'
        windowFromFile(mapFile, self)


def main():
    app = GUI()
    Gtk.main()

if __name__ == "__main__":
    sys.exit(main())

