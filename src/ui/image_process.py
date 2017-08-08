#!/usr/bin/python3
# -*- coding: utf-8 -*-

import copy

from gi.repository import Gtk

UI_FILE = __name__ + ".ui"

default_image = 'Images/PSPyoda.gif'


class GUI:
    def __init__(self, state, image_file_path=None):
        print('image_file_path at begining of init')
        print(image_file_path)
        # global app state
        self.globState = state
        # local config
        self.config = copy.deepcopy(state['config'])

        self.builder = state['GtkBuilder']
        self.builder.add_from_file(UI_FILE)
        self.builder.connect_signals(self)

        self.window = self.builder.get_object(__name__ + '_dialog')
        self.window.show_all()

        print('pre IF')
        print(image_file_path)
        if image_file_path is None:
            image_file_path = self.config['localDir'] + '/' + default_image
        print('post IF')
        print(image_file_path)

        self.image = self.builder.get_object('main_image')
        print('self.image:')
        print(self.image)
        self.image.set_from_file(image_file_path)
    
