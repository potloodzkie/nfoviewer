# folder_tree.py
import os
from gi.repository import Gtk

class FolderTree(Gtk.ScrolledWindow):
    def __init__(self):
        super().__init__()
        self.set_size_request(200, 400)

        # Add boolean column for loaded flag
        self.file_store = Gtk.TreeStore(str, str, bool)
        self.tree_view = Gtk.TreeView(model=self.file_store)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Folder", renderer, text=0)
        self.tree_view.append_column(column)

        cwd = os.getcwd()
        self.load_directory(cwd, None)

        self.add(self.tree_view)
        self.tree_view.show_all()

        # Connect the row-expanded signal to the load_children method
        self.tree_view.connect("row-expanded", self.load_children)

    def load_directory(self, directory, parent_iter):
        if os.path.isdir(directory):
            try:
                # Sort folders alphabetically
                for filename in sorted(os.listdir(directory)):
                    full_path = os.path.join(directory, filename)
                    if os.path.isdir(full_path):
                        new_iter = self.file_store.append(parent_iter, [filename, full_path, False])
                        # Add dummy node
                        self.file_store.append(new_iter, [None, None, None])

            except PermissionError:
                pass

    def load_children(self, tree_view, iter, path):
        # Check if this directory has been loaded before
        if self.file_store[iter][2]:
            return

        # Clear existing children
        while self.file_store.iter_has_child(iter):
            self.file_store.remove(self.file_store.iter_children(iter))

        # Load any new children
        self.load_directory(self.file_store[iter][1], iter)

        # Set loaded flag to True
        self.file_store[iter][2] = True
