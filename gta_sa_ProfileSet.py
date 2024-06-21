from Modulos.Modulo_System import *
from Modulos.Modulo_Language import *
from Modulos.Modulo_ShowPrint import *
from pathlib import Path as pathlib
import os, subprocess

from Modulos.gta_modloader_function import *




'''
Funcion que convierte texto a numero, o a una lista de numeros.
Solo si se escriben caracteres tipo numero, o el caracter "," o espacio " "
'''
def input_text_to_number(text='0', list_mode=True):
    # Solo se dovolveran numeros, el texto solo incluye estos caracteres
    only_include = '0123456789'
    character_coma = ','
    character_space = ' '
    only_include += character_coma
    only_include += character_space

    # Determinar si todos los caracteres, se incluyen en "only_include"
    # Determinar si hay comas, si las hay se listaran los numeros
    list_text = []
    for character in text:
        list_text.append(False)

    coma = False
    number = 0
    for character in text:
        for character_oi in only_include:
            if character_oi == character:
                list_text[number] = True
                if character == character_coma:
                    coma = True
        number += 1

    if coma == True and list_mode == False:
        coma = False
        text = text.replace(character_coma, '')

    input_good = True
    for bool in list_text:
        if bool == False:
            input_good = False

    # Devolver de texto a numero o no
    if input_good == True:
        text = text.replace(character_space, '')

        if text.replace(character_coma, '') == '':
            go = False
        else:
            go = True

        if go == True:
            if coma == True:
                numbers = []
                for number in text.split(character_coma):
                    numbers.append( int(number) )

                return numbers
            else:
                return int(text)
        else:
            return None
    else:
        return None
#print(
#    input_text_to_number(),
#    input_text_to_number('8, 20, 30'),
#    input_text_to_number('32, 54, 80', list_mode=False)
#)
#input()




# Texto que sera reutilizado por varias funciones
option_text_input = f'{ get_text("option") }: '


'''
Menu seleccionar perfil
'''
def menu_set_profile():
    menu_title = Title(f'Modloader {get_text("set_profile")}',print_mode=False)
    menu_profiles = ''
    dict_profiles = {}
    number = 1
    for profile in get_profiles():
        menu_profiles += f'{number}. {profile}\n'
        dict_profiles.update( {number:profile} )
        number += 1

    loop = True
    while loop:
        # Mostrar Opciones y establecer opcion
        CleanScreen()
        try:
            option = int(input(
                menu_title +
                get_current_profile(more_text=True) +
                menu_profiles +
                option_text_input
            ))
        except:
            option = -1


        # Verificar que la opcion sea correcta.
        go = False
        for profile in dict_profiles.keys():
            if option == profile:
                go = True


        # Establecer perfil o no
        if go == True:
            option_continue = Continue()
            if option_continue == True:
                loop = False
                return dict_profiles[option]
            else:
                pass
        else:
            loop = False
            CleanScreen()
            Continue(
                text=f'{get_text("option")}: {option}',
                message_error=True
            )
            #input(
            #    'ERROR\n'+
            #    f"{get_text('continue_enter')}..."
            #)
            return None




'''
Menu Seleccionar Capetas o archivos de Mods
'''
def menu_set_bool():
    pass


def menu_set_mods_files(profile=None, parameter=None):
    menu_title = Title( f"{get_text('select')}: {get_text('mods_files')}", print_mode=False)
    menu_options = ''
    dict_mods_files = {}
    number = 1
    for mod in get_mods_files():
        dict_mods_files.update( { number: mod } )
        menu_options += f'{number}. {mod}\n'
        number += 1

    # Loop
    loop = True
    while loop:
        CleanScreen()
        option = input_text_to_number(
            input(
                menu_title +
                menu_options +
                option_text_input
            )
        )
        if type(option) == list:
            mode_list = True
            selected_option = []
            for number in option:
                for key in dict_mods_files.keys():
                    if number == key:
                        selected_option.append( dict_mods_files[number] )
        else:
            mode_list = False
            selected_option = None
            if not(option) == None:
                for key in dict_mods_files.keys():
                    if option == key:
                        selected_option = dict_mods_files[option]


        # Establecer Archivos de Mods
        if mode_list == True:
            if not selected_option == []:
                for mod in selected_option:
                    set_profile_parameter_mod(
                        profile=profile, parameter=parameter, mod_file=mod
                    )
        else:
            if not selected_option == None:
                set_profile_parameter_mod(
                    profile=profile, parameter=parameter, mod_file=selected_option
                )
        print(
            selected_option, '\n',
            option
        )
        loop = False




def menu_set_mods_dirs(profile=None):
    pass




'''
Manu Configurar perfil
'''
def menu_config_profile():
    profile = menu_set_profile()
    if not profile == None:
        menu_title = Title(f"Modloader {get_text('config_profile')}", print_mode=False)
        dict_options = {
            1: 'config_bools',
            2: 'IgnoreFiles',
            3: 'IgnoreMods',
            4: 'IncludeMods',
            5: 'ExclusiveMods',
            0: 'back'
        }
        menu_options = ''
        for option in dict_options.keys():
            menu_options += f"{option}. { get_text(dict_options[option]) }\n"
        loop = True
        while loop:
            # Mostrar Opciones
            CleanScreen()
            try:
                option = int(input(
                    menu_title +
                    menu_options +
                    option_text_input
                ))
            except:
                option = -1

            # Verificar que la Opcion este correta
            go = False
            for key in dict_options.keys():
                if option == key:
                    go = True

            # Accionar opcion
            if go == True:
                option = dict_options[option]
                if not option == 'back':
                    if option == 'config_bools':
                        input( get_profile_parameter_Config(profile=profile) )
                    else:
                        if (
                            option == 'IgnoreFiles'
                        ):
                            menu_set_mods_files(profile=profile, parameter=option)
                        else:
                            for x in get_mods_dirs():
                                print( x )
                        input( get_profile_parameter_listMods(profile=profile, parameter=option) )
                else:
                    loop = False




# Menu Loop
menu_title = Title(f'GTA Profile Set',print_mode=False)
dict_options = {
    1 : 'set_profile',
    2 : 'config_profile',
    0 : 'exit'
}
menu_options = ''
for option in dict_options.keys():
    menu_options += f'{option}. {get_text( dict_options[option] )}\n'


loop = True
while loop:
    # Mostrar Opciones y establecer opcion
    CleanScreen()
    try:
        option = int(input(
            menu_title +
            get_current_profile(more_text=True) +
            menu_options +
            option_text_input
        ))
    except:
        option = -1



    # Establecer opcion.
    go = False
    for dict_option in dict_options.keys():
        if option == dict_option:
            go = True

    if go == True:
        option = dict_options[option]
        if option == 'set_profile':
            profile = menu_set_profile()
            if not set_profile( profile=profile, text_ini=get_text_modloader() ) == None:
                exec_and_exit = Continue(
                    get_current_profile(more_text=True) +
                    f'{get_text("exit_and_exec_game")}?'
                )
                if exec_and_exit == True:
                    loop = False
                    execute_game()
                else:
                    pass
        elif option == 'config_profile':
            menu_config_profile()
        elif option == 'exit':
            loop = False
    else:
        pass

