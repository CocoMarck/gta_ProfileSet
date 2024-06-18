from Modulos.Modulo_System import *
from Modulos.Modulo_Files import *
from Modulos.Modulo_Language import *
from Modulos.Modulo_System import *
from Modulos.Modulo_ShowPrint import *
from Modulos.Modulo_Text import *
from pathlib import Path as pathlib
import os, subprocess


dir_main = pathlib().absolute()

exe_gta_sa = os.path.join(dir_main, 'gta_sa.exe')

dir_modloader = os.path.join( dir_main, 'modloader' )
modloader_file = os.path.join( dir_modloader, 'modloader.ini' )


if os.path.isfile( modloader_file ):
    #print('Existe el archivo')

    text_ini = Text_Read(
        file_and_path=modloader_file,
        option='ModeText',
        encoding="utf-8"
    )
    #with open( modloader_file, 'r', encoding='utf-8') as text:
    #    pass#text_ini = text.read()
    #text_ini = Ignore_Comment(text=text_ini, comment=';')
else:
    #print( 'No existe el archivo' )
    text_ini = None




'''
Obtener perfiles
Devuelve en una lista los perfiles
'''
def get_profiles():
    if not text_ini == None:
        profiles = []
        for line in text_ini.split('\n'):
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
    if not text_ini == None:
        text_ready = ''
        for line in text_ini.split('\n'):
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
        with open(modloader_file, 'w') as text:
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
print( get_mods_dirs() )
print( get_mods_files() )
input()




'''
Ejecutar juego
'''
def execute_game():
    if os.path.isfile(exe_gta_sa):
        subprocess.Popen(exe_gta_sa)




# Menu Loop
menu_title = Title('Modloader Set Profile',print_mode=False)
menu_options = ''
dict_profiles = {}
number = 1
for profile in get_profiles():
    menu_options += f'{number}. {profile}\n'
    dict_profiles.update( {number:profile} )
    number += 1
menu_options += f'X. {get_text("enter_to_start")}\n\n'

loop = True
while loop:
    # Mostrar Opciones y establecer opcion
    CleanScreen()
    try:
        option = int(input(
            menu_title +
            menu_options +
            f'{ get_text("option") }: '
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
        #if option_continue == YesNo('yes'):
        #    option_continue = True
        #elif option_continue == YesNo('no'):
        #    option_continue = False
        if option_continue == True:
            set_profile( profile=dict_profiles[option], text_ini=text_ini )
            execute_game()
            loop = False
        else:
            pass
    else:
        execute_game()
        loop = False
