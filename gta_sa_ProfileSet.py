from Modulos.Modulo_System import *
from Modulos.Modulo_Language import *
from Modulos.Modulo_ShowPrint import *
from pathlib import Path as pathlib
import os, subprocess

from Modulos.gta_modloader_function import *




def input_text_to_number(text='0', list_mode=True):
    '''
    Funcion que convierte texto a numero, o a una lista de numeros.
    Solo si se escriben caracteres tipo numero, o el caracter "," o espacio " "
    '''
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




def menu_set_profile():
    '''
    Menu seleccionar perfil
    '''
    menu_title = Title( f'Modloader {get_text("set_profile")}', print_mode=False )
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




def menu_set_bool():
    '''
    Seleccionar el activar las opciones de excluir o ignorar todos los mods
    '''
    pass


def menu_add_mods(option='files'):
    '''
    Menu Seleccionar Capetas o archivos de Mods
    '''
    menu_title = Title(
        f"{get_text('select')}: {get_text(f'mods_{option}')}",
        print_mode=False
    )
    menu_options = ''
    dict_mods_files = {}
    number = 1
    if option == 'files':
        for mod in get_mods_files():
            dict_mods_files.update( { number: mod } )
            menu_options += f'{number}. {mod}\n'
            number += 1
    elif option == 'dirs':
        for mod in get_mods_dirs():
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


        # Devolver Archivos de Mods
        loop = False
        if mode_list == True:
            if selected_option == []:
                return None
            else:
                return selected_option
        else:
            return selected_option




def menu_add_or_remove_mod(profile=None, parameter=None):
    '''
    Menu para selecionar si agregar o remover mod
    '''
    # Texto para menu
    menu_title = Title(f"{get_text('add')} | {get_text('remove')}" ,print_mode=False)
    dict_options = {
        1:get_text('add'),
        2:get_text('remove'),
        0:get_text('back')
    }
    menu_options = ''
    for key in dict_options.keys():
        menu_options += f"{key}. {dict_options[key]}\n"

    menu_mods = ''
    if (
        (not parameter == None)and
        (not profile == None)
    ):
        menu_mods += 'Mods:\n'
        for mod in get_profile_parameter_listMods(profile=profile, parameter=parameter):
            menu_mods += f'{mod}\n'
        menu_mods += '\n'

    # Loop
    loop = True
    while loop:
        # Mostrar opciones
        CleanScreen()
        try:
            option = int(input(
                menu_title +
                menu_mods +
                menu_options +
                option_text_input
            ))
        except:
            option = -1

        # Verificar que la opcion seleccionada exista
        go = False
        for key in dict_options.keys():
            if key == option:
                go = True

        # Parar loop y Devolver agregar o remover.
        if go == True:
            loop = False
            if option == 1:
                return 'add'
            elif option == 2:
                return 'remove'
            elif option == 0:
                return None




