#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PolSARpro GTK3 / PyGi UI start file
"""

from gi.repository import Gtk

#Comment the first line and uncomment the second before installing
#or making the tarball (alternatively, use project variables)
UI_FILE = "main.ui"

import sys
from os.path import abspath


class GUI:
    """
    The main window containing the menu
    """
    def __init__(self):
        """
        Init the store, later should read config from a file
        """
        # the state instance variable store all the datas
        # shared between differents parts of the application
        uiDir = abspath(__file__ + '/../')
        rootDir = abspath(uiDir + '/../../')

        self.state = {'config': {
            'localDir': uiDir,
            'rootDir': rootDir,
            'data_set_choosen': '',
            'single_data_set': {
                'rootDir': rootDir,
                'inputDir': rootDir,
                'colorMapDir': abspath(uiDir + '/ColorMap/'),
                'displaySize': {'rows': 934, 'columns': 934},
                },
            'dual_data_sets': {
                'inputMasterDir': rootDir,
                'inputSlaveDir': rootDir,
                'colorMapDir': abspath(uiDir + '/ColorMap/'),
                'displaySize': {'rows': 934, 'columns': 934},
                }
        }}

        # buiding GTK ui
        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_FILE)
        self.builder.connect_signals(self)
        window = self.builder.get_object('main_menu_window')
        window.move(0, 0)
        window.show_all()

    def destroy(window, self):
        Gtk.main_quit()

    def open_window_from_widget_name(self, widget, *args):
        """
        Signal manager for opening the window from the menu items.
        The py file of the window MUST have the same name than
        the menu item widget.
        The py and ui files are dunamically imported at runtime
        """
        ui = __import__(Gtk.Buildable.get_name(widget))
        ui.GUI(self.state)


def main(*args):
    GUI()
    Gtk.main()

if __name__ == "__main__":
    sys.exit(main())
