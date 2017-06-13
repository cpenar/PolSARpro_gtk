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

class WindowColorMapFromFile:
    """Open a color map window 
    with the color map initialized from .pal file"""

    ColorMapDir = 'ColorMap/'

    def __init__(self, fileName):
        filePath = ColorMapDir + fileName + '.pal'
        colormap = self.colorMapFromFile(filePath)


    def colorMapFromFile(self, fileName):
        try:
            f = open(fileName)
            content = f.read().splitlines()
            if content[0] != 'JASC-PAL':
                raise Exception( 'Unknown type file ' + content[0] 
                    + '. Expected : JASC-PAL')

            # 4 first lines are useless
            content = content [4:0]

            # We remove the last lines that are values '1 0 1'
            while content[-1] = '1 0 1':
                content.pop()

            return content

        except Exception, e:
            print(e)

