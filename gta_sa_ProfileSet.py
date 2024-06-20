from Modulos.Modulo_System import *
from Modulos.Modulo_Files import *
from Modulos.Modulo_Language import *
from Modulos.Modulo_ShowPrint import *
from Modulos.Modulo_Text import *
from pathlib import Path as pathlib
import os, subprocess

from Modulos.gta_modloader_function import *



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
                            print( get_mods_files() )
                        else:
                            print( get_mods_dirs() )
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
            if not set_profile == None:
                set_profile( profile=profile, text_ini=get_text_modloader() )
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

