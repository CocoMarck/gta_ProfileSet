from controllers.gta_sa_modloader.gta_sa_modloader_controller import GTASAModloaderController
from config.constants import MAX_PRIORITY

# GUI
from functools import partial
from views.dialogs.qt import (SetItemDialog, SetPathDialog)

from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QDialog,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QSpinBox
)
from config.paths import PRIORITY_FORM_UI_FILE


class PriorityForm(QWidget):
    def __init__(self, modloader_controller: GTASAModloaderController, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.resize(256, 256)
        uic.loadUi( PRIORITY_FORM_UI_FILE, self )

        # Controller
        self.modloader_controller = modloader_controller
        self.profile_model = self.modloader_controller.profile_model

        # Almacen de spinbox priorities
        self.priority_widgets = []

        # Connect
        self.buttonAddPriorities.clicked.connect( self.on_add_priorities )
        self.buttonRemovePriorities.clicked.connect( self.on_remove_priorities )

        # Priorities
        self.update()

    def update(self):
        self.set_priorities()

    def set_priorities(self):
        #first -> clear widgets, and `dict_priorities`.
        for widget in self.priority_widgets:
            widget.deleteLater()
        self.priority_widgets.clear()
        for key in self.profile_model.priority.keys():
            spin_box_prioriry = QSpinBox(
               minimum=0, maximum=MAX_PRIORITY, singleStep=1, value=self.profile_model.priority[key]
            )
            spin_box_prioriry.valueChanged.connect( partial(self.on_save_priority, name=key) )
            label = QLabel(key)
            self.scrollAreaFormLayout.addRow( label, spin_box_prioriry )
            self.priority_widgets.extend( [label, spin_box_prioriry] )

    def on_save_priority(self, value, name):
        self.modloader_controller.save_priority( name, value )

    def on_add_priorities(self):
        set_item_dialog = SetItemDialog(
            self, items=self.modloader_controller.get_mod_dir_names(),
            checkable=True, size=[256, 256]
        )
        if set_item_dialog.exec() == QDialog.DialogCode.Accepted:
            items = set_item_dialog.get_item()
            if isinstance(items, list):
                for name in items:
                    self.modloader_controller.save_priority( name )
                    self.set_priorities()

    def on_remove_priorities(self):
        set_item_dialog = SetItemDialog(
            self, items=self.profile_model.priority.keys(),
            checkable=True, size=[256, 256]
        )
        if set_item_dialog.exec() == QDialog.DialogCode.Accepted:
            items = set_item_dialog.get_item()
            if isinstance(items, list):
                for name in items:
                    self.modloader_controller.remove_priority(
                        name, self.profile_model.priority[name]
                    )
                    self.set_priorities()
