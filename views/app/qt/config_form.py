from controllers.gta_sa_modloader.gta_sa_modloader_controller import GTASAModloaderController

from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
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

    def update(self):
        self.set_ignore_all_mods()
        self.set_exclude_all_mods()

    def on_ignore_all_mods(self, state):
        state = Qt.CheckState(state)
        value = state == Qt.CheckState.Checked
        self.modloader_controller.update_ignore_all_mods( value )

    def on_exclude_all_mods(self, state):
        state = Qt.CheckState(state)
        value = state == Qt.CheckState.Checked
        self.modloader_controller.update_exclude_all_mods( value )
