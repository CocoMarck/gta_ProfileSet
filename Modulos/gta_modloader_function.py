from Modulos.Modulo_System import *
from Modulos.Modulo_Files import *
from Modulos.Modulo_Language import *
from Modulos.Modulo_Text import *
from pathlib import Path as pathlib
import os, subprocess


dir_main = pathlib().absolute()

exe_gta_sa = os.path.join(dir_main, 'gta_sa.exe')

dir_modloader = os.path.join( dir_main, 'modloader' )
modloader_file = os.path.join( dir_modloader, 'modloader.ini' )
encoding = 'utf-8'




def execute_game():
    '''
    Ejecutar juego
    '''
    if os.path.isfile(exe_gta_sa):
        subprocess.Popen(exe_gta_sa)




def get_text_modloader(mode_list=False):
    if os.path.isfile( modloader_file ):
        #print('Existe el archivo')

        text_ini = Text_Read(
            file_and_path=modloader_file,
            option='ModeText',
            encoding=encoding
        )
        #with open( modloader_file, 'r', encoding='utf-8') as text:
        #    pass#text_ini = text.read()
        if mode_list == True:
            text_ini = text_ini.split('\n')
        return text_ini
    else:
        #print( 'No existe el archivo' )
        return None
#text_ini = get_text_modloader()
#text_ini_list = get_text_modloader(mode_list=True)




'''
Obtener perfil actual
'''
def get_current_profile(more_text=False):
    profile = None
    text_ini = get_text_modloader()
    if not text_ini == None:
        text_ready = ''
        for line in text_ini.split('\n'):
            if (
                line.startswith('Profile')
            ):
                line_text = Ignore_Comment(line, ';').replace(' ','')
                line_profile = line_text.split('=')
                profile = line_profile[1]
    if more_text == True and (not profile == None):
        return f'{get_text("current_profile")}: {profile}\n'
    else:
        return profile




'''
Obtener perfiles
Devuelve en una lista los perfiles
'''
def get_profiles():
    text_ini = get_text_modloader(mode_list=True)
    if not text_ini == None:
        profiles = []
        for line in text_ini:
            if line.startswith('[Profiles.'):
                line_text = Ignore_Comment(line, ';').replace(' ', '').replace('[', '').replace(']','')
                profile = line_text.split('.')
                if profile[2] == 'Config':
                    profiles.append(profile[1])
        return profiles
#print( get_profiles() )



'''
Cambiar perfil
Establece en el archivo "modloader.ini", el perfil "Profile=El_asignado"
'''
def set_profile(profile=None, text_ini=None):
    good_change = False
    text_ini = get_text_modloader(mode_list=True)
    if not text_ini == None:
        text_ready = ''
        for line in text_ini:
            if (
                line.startswith('Profile') and
                (not profile == None)
            ):
                line_text = Ignore_Comment(line, ';').replace(' ','')
                line_profile = line_text.split('=')
                #for text in line_profile:
                    #print( text )
                if line_profile[1] == profile:
                    pass
                else:
                    line = f'{line_profile[0]}={profile}'
                    good_change = True
                #print(line)
            text_ready += f'{line}\n'
        text_ready = text_ready[:-1]

    if good_change == True:
        with open(modloader_file, 'w', encoding=encoding) as text:
            text.write(text_ready)

        return text_ready
    else:
        return None



'''
Obtener los mods del juego
'''
def get_mods_dirs(path=False):
    # Devuelve en una lista las carpetas "main" en modloader
    all_files = Files_List( files='*', path=dir_modloader, remove_path=False)
    dirs = []
    for file in all_files:
        if os.path.isdir(file):
            file_ready = file.replace(dir_modloader, '')
            if get_system() == 'win':
                file_ready = file_ready.replace( '\\', '')
            else:
                file_ready = file_ready.replace( '/', '')

            if not file_ready.startswith('.'):
                add = True
            else:
                add = False

            if path == True:
                file_ready = file


            if add == True:
                dirs.append( file_ready )
    return dirs




def get_mods_files():
    import fnmatch
    # Devuelve en una lista "archivos.asi" y "archivos.cs"
    all_files_mods = get_mods_dirs(path=True)
    other_files = []
    for file_mod in all_files_mods:
        for name_dir, dirs, files in os.walk(file_mod):
            for file in files:
                if (
                    fnmatch.fnmatch(file, '*.asi') or
                    fnmatch.fnmatch(file, '*.cs')
                ):
                    other_files.append(file)
    return other_files
#print( get_current_profile() )
#print( get_mods_dirs() )
#print( get_mods_files() )
#input()




