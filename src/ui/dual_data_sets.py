#!/usr/bin/python3
# -*- coding: utf-8 -*-

import copy

from gi.repository import Gtk

# importing lib tools
from lib import colorMap

UI_FILE = __name__ + ".ui"


class GUI:
    def __init__(self, state):
        # global app state
        self.globState = state
        # local config
        self.config = copy.deepcopy(state['config'])

        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_FILE)
        self.builder.connect_signals(self)

        self.window = self.builder.get_object(__name__ + '_dialog')
        self.window.show_all()

        self.rows = self.config[__name__]['displaySize']['rows']
        self.columns = self.config[__name__]['displaySize']['columns']

        self.spinButtonRows = self.builder.get_object('spin_button_rows')
        self.spinButtonRows.set_value(self.rows)

        self.spinButtonColumns = self.builder.get_object('spin_button_columns')
        self.spinButtonColumns.set_value(self.columns)

        self.masterFileChooser = self.builder.get_object(
            'input_master_dir_file_chooser')
        inputMasterDir = self.config[__name__]['inputMasterDir']
        self.masterFileChooser.set_current_folder(inputMasterDir)

        self.slaveFileChooser = self.builder.get_object(
            'input_slave_dir_file_chooser')
        inputSlaveDir = self.config[__name__]['inputSlaveDir']
        self.slaveFileChooser.set_current_folder(inputSlaveDir)

    def selection_changed(self, widget, *args):
        self.config[__name__]['inputDir'] = widget.get_filename()

    def window_color_map_from_widget_name(self, widget, *args):
        mapFile = self.config[__name__]['colorMapDir'] + '/'
        mapFile += Gtk.Buildable.get_name(widget) + '.pal'
        colorMap.GUI(mapFile)

    def value_changed_rows(self, widget, *args):
        self.rows = int(widget.get_value())

    def value_changed_columns(self, widget, *args):
        self.columns = int(widget.get_value())

    def update_rows_columns(self, widget, *args):
        self.config[__name__]['displaySize']['rows'] = self.rows
        self.config[__name__]['displaySize']['columns'] = self.columns

    def save_and_exit(self, widget, *args):
        self.globState['config'].update(self.config)
        self.window.destroy()
