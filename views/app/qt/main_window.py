from controllers.gta_sa_modloader.gta_sa_modloader_controller import GTASAModloaderController

# Rutas
from config.paths import ICON_FILE, MAIN_WINDOW_UI_FILE


# GUI
## Dialogs
from views.dialogs.qt import (SetItemDialog, SetPathDialog)

## Essentals
import sys, os
from functools import partial
from PyQt6.QtWidgets import(
    QApplication,
    QMainWindow,
    QWidget,
    QDialog,
    QFileDialog,
    QMessageBox,
    QScrollArea,
    QLineEdit,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QInputDialog

)
from PyQt6 import uic
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt

## Tabs
from .config_form import ConfigForm
from .priority_form import PriorityForm
from .ignore_files_form import IgnoreFilesForm
from .ignore_mods_form import IgnoreModsForm
from .include_mods_form import IncludeModsForm
from .exclusive_mods_form import ExclusiveModsForm


class MainWindow(QMainWindow):
    def __init__(self, modloader_controller: GTASAModloaderController, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle( 'Modloader Controller' )
        #self.setWindowIcon( QIcon( str(ICON_FILE) )
        self.resize( 1024, 512 )
        uic.loadUi( MAIN_WINDOW_UI_FILE, self)

        # Controller
        self.modloader_controller = modloader_controller
        self.profile_model = self.modloader_controller.profile_model
        self.folder_model = self.modloader_controller.folder_model

        # Tabs
        self.config_form = ConfigForm( self.modloader_controller )
        self.tabWidget.addTab( self.config_form, 'Config' ) # Index 0

        self.priority_form = PriorityForm( self.modloader_controller )
        self.tabWidget.addTab( self.priority_form, 'Priority') # Index 1

        self.ignore_files_form = IgnoreFilesForm( self.modloader_controller )
        self.tabWidget.addTab( self.ignore_files_form, 'IgnoreFiles' )

        self.ignore_mods_form = IgnoreModsForm( self.modloader_controller )
        self.tabWidget.addTab( self.ignore_mods_form, 'IgnoreMods' )

        self.include_mods_form = IncludeModsForm( self.modloader_controller )
        self.tabWidget.addTab( self.include_mods_form, 'IncludeMods' )

        self.exclusive_mods_form = ExclusiveModsForm( self.modloader_controller )
        self.tabWidget.addTab( self.exclusive_mods_form, 'ExclusiveMods' )

        self.tabWidget.currentChanged.connect( self.on_tab_changed )

        self.dict_tabs = {
            0: self.config_form, 1: self.priority_form, 2: self.ignore_files_form,
            3: self.ignore_mods_form, 4: self.include_mods_form, 5: self.exclusive_mods_form
        }

        # Actions
        self.actionOpenProfile.triggered.connect( self.on_open_profile )
        self.actionSetFolderProfile.triggered.connect( self.on_set_folder_profile )

        # Inicializar valores
        self.on_current_profile()
        self.on_current_folder_profile()

    def on_tab_changed(self, index):
        if index in self.dict_tabs.keys():
            self.dict_tabs.update()

    def update_forms(self):
        for form in self.dict_tabs.values():
            form.update()

    def on_current_profile(self):
        self.labelCurrentProfile.setText( str(self.profile_model.profile) )

    def on_current_folder_profile(self):
        self.labelCurrentFolderProfile.setText( str(self.folder_model.profile) )

    def on_open_profile(self):
        set_item_dialog = SetItemDialog(
            self, items=self.modloader_controller.get_profiles(),
            checkable=False, size=[256, 256]
        )
        if set_item_dialog.exec() == QDialog.DialogCode.Accepted:
            item = set_item_dialog.get_item()
            if isinstance(item, str):
                self.modloader_controller.select_profile( item )
                self.on_current_profile()
                self.update_forms()

    def on_set_folder_profile(self):
        set_item_dialog = SetItemDialog(
            self, items=self.modloader_controller.get_profiles(),
            checkable=False, size=[256, 256]
        )
        if set_item_dialog.exec() == QDialog.DialogCode.Accepted:
            item = set_item_dialog.get_item()
            if isinstance(item, str):
                self.modloader_controller.set_folder_profile( item )
                self.on_current_folder_profile()

    def on_get_ini_text(self):
        print( self.modloader_controller.get_ini_text() )


# Contruir
def build_app( modloader_controller: GTASAModloaderController ):
    app = QApplication(sys.argv)
    #app.setStyleSheet( qss_style )

    window = MainWindow( modloader_controller )
    window.show()

    sys.exit( app.exec() )
