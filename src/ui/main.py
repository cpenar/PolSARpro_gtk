#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, GdkPixbuf, Gdk

#Comment the first line and uncomment the second before installing
#or making the tarball (alternatively, use project variables)
UI_FILE = "main.ui"
#UI_FILE = "/usr/local/share/example_use_glade_anjuta/ui/example_use_glade_anjuta.ui"

import sys, os

class GUI:
   def __init__(self):
      # the state instance variable store all the datas
      # shared between differents parts of the application
      self.state = { 'config': {
          'rootDir': os.path.abspath(__file__ + '/../../../'),
          'inputDir': os.path.abspath(__file__ + '/../../../'),
          'displaySize': { 'rows': 934, 'colums': 934 },
          } 
      }
              
      print(self.state)
      
      # buiding GTK ui
      self.builder = Gtk.Builder()
      self.builder.add_from_file(UI_FILE)
      self.builder.connect_signals(self)
      window = self.builder.get_object('main_menu_window')
      window.show_all()

   def destroy(window, self):
      Gtk.main_quit()

   def open_window(self, widget, *args):
      # one signal manager for all menu item signals.
      # py files MUST have same name than menu item widget.
      # allows them to be dynamically imported at runtime.
      ui = __import__(Gtk.Buildable.get_name(widget))
      ui.GUI(self.state)

def main(*args):
   app = GUI()
   Gtk.main()

if __name__ == "__main__":
   sys.exit(main())

