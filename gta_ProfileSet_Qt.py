from Modulos.gta_modloader_function import *
from Modulos.Modulo_Language import get_text
import sys, os
from functools import partial
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt


# Establecer dimenciones de windegts y ventana
# Limite de resolucion: Anchura y altura de 480px como minimo.
display = get_display_resolution()

def get_display_number(multipler=0, divisor=0, based='width'):
    if based == 'width':
        base = display[0]
    else:
        base = display[1]

    lim_max = int( max(display)*0.75 )
    lim_min = 8

    number = None
    if multipler > 0:
        number = base*multipler
    else:
        if divisor > 0:
            number = base/divisor

    if not number == None:
        if number > lim_max:
            return lim_max
        elif number < lim_min:
            return lim_min
        else:
            return int(number)


num_font = get_display_number(divisor=120)
num_space_padding = int(num_font/3)
nums_space_margin = [
    int(num_font/2),
    int(num_font/4)
]

nums_win_main = [
    get_display_number(multipler=0.3, based='width'),
    get_display_number(multipler=0.3, based='height')
]
nums_win_set_something = [
    get_display_number(multipler=0.25, based='width'),
    get_display_number(multipler=0.35, based='height')
]
nums_win_cfg_param = [
    get_display_number(multipler=0.25, based='width'),
    get_display_number(multipler=0.25, based='height')
]

'''
print(display)
print(num_font)
print(num_space_padding)
print(nums_space_margin)
print(nums_win_main)
print(nums_win_set_something)
print(nums_win_cfg_param)
'''



# Estilo de programa
style = (
    'QLabel {\n'
    f'font-size: {num_font}px;\n'

    f'margin-left: {nums_space_margin[0]}px;\n'
    f'margin-right: {nums_space_margin[0]}px;\n'
    f'margin-top: {nums_space_margin[1]}px;\n'
    f'margin-bottom: {nums_space_margin[1]}px;\n'
    '}\n'

    'QPushButton {\n'
    f'font-size: {num_font}px;\n'
    #f'margin: {nums_space_margin[0]}px;\n' # Espacio entre widgets
    f'margin-left: {nums_space_margin[0]}px;\n'
    f'margin-right: {nums_space_margin[0]}px;\n'
    f'margin-top: {nums_space_margin[1]}px;\n'
    f'margin-bottom: {nums_space_margin[1]}px;\n'

    f'padding: {num_space_padding}px;\n' # Size adicional para el widget

    #'border-radius: 8px;\n'
    #'border: 1px solid;\n'
    '}\n'


    'QLineEdit {\n'
    f'font-size: {num_font}px;\n'

    f'margin-left: {nums_space_margin[0]}px;\n'
    f'margin-right: {nums_space_margin[0]}px;\n'
    f'margin-top: {nums_space_margin[1]}px;\n'
    f'margin-bottom: {nums_space_margin[1]}px;\n'

    f'padding: {num_space_padding}px;\n' # Size adicional para el widget
    '}\n'
)




