from core.system_util import get_system
from core.text_util import read_text, ignore_comment
import subprocess
import pathlib

from models.gta_sa_modloader import GTASAModloaderModel




# Prefix's
MODLOADER_FILE_NAME_PREFIX = 'modloader.ini'
FOLDER_CONFIG_PREFIX = '[Folder.Config]'
ENCODING_PREFIX = 'utf-8'
LIMIT_PRIORITY_PREFIX = 100
DEFAULT_PROFILE_PREFIX = 'Default'




def get_text( text ):
    return str(text)




# Controller
class GTASAModloaderController():
    def __init__(self, gta_sa_modloader_model: GTASAModloaderModel, gta_sa_dir:pathlib.Path ):
        self.model = gta_sa_modloader_model
        self.gta_sa_dir = gta_sa_dir
        self.gta_sa_file = self.gta_sa_dir.joinpath( 'gta_sa.exe' )
        self.modloader_dir = self.gta_sa_dir.joinpath( 'modloader' )
        self.modloader_file = self.modloader_dir.joinpath( MODLOADER_FILE_NAME_PREFIX )


    def get_modloader_text_lines(self):
        '''
        Obtener lineas de texto, del archivo `modlaoder.ini`
        '''
        text_lines = []
        if self.modloader_file.exists():
            # Leer el archivo, establecer lineas.
            text_lines = read_text(
                file_and_path=self.modloader_file,
                option='ModeList',
                encoding=ENCODING_PREFIX
            )

        return text_lines

    def get_folder_config_line_number(self):
        '''
        Obtener numero de linea, que sea [Folder.Config]. Solo primer coincidencia.
        '''
        folder_config_line_number = None
        line_number = 0
        text_lines = self.get_modloader_text_lines()
        for line in text_lines:
            if (
                line.replace(' ', '').startswith('[Folder.Config]') and
                folder_config_line_number == None
            ):
                folder_config_line_number = line_number
                break
            line_number += 1

        return folder_config_line_number

    def get_current_profile(self):
        '''
        Obtener perfil de configruación actual.
        '''
        folder_config_line_number = self.get_folder_config_line_number()
        profile = None

        if isinstance(folder_config_line_number, int):
            text_lines = self.get_modloader_text_lines()
            ready_text =  ''
            line_number = 0

            while True:
                # Establecer el texto del profile actual
                line_number += 1
                current_line_number = folder_config_line_number + line_number
                if current_line_number < len(text_lines):
                    text_line = ignore_comment(
                        text_lines[current_line_number], ';'
                    ).replace( ' ', '' )
                    if text_line.startswith( '[Profiles.' ):
                        break
                    elif text_line.startswith( 'Profile=' ):
                        profile = text_line.split('=')[1]
                        break
                else:
                    break
        self.model.profile = profile



    def get_profiles(self):
        '''
        Obtener perfiles. Devuelve una lista de los perfiles.
        '''
        profiles = []
        text_lines = self.get_modloader_text_lines()

        for line in text_lines:
            if line.startswith('[Profiles.'):
                text_line = ignore_comment(
                    line, ';'
                ).replace(' ', '').replace('[', '').replace(']','')
                profile = text_line.split('.')
                if profile[2] == 'Config':
                    profiles.append( profile[1] )
        return profiles


    def text_in_kebab_format(self, text):
        '''
        Formatear texto, tipo `kebab-case`
        '''
        return text.lower().replace(' ', '-')

    def formatted_profile(self):
        self.model.profile = self.text_in_kebeb_format( self.model.profile )


    def set_profile(self):
        '''
        Establecer profile. `Profile=profile`
        '''
        self.formatted_profile()
        text_lines = self.get_modloader_text_lines()
        text_changed = False
        ready_text = ''
        for line in text_lines:
            # Determinar cambio
            if (
                line.replace(' ', '').startswith('Profile=') and
                self.model.profile is not None and
                self.model.profile is not DEFAULT_PROFILE_PREFIX.lower() # Evita bugasos
            ):
                formatted_line = ignore_comment( line, ';' ).replace(' ', '')
                profile_line = formatted_line.split('=')
                if profile_line[1] is not self.model.profile:
                    line = f'{profile_line[0]}={self.model.profile}'
                    text_changed = True
            ready_text += f'{line}\n'
        ready_text = ready_text[:-1]

        if text_changed:
            # Escibir texto
            with open(self.modloader_file, 'w', encoding=ENCODING_PREFIX) as text_file:
                text_file.write(ready_text)

        return text_changed


