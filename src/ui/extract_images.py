#!/usr/bin/python3
# -*- coding: utf-8 -*-

import copy
import os

from gi.repository import GLib

from lib.async_exe import Async_exec

UI_FILE = __name__ + ".ui"


class GUI:
    def __init__(self, state):
        # global app state
        self.globState = state

        # copy of global config
        self.config = copy.deepcopy(state['config'])

        self.builder = state['GtkBuilder']
        self.builder.add_from_file(UI_FILE)
        self.builder.connect_signals(self)

        self.window = self.builder.get_object(__name__ + '_dialog')

        self.input_dir_entry = self.builder.get_object('input_dir_entry')
        self.input_dir_entry.set_text(
            self.config['single_data_set']['inputDir'])

        self.output_file_chooser = self.builder.get_object(
            'output_dir_file_chooser')
        self.output_file_chooser.set_filename(self.config['ALOSDirOutput'])

        self.builder.get_object('end_row_entry')\
            .set_text(self.config['initial_rows_number'])

        self.builder.get_object('end_col_entry')\
            .set_text(self.config['initial_cols_number'])

        self.config['offset_col'] = 0
        self.config['offset_row'] = 0

    def on_T3_button_toggled(self, widget, *args):
        sym_button = self.builder.get_object('symmetrization_button')

        sym_button.set_sensitive(True)
        sym_button.set_active(True)

        self.config['output_data_format'] = 'T3'

        self.builder.get_object('output_dir_complement_entry')\
            .set_text('/T3')

        self.config['extractOutputDir'] = self.config['ALOSDirOutput'] + '/T3'

        self.builder.get_object('validate_button')\
            .set_sensitive(True)

    def on_symmetrization_button_toggled(self, widget, *args):
        if widget.get_active():
            self.config['symmetrisation'] = '1'
        else:
            self.config['symmetrisation'] = '0'

    def on_sub_sampling_button_toggled(self, widget, *args):
        self.builder.get_object('sub_sampling_box')\
            .set_sensitive(True)

        self.builder.get_object('multi_look_box')\
            .set_sensitive(False)

        self.builder.get_object('sub_sampling_row_entry')\
            .set_text('?')

        self.builder.get_object('sub_sampling_col_entry')\
            .set_text('?')

        self.builder.get_object('T3_button').set_sensitive(True)

        sym_button = self.builder.get_object('symmetrization_button')

        sym_button.set_sensitive(True)
        sym_button.set_active(True)

    def on_full_resolution_button_toggled(self, widget, *args):
        pass

    def on_multi_look_button_toggled(self, widget, *args):
        pass

    def on_sub_sampling_row_entry_changed(self, widget, *args):
        self.config['sub_sampling_row'] = widget.get_text()

    def on_sub_sampling_col_entry_changed(self, widget, *args):
        self.config['sub_sampling_col'] = widget.get_text()

    def output_selection_changed(self, widget, *args):
        self.config['ALOSDirOutput'] = widget.get_filename()

    def cancel_window(self, widget, *args):
        self.window.destroy()

    def run_extract(self, widget, *args):
        # Stacking alos_convert_11.exe

        process_file = self.config['compiled_psp_path'] \
            + '/Soft/bin/data_import/alos_convert_11.exe'

        final_row_number = int(self.config['initial_rows_number']) \
            - self.config['offset_row']

        final_col_number = int(self.config['initial_cols_number']) \
            - self.config['offset_col']

        if not os.path.exists(self.config['extractOutputDir']):
            os.makedirs(self.config['extractOutputDir'])

        process_args = [
            '-if1', self.config['IMG-HH'],
            '-if2', self.config['IMG-VH'],
            '-if3', self.config['IMG-HV'],
            '-if4', self.config['IMG-VV'],
            '-od', self.config['extractOutputDir'],
            '-odf', self.config['output_data_format'],
            '-nr', self.config['initial_rows_number'],
            '-nc', self.config['initial_cols_number'],
            '-ofr', str(self.config['offset_row']),
            '-ofc', str(self.config['offset_col']),
            '-fnr', str(final_row_number),
            '-fnc', str(final_col_number),
            '-sym', self.config['symmetrisation'],
            '-cf', self.config['ALOSConfigFile'],
            '-nlr', '1',
            '-nlc', '1',
            '-ssr', self.config['sub_sampling_row'],
            '-ssc', self.config['sub_sampling_col'],
            '-mem', '1000',
            '-errf', self.config['tempDir'] + '/MemoryAllocError.txt',
        ]

        async_proc_chain = Async_exec(
            process_file,
            process_args,
            self.process_output_to_progress_bar)

        # Stacking create_mask_valid_pixels.exe

        final_row_number = \
            final_row_number // int(self.config['sub_sampling_row'])
        final_col_number = \
            final_col_number // int(self.config['sub_sampling_col'])

        process_file = self.config['compiled_psp_path'] \
            + '/Soft/bin/tools/create_mask_valid_pixels.exe'

        process_args = [
            '-id', self.config['extractOutputDir'],
            '-od', self.config['extractOutputDir'],
            '-idf', self.config['output_data_format'],
            '-ofr', str(self.config['offset_row']),
            '-ofc', str(self.config['offset_col']),
            '-fnr', str(final_row_number),
            '-fnc', str(final_col_number),
        ]

        async_proc_chain.add(process_file, process_args,
                             self.process_output_to_progress_bar)

        # Stacking apply_mask_valid_pixels.exe
        process_file = self.config['compiled_psp_path'] \
            + '/Soft/bin/tools/apply_mask_valid_pixels.exe'

        process_args = [
            '-bf', self.config['extractOutputDir'] + '/mask_valid_pixels.bin',
            '-mf', self.config['extractOutputDir'] + '/mask_valid_pixels.bin',
            '-iodf', '4',
            '-fnr', str(final_row_number),
            '-fnc', str(final_col_number),
        ]

        async_proc_chain.add(process_file, process_args,
                             self.process_output_to_progress_bar)

        # Stacking create_bmp_file.exe
        process_file = self.config['compiled_psp_path'] \
            + '/Soft/bin/bmp_process/create_bmp_file.exe'

        process_args = [
            '-mcol', 'black',
            '-if', self.config['extractOutputDir'] + '/mask_valid_pixels.bin',
            '-of', self.config['extractOutputDir'] + '/mask_valid_pixels.bmp',
            '-ift', 'float',
            '-oft', 'real',
            '-clm', 'jet',
            '-nc', self.config['initial_cols_number'],
            '-ofr', str(self.config['offset_row']),
            '-ofc', str(self.config['offset_col']),
            '-fnr', str(final_row_number),
            '-fnc', str(final_col_number),
            '-mm', '0',
            '-min', '0',
            '-max', '1',
            '-mask', self.config['extractOutputDir']
                     + '/mask_valid_pixels.bin',
        ]

        async_proc_chain.add(process_file, process_args,
                             self.process_output_to_progress_bar)

        # Stacking apply_mask_valid_pixels.exe on Txx

        process_file = self.config['compiled_psp_path'] \
            + '/Soft/bin/tools/apply_mask_valid_pixels.exe'

        for bf in ['T11.bin', 'T12_real.bin', 'T12_imag.bin',
                   'T13_real.bin', 'T13_imag.bin', 'T22.bin',
                   'T23_real.bin', 'T23_imag.bin', 'T33.bin']:
            process_args = [
                '-bf', self.config['extractOutputDir'] + bf,
                '-mf', self.config['extractOutputDir'] + '/mask_valid_pixels.bin',
                '-iodf', '4',
                '-fnr', str(final_row_number),
                '-fnc', str(final_col_number),
            ]

            async_proc_chain.add(process_file, process_args,
                                 self.process_output_to_progress_bar)

        # Stacking create_pauli_rgb_file.exe

        self.config['output_bmp_file'] = self.config['extractOutputDir'] + '/PauliRGB.bmp'

        process_file = self.config['compiled_psp_path'] \
            + '/Soft/bin/bmp_process/create_pauli_rgb_file.exe'

        process_args = [
            '-id', self.config['extractOutputDir'],
            '-of', self.config['output_bmp_file'],
            '-iodf', 'T3',
            '-ofr', str(self.config['offset_row']),
            '-ofc', str(self.config['offset_col']),
            '-fnr', str(final_row_number),
            '-fnc', str(final_col_number),
            '-mem', '1000',
            '-errf', self.config['tempDir'] + '/MemoryAllocError.txt',
            '-mask', self.config['extractOutputDir'] + '/mask_valid_pixels.bin',
            '-auto', '1',
        ]

        async_proc_chain.add(process_file, process_args,
                             self.process_output_to_progress_bar)

        # post exec
        async_proc_chain.end(self.open_output_bmp_file)

        # Fire the async process chain execution
        async_proc_chain.run()

        # Hide this window
        self.window.destroy()

    def process_output_to_progress_bar(self, process):
        from time import sleep

        def reset_progress_bar():
            progress_bar = self.builder.get_object('progress_bar')
            progress_bar.set_fraction(0)
            return False

        def max_progress_bar():
            progress_bar = self.builder.get_object('progress_bar')
            progress_bar.set_fraction(1)
            return False

        def update_progress_bar(fraction):
            progress_bar = self.builder.get_object('progress_bar')
            progress_bar.set_fraction(fraction)
            return False

        GLib.idle_add(reset_progress_bar)

        while not process.poll():
            stdout = process.stdout.readline()
            try:
                value = float(stdout) / 100
                print('val : ', value)
                GLib.idle_add(update_progress_bar, value)
            except:
                print(stdout)
            sleep(0.1)

        GLib.idle_add(max_progress_bar)

    def open_output_bmp_file(self):
        import image_process
        GLib.idle_add(image_process.GUI(self.globState, self.config['output_bmp_file']))

