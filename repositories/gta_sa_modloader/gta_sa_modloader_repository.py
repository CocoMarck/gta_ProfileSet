from core.text_util import read_text, ignore_comment
import pathlib


# Constantes
MAX_PRIORITY = 100

## Relación a los dominios y secciones del `modloader.ini`.
DOMAIN_FOLDER = 'Folder'
DOMAIN_PROFILES = 'Profiles'

SECTION_CONFIG = 'Config'
SECTION_PRIORITY = 'Priority'
SECTION_IGNORE_FILES = 'IgnoreFiles'
SECTION_IGNORE_MODS = 'IgnoreMods'
SECTION_INCLUDE_MODS = 'IncludeMods'
SECTION_EXCLUSIVE_MODS = 'ExclusiveMods'
PROFILE_SECTIONS = (
    SECTION_CONFIG, SECTION_PRIORITY, SECTION_IGNORE_FILES, SECTION_IGNORE_MODS,
    SECTION_INCLUDE_MODS, SECTION_EXCLUSIVE_MODS
)

## Relacionado con los archivos y el archivo de configuración
GTA_SA_FILENAME = 'gta_sa.exe'
MODLOADER_NAME = 'modloader'
MODLOADER_FILENAME = f'{MODLOADER_NAME}.ini'
ENCODING = 'utf-8'
DEFAULT_PROFILE = 'Default'




# La chamba
class GTASAModloaderRepository:
    def __init__(self, gta_sa_dir:pathlib.Path):
        self.gta_sa_dir = gta_sa_dir
        self.gta_sa_file = self.gta_sa_dir.joinpath( 'gta_sa.exe' )
        self.modloader_dir = self.gta_sa_dir.joinpath( MODLOADER_NAME )
        self.modloader_file = self.modloader_dir.joinpath( MODLOADER_FILENAME )


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
                encoding=ENCODING
            )

        return text_lines


    def build_folder_section(self, section ):
        return f'[{DOMAIN_FOLDER}.{section}]'

    def build_profile_section(self, profile, section ):
        return f'[{DOMAIN_PROFILES}.{profile}.{section}]'

    def is_profile_section( self, line ):
        return line.startswith( f'[{DOMAIN_PROFILES}.' )


    def get_folder_config_line_number(self):
        '''
        Obtener numero de linea, que sea [Folder.Config]. Solo primer coincidencia.
        '''
        folder_config_line_number = None
        line_number = 0
        for line in self.get_text_lines():
            if (
                line.replace(' ', '').startswith( self.build_folder_section(SECTION_CONFIG) ) and
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
            text_lines = self.get_text_lines()
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
        for line in self.get_text_lines():
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

    def format_profile(self, profile):
        return self.text_in_kebab_format( text=profile )


    def write_text_lines( self, lines ):
        with open(self.modloader_file, 'w', encoding=ENCODING) as text:
            text.writelines( lines )


    def write_profile(self, profile, formatted=False):
        '''
        Establecer profile. `Profile=profile`. Indicar si sera formateado o no.
        '''
        if formatted:
            profile = self.format_profile( profile=profile )

        text_changed = False
        ready_text = ''
        for line in self.get_text_lines():
            # Determinar cambio
            if (
                line.replace(' ', '').startswith('Profile=') and
                profile != None
            ):
                formatted_line = ignore_comment( line, ';' ).replace(' ', '')
                profile_line = formatted_line.split('=')
                if profile_line[1] != profile:
                    line = f'{profile_line[0]}={profile}'
                    text_changed = True
            ready_text += f'{line}\n'
        ready_text = ready_text[:-1]

        if text_changed:
            # Escibir texto
            with open(self.modloader_file, 'w', encoding=ENCODING) as text_file:
                text_file.write(ready_text)

        return text_changed


    def get_profile_section_line_numbers( self, profile: str ):
        # sección, y su linea indefinida
        dict_section_line_numbers = {}
        for section in PROFILE_SECTIONS:
            dict_section_line_numbers.update( {section: None} )

        # Leer texto
        line_number = 0
        for line in self.get_text_lines():
            if self.is_profile_section( line=line ):
                formatted_line = (
                    ignore_comment(line, ';').replace(' ', '').replace('[', '').replace(']','')
                )
                profile_list = formatted_line.split('.')
                if len(profile_list) == 3 and profile == profile_list[1]:
                    # Establecer numero de linea, si tiene el nombre de parametro.
                    if profile_list[2] in PROFILE_SECTIONS:
                        dict_section_line_numbers[ profile_list[2] ] = line_number
            line_number += 1

        return dict_section_line_numbers


    def get_profile_values_section(self, profile, section):
        '''
        Diccionario, que establece donde poner los valores, con este diccinoario se puede construir el `modloader.ini`, con los cambios necesarios.
        '''
        # Obtener datos
        text_lines = self.get_text_lines()
        dict_section_line_numbers = self.get_profile_section_line_numbers( profile=profile )

        # Primeras lineas, antes de escritura de valores
        dict_values_section = {
            'first_lines': [], 'line_values': [], 'last_lines': []
        }
        line_number = 0
        for line in text_lines:
            if line_number < dict_section_line_numbers[section]+1:
                dict_values_section['first_lines'].append( line )
                line_number += 1

        # Determinar lineas de escritura de valores
        line_number = 0
        final_line_number = None
        for line in text_lines:
            if line_number > dict_section_line_numbers[section]:
                if line.startswith( '[Profiles.' ) and final_line_number == None:
                    final_line_number = line_number
                    break
                if line.replace(' ', '') != '':
                    dict_values_section['line_values'].append( line )
            line_number += 1

        # Despues de lineas de valores, las lineas finales
        line_number = 0
        for line in text_lines:
            if line_number >= final_line_number:
                dict_values_section['last_lines'].append( line )
            line_number += 1

        # Retornar linea de valores a remplazar
        return dict_values_section


    def insert_dict_values_section(self, dict_values_section, value):
        '''
        Insertar valor en sección especifica, en dicionario a construir como texto.
        '''
        dict_values_section['line_values'].append( value )

        return dict_values_section

    def update_dict_values_section(self, dict_values_section, parameter_name, value):
        '''
        Actualizar parametro en sección especifica, en dicionario a construir como texto.
        '''
        index = 0
        for x in dict_values_section['line_values']:
            if x.startswith(parameter_name):
                dict_values_section['line_values'][index] = f'{parameter_name}={value}'
            index += 1

        return dict_values_section


