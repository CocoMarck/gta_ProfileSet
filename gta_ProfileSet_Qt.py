from Modulos.gta_modloader_function import *
from Modulos.Modulo_Language import get_text
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt



class Window_Main(QWidget):
    '''
    Ventana main:
    Agregar o remover perfil
    Seleccionar perfil
    Configurar perfil
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('GTA Profile Set')
        #self.setWindowIcon( QIcon() )
        self.resize(256, -1)

        # Contenedor principal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)

        # Seccion vertical, mostrar perfil actual
        hbox = QHBoxLayout()
        hbox.addStretch()

        label = QLabel( f"{get_text('current_profile')}: {get_current_profile()}" )
        hbox.addWidget( label )

        hbox.addStretch()
        vbox_main.addLayout( hbox )



        # Secciones verticales - Botones
        button_config_profile = QPushButton( get_text('config_profile') )
        button_config_profile.clicked.connect( self.config_profile )
        vbox_main.addWidget( button_config_profile )

        button_set_profile = QPushButton( get_text('set_profile') )
        button_set_profile.clicked.connect( self.set_profile )
        vbox_main.addWidget( button_set_profile )

        # Seccion vertical - Agregar o remover perfil
        hbox = QHBoxLayout()
        hbox.addStretch()

        label = QLabel( get_text('add_or_remove') )
        hbox.addWidget(label)

        hbox.addStretch()
        vbox_main.addLayout( hbox )

        hbox = QHBoxLayout()
        hbox.addStretch()

        for option in ['add', 'remove']:
            button = QPushButton( get_text(option) )
            if option == 'add':
                button.clicked.connect( self.add_profile )
            elif option == 'remove':
                button.clicked.connect( self.remove_profile )
            hbox.addWidget(button)
            hbox.addStretch()
        vbox_main.addLayout(hbox)


        # Fin, mostrar todo lo contenido en la Ventana
        self.show()


    def config_profile(self):
        # Dialogo de seleccion de perfil, y luego dialogo de configuracion de perfil
        self.hide()
        set_profile = Dialog_set_something(
            self, option='set_profile', profile=None, list_mode=False
        )
        if set_profile.kill == False:
            set_profile.exec()
        else:
            set_profile.close()
        self.show()

    def set_profile(self):
        # Dialogo de seleccion de perfil, y establecer perfil
        self.hide()
        set_profile = Dialog_set_something(
            self, option='set_profile', profile=None, list_mode=False
        )
        if set_profile.kill == False:
            set_profile.exec()
        else:
            set_profile.close()
        self.show()

    def add_profile(self):
        # Dialogo de texto para Agergar perfil
        print( 'add' )

    def remove_profile(self):
        # Dialogo de Seleccionar y Remover perfil
        print('remove')




class Dialog_set_something( QDialog ):
    '''
    Selecionar cosas
    - Perfil
    - Parametro de un perfil
    - Mods en la carpeta modloader
    - Mods en los parametros de un perfil

    option=str
    Aqui se establece lo que se selecionara

    profile=str
    Si se elige selecionar algun parametro en "option", se necesita de este parametro "profile"

    list_mode=bool
    Establece si la seleccion podra ser de varias opciones o de solo una opcion.
    '''
    def __init__( self, parent=None, option='set_profile', profile=None, list_mode=True ):
        super().__init__(parent)

        self.setWindowTitle( get_text(option) )
        self.resize(308, -1)

        self.__list_mode = list_mode

        # Establecer el continuar o no
        list_options = None
        if option == 'set_profile':
            list_options = get_profiles()
        elif option == 'mods_files':
            list_options = get_mods_files()
        elif option == 'mods_dirs':
            list_options = get_mods_dirs()

        elif (
            option == 'Priority' or
            option == 'IgnoreFiles' or
            option == 'IgnoreMods' or
            option == 'IncludeMods' or
            option == 'ExcludeMods'
        ):
            list_options = get_profile_parameter_listMods( profile=profile, parameter=option )

        if list_options == []:
            list_options = None

        # Contenedor principal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)

        # Scroll de botones
        scroll_area = QScrollArea()
        scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded,
        )
        scroll_area.setWidgetResizable(True) # Para centrer el scroll
        vbox_main.addWidget(scroll_area)

        # Scroll - Contenedor de botones
        widget_buttons = QWidget()
        widget_vbox_main = QVBoxLayout()
        widget_buttons.setLayout(widget_vbox_main)

        # Scroll Layout - Botones
        self.__list_buttons = []
        if not list_options == None:
            for option in list_options:
                button = QPushButton( option )
                button.setCheckable( self.__list_mode )
                self.__list_buttons.append( button )
                widget_vbox_main.addWidget( button )

        # Scroll - Agregar el contenedor
        scroll_area.setWidget(widget_buttons)

        # Seccion vertical - Aceptar o cancelar
        self.selected_options = None
        hbox = QHBoxLayout()
        for option in ['ok', 'cancel']:
            hbox.addStretch()

            button = QPushButton( get_text(option) )
            hbox.addWidget( button )

            hbox.addStretch()
        vbox_main.addLayout(hbox)

        # Fin, mostrar ventana y sus widgets agregados
        self.show()

        # Cerrar o no
        if list_options == None:
            self.kill = True
        else:
            self.kill = False


if __name__ == '__main__':
    if test_to_pass() == True:
        app = QApplication(sys.argv)
        window = Window_Main()
        sys.exit(app.exec())
