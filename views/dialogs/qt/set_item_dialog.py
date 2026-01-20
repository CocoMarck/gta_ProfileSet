from functools import partial
from PyQt6.QtWidgets import(
    QDialog,
    QWidget,
    QScrollArea,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)
from PyQt6.QtCore import Qt

class SetItemDialog( QDialog ):
    def __init__(
        self, parent=None, size=[256, 256], text_dict={
            "title": "Set something",
            "ok": "Ok",
            "cancel": "Cancel",
            'search': 'Search'
        },
        items=[], checkable=False, search=True
    ):
        super().__init__(parent)

        self.setWindowTitle( text_dict['title'] )
        self.resize( size[0], size[1] )

        # Contenedor principal
        self.main_layout = QVBoxLayout()
        self.setLayout( self.main_layout )

        # Scroll de botones
        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded,
        )
        self.scroll_area.setWidgetResizable(True) # Para centrer el scroll
        self.main_layout.addWidget( self.scroll_area )

        # Scroll/Widget, contenedor de botones
        self.selected_items = []
        self.checkable = checkable
        self.widget_buttons = QWidget()
        self.widget_buttons_vbox = QVBoxLayout()
        self.widget_buttons.setLayout( self.widget_buttons_vbox )

        self.items = items
        self.button_dict = {}
        for i in self.items:
            button = QPushButton( str(i) )
            button.setCheckable(checkable)
            button.clicked.connect( partial(self.on_button_item, button=button) )
            self.button_dict.update( {button: i} )
            self.widget_buttons_vbox.addWidget( button )

        self.scroll_area.setWidget( self.widget_buttons )

        # Buscar
        self.search = search
        if self.search:
            self.line_edit_search = QLineEdit(self, placeholderText=text_dict['search'] )
            self.line_edit_search.textChanged.connect(self.on_search)
            self.main_layout.addWidget(self.line_edit_search)

        # Aceptar o cancelar
        self.text_dict = text_dict
        hbox = QHBoxLayout()
        button_options = ['cancel']
        if self.checkable:
            button_options = ['ok', 'cancel']
        for option in button_options:
            hbox.addStretch()
            button = QPushButton( self.text_dict[option] )
            if option == 'ok':
                button.clicked.connect( self.accept )
            elif option == 'cancel':
                button.clicked.connect( self.close )
            hbox.addWidget( button )
            hbox.addStretch()
        self.main_layout.addLayout(hbox)


    def on_button_item(self, button):
        if self.checkable:
            self.selected_items = []
            for b in self.button_dict.keys():
                if b.isChecked():
                    self.selected_items.append( self.button_dict[b] )
        else:
            self.selected_items = self.button_dict[button]
            self.accept()


    def on_search(self, text):
        lower_text = text.lower()
        if not lower_text:
            return
        for button in self.button_dict.keys():
            if button.text().lower().startswith(lower_text):
                button.setFocus()
                self.scroll_area.ensureWidgetVisible(button)
                self.line_edit_search.setFocus()
                break


    def get_item(self):
        if self.selected_items == []:
            return None
        else:
            return self.selected_items