def menu_config_profile():
    '''
    Manu Configurar perfil
    '''
    profile = menu_set_profile()
    if not profile == None:
        menu_title = Title(f"{get_text('config_profile')} | {profile}", print_mode=False)
        dict_options = {
            1: 'config_bools',
            2: 'Priority',
            3: 'IgnoreFiles',
            4: 'IgnoreMods',
            5: 'IncludeMods',
            6: 'ExclusiveMods',
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
                        # Menu elegir si agregar o remover mod
                        add_or_remove = menu_add_or_remove_mod(profile=profile, parameter=option)
                        mods = None

                        if not add_or_remove == None:
                            if (
                                option == 'IgnoreFiles'
                            ):
                                # Agregar mods archivos
                                mods = menu_add_mods('files')
                            else:
                                # Agregar mods tipo carpeta
                                mods = menu_add_mods('dirs')

                        # Agergar o remover mods
                        if (
                            add_or_remove == 'add' or add_or_remove == 'remove'
                        ):
                            if not mods == None:
                                if type(mods) == list:
                                    for mod in mods:
                                        add_or_remove_mod(
                                            profile=profile, parameter=option, mod_file=mod,
                                            option=add_or_remove
                                        )
                                else:
                                    add_or_remove_mod(
                                        profile=profile, parameter=option, mod_file=mods,
                                        option=add_or_remove
                                    )
                        input( get_profile_parameter_listMods(profile=profile, parameter=option) )
                else:
                    loop = False




def menu_add_or_remove_profile():
    '''
    Menu agregar o remover perfil
    '''
    menu_title = Title( get_text('add_or_remove_profile'), print_mode=False )
    dict_options = {
        1:'add',
        2:'remove',
        0:'back'
    }
    menu_options = ''
    for key in dict_options.keys():
        menu_options += f"{key}. {get_text(dict_options[key])}\n"

    # Loop
    loop = True
    while loop:
        CleanScreen()
        try:
            option = int(input(
                menu_title +
                menu_options +
                option_text_input
            ))
        except:
            option = -1

        # Verificar opcion correcta
        go = False
        for key in dict_options.keys():
            if key == option:
                go = True


        # Establecer opcion
        if go == True:
            option = dict_options[option]
            profile = None
            if option == 'add':
                CleanScreen()
                profile = input(
                    f"{get_text(option)}\n"
                    f"{get_text('profile')}: "
                )

            elif option == 'remove':
                profile = menu_set_profile()

            elif option == 'back':
                loop = False

            if not profile == None:
                if not profile == None:
                    CleanScreen()
                    if Continue(
                        menu_title +
                        f"{get_text(option)}?"
                    ) == True:
                        if option == 'add':
                            add_profile(profile=profile)
                        elif option == 'remove':
                            remove_profile(profile=profile)
            else:
                loop = False




def menu_execute_game(always_exec=True):
    '''
    Ejecutar juego
    always_exec, establece si siempre ejcutar aunque elijas no en el input "salir y ejecutar"
    '''
    CleanScreen()
    menu_title = Title( get_text('exec'), print_mode=False )
    exec_and_exit = Continue(
        menu_title +
        get_current_profile(more_text=True) +
        f'{get_text("exit_and_exec_game")}?'
    )
    if exec_and_exit == True:
        execute_game()
    else:
        if always_exec == True:
            execute_game()
    return exec_and_exit





# Menu Loop
def menu_main():
    '''
    El menu Main
    '''
    menu_title = Title( text=f'GTA Profile Set', print_mode=False)
    dict_options = {
        1 : 'start',
        2 : 'set_profile',
        3 : 'config_profile',
        4 : 'add_or_remove_profile',
        0 : 'exit'
    }
    menu_options = ''
    for option in dict_options.keys():
        menu_options += f'{option}. {get_text( dict_options[option] )}\n'


    loop = True
    while loop:
        # Mostrar Opciones y establecer opcion
        CleanScreen()
        option = int(input(
            menu_title +
            get_current_profile(more_text=True) +
            menu_options +
            option_text_input
        ))
        #try:
        #    option = int(input(
        #        menu_title +
        #        get_current_profile(more_text=True) +
        #        menu_options +
        #        option_text_input
        #    ))
        #except:
        #    option = -1



        # Verificar opcion
        go = False
        for dict_option in dict_options.keys():
            if option == dict_option:
                go = True

        # Establecer ocion
        if go == True:
            option = dict_options[option]
            if option == 'start':
                if menu_execute_game(True) == True:
                    loop = False

            elif option == 'set_profile':
                profile = menu_set_profile()
                if not profile == None:
                    set_profile( profile=profile, text_ini=get_text_modloader() )
                    if menu_execute_game(False) == True:
                        loop = False

            elif option == 'config_profile':
                menu_config_profile()

            elif option == 'add_or_remove_profile':
                menu_add_or_remove_profile()

            elif option == 'exit':
                loop = False
        else:
            pass


if __name__ == '__main__':
    menu_main()
