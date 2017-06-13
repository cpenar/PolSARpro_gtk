## Process this file with automake to produce Makefile.in
## Created by Anjuta


uidir = $(pkgdatadir)/ui
ui_DATA = single_data_set.ui


## The main script
bin_SCRIPTS = single_data_set.py \
	color-map-file.py \
	tool/color-map-file.py

## Directory where .class files will be installed
single_data_setdir = $(pythondir)/single_data_set


single_data_set_PYTHON = \
	single_data_set.py


EXTRA_DIST = $(ui_DATA)


# Remove ui directory on uninstall
uninstall-local:

	-rm -r $(uidir)

	-rm -r $(pkgdatadir)

SUBDIRS = \
	tool
