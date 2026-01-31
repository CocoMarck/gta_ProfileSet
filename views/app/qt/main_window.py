from controllers.gta_sa_modloader.gta_sa_modloader_controller import GTASAModloaderController
from core.launcher.gta_sa_launcher import GTASALauncher

# Rutas
from config.paths import ICON_FILE, MAIN_WINDOW_UI_FILE



# Style
from views.interface_number import (
    WINDOW_MAIN_SIZE, SET_ITEM_DIALOG_SIZE, FONT_SIZE, MARGIN_XY, PADDING_SPACE,
    TEXT_EDITOR_NORMAL_SIZE, TEXT_EDITOR_SMALL_SIZE
)
from views.style_sheet.css_util import get_list_text_widget, text_widget_style
FONT_FILE = "monospace"
qss_style = ''
for widget in get_list_text_widget('Qt'):
    if widget == "QTextEdit":
        qss_style += text_widget_style(
            widget=widget, font=FONT_FILE, font_size=FONT_SIZE,
            margin_based_font=True, padding=None, idented=4
        )
    elif widget == "QMenuBar":
        qss_style += text_widget_style(
            widget=widget, font=FONT_FILE, font_size=FONT_SIZE,
            margin_based_font=None, padding=None, idented=4
        )
    else:
        qss_style += text_widget_style(
            widget=widget, font=FONT_FILE, font_size=FONT_SIZE,
            margin_xy=MARGIN_XY, padding=PADDING_SPACE, idented=4
        )
print(qss_style)


# GUI
## Dialogs
from views.dialogs.qt import (SetItemDialog, SetPathDialog, TextEditorDialog)

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



#os.environ.setdefault("QT_QPA_PLATFORM", "xcb") # Wayland, forzar en x11, para que se vea el icon. Fix feo jejej.


class MainWindow(QMainWindow):
    def __init__(
        self, modloader_controller: GTASAModloaderController, gta_sa_launcher: GTASALauncher,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.setWindowTitle( 'Modloader Controller' )
        self.setWindowIcon( QIcon( str(ICON_FILE) ) )
        self.resize( WINDOW_MAIN_SIZE[0], WINDOW_MAIN_SIZE[1] )
        uic.loadUi( MAIN_WINDOW_UI_FILE, self)

        # Controller
        self.modloader_controller = modloader_controller
        self.profile_model = self.modloader_controller.profile_model
        self.folder_model = self.modloader_controller.folder_model

        # Launcher
        self.gta_sa_launcher = gta_sa_launcher

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
        self.actionLoadProfile.triggered.connect( self.on_load_profile )
        self.actionSetFolderProfile.triggered.connect( self.on_set_folder_profile )
        self.actionSaveProfile.triggered.connect( self.on_save_profile )
        self.actionRemoveProfile.triggered.connect( self.on_remove_profile )
        self.actionStartGame.triggered.connect( self.on_start_game )
        self.actionRenameProfile.triggered.connect( self.on_rename_profile )
        self.actionReadIni.triggered.connect( self.on_read_ini )
        self.actionGetMods.triggered.connect( self.on_get_mods )

        # Inicializar valores
        self.on_current_profile()
        self.on_current_folder_profile()

    def on_tab_changed(self, index):
        if index in self.dict_tabs.keys():
            self.dict_tabs[index].update()

    def update_forms(self):
        for form in self.dict_tabs.values():
            form.update()

    def on_current_profile(self):
        self.labelCurrentProfile.setText( str(self.profile_model.profile) )

    def on_current_folder_profile(self):
        self.labelCurrentFolderProfile.setText( str(self.folder_model.profile) )

    def on_load_profile(self):
        set_item_dialog = SetItemDialog(
            self, items=self.modloader_controller.get_profiles(),
            checkable=False, size=SET_ITEM_DIALOG_SIZE
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
            checkable=False, size=SET_ITEM_DIALOG_SIZE
        )
        if set_item_dialog.exec() == QDialog.DialogCode.Accepted:
            item = set_item_dialog.get_item()
            if isinstance(item, str):
                self.modloader_controller.set_folder_profile( item )
                self.on_current_folder_profile()

    def on_read_ini(self):
        dialog = TextEditorDialog(
            text=self.modloader_controller.get_ini_text(), size=TEXT_EDITOR_NORMAL_SIZE
        )
        dialog.exec()

    def on_save_profile(self):
        name, ok = QInputDialog.getText(self, 'save-profile', 'name')
        if name and ok:
            self.modloader_controller.save_profile( name )

    def on_remove_profile(self):
        set_item_dialog = SetItemDialog(
            self, items=self.modloader_controller.get_profiles(),
            checkable=False, size=SET_ITEM_DIALOG_SIZE
        )
        if set_item_dialog.exec() == QDialog.DialogCode.Accepted:
            item = set_item_dialog.get_item()
            if isinstance(item, str):
                remove = self.modloader_controller.remove_profile( item )
                if remove:
                    self.update_forms()
                    self.on_current_folder_profile()
                    self.on_current_profile()

    def on_start_game(self):
        print( self.gta_sa_launcher.launch() )

    def on_rename_profile(self):
        set_item_dialog = SetItemDialog(
            self, items=self.modloader_controller.get_profiles(),
            checkable=False, size=SET_ITEM_DIALOG_SIZE
        )
        if set_item_dialog.exec() == QDialog.DialogCode.Accepted:
            item = set_item_dialog.get_item()
            if isinstance(item, str):
                name, ok = QInputDialog.getText(self, 'rename-profile', 'name')
                if name and ok:
                    rename = self.modloader_controller.rename_profile( item, name )
                    if rename:
                        self.update_forms()
                        self.on_current_folder_profile()
                        self.on_current_profile()

    def on_get_profile_mods(self):
        set_item_dialog = SetItemDialog(
            self, items=self.modloader_controller.get_profiles(),
            checkable=False, size=SET_ITEM_DIALOG_SIZE
        )
        if set_item_dialog.exec() == QDialog.DialogCode.Accepted:
            item = set_item_dialog.get_item()
            mods = str( self.modloader_controller.get_profile_mods_dir(item) )
            dialog = TextEditorDialog( text=mods )
            dialog.exec()

    def on_get_mods(self):
        mods_text = ""
        for m in self.modloader_controller.get_mods_dir():
            mods_text += f"{m}\n"
        dialog = TextEditorDialog( text=mods_text[:-1], size=TEXT_EDITOR_SMALL_SIZE )
        dialog.exec()

    def closeEvent(self, event):
        self.gta_sa_launcher.stop()
        event.accept()


# Contruir
def build_app( modloader_controller: GTASAModloaderController, gta_sa_launcher: GTASALauncher ):
    app = QApplication(sys.argv)
    app.setStyleSheet( qss_style )

    window = MainWindow( modloader_controller, gta_sa_launcher )
    window.show()

    sys.exit( app.exec() )
