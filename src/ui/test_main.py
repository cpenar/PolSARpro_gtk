# -*- coding: utf-8 -*-

import sys

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from . import main

def test_gtk():
    window = Gtk.Window(title="foo")
    window.show()
    assert window.get_title() == "foo"
    window.destroy()


def test_locale():
    assert sys.getfilesystemencoding().upper() == "UTF-8"
