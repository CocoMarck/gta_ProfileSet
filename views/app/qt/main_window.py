# GTASAModloaderController
from models.gta_sa_modloader import ProfileModel, FolderModel
#from repositories.gta_sa_modloader.path_repository import PathRepository
#from repositories.gta_sa_modloader.text_repository import TextRepository
#from repositories.gta_sa_modloader.folder_repository import FolderRepository
#from repositories.gta_sa_modloader.profile_repository import ProfileRepository
from controllers.gta_sa_modloader.gta_sa_modloader_controller import GTASAModloaderController

# Rutas
from config.paths import ICON_FILE, MAIN_WINDOW_UI_FILE, GTA_SA_DIR

# Controller
profile_model = ProfileModel()
folder_model = FolderModel()
modloader_controller = GTASAModloaderController( folder_model, profile_model, GTA_SA_DIR )
modloader_controller.sync_active_profile()


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


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle( 'Modloader Controller' )
        #self.setWindowIcon( QIcon( str(ICON_FILE) )
        self.resize( 512, 256 )
        uic.loadUi( MAIN_WINDOW_UI_FILE, self)

        # Tabs
        self.config_form = ConfigForm( modloader_controller )
        self.tabWidget.addTab( self.config_form, 'Config' ) # Index 0

        self.tabWidget.currentChanged.connect( self.on_tab_changed )

        # Actions
        self.actionOpenProfile.triggered.connect( self.on_open_profile )
        self.actionSetFolderProfile.triggered.connect( self.on_set_folder_profile )

        # Inicializar valores
        self.on_current_profile()
        self.on_current_folder_profile()

    def on_tab_changed(self, index):
        if index == 0:
            self.config_form.update()

    def update_forms(self):
        self.config_form.update()

    def on_current_profile(self):
        self.labelCurrentProfile.setText( str(profile_model.profile) )

    def on_current_folder_profile(self):
        self.labelCurrentFolderProfile.setText( str(folder_model.profile) )

    def on_open_profile(self):
        set_item_dialog = SetItemDialog(
            self, items=modloader_controller.get_profiles(),
            checkable=False, size=[256, 256]
        )
        set_item_dialog.exec()
        item = set_item_dialog.get_item()
        if isinstance(item, str):
            modloader_controller.select_profile( item )
            self.on_current_profile()
            self.update_forms()

    def on_set_folder_profile(self):
        set_item_dialog = SetItemDialog(
            self, items=modloader_controller.get_profiles(),
            checkable=False, size=[256, 256]
        )
        set_item_dialog.exec()
        item = set_item_dialog.get_item()
        if isinstance(item, str):
            modloader_controller.set_folder_profile( item )
            self.on_current_folder_profile()

    def on_get_ini_text(self):
        print( modloader_controller.get_ini_text() )


# Contruir
def build_app():
    app = QApplication(sys.argv)
    #app.setStyleSheet( qss_style )

    window = MainWindow()
    window.show()

    sys.exit( app.exec() )
