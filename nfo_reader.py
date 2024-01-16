# nfo_reader.py
import os
from gi.repository import Gtk
from folder_tree import FolderTree  # Add this line
from browse_button import BrowseButton  # Add this line

class NFOReader(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_default_size(600, 600)

        self.folder_tree = FolderTree()
        self.folder_tree.tree_view.get_selection().connect('changed', self.on_folder_selected)

        self.browse_button = BrowseButton(self.folder_tree, self.load_folder_contents)

        self.combobox = Gtk.ComboBoxText()
        self.combobox.set_hexpand(True)
        self.combobox.connect("changed", self.on_file_selected)

        self.textview = Gtk.TextView()
        content_scrolledwindow = Gtk.ScrolledWindow()
        content_scrolledwindow.set_size_request(400, 300)
        content_scrolledwindow.add(self.textview)
        
        # Set line spacing in TextView
        text_buffer = self.textview.get_buffer()
        tag = text_buffer.create_tag("smaller_font", scale=0.8)
        text_buffer.apply_tag(tag, text_buffer.get_start_iter(), text_buffer.get_end_iter())

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        hbox.pack_start(self.browse_button, False, True, 0)
        hbox.pack_start(self.folder_tree, True, True, 0)
        hbox.pack_end(content_scrolledwindow, True, True, 0)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vbox.pack_start(self.combobox, False, True, 0)
        vbox.pack_start(hbox, True, True, 0)

        self.add(vbox)

    def on_folder_selected(self, *args):
        model, treeiter = args[0].get_selected()
        self.load_folder_contents(model, treeiter)

    def load_folder_contents(self, model, tree_iter):
        if tree_iter is not None:
            folder_path = model[tree_iter][1]
            try:
                files = [f for f in os.listdir(folder_path) if f.endswith('.nfo')]
                self.combobox.remove_all()
                for file in files:
                    self.combobox.append_text(file)
                if len(files) == 1:
                    self.combobox.set_active(0)
            except Exception:
                pass

    def on_file_selected(self, widget):
        model, treeiter = self.folder_tree.tree_view.get_selection().get_selected()
        if treeiter is not None:
            folder_path = model[treeiter][1]
            nfo_file = self.combobox.get_active_text()
            if nfo_file is not None:
                nfo_file_path = os.path.join(folder_path, nfo_file)
                content = self.read_nfo_file(nfo_file_path)
                self.textview.get_buffer().set_text(content)

    def read_nfo_file(self, file_path):
        with open(file_path, 'r', encoding='cp437') as file:
            content = file.read()
        return content
