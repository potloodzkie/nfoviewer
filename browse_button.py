# browse_button.py
from gi.repository import Gtk

class BrowseButton(Gtk.Button):
    def __init__(self, folder_tree, callback):
        super().__init__(label="Browse")
        self.folder_tree = folder_tree
        self.callback = callback
        self.connect("clicked", self.on_browse_clicked)

    def on_browse_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Choose a directory",
            parent=None,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
        )

        # Add buttons using add_buttons method
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK
        )

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            selected_folder = dialog.get_filename()
            dialog.destroy()
            self.load_selected_folder(selected_folder)

        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

    def load_selected_folder(self, selected_folder):
        # Load the selected folder and update the tree view
        self.folder_tree.file_store.clear()
        self.folder_tree.load_directory(selected_folder, None)

        # Get the selected tree_iter
        model, tree_iter = self.folder_tree.tree_view.get_selection().get_selected()

        # Trigger the callback to load folder contents
        if tree_iter is not None:
            self.callback(model, tree_iter)
