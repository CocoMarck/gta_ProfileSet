from core.text_util import ignore_comment
from .text_repository import TextRepository


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

IGNORE_ALL_MODS_PARAMETER = "IgnoreAllMods"
EXCLUDE_ALL_MODS_PARAMETER = "ExcludeAllMods"
PARENTS_PARAMETER = "Parents"

PROFILE_CONFIG_PARAMETERS = [
    IGNORE_ALL_MODS_PARAMETER, EXCLUDE_ALL_MODS_PARAMETER, PARENTS_PARAMETER
]

# Limites
MAX_PRIORITY = 100

# Default
DEFAULT_PRIORITY = 50
DEFAULT_PROFILE = 'Default'


class ProfileRepository():
    def __init__(self, text_repository: TextRepository):
        self.text_repository = text_repository

    def is_profile_section( self, line ):
        return line.startswith( f'[{DOMAIN_PROFILES}.' )

    def get_profiles(self):
        '''
        Obtener perfiles. Devuelve una lista de los perfiles.
        '''
        profiles = []
        for line in self.text_repository.get_lines():
            if self.is_profile_section( line ):
                text_line = ignore_comment(
                    line, ';'
                ).replace(' ', '').replace('[', '').replace(']','')
                profile = text_line.split('.')
                if profile[2] == 'Config':
                    profiles.append( profile[1] )
        return profiles

    # Insartar o acutalizar datos en sección de perfil
    def get_section_line_numbers( self, profile: str ):
        # sección, y su linea indefinida
        dict_section_line_numbers = {}
        for section in PROFILE_SECTIONS:
            dict_section_line_numbers.update( {section: None} )

        # Leer texto
        line_number = 0
        for line in self.text_repository.get_lines():
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


    def get_dict_values_section(self, profile, section):
        '''
        Diccionario, que establece donde poner los valores, con este diccinoario se puede construir el `modloader.ini`, con los cambios necesarios.
        '''
        # Obtener datos
        text_lines = self.text_repository.get_lines()
        dict_section_line_numbers = self.get_section_line_numbers( profile=profile )

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
                if self.is_profile_section( line ) and final_line_number == None:
                    final_line_number = line_number
                    break
                if line.replace(' ', '') != '':
                    dict_values_section['line_values'].append( line )
            line_number += 1
        the_section_is_the_final_line = line_number-1 == dict_section_line_numbers[section]

        # Despues de lineas de valores, las lineas finales
        if not the_section_is_the_final_line:
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
        return True

    def update_dict_values_section(self, dict_values_section, parameter_name, value):
        '''
        Actualizar parametro en sección especifica, en dicionario a construir como texto.
        '''
        index = 0
        for x in dict_values_section['line_values']:
            if x.startswith(parameter_name):
                dict_values_section['line_values'][index] = f'{parameter_name}={value}'
                return True
            index += 1
        return False

    def build_lines_dict_values_section(self, dict_values_section):
        '''
        Construir lineas de diccionario
        '''
        final_text_lines = []
        final_text_lines.extend( dict_values_section['first_lines'] )
        final_text_lines.extend( dict_values_section['line_values'] )
        final_text_lines.append( '' )
        final_text_lines.extend( dict_values_section['last_lines'] )

        return final_text_lines


    # Config
    def update_config(self, profile: str, parameter_name: str, value: bool):
        '''
        Actualizar parametro de configuración de perfil
        '''
        dict_values_section = self.get_dict_values_section(
            profile=profile, section=SECTION_CONFIG
        )
        update = False
        if parameter_name in PROFILE_CONFIG_PARAMETERS and isinstance(value, bool):
            update = self.update_dict_values_section(
                dict_values_section, parameter_name=parameter_name, value=str(value).lower()
            )

        if update:
            self.text_repository.write_lines(
                self.build_lines_dict_values_section( dict_values_section )
            )

        return update



    # Priority
    def filter_priority(self, value: int):
        if value > MAX_PRIORITY:
            value = MAX_PRIORITY
        elif value < 0:
            value = 0
        return value

    def insert_priority(
            self, profile: str, parameter_name: str, value: int = DEFAULT_PRIORITY
        ):
        '''
        Insertar parametro de pioridad de mod en perfil.
        '''
        dict_values_section = self.get_dict_values_section(
            profile=profile, section=SECTION_PRIORITY
        )
        insert = self.insert_dict_values_section(
            dict_values_section,
            value=f'{parameter_name}={self.filter_priority(value=value)}'
        )

        if insert:
            self.text_repository.write_lines(
                self.build_lines_dict_values_section( dict_values_section )
            )

        return insert

    def update_priority(
            self, profile: str, parameter_name: str, value: int
        ):
        '''
        Actualizar parametro de pioridad de mod en un perfil
        '''
        dict_values_section = self.get_dict_values_section(
            profile=profile, section=SECTION_PRIORITY
        )
        update = self.update_dict_values_section(
            dict_values_section, parameter_name=parameter_name, value=self.filter_priority(value)
        )

        if update:
            self.texte_repository.write_lines(
                self.build_lines_dict_values_section( dict_values_section )
            )

        return update
