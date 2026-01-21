from controllers.gta_sa_modloader.gta_sa_modloader_controller import GTASAModloaderController


# GUI
from views.dialogs.qt import (SetItemDialog, SetPathDialog)

from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QWidget,
    QTableWidget,
    QTableWidgetItem
)
from config.paths import CONFIG_FORM_UI_FILE

class ConfigForm(QWidget):
    def __init__(self, modloader_controller: GTASAModloaderController):
        super().__init__(  )

        self.resize( 256, 256)
        uic.loadUi( CONFIG_FORM_UI_FILE, self )

        # Controller
        self.modloader_controller = modloader_controller
        self.profile_model = self.modloader_controller.profile_model

        # Inicializar
        self.update()

        # Cambiar estados
        self.checkboxIgnoreAllMods.stateChanged.connect( self.on_ignore_all_mods )
        self.checkboxExcludeAllMods.stateChanged.connect( self.on_exclude_all_mods )

        # Botones
        self.buttonAddParents.clicked.connect( self.on_add_parents )
        self.buttonRemoveParents.clicked.connect( self.on_remove_parents )

    def set_ignore_all_mods(self):
        if self.profile_model.ignore_all_mods:
            self.checkboxIgnoreAllMods.setCheckState( Qt.CheckState.Checked )
        else:
            self.checkboxIgnoreAllMods.setCheckState( Qt.CheckState.Unchecked )

    def set_exclude_all_mods(self):
        if self.profile_model.exclude_all_mods:
            self.checkboxExcludeAllMods.setCheckState( Qt.CheckState.Checked )
        else:
            self.checkboxExcludeAllMods.setCheckState( Qt.CheckState.Unchecked )

    def set_parents(self):
        text = ''
        for parent in self.profile_model.parents:
            text += f'{parent}\n'
        self.texteditParents.setText( text[:-1] )

    def update(self):
        self.set_ignore_all_mods()
        self.set_exclude_all_mods()
        self.set_parents()

    def on_ignore_all_mods(self, state):
        state = Qt.CheckState(state)
        value = state == Qt.CheckState.Checked
        self.modloader_controller.update_ignore_all_mods( value )

    def on_exclude_all_mods(self, state):
        state = Qt.CheckState(state)
        value = state == Qt.CheckState.Checked
        self.modloader_controller.update_exclude_all_mods( value )

    def on_add_parents(self):
        set_item_dialog = SetItemDialog(
            self, items=self.modloader_controller.get_profiles(),
            checkable=True, size=[256, 256]
        )
        if set_item_dialog.exec() == QDialog.DialogCode.Accepted:
            items = set_item_dialog.get_item()
            if isinstance(items, list):
                self.modloader_controller.save_parents( items )
                self.set_parents()

    def on_remove_parents(self):
        set_item_dialog = SetItemDialog(
            self, items=self.profile_model.parents,
            checkable=True, size=[256, 256]
        )
        if set_item_dialog.exec() == QDialog.DialogCode.Accepted:
            items = set_item_dialog.get_item()
            if isinstance(items, list):
                self.modloader_controller.remove_parents( items )
                self.set_parents()
