# main.py
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from folder_tree import FolderTree
from browse_button import BrowseButton
from nfo_reader import NFOReader

def main():
    window = NFOReader()
    window.connect('destroy', Gtk.main_quit)
    window.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
