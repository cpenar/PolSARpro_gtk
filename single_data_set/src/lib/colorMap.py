# vim: set et ts=4 sw=4: #
# -*- Mode: Python; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- #
# color-map-file.py
# Copyright (C) 2017 Carlos Penaranda <cpenar@MR032028>
#
# single_data_set is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# single_data_set is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk, Gdk
import os, math


def windowFromFile(fileName, gui):
    """Open a color map window 
    with the color map initialized from .pal file"""

    templateFile = 'colormap_window_template.ui'

    try:
        f = open(fileName)
        colorMap = f.read().splitlines()
        if colorMap[0] != 'JASC-PAL':
            raise Exception( 'Unknown type file ' + content[0] 
                + '. Expected : JASC-PAL')

        # 4 first lines are useless
        colorMap = colorMap [4:]

        # We remove the last lines that are values '1 0 1'
        while colorMap[-1] == '1 0 1':
            colorMap.pop()

        gui.builder.add_from_file(os.path.dirname(fileName) + '/../ui/'
            + templateFile)


        # the vert box containing hori boxes of colorbuttons
        boxBtn = gui.builder.get_object('boxColorMapBtn')
        
        # how many rows of 8 btn do we need to show them all ?
        btnRows = math.ceil( len(colorMap) / 8 )

        # lets build one horizontal box per row and put the buttons inside
        for row in range(btnRows):
            box = Gtk.Box()
            box.set_visible(True)
            boxBtn.pack_start(box, True, True, 0)
            for rgbColorCode in colorMap[row*8 : row*8 + 7] :
                RGBAstr = 'rgb(' + ','.join(rgbColorCode.split()) + ')'
                color = Gdk.RGBA()
                Gdk.RGBA.parse(color, RGBAstr)
                btn = Gtk.ColorButton()
                btn.set_rgba(color)
                btn.set_visible(True)
                box.pack_start(btn, True, True, 0)

        cm_window = gui.builder.get_object('window_color_map')
        cm_window.set_visible(True)
        

    except Exception as e:
        print(e)

