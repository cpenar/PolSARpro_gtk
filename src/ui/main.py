#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

#Comment the first line and uncomment the second before installing
#or making the tarball (alternatively, use project variables)
UI_FILE = "main.ui"

import sys
import os
from os.path import abspath

from pprint import pprint as pretty


class GUI:
    def __init__(self):
        # the state instance variable store all the datas
        # shared between differents parts of the application
        uiDir = abspath(__file__ + '/../')
        rootDir = abspath(uiDir + '/../../')

        # are we in windows msys2 environment ?
        win_prefix = ""
        try:
            if os.environ['OS'].startswith('Windows'):
                win_prefix = "C:/msys64"
        except:
            pass

        # env variable pointing to the root of a PolSARpro compiled version
        try:
            compiled_psp_path = os.environ["COMPILED_PSP_PATH"]
        except KeyError:
            print("ERROR: missing environment variable COMPILED_PSP_PATH.\n"
                  + "Necessary for Dev phase.\n"
                  + "Set COMPILED_PSP_PATH and relaunch the app, example :\n\n"
                  + "export COMPILED_PSP_PATH=/some/path/to/bleh")
            sys.exit(1)

        self.state = {
            'config': {
                'compiled_psp_path': compiled_psp_path,
                'localDir': uiDir,
                'rootDir': rootDir,
                'tempDir': win_prefix + '/tmp/PolSARpro',
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
            }
        }

        # buiding GTK ui and positiong main window
        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_FILE)
        self.builder.connect_signals(self)
        window = self.builder.get_object('main_menu_window')
        window.move(0, 0)
        window.show_all()

        # Storing the builder to pass to children
        self.state['GtkBuilder'] = self.builder

        # status window: resizing and positing
        status_window = self.builder.get_object('status_window')

        screen_height = Gdk.Screen.height()
        status_window_heigth = status_window.get_allocated_height()
        status_window.move(0, screen_height - status_window_heigth)
        status_window.set_size_request(Gdk.Screen.width(), 0)

        # Initialising tempDir
        self.initTempDIr()

        # TEST: adding stuff in buffer

        self.add_to_status_view('Initialisation')

    def initTempDIr(self):
        tempDir = self.state['config']['tempDir']

        if not os.path.exists(tempDir):
            os.makedirs(tempDir)

        if not os.access(tempDir, os.W_OK) or not os.path.isdir(tempDir):
            raise OSError(tempDir + ' should be a writeable directory')

    def add_to_status_view(self, text):
        status_view = self.builder.get_object('main_status_bar')
        status_buffer = status_view.get_buffer()

        status_buffer.set_text(
            status_buffer.get_text(
                status_buffer.get_start_iter(),
                status_buffer.get_end_iter(),
                False)
            + "\n" + text)

    def destroy(window, self):
        Gtk.main_quit()

    def open_window_from_widget_name(self, widget, *args):
        # one signal manager for all menu item signals.
        # py files MUST have same name than menu item widget.
        # allows them to be dynamically imported at runtime.

        # debug purpose
        print('\nState when entering ' + Gtk.Buildable.get_name(widget))
        pretty(self.state)

        ui = __import__(Gtk.Buildable.get_name(widget))
        ui.GUI(self.state)


def main(*args):
    GUI()
    Gtk.main()

if __name__ == "__main__":
    sys.exit(main())
