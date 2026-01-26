from PyQt6.QtWidgets import QWidget, QDialog, QPushButton, QVBoxLayout, QTextEdit

class TextEditorDialog(QDialog):
    def __init__(
        self, parent=None, text_dict=None, title=None, text="", read_only=True, size=None
    ):
        '''
        Dialogo simple, con text edit. Signal de accept, para retornar textito.
        '''
        super().__init__(parent)

        # Fallback
        self.text = text
        self.read_only = read_only
        self.text_dict = text_dict or {"title": "Text edit", "ok": "Ok"}
        self.size = size or [512, 512]

        #
        self.setWindowTitle( title or self.text_dict["title"] )
        self.resize( self.size[0], self.size[1] )

        # Widgets
        vbox_main = QVBoxLayout()
        self.setLayout( vbox_main )

        self.text_edit = QTextEdit( self.text.replace('\n', '<br>') )
        self.text_edit.setReadOnly( self.read_only )
        vbox_main.addWidget( self.text_edit )

        self.button_ok = QPushButton( self.text_dict['ok'] )
        self.button_ok.clicked.connect( self.accept )
        vbox_main.addWidget( self.button_ok )

    def get_text(self):
        return self.text_edit.toPlainText()
