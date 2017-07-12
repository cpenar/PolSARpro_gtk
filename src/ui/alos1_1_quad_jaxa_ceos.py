#!/usr/bin/python3
# -*- coding: utf-8 -*-

import copy
import os

from gi.repository import Gtk

from time import strftime
from lib.tools import exec_bin

UI_FILE = __name__ + ".ui"


class GUI:
    def __init__(self, state):
        # local config, dont need
        # self.this_window_conf = {}

        # global app state
        self.globState = state

        # copy of global config
        self.config = copy.deepcopy(state['config'])

        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_FILE)
        self.builder.connect_signals(self)

        self.window = self.builder.get_object(__name__ + '_dialog')

        self.input_dir_entry = self.builder.get_object('input_dir_entry')
        self.input_dir_entry.set_text(
            self.config['single_data_set']['inputDir'])

        self.output_file_chooser = self.builder.get_object(
            'output_dir_file_chooser')
        self.output_file_chooser.set_filename(
            self.config['single_data_set']['inputDir'])

        self.sar_lead_chooser = self.builder.get_object(
            'sar_lead_file_chooser')
        self.sar_lead_chooser.set_current_folder(
            self.config['single_data_set']['inputDir'])

    def cancel_window(self, widget, *args):
        self.window.destroy()

    def output_selection_changed(self, widget, *args):
        self.config['ALOSDirOutput'] = widget.get_filename()

    def sar_lead_selection_changed(self, widget, *args):
        # we have to break to function when filename is reseted
        if widget.get_filename() is None:
            return True

        basename = os.path.basename(widget.get_filename())

        check_button = self.builder.get_object('check_lead_file_button')

        if self.is_leader_file(basename):
            self.name_files_motif = basename[4:]
            self.config['sar_lead_file'] = widget.get_filename()
            check_button.set_sensitive(True)
        else:
            print('Not a leader file : ' + widget.get_filename())
            widget.unselect_filename(widget.get_filename())

    def is_leader_file(self, filename):
        # TODO: more checks ?
        return filename.startswith('LED-')

    def check_leader_file(self, widget, *args):
        # TODO: get the infos and populate the entries

        prefix_image_files = []

        # find and set trailer file
        trl_file_name = 'TRL-' + self.name_files_motif
        trl_file_path = self.config['single_data_set']['inputDir'] \
            + '/' + trl_file_name

        if os.access(trl_file_path, os.R_OK):
            self.builder.get_object('sar_trailer_box').set_sensitive(True)
            trl_file_entry = self.builder.get_object('sar_trailer_file_entry')
            trl_file_entry.set_text(trl_file_path)
            self.config['sar_trailer_file_entry'] = trl_file_path
        else:
            # TODO: notify the error
            print('Cant access : ' + trl_file_path)
            return False

        # find and set the image files abd populate the entries
        prefix_image_files = [
            'HH',
            'VH',
            'HV',
            'VV']

        for prefix in prefix_image_files:
            just_the_name = 'IMG-' + prefix + '-' + self.name_files_motif
            image_file_path = self.config['single_data_set']['inputDir'] \
                + '/' + just_the_name

            if os.access(image_file_path, os.R_OK):
                entry = self.builder.get_object(prefix + '_entry')
                entry.set_text(image_file_path)
                self.config['IMG-' + prefix] = image_file_path
            else:
                # Break the function
                # TODO: better error
                print('Cant access : ' + image_file_path)
                return False

        # Finally if all went ok lets activate the other boxes
        self.builder.get_object('sar_image_box').set_sensitive(True)
        self.builder.get_object('manage_headers_box').set_sensitive(True)
        self.builder.get_object('read_header_button').set_sensitive(True)
        self.builder.get_object('validate_button').set_sensitive(True)

    def read_headers(self, widget, *args):

        exe_file = self.config['compiled_psp_path'] \
            + '/Soft/bin/data_import/alos_header.exe'

        self.config['ALOSConfigFile'] = self.config['tempDir'] + '/' \
            + strftime("%Y_%m_%d_%H_%M_%S") + '_alos_config.txt'

        exe_args = [
            '-od', self.config['ALOSDirOutput'],
            '-ilf', self.config['sar_lead_file'],
            '-iif', self.config['IMG-HH'],
            '-itf', self.config['sar_trailer_file_entry'],
            '-ocf', self.config['ALOSConfigFile'],
        ]

        (_, return_code) = exec_bin(exe_file, exe_args)
        if return_code is not 1:
            # return should be 1 ?
            raise Exception('Wrong return code')

        # else we can continue and read the output file
        with open(self.config['ALOSConfigFile'], 'r') as output:
            lines = output.read().splitlines()
            self.config['initial_rows_number'] = lines[1]
            self.config['initial_cols_number'] = lines[4]

        # remove the temp file
        # dont remove for test time
        # os.remove(alos_output_file)

        # update the entries
        self.builder.get_object('initial_rows_entry').set_text(
            self.config['initial_rows_number'])

        self.builder.get_object('initial_cols_entry').set_text(
            self.config['initial_cols_number'])

        self.builder.get_object('headers_infos_box').set_sensitive(True)

    def validate(self, widget, *args):
        # save the config and open the 'extract' window
        self.globState['config'].update(self.config)
        self.window.destroy()
        # TODO: open the 'Extract PolSAR Images window'
