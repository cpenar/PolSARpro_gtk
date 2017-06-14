#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, GdkPixbuf, Gdk

#Comment the first line and uncomment the second before installing
#or making the tarball (alternatively, use project variables)
UI_FILE = "main.ui"
#UI_FILE = "/usr/local/share/example_use_glade_anjuta/ui/example_use_glade_anjuta.ui"

import sys

class GUI:
   def __init__(self):
      self.builder = Gtk.Builder()
      self.builder.add_from_file(UI_FILE)
      self.builder.connect_signals(self)
      window = self.builder.get_object('main_menu_window')
      window.show_all()
      # the state instance variable store all the datas
      # shared between different part of the application
      self.state = {}

   def destroy(window, self):
      Gtk.main_quit()

   def open_window(self, widget, *args):
      # allows to have only one signal manager for all menu item signals
      # py files MUST have same name than menu item widget
      # and allows them to be dynamically imported at runtime
      ui = __import__(Gtk.Buildable.get_name(widget))
      ui.GUI(self)

def main(*args):
   app = GUI()
   Gtk.main()

if __name__ == "__main__":
   sys.exit(main())