'''
Parametros del perfil
Estado actual de parametros
Activar o desactivar parametros
Obtener y establecer Archivos Ingnorados, Mods Ignorados, Mods Incluidos y Mods Excluidos
'''
def get_profile_parameters_line(profile=None, parameter=None):
    dict_parameter_number = {
        'Config':0,
        'Priority':0,
        'IgnoreFiles':0,
        'IncludeMods':0,
        'IncludeMods':0,
        'ExclusiveMods':0
    }
    number_line = 0
    text_ini = get_text_modloader(mode_list=True)
    for line in text_ini:
        if line.startswith('[Profiles.'):
            line_text = Ignore_Comment(line, ';').replace(' ', '').replace('[', '').replace(']','')
            profile_list = line_text.split('.')
            #print(profile_list)
            if profile == profile_list[1]:
                if profile_list[2] == 'Config':
                    dict_parameter_number['Config'] = number_line
                elif profile_list[2] == 'Priority':
                    dict_parameter_number['Priority'] = number_line
                elif profile_list[2] == 'IgnoreFiles':
                    dict_parameter_number['IgnoreFiles'] = number_line
                elif profile_list[2] == 'IgnoreMods':
                    dict_parameter_number['IgnoreMods'] = number_line
                elif profile_list[2] == 'IncludeMods':
                    dict_parameter_number['IncludeMods'] = number_line
                elif profile_list[2] == 'ExclusiveMods':
                    dict_parameter_number['ExclusiveMods'] = number_line
        number_line += 1

    if parameter == None:
        return dict_parameter_number
    else:
        for key in dict_parameter_number.keys():
            if parameter == key:
                return dict_parameter_number[parameter]




def get_profile_parameter_Config(profile=None):
    profile_line = get_profile_parameters_line(profile=profile, parameter='Config')

    dict_parameters = {
        'IgnoreAllMods':None,
        'ExcludeAllMods':None
    }
    text_ini_list = get_text_modloader(mode_list=True)
    if profile_line > 0:
        number = 0
        loop = True
        while loop:
            number += 1
            if profile_line+number < len(text_ini_list):
                line_text = Ignore_Comment( text_ini_list[profile_line+number], ';' )
                if line_text.startswith('IgnoreAllMods'):
                    true_or_false = line_text.replace(' ', '').split('=')[1].lower()
                    if true_or_false == 'true':
                        dict_parameters['IgnoreAllMods'] = True
                    else:
                        dict_parameters['IgnoreAllMods'] = False

                elif line_text.startswith('ExcludeAllMods'):
                    true_or_false = line_text.replace(' ', '').split('=')[1].lower()
                    if true_or_false == 'true':
                        dict_parameters['ExcludeAllMods'] = True
                    else:
                        dict_parameters['ExcludeAllMods'] = False

                if (
                    (not dict_parameters['IgnoreAllMods'] == None) and
                    (not dict_parameters['ExcludeAllMods'] == None)
                ):
                    loop = False
            else:
                loop = False

    return dict_parameters




def get_profile_parameter_listMods(profile=None, parameter='IgnoreFiles'):
    '''
    Listar los mods que contenga algun parametro del perfil
    '''
    profile_line = get_profile_parameters_line( profile=profile, parameter=parameter )

    list_IgnoreFiles = []
    text_ini_list = get_text_modloader(mode_list=True)
    if profile_line > 0:
        number = 0
        loop = True
        while loop:
            number += 1
            if (profile_line+number) < len(text_ini_list):
                line_text = Ignore_Comment( text_ini_list[profile_line+number], ';' )#.replace(' ', '')
                if line_text.startswith('[Profiles.'):
                    loop = False
                elif line_text == '':
                    pass
                else:
                    list_IgnoreFiles.append(line_text)
            else:
                loop = False
    return list_IgnoreFiles
#print( get_profile_parameters_line(profile='Default') )
#print( get_profile_parameter_Config(profile='Default') )
#print( get_profile_parameter_listMods(profile='Default', parameter='IgnoreFiles') )
#print( get_profile_parameter_listMods(profile='Default', parameter='IgnoreMods') )
#print( get_profile_parameter_listMods(profile='Default', parameter='IncludeMods') )
#input()




