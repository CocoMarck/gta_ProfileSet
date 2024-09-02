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
option_text_input = f'\n{ get_text("option") }: '




# Menu | Retornar texto
def menu_return_text( title=get_text('text') ):
    title = Title( text=title, print_mode=False)

    loop = True
    while loop:
        CleanScreen()
        option = input(
            title +
            f'{get_text("text")}: '
        )

        return_text = Continue()

        if return_text == True:
            if not option == '':
                loop = False
                return option
            else:
                loop = False
                return None
        else:
            loop = False
            return None




# Menu | Selecionar/Config/Remover | Perfil
def menu_set_something( profile=None, option='set_profile', set_mode='normal' ):
    '''
    Esta Menu puede:
    establecer un perfil
    configurar perfil
    remover perfil
    solo retornar el perfil.

    establecer mods o mod (directorio o archivo)
    '''

    change_title = False
    if option == 'return_profile':
        title = 'set_profile'
    else:
        title = option


    # Opcion seleccionada
    dict_options = {}
    text_options = ''
    list_options = []
    number = 0
    if (
        option == 'return_profile' or
        option == 'set_profile' or
        option == 'add_profile' or
        option == 'remove_profile' or
        option == 'config_profile'
    ):
        list_options = abc_list( get_profiles() )

    elif option == 'mods_files':
        list_options = not_repeat_item(
            abc_list( get_mods_files() )
        )
    elif option == 'mods_dirs':
        list_options = not_repeat_item(
            abc_list( get_mods_dirs() )
        )

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
        change_title = True
        title = f'{profile} | {option}'

    elif option == 'set_parameter':
        list_options = [
            'Config',
            'Priority',
            'IgnoreFiles',
            'IgnoreMods',
            'IncludeMods',
            'ExclusiveMods'
        ]
        change_title = True
        title = f'{profile} | {get_text(option)}'

    for item in list_options:
        number += 1
        dict_options.update( {number: item} )
        text_options += f'{number}. {item}\n'

    dict_options.update( {0: 'exit'} )
    text_options += f'0. {get_text("exit")}\n'

    prefix = option


    # Titulo
    if change_title == False:
        title = Title( get_text(title), print_mode=False )
    else:
        title = Title( title, print_mode=False )



    # Menu
    loop = True

    while loop:
        CleanScreen()
        try:
            if set_mode == 'normal':
                option = int(input(
                    title +
                    text_options +
                    option_text_input
                ))
            elif set_mode == 'list':
                option = input_text_to_number(
                    input(
                        title +
                        text_options +
                        option_text_input
                    )
                )
        except:
            option = -1

        # Determinar si la opcion es correcta
        go = False
        if option != -1:
            if type(option) == int:
                for key in dict_options.keys():
                    if option == key:
                        go = True
                        option = dict_options[option]

            elif type(option) == list:
                options = []
                for item in option:
                    for key in dict_options.keys():
                        if item == key:
                            go = True
                            options.append( dict_options[item] )
                option = options

        # Opcion
        if go == True:
            loop = False

            if not option == 'exit':
                if prefix == 'set_profile':
                    set_profile( option )

                elif prefix == 'config_profile':
                    menu_set_something( profile=option, option='set_parameter' )

                elif prefix == 'set_parameter':
                    menu_config_parameter( profile=profile, parameter=option )

                elif prefix == 'remove_profile':
                    remove_profile( option )

                return option




