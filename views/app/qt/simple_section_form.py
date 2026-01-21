from config.constants import (
    SECTION_IGNORE_FILES, SECTION_IGNORE_MODS, SECTION_INCLUDE_MODS, SECTION_EXCLUSIVE_MODS,
    SIMPLE_PROFILE_SECTIONS
)
from controllers.gta_sa_modloader.gta_sa_modloader_controller import GTASAModloaderController

# GUI
from views.dialogs.qt import SetItemDialog

from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QDialog,
    QLabel,
    QSpinBox
)
from config.paths import SIMPLE_SECTION_FORM_UI_FILE

class SimpleSectionForm(QWidget):
    def __init__(self, modloader_controller: GTASAModloaderController, section: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.resize(256, 256)
        uic.loadUi( SIMPLE_SECTION_FORM_UI_FILE, self )

        # Controller
        self.modloader_controller = modloader_controller
        self.profile_model = self.modloader_controller.profile_model

        # Determinar secciones y que se seleccionara en add y remove.
        self.get_filenames_model = None
        self.get_filenames = None
        self.save_filename = None
        self.remove_filename = None
        self.good_section = section in SIMPLE_PROFILE_SECTIONS
        if self.good_section:
            if section == SECTION_IGNORE_FILES:
                self.get_filenames_model = lambda: self.profile_model.ignore_files
                self.get_filenames = self.modloader_controller.get_mod_file_names
                self.save_filename = self.modloader_controller.save_ignore_file
                self.remove_filename = self.modloader_controller.remove_ignore_file
            else:
                self.get_filenames = self.modloader_controller.get_mod_dir_names

            if section == SECTION_IGNORE_MODS:
                self.get_filenames_model = lambda: self.profile_model.ignore_mods
                self.save_filename = self.modloader_controller.save_ignore_mod
                self.remove_filename = self.modloader_controller.remove_ignore_mod

            elif section == SECTION_INCLUDE_MODS:
                self.get_filenames_model = lambda: self.profile_model.include_mods
                self.save_filename = self.modloader_controller.save_include_mod
                self.remove_filename = self.modloader_controller.remove_include_mod

            elif section == SECTION_EXCLUSIVE_MODS:
                self.get_filenames_model = lambda: self.profile_model.exclusive_mods
                self.save_filename = self.modloader_controller.save_exclusive_mod
                self.remove_filename = self.modloader_controller.remove_exclusive_mod
        else:
            raise ValueError(f'SimpleSectionForm: bad section: {section}')

        # Contenido en scroll.
        self.widget_filenames = []

        # Connect
        self.buttonAdd.clicked.connect( self.on_add_filenames )
        self.buttonRemove.clicked.connect( self.on_remove_filenames )

        self.update()

    def update(self):
        self.set_filenames()

    def set_filenames(self):
        for widget in self.widget_filenames:
            widget.deleteLater()
        self.widget_filenames.clear()
        for name in self.get_filenames_model():
            label = QLabel( name )
            self.widget_filenames.append( label )
            self.scrollVBoxLayout.addWidget( label )


    def on_add_filenames(self):
        set_item_dialog = SetItemDialog(
            self, items=self.get_filenames(), checkable=True, size=[256, 256]
        )
        if set_item_dialog.exec() == QDialog.DialogCode.Accepted:
            items = set_item_dialog.get_item()
            if isinstance(items, list):
                for name in items:
                    self.save_filename( name )
                self.set_filenames()


    def on_remove_filenames(self):
        set_item_dialog = SetItemDialog(
            self, items=self.get_filenames_model(), checkable=True, size=[256, 256]
        )
        if set_item_dialog.exec() == QDialog.DialogCode.Accepted:
            items = set_item_dialog.get_item()
            if isinstance(items, list):
                for name in items:
                    self.remove_filename( name )
                self.set_filenames()

