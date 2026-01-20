import pathlib
from PyQt6.QtWidgets import(
    QDialog,
    QWidget,
    QLineEdit,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog

)

class SetPathDialog(QDialog):
    def __init__(
        self, parent=None, size=[256,256], text_dict={
            "title": "Select path",
            'input': 'Input',
            'path': 'Path',
            'search': 'Buscar',
            'ok': 'Ok',
            'clear_input': 'Clear input'
        }, mode="dir", path="./", glob_file_prefix="ALL (*)"
    ):
        '''
        '''
        super().__init__(parent)

        self.text_dict = text_dict
        self.mode = mode
        self.path = path
        self.parent = parent
        self.glob_file_prefix = glob_file_prefix

        self.setWindowTitle( self.text_dict['title'] )
        self.resize( size[0], size[1] )

        # Contenedor principal
        self.main_layout = QVBoxLayout()
        self.setLayout( self.main_layout )

        hbox = QHBoxLayout()
        self.main_layout.addLayout( hbox )

        label = QLabel( self.text_dict['input'] )
        hbox.addWidget( label )

        self.line_edit_path = QLineEdit(
            text=str(path), placeholderText=self.text_dict['path']
        )
        hbox.addWidget( self.line_edit_path )

        button_set_path = QPushButton( self.text_dict['search'] )
        button_set_path.clicked.connect( self.on_set_path )
        hbox.addWidget( button_set_path )

        # Separador
        self.main_layout.addStretch()

        # Aceptar y cancelar
        hbox = QHBoxLayout()
        self.main_layout.addLayout( hbox )

        button_ok = QPushButton( self.text_dict['ok'] )
        button_ok.clicked.connect( self.on_ok )
        hbox.addWidget( button_ok )

        button_clear_input = QPushButton( self.text_dict['clear_input'] )
        button_clear_input.clicked.connect( self.line_edit_path.clear )
        hbox.addWidget( button_clear_input )

        # Mostrar
        self.show()

    def get_path(self):
        text = self.line_edit_path.text()
        if isinstance( text, str ):
            path = pathlib.Path( text )
            exists = path.exists()
            good_path = False
            if exists:
                if self.mode == "dir" and path.is_dir():
                    good_path = True
                if self.mode == "file" and path.is_file():
                    good_path = True

            if good_path:
                return path
        else:
            return None

    def on_set_path(self):
        if self.mode == "dir":
            path = QFileDialog.getExistingDirectory(
                self.parent, self.text_dict['path'], self.line_edit_path.text()
            )
            if path:
                self.line_edit_path.setText( str( pathlib.Path(path) ) )
        elif self.mode == "file":
            path, ok = QFileDialog.getOpenFileName(
                self.parent, self.text_dict['path'], self.line_edit_path.text(), self.glob_file_prefix
            )
            if path and ok:
                self.line_edit_path.setText( str( pathlib.Path(path) ) )

    def on_ok(self):
        '''
        Solo si existe el path, y cumple con el mode, aceptar, de lo contrario, solo cerrar.
        '''
        path = self.get_path()
        if path is not None:
            self.accept()
        else:
            self.close()