# Programa....
icon_gta_ProfileSet = os.path.join(dir_main, 'gta_ProfileSet.ico')



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
        self.setWindowIcon( QIcon(icon_gta_ProfileSet) )
        self.resize(nums_win_main[0], nums_win_main[1])

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

        button_start_game = QPushButton( get_text('start') )
        button_start_game.clicked.connect( self.start_game )
        vbox_main.addWidget( button_start_game )

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

    def start_game(self):
        # Ejecutar juego por hilo, subproceso. Sin salirse del launcher
        execute_game()


    def config_profile(self):
        # Dialogo de seleccion de perfil, y luego dialogo de configuracion de perfil
        #self.hide()

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

        #self.show()

    def set_profile(self):
        # Dialogo de seleccion de perfil, y establecer perfil
        #self.hide()

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

        #self.show()

    def add_profile(self):
        # Dialogo de texto para Agergar perfil
        #self.hide()

        profile, ok = QInputDialog.getText(
            self,
            get_text('set_profile'), # Titulo
            f"{get_text('profile')}:"
        )
        if ok and profile:
            # Agregar perfil, solo si se preciona ok y hay texto en el input
            add_profile( profile=profile )

        #self.show()


    def remove_profile(self):
        # Dialogo de Seleccionar y Remover perfil
        #self.hide()

        dialog_set_profile = Dialog_set_something(
            self, option='set_profile',list_mode=False
        )
        dialog_set_profile.exec()
        if not dialog_set_profile.selected_options == None:
            # Preguntar si remover o no
            message_question = QMessageBox.question(
                self,
                get_text('remove'), # Titulo
                f"¿{get_text('remove')}?", # Pregunta
                QMessageBox.StandardButton.Yes |
                QMessageBox.StandardButton.No
            )
            if message_question == QMessageBox.StandardButton.Yes:
                remove_profile( profile=dialog_set_profile.selected_options )

        #self.show()




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
        self.resize(nums_win_set_something[0], nums_win_set_something[1])

        self.__list_mode = list_mode

        # Establecer el continuar o no
        search = True
        list_options = None
        if option == 'set_profile':
            list_options = get_profiles()
        elif option == 'mods_files':
            list_options = not_repeat_item(
                abc_list( get_mods_files() )
            )
        elif option == 'mods_dirs':
            list_options = abc_list( get_mods_dirs() )
        elif option == 'set_parameter':
            list_options = [
                'Config',
                'Priority',
                'IgnoreFiles',
                'IgnoreMods',
                'IncludeMods',
                'ExclusiveMods'
            ]
            search = False

        elif (
            option == 'Priority' or
            option == 'IgnoreFiles' or
            option == 'IgnoreMods' or
            option == 'IncludeMods' or
            option == 'ExclusiveMods'
        ):
            list_options = abc_list(
                get_profile_parameter_listMods( profile=profile, parameter=option )
            )


        if list_options == []:
            list_options = None
            search = False

        # Contenedor principal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)

        # Scroll de botones
        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded,
        )
        self.scroll_area.setWidgetResizable(True) # Para centrer el scroll
        vbox_main.addWidget(self.scroll_area)

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
        self.scroll_area.setWidget(widget_buttons)


        # Seccion Vertical - Buscar y Seleccionar boton (mod)
        if search == True:
            self.line_edit = QLineEdit(self, placeholderText=get_text('option_search') )
            self.line_edit.textChanged.connect(self.select_button)
            vbox_main.addWidget(self.line_edit)


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

    def select_button(self):
        text = self.line_edit.text().lower()

        # Si el campo de texto esta vacio no hacer nada
        if not text:
            return

        # Recorrer los botones y seleccionar el mas cercano por inicial
        for button in self.__list_buttons:
            if button.text().lower().startswith(text):
                # Simular el clic en el boton que coincide
                button.setFocus()
                self.scroll_area.ensureWidgetVisible(button)
                self.line_edit.setFocus()
            else:
                pass


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
    Se establece la opcion selecionada
    '''
    def __init__(self, parent=None, profile=None, parameter=None):
        super().__init__(parent)

        if not parameter == 'Config':
            title = f'{ get_text(str(parameter)) } | {profile}'
        else:
            title = f'{ get_text("cfg") } | {profile}'
        self.setWindowTitle(title)
        self.resize( nums_win_cfg_param[0], nums_win_cfg_param[1] )

        # Opcion
        self.option = None
        self.__profile = profile
        self.__label_mods = QLabel()
        self.__parameter = parameter

        # Contenedor Principal
        vbox_main = QVBoxLayout()
        self.setLayout(vbox_main)

        # Scroll de opciones, solo si el parametro no es igual a 'Config'
        if not parameter == 'Config':
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
            hbox = QHBoxLayout()
            hbox.addStretch()

            self.__label_mods = QLabel( )
            self.__label_mods.setTextInteractionFlags( Qt.TextInteractionFlag.TextSelectableByMouse )
            self.set_label_mods()
            hbox.addWidget( self.__label_mods )

            hbox.addStretch()
            self.__widget_vbox_main.addLayout(hbox)

            # Scroll - Agregar el contenedor
            scroll_area.setWidget( self.__widget_buttons )


            # Seccion Vertical de boton de pioridad
            if parameter == 'Priority':
                self.__priority = True
                button_priority = QPushButton( get_text('cfg_priority') )
                button_priority.clicked.connect( self.change_priority )
                vbox_main.addWidget( button_priority )
            else:
                self.__priority = False

        else:
            # Opciones de conifguracion de perfil
            self.__dict_config_label = {}
            dict_config = get_profile_parameter_Config( profile=profile )
            for option in ['ExcludeAllMods', 'IgnoreAllMods', 'Parents']:
                hbox = QHBoxLayout()
                vbox_main.addLayout(hbox)

                button = QPushButton( get_text(option) )
                if option == 'ExcludeAllMods' or option == 'IgnoreAllMods':
                    button.setCheckable( True )
                    if not dict_config[option] == None:
                        button.setChecked( dict_config[option] )
                    button.clicked.connect( partial(self.change_config, option=option, button=button) )
                elif option == 'Parents':
                    button.clicked.connect( partial(self.change_config, option=option) )
                hbox.addWidget( button )
                hbox.addStretch()

                label = QLabel( str(dict_config[option]) )
                hbox.addWidget( label )

                self.__dict_config_label.update( {option:label} )

        # Seccion Vertical botones de agregar y remover, o cancelar.
        button_Cancel = False
        if (
            (not parameter == None) and
            (not parameter == 'Config')
        ):
            hbox = QHBoxLayout()
            for option in ['add', 'custom', 'remove']:
                hbox.addStretch()
                button = QPushButton( get_text(option) )

                button.clicked.connect( partial( self.add_or_remove, option=option) )

                hbox.addWidget(button)
                hbox.addStretch()

            vbox_main.addLayout(hbox)
        else:
            button_cancel = QPushButton( get_text('cancel') )
            button_cancel.clicked.connect( self.close )
            vbox_main.addWidget(button_cancel)

        # Mostrar todo
        self.show()

    def set_label_mods(
        self,
        list_mods=None
    ):
        # Establecer los mods en el label
        if list_mods == None:
            list_mods = get_profile_parameter_listMods( profile=self.__profile, parameter=self.__parameter)
            list_mods = abc_list( list=list_mods)
        text = ''
        if not list_mods == None:
            for mod in list_mods:
                text += f'{mod}\n'

        text = text[:-1]
        if not self.__label_mods == None:
            self.__label_mods.setText(text)

    def change_config(self, button=None, option=None):
        # Cambiar configuracion de perfil
        if option == 'ExcludeAllMods' or option == 'IgnoreAllMods':
            if not self.__dict_config_label[option].text() == 'None':
                if button.isChecked() == False:
                    value = True
                elif button.isChecked() == True:
                    value = False
                set_profile_parameter_Config( profile=self.__profile, option=option, value=value)
                self.__dict_config_label[option].setText( str(value) )
        elif option == 'Parents':
            # Abrir dialogo de texto y agregar o no texto a Parents
            try:
                parents, ok = QInputDialog.getText(
                    self,
                    get_text(option),
                    f"{get_text('text')}:"
                )
                if ok and parents:
                    # Establecer padres de perfil, solo si se preciona ok y hay texto
                    set_profile_parameter_Config( profile=self.__profile, option=option, value=parents )
                    self.__dict_config_label[option].setText( parents )
            except:
                # Mensaje de error
                QMessageBox.critical(
                    self,
                    'ERROR',
                    f"{get_text('error_admin')}\n{get_text('error_parameter')}"
                )

    def change_priority(self):
        # Cambiar pioridad
        set_mod = Dialog_set_something(
            self, option=self.__parameter, profile=self.__profile, list_mode=True
        )
        set_mod.exec()
        if not set_mod.selected_options == None:
            for mod in set_mod.selected_options:
                # Entrada de texto que solo permite numeros
                priority, ok = QInputDialog.getInt(
                    self,
                    get_text('Priority'),
                    f'{mod}:'
                )
                if ok and priority:
                    # Cambiar pioridad si se preciona ok, si hay un numero establecido
                    if priority > limit_priority:
                        priority = 100
                    elif priority < 1:
                        priority = 1
                    change_mod_priority( priority=priority, profile=self.__profile, mod_file=mod )

        # Actualizar labels
        self.set_label_mods()

    def add_or_remove(self, option='add'):
        set_mod = None

        # Agregar mods
        if option == 'add':
            if self.__parameter == 'IgnoreFiles':
                set_mod = Dialog_set_something( self, option='mods_files', list_mode=True )
            elif not self.__parameter == None:
                set_mod = Dialog_set_something( self, option='mods_dirs', list_mode=True )

            if not set_mod == None:
                set_mod.exec()
                if not set_mod.selected_options == None:
                    for mod in set_mod.selected_options:
                        add_or_remove_mod(
                            profile=self.__profile, parameter=self.__parameter, mod_file=mod,
                            option='add'
                        )

        # Agregar mod custom
        elif option == 'custom':
            text, ok = QInputDialog.getText(
                self,
                get_text('add'), # Titulo
                f"{get_text('text')}:"
            )
            if ok and text:
                # Agregar perfil, solo si se preciona ok y hay texto en el input
                add_or_remove_mod(
                    profile=self.__profile, parameter=self.__parameter, mod_file=text,
                    option='add'
                )


        # Remover mods
        elif option == 'remove':
            if not self.__parameter == None:
                set_mod = Dialog_set_something(
                    self, option=self.__parameter, profile=self.__profile, list_mode=True
                )
                set_mod.exec()
                if not set_mod.selected_options == None:
                    for mod in set_mod.selected_options:
                        add_or_remove_mod(
                            profile=self.__profile, parameter=self.__parameter, mod_file=mod,
                            option='remove'
                        )

        # Actualizar lista de mods
        self.set_label_mods()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet( style )
    app.setWindowIcon( QIcon(icon_gta_ProfileSet) ) # Establecer icono a todo
    test = test_to_pass()
    if test == True:
        window = Window_Main()
        sys.exit(app.exec())
    else:
        QMessageBox.critical(
            None,
            'ERROR',
            f'{test}',

        )
