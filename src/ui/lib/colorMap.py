#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Gdk
import os
import math


class GUI:
    def __init__(self, fileName):
        """Open a color map window
        with the color map initialized from .pal file"""

        templateFile = 'colormap_window_template.ui'

        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.dirname(fileName) + '/../'
                                   + templateFile)
        self.builder.connect_signals(self)

        # Gtk.Entry input_file_entry texte
        self.inputEntry = self.builder.get_object('input_file_entry')
        self.inputEntry.set_text(fileName.split('/')[-1])

        # Output
        self.outputEntry = self.builder.get_object('output_file_entry')
        self.outputEntry.set_text(fileName.split('/')[-1])

        self.fcDialog = self.builder.get_object('output_filechooserdialog')

        # the vertical box containing horizontal boxes of colorbuttons
        self.boxBtn = self.builder.get_object('boxColorMapBtn')

        self.open_colormap_file(fileName)

        self.cmWindow = self.builder.get_object('dialog_color_map')
        self.cmWindow.set_visible(True)

    def open_file_chooser(self, widget, *args):
        self.fcDialog.set_visible(True)

    def cancel_file_chooser(self, widget, *arg):
        self.fcDialog.set_visible(False)
        return True

    def save_file_chooser(self, widget, *args):
        fileName = self.fcDialog.get_uri().split('/')[-1]
        self.outputEntry.set_text(fileName)
        self.fcDialog.set_visible(False)

    def open_colormap_file(self, fileName):
        f = open(fileName, 'r')
        colorMap = f.read().splitlines()
        if colorMap[0] != 'JASC-PAL':
            raise Exception('Unknown type file ' + colorMap[0]
                            + '. Expected : JASC-PAL')

        # 4 first lines and one last are useless
        colorMap = colorMap[4:-1]

        # We remove the last lines that are values '1 0 1'
        while colorMap[-1] == '1 0 1':
            colorMap.pop()

        # how many rows of 8 btn do we need to show them all ?
        btnRows = math.ceil(len(colorMap) / 8)

        # lets build one horizontal box per row and put the buttons inside
        for row in range(btnRows):
            box = Gtk.Box()
            box.set_visible(True)
            box.set_halign(Gtk.Align.CENTER)
            self.boxBtn.pack_start(box, True, True, 0)

            for rgbColorCode in colorMap[row*8:row*8 + 7]:
                RGBAstr = 'rgb(' + ','.join(rgbColorCode.split()) + ')'
                color = Gdk.RGBA()
                Gdk.RGBA.parse(color, RGBAstr)
                btn = Gtk.ColorButton()
                btn.set_rgba(color)
                btn.set_visible(True)
                box.pack_start(btn, True, True, 0)

    def save_colormap(self, widget, *args):
        pass

    def cancel_colormap(self, widget, *args):
        self.cmWindow.set_visible(False)
