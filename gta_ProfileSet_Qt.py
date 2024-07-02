from Modulos.gta_modloader_function import *
from Modulos.Modulo_Language import get_text
import sys
from functools import partial
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt



class Window_Main(QWidget):
    '''
    Ventana main:
    Configurar perfil
    Seleccionar perfil
    Agregar o remover perfil
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('GTA Profile Set')
        #self.setWindowIcon( QIcon() )
        self.resize(256, 1)

        # Contenedor principal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)


        # Seccion vertical, mostrar perfil actual
        hbox = QHBoxLayout()
        hbox.addStretch()

        self.label_current_profile = QLabel( f"{get_text('current_profile')}: {get_current_profile()}" )
        hbox.addWidget( self.label_current_profile )

        hbox.addStretch()
        vbox_main.addLayout( hbox )


        # Secciones verticales - Botones
        vbox_main.addStretch()

        button_config_profile = QPushButton( get_text('config_profile') )
        button_config_profile.clicked.connect( self.config_profile )
        vbox_main.addWidget( button_config_profile )

        button_set_profile = QPushButton( get_text('set_profile') )
        button_set_profile.clicked.connect( self.set_profile )
        vbox_main.addWidget( button_set_profile )


        # Seccion vertical - Agregar o remover perfil
        vbox_main.addStretch()

        hbox = QHBoxLayout()

        label = QLabel( f"{get_text('add_or_remove_profile')}: " )
        hbox.addWidget(label)

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
        dialog_set_profile = Dialog_set_something(
            self, option='set_profile', profile=None, list_mode=False
        )
        if dialog_set_profile.kill == False:
            dialog_set_profile.exec()
            if not dialog_set_profile.selected_options == None:
                # Establecer perfil
                profile = dialog_set_profile.selected_options
                dialog_set_profile.close()

                # Loop de establecer parametro
                loop = True
                while loop:
                    # Establecer parametro
                    dialog_set_parameter=Dialog_set_something(
                        self, option='set_parameter', profile=profile, list_mode=False
                    )
                    dialog_set_parameter.exec()
                    parameter = dialog_set_parameter.selected_options

                    # Configurar parametro, agregar mod o remover mod, cambiar pioridad de mod.
                    if not parameter == None:
                        dialog_config_parameter = Dialog_config_parameter(
                            self, profile=profile, parameter=parameter
                        )
                        dialog_config_parameter.exec()
                    else:
                        loop = False
            else:
                dialog_set_profile.close()
            self.show()

    def set_profile(self):
        # Dialogo de seleccion de perfil, y establecer perfil
        self.hide()
        dialog_set_profile = Dialog_set_something(
            self, option='set_profile', profile=None, list_mode=False
        )
        if dialog_set_profile.kill == False:
            dialog_set_profile.exec()
            if (
                ( not dialog_set_profile.selected_options == None ) and
                ( not dialog_set_profile.selected_options == get_current_profile() )
            ):
                # Preguntar si establecer o no, y luego establecer perfil
                set_profile(profile=dialog_set_profile.selected_options)
                self.label_current_profile.setText( get_current_profile(more_text=True) )
        else:
            dialog_set_profile.close()
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

        if profile == None:
            self.setWindowTitle( get_text(option) )
        else:
            self.setWindowTitle( f"{get_text(option)} | {profile}" )
        self.resize(308, 256)

        self.__list_mode = list_mode

        # Establecer el continuar o no
        list_options = None
        if option == 'set_profile':
            list_options = get_profiles()
        elif option == 'mods_files':
            list_options = get_mods_files()
        elif option == 'mods_dirs':
            list_options = get_mods_dirs()
        elif option == 'set_parameter':
            list_options = [
                'Priority',
                'IgnoreFiles',
                'IgnoreMods',
                'IncludeMods',
                'ExclusiveMods',
            ]

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
                if self.__list_mode == False:
                    button.clicked.connect( partial(self.set_option, button=button) )
                self.__list_buttons.append( button )
                widget_vbox_main.addWidget( button )

        # Scroll - Agregar el contenedor
        scroll_area.setWidget(widget_buttons)

        # Seccion vertical - Aceptar o cancelar
        self.selected_options = None
        hbox = QHBoxLayout()
        if list_mode == True:
            button_options = ['ok', 'cancel']
        else:
            button_options = ['cancel']

        for option in button_options:
            hbox.addStretch()

            button = QPushButton( get_text(option) )
            if option == 'ok':
                button.clicked.connect( self.set_option )
            elif option == 'cancel':
                button.clicked.connect( self.close )
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


    def set_option(self, button):
        # Establecer opciones selecionadas
        if self.__list_mode == True:
            # Si esta en modo lista, se estableceran todos los botones selecionados
            self.selected_options = []
            for btn in self.__list_buttons:
                if btn.isChecked() == True:
                    self.selected_options.append( btn.text() )

            if self.selected_options == []:
                self.selected_options = None

        else:
            # Si esta no esta en modo lista, se establecera el primer boton selecionado
            self.selected_options = button.text()

        self.close()




class Dialog_config_parameter(QDialog):
    '''
    Dialogo para seleccionar si agregar mod o remover mod en el parametro
    Dialogo para cambiar pioridad del mod.
    Se devuelve la opcion selecionada
    '''
    def __init__(self, parent=None, profile=None, parameter=None):
        super().__init__(parent)

        self.setWindowTitle(
            f'{ get_text(str(parameter)) } | {profile}'
        )
        self.resize( 436, 1 )

        # Opcion
        self.option = None
        self.__profile = profile
        self.__parameter = parameter

        # Contenedor Principal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)

        # Scroll de botones
        scroll_area = QScrollArea()
        scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        scroll_area.setWidgetResizable(True)
        vbox_main.addWidget(scroll_area)

        # Scroll - Contenedor de labels
        self.__widget_buttons = QWidget()
        self.__widget_vbox_main = QVBoxLayout()
        self.__widget_buttons.setLayout(self.__widget_vbox_main)

        # Scroll Layout - labels
        list_mods = get_profile_parameter_listMods( profile=self.__profile, parameter=self.__parameter )
        if list_mods == []:
            list_mods = None

        if not list_mods == None:
            for mod in get_profile_parameter_listMods( profile=self.__profile, parameter=self.__parameter ):
                hbox = QHBoxLayout()
                hbox.addStretch()

                label = QLabel(mod)
                hbox.addWidget( label )

                hbox.addStretch()
                self.__widget_vbox_main.addLayout(hbox)

        # Scroll - Agregar el contenedor
        scroll_area.setWidget( self.__widget_buttons )

        vbox_main.addStretch()

        # Seccion Vertical de boton de pioridad
        if parameter == 'Priority':
            self.__priority = True
            button_priority = QPushButton( get_text('cfg_priority') )
            button_priority.clicked.connect( self.change_priority )
            vbox_main.addWidget( button_priority )
        else:
            self.__priority = False

        # Seccion Vertical botones de agregar y remover, o cancelar.
        vbox_main.addStretch()
        if not parameter == None:
            hbox = QHBoxLayout()
            for option in ['add', 'remove']:
                hbox.addStretch()
                button = QPushButton( get_text(option) )

                if option == 'add':
                    button.clicked.connect( self.add )
                elif option == 'remove':
                    button.clicked.connect( self.remove )

                hbox.addWidget(button)
                hbox.addStretch()

            vbox_main.addLayout(hbox)
        else:
            button_cancel = QPushButton( get_text('cancel') )
            button_cancel.clicked.connect( self.colse )
            vbox_main.addWidget(button_cancel)

        # Mostrar todo
        self.show()

    def change_priority(self):
        self.option = 'change_priority'
        self.close()

    def add(self):
        # Agregar mods
        self.option = 'add'

        set_mod = None
        if self.__parameter == 'IgnoreFiles':
            set_mod = Dialog_set_something( self, option='mods_files', list_mode=True )
        elif not self.__parameter == None:
            set_mod = Dialog_set_something( self, option='mods_dirs', list_mode=True )

        if not set_mod == None:
            set_mod.exec()

    def remove(self):
        # Remover mods
        self.option = 'remove'

        set_mod = None
        if not self.__parameter == None:
            set_mod = Dialog_set_something(
                self, option=self.__parameter, profile=self.__profile, list_mode=True
            )
            set_mod.exec()



if __name__ == '__main__':
    if test_to_pass() == True:
        app = QApplication(sys.argv)
        window = Window_Main()
        sys.exit(app.exec())