def menu_config_parameter(profile=None, parameter=None, set_mode='normal'):
    '''
    Para configurar un parametro de un perfil
    '''
    # Opciones
    dict_options = {}
    text_options = ''
    list_options = []
    if parameter == 'Config':
        dict_config = get_profile_parameter_Config( profile=profile )
        for key in dict_config.keys():
            list_options.append( key )
        change_options = []

        # Agregar opciones del parametro
        number = 4
        for item in list_options:
            number += 1
            dict_options.update( {number:item} )
            text_options += f'{number}. {item}={dict_config[item]}\n'

    elif (
        parameter == 'Priority' or
        parameter == 'IgnoreFiles' or
        parameter == 'IgnoreMods' or
        parameter == 'IncludeMods' or
        parameter == 'ExclusiveMods'
    ):
        change_options = ['add', 'remove', 'custom']
        list_options = get_profile_parameter_listMods( profile=profile, parameter=parameter )
        if parameter == 'Priority':
            change_options.append('cfg_priority')

        # Agregar opciones del parametro
        for item in list_options:
            text_options += f'{item}\n'

    # Opciones para agergar remover o cambiar mods.
    number = 0
    for item in change_options:
        number += 1
        dict_options.update( {number: item} )
        text_options += f'{number}. {get_text(item)}    '
    text_options += '\n'

    # Opcion salir
    dict_options.update( {0: 'exit'} )
    text_options += f'0. {get_text("exit")}\n'

    # Titulo
    title = Title( f'{profile} | {parameter}', print_mode=False )


    # Bucle
    loop = True
    while loop:
        # Mostrar menu de opciones
        CleanScreen()
        try:
            if set_mode == 'normal':
                option = int(input(
                    title +
                    text_options +
                    option_text_input
                ))
            else:
                option = input_text_to_number(text=input(
                    title +
                    text_options +
                    option_text_input
                ))
        except:
            option = -1

        # Verificar opcion
        go = False
        for key in dict_options:
            if option == key:
                go = True

        # Opcion seleccionada
        if go == True:
            option = dict_options[option]
            #input(option)

            if option == 'add':
                if parameter == 'IgnoreFiles':
                    mods = menu_set_something( profile=profile, option='mods_files', set_mode='list' )
                else:
                    mods = menu_set_something( profile=profile, option='mods_dirs', set_mode='list' )

            elif option == 'custom':
                mods = menu_return_text()

            elif option == 'remove':
                mods = menu_set_something( profile=profile, option=parameter, set_mode='list' )

            elif option == 'cfg_priority':
                mods = menu_set_something( profile=profile, option=parameter, set_mode='list' )
                if type(mods) == list:
                    for mod in mods:
                        CleanScreen()
                        Title( mod )
                        try:
                            number = int(input(
                                f"{get_text('priority_value')}: "
                            ))
                            change_mod_priority(priority=number, profile=profile, mod_file=mod)

                        except:
                            pass
                elif type(mods) == str:
                    CleanScreen()
                    Title( mods )
                    try:
                        number = int(input(
                            f"{get_text('priority_value')}: "
                        ))
                        change_mod_priority(priority=number, profile=profile, mod_file=mods)

                    except:
                        pass


            elif (
                option == 'IgnoreAllMods' or
                option == 'ExcludeAllMods' or
                option == 'Parents'
            ):
                dict_config = get_profile_parameter_Config(profile=profile)

                if not option == 'Parents':
                    value = None
                    if dict_config[option] == False:
                        value = True
                    elif dict_config[option] == True:
                        value = False
                else:
                    value = menu_return_text()
                set_profile_parameter_Config( profile=profile, option=option, value=value )

                # Opciones de menu
                list_options = []
                text_options = ''
                dict_config = get_profile_parameter_Config( profile=profile )
                for key in dict_config.keys():
                    list_options.append( key )
                number = 4
                for item in list_options:
                    number += 1
                    text_options += f'{number}. {item}={dict_config[item]}\n'
                text_options += '\n'
                text_options += f'0. {get_text("exit")}\n'


            elif option == 'exit':
                loop = False


            if option == 'custom' or option == 'remove' or option == 'add':
                if option == 'custom':
                    option = 'add'

                if type(mods) == list:
                    for mod in mods:
                        add_or_remove_mod( profile=profile, parameter=parameter, mod_file=mod, option=option )
                elif type(mods) == str:
                    add_or_remove_mod( profile=profile, parameter=parameter, mod_file=mods, option=option )



            if not change_options == []:
                # Actualizar opciones
                text_options = ''
                list_options = get_profile_parameter_listMods( profile=profile, parameter=parameter )
                for item in list_options:
                    text_options += f'{item}\n'

                # Opciones para agergar remover o cambiar mods.
                number = 0
                for item in change_options:
                    number += 1
                    dict_options.update( {number: item} )
                    text_options += f'{number}. {get_text(item)}    '
                text_options += '\n'

                text_options += f'0. {get_text("exit")}\n'




# Menu principal | Loop Principal
#python .\gta_ProfileSet_Shell-1.py
def menu_main():
    dict_options = {
        1:'start',
        2:'config_profile',
        3:'set_profile',
        4:'add_profile',
        5:'remove_profile',
        0:'exit'
    }
    text_options = ''
    for key in dict_options.keys():
        text_options += f'{key}. { get_text(dict_options[key]) }\n'
    title = Title('GTA Profile Set', print_mode=False)

    loop = True
    while loop:
        CleanScreen()
        try:
            option = int(input(
                title +
                f'{get_text("current_profile")}: {get_current_profile()}\n\n' +
                text_options +
                option_text_input
            ))
        except:
            option = -1

        go = False
        if option != -1:
            for key in dict_options.keys():
                if key == option:
                    go = True

        if go == True:
            option = dict_options[option]
            #input( option )

            if option == 'start':
                execute_game()

            elif option == 'config_profile':
                #menu_set_something( option=option )
                profile = menu_set_something( option='return_profile' )
                if type(profile) == str:
                    loop_config = True
                    while loop_config:
                        parameter = menu_set_something( profile=profile, option='set_parameter' )
                        if parameter == 'exit' or parameter == None:
                            loop_config = False
                        else:
                            pass

            elif option == 'set_profile':
                menu_set_something(option=option)

            elif option == 'add_profile':
                profile = menu_return_text( title=get_text(option) )
                if not profile == None:
                    add_profile( profile=profile )

            elif option == 'remove_profile':
                menu_set_something(option=option)

            elif option == 'exit':
                loop = False




if __name__ == '__main__':
    test = test_to_pass()
    if test == True:
        menu_main()
    else:
        input('ERROR - modloader.ini does not exist')
