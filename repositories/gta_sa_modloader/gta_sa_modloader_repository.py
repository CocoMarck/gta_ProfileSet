from core.text_util import read_text, ignore_comment
import pathlib


# Values
MAX_PRIORITY = 100

# Prefix's
MODLOADER_FILE_NAME_PREFIX = 'modloader.ini'
FOLDER_CONFIG_PREFIX = '[Folder.Config]'
ENCODING_PREFIX = 'utf-8'
DEFAULT_PROFILE_PREFIX = 'Default'


class GTASAModloaderRepository:
    def __init__(self, gta_sa_dir:pathlib.Path):
        self.gta_sa_dir = gta_sa_dir
        self.gta_sa_file = self.gta_sa_dir.joinpath( 'gta_sa.exe' )
        self.modloader_dir = self.gta_sa_dir.joinpath( 'modloader' )
        self.modloader_file = self.modloader_dir.joinpath( MODLOADER_FILE_NAME_PREFIX )


    def get_text_lines(self):
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
        for line in self.get_text_lines():
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

        return profile


    def get_profiles(self):
        '''
        Obtener perfiles. Devuelve una lista de los perfiles.
        '''
        profiles = []
        for line in self.get_modloader_text_lines():
            if line.startswith('[Profiles.'):
                text_line = ignore_comment(
                    line, ';'
                ).replace(' ', '').replace('[', '').replace(']','')
                profile = text_line.split('.')
                if profile[2] == 'Config':
                    profiles.append( profile[1] )
        return profiles
