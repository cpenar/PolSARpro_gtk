#!/usr/bin/python3
# -*- coding: utf-8 -*-

import copy
import pprint as pp

from gi.repository import Gtk

# importing lib tools
from lib import colorMap

UI_FILE = "single_data_set.ui"


class GUI:
    def __init__(self, state):
        # global app state
        self.globState = state
        # local config
        self.config = copy.deepcopy(state['config'])

        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_FILE)
        self.builder.connect_signals(self)

        self.window = self.builder.get_object('single_data_set_dialog')
        self.window.show_all()

        self.fileChooser = self.builder.get_object('input_dir_file_chooser')
        self.fileChooser.set_current_folder(self.config['inputDir'])

        self.rows = self.config['displaySize']['rows']
        self.columns = self.config['displaySize']['columns']

        self.spinButtonRows = self.builder.get_object('spin_button_rows')
        self.spinButtonRows.set_value(self.rows)

        self.spinButtonColumns = self.builder.get_object('spin_button_columns')
        self.spinButtonColumns.set_value(self.columns)

    def selection_changed(self, widget, *args):
        self.config['inputDir'] = widget.get_filename()

    def window_color_map_from_widget_name(self, widget, *args):
        mapFile = self.config['colorMapDir']
        mapFile += Gtk.Buildable.get_name(widget) + '.pal'
        colorMap.GUI(mapFile)

    def value_changed_rows(self, widget, *args):
        self.rows = int(widget.get_value())

    def value_changed_columns(self, widget, *args):
        self.columns = int(widget.get_value())

    def update_rows_columns(self, widget, *args):
        pp.pprint(self.config)
        self.config['displaySize']['rows'] = self.rows
        self.config['displaySize']['columns'] = self.columns
        pp.pprint(self.config)

    def save_and_exit(self, widget, *args):
        pp.pprint(self.globState)
        self.globState['config'].update(self.config)
        pp.pprint(self.globState)
        self.window.destroy()