# Agregar O remover Mods al parametro de im perfil
def add_or_remove_mod(profile=None, parameter=None, mod_file=None, option='add'):
    '''
    Agregar Mod en algun parametro de un perfil
    '''
    # Listar mods
    # add: agregar todos los mods, agregando "mod_file".
    # remove: agergar todos los mods anteriores, pero remover el "mod_file"
    list_mods = []

    add_mod = True
    for mod in get_profile_parameter_listMods(profile=profile, parameter=parameter):
        if mod.startswith(mod_file):
            add_mod = False
            if option == 'add':
                list_mods.append(mod)
            elif option == 'remove':
                pass
        else:
            list_mods.append(mod)

    if option == 'add':
        if add_mod == True:
            list_mods.append(mod_file)

    # Modloader | Detectar Lineas a ignorar
    number_parameter_start = get_profile_parameters_line(profile=profile, parameter=parameter)+1
    number = 0
    count_parameter_fin = True
    number_parameter_fin = 0
    modloader_ini = get_text_modloader(mode_list=True)
    for line in modloader_ini:
        if number > number_parameter_start:
            line = Ignore_Comment( line, ';' )
            if count_parameter_fin == True:
                if not line.startswith('[Profiles.'):
                    number_parameter_fin += 1
                else:
                    count_parameter_fin = False

        number += 1
    number_parameter_fin += number_parameter_start

    # Modloader | Agregar mod al IgnoreMods
    text_ready = ''
    number = 0
    for line in modloader_ini:
        # En la linea de inicio se agergaran los mods
        if number == number_parameter_start:
            add_line = False
            for mod in list_mods:
                text_ready += f'{mod}\n'
            text_ready += '\n\n'
        elif number > number_parameter_start:
            if number > number_parameter_fin:
                add_line = True
            else:
                add_line = False
        else:
            add_line = True

        if add_line == True:
            text_ready += f'{line}\n'
        number += 1

    text_ready = text_ready[:-1]
    with open(modloader_file, 'w', encoding=encoding) as text:
        text.write(text_ready)
    return text_ready

#print(
#    add_or_remove_mod(profile='Default', parameter='IgnoreFiles', mod_file='imfx.asi'),
#    add_or_remove_mod(profile='Default', parameter='ExclusiveMods', mod_file='imfx.asi'),
#)
#input()





def add_profile(profile=None):
    '''
    Agregar perfil, solo si no existe
    No incluir espacions
    No incluir caracteres especiales como ". ' @ : ;"
    '''
    if profile == '':
        profile == None
    else:
        profile = profile.replace(' ', '')
    list_profiles = get_profiles()
    modloader_ini = get_text_modloader()
    if not profile == None:
        go = True
        for a_profile in list_profiles:
            if a_profile == profile:
                go = False

        if go == True:
            text_ready = (
                modloader_ini +
                (
                '\n'
                f'[Profiles.{profile}.Config]\n'
                '\n'
                f'[Profiles.{profile}.Priority]\n'
                '\n'
                f'[Profiles.{profile}.IgnoreFiles]\n'
                '\n'
                f'[Profiles.{profile}.IgnoreMods]\n'
                '\n'
                f'[Profiles.{profile}.IncludeMods]\n'
                '\n'
                f'[Profiles.{profile}.ExclusiveMods]\n'
                )
            )
            with open(modloader_file, 'w', encoding=encoding) as text:
                text.write(text_ready)
            return True
#print( add_profile('Cacas') )
#print( add_profile('Default') )
#print( add_profile('Test') )
#input()




def remove_profile(profile=None):
    '''
    Borrar un perfil
    Solo se borra si el perfil existe y si no es "Default"
    '''
    list_profiles = get_profiles()

    if (
        (not profile == 'Default') and
        ( type(profile) == str )
    ):
        go = False
        for a_profile in list_profiles:
            if a_profile == profile:
                go = True

        if go == True:
            # Texto modloader
            modloader_ini = get_text_modloader(mode_list=True)

            # Inicio de linea del parametro y fin de lina del parametro
            list_number = [
                get_profile_parameters_line(profile=profile, parameter='Config'),
                get_profile_parameters_line(profile=profile, parameter='Priority'),
                get_profile_parameters_line(profile=profile, parameter='IgnoreFiles'),
                get_profile_parameters_line(profile=profile, parameter='IgnoreMods'),
                get_profile_parameters_line(profile=profile, parameter='IncludeMods'),
                get_profile_parameters_line(profile=profile, parameter='ExclusiveMods'),
            ]
            start_number = min(list_number)
            limit_number = max(list_number)

            # Agregar solo el texto, pero excluir el del parametro removido
            text_ready = ''
            number = 0
            for line in modloader_ini:
                if number >= start_number:
                    if not number <= limit_number:
                        text_ready += f'{line}\n'
                else:
                    text_ready += f'{line}\n'
                number += 1
            text_ready = text_ready[:-1]

            with open(modloader_file, 'w', encoding=encoding) as text:
                text.write(text_ready)

            return True
#print( get_profile_parameter_listMods(profile='Default', parameter='Priority') )
#print( remove_profile('Cacas') )
#input()
