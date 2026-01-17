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
            line = self.text_repository.dismiss_comment( line )
            if line_number > dict_section_line_numbers[section]:
                if self.is_profile_section( line ) and final_line_number == None:
                    final_line_number = line_number
                    break
                if line.replace(' ', '') != '':
                    dict_values_section['line_values'].append( line )
            line_number += 1
        the_section_is_the_final_line = line_number-1 == dict_section_line_numbers[section]

        # Despues de lineas de valores, las lineas finales
        if not the_section_is_the_final_line and isinstance(final_line_number, int):
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
        if parameter_name in PROFILE_CONFIG_PARAMETERS:
            update = self.update_dict_values_section(
                dict_values_section, parameter_name=parameter_name, value=value
            )

        if update:
            self.text_repository.write_lines(
                self.build_lines_dict_values_section( dict_values_section )
            )

        return update

    def update_exclude_all_mods(self, profile: str, value: bool):
        update = False
        if isinstance(value, bool):
            update = self.update_config( profile, EXCLUDE_ALL_MODS_PARAMETER, str(value).lower() )
        return update

    def update_ignore_all_mods(self, profile: str, value: bool):
        update = False
        if isinstance(value, bool):
            update = self.update_config( profile, IGNORE_ALL_MODS_PARAMETER, str(value).lower() )
        return update

    def get_parents(self, profile: str):
        parents_value = ''
        for line in self.get_dict_values_section( profile, SECTION_CONFIG )['line_values']:
            if self.text_repository.detect_line_as_parameter( line, PARENTS_PARAMETER ):
                parents_value = line.split( '=' )[1]
                break
        return self.text_repository.str_to_list( parents_value )

    def write_parents(self, profile: str, values: list):
        '''
        Escribir padres herdados, solo insertar cuando no exista. Texto normalizado, para forzar coincidencias, y evitar bugs.
        '''
        write = False
        if isinstance(values, list):
            new_parents = []
            parents = self.get_parents( profile )
            for new_parent in values:
                if not ( self.text_repository.normalize_text(new_parent) in parents):
                    new_parents.append( new_parent )
            if new_parents != []:
                parents.extend(new_parents)
                count = 0
                for parent in parents:
                    if parent == '$None':
                        parents.pop( count )
                    count += 1
                write = self.update_config(
                    profile, PARENTS_PARAMETER, self.text_repository.list_to_str( parents )
                )
        return write

    def remove_parents(self, profile: str, values: list):
        '''
        Elimitar todos los padres heredados.
        '''
        remove = False
        if isinstance(values, list):
            parents = self.get_parents( profile )
            count = 0
            for parent in parents:
                if parent in values:
                    parents.pop( count )
                    remove = True
                count += 1
            if remove:
                remove = self.update_config(
                    profile, PARENTS_PARAMETER, self.text_repository.list_to_str( parents )
                )
        return remove

    def clear_parents(self, profile):
        remove = self.update_config( profile, PARENTS_PARAMETER, '$None' )
        return remove


    # Obtención de valores simples. Funciones genericas.
    def insert_simple_value(self, profile: str, section: str, value):
        '''
        Insertar valor simple a una seccion del perfil.
        '''
        dict_values_section = self.get_dict_values_section( profile, section )
        insert = self.insert_dict_values_section( dict_values_section, value=value )
        if insert:
            self.text_repository.write_lines(
                self.build_lines_dict_values_section( dict_values_section )
            )
        return insert

    def save_simple_value( self, profile: str, section: str, value:str ):
        '''
        Guardar valor simple a una sección del perfil
        '''
        dict_values_section = self.get_dict_values_section( profile, section )
        exists = self.exists_in_dict_values_section( dict_values_section, value )
        if not exists:
            return self.insert_simple_value( profile, section, value )
        else:
            return False

    def get_simple_values(self, profile:str, section:str ):
        '''
        Obtener valores simples
        '''
        return self.get_dict_values_section( profile, section )['line_values']

    def remove_simple_value(self, profile:str, section:str, value: str):
        '''
        Remover un valor simple
        '''
        dict_values_section = self.get_dict_values_section( profile, section )
        remove = False
        count = 0
        for line in dict_values_section['line_values']:
            if line == value:
                remove = True
                dict_values_section['line_values'].pop(count)
            count += 1
        if remove:
            self.text_repository.write_lines(
                self.build_lines_dict_values_section( dict_values_section )
            )
        return remove


    # Priority
    def filter_priority(self, value: int):
        if value > MAX_PRIORITY:
            value = MAX_PRIORITY
        elif value < 0:
            value = 0
        return value

    def exists_in_dict_values_section( self, dict_values_section, parameter_name ):
        '''
        Detectar si existe parametro en la sección del perfil.
        '''
        exists = False
        for x in dict_values_section['line_values']:
            if x.startswith( parameter_name ):
                exists = True
                break
        return exists

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

    def update_priority( self, profile: str, parameter_name: str, value: int ):
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
            self.text_repository.write_lines(
                self.build_lines_dict_values_section( dict_values_section )
            )

        return update

    def save_priority(
            self, profile: str, parameter_name: str, value:int = DEFAULT_PRIORITY
        ):
        '''
        Guardar o insertar parametro de pioridad de mod.
        '''
        dict_values_section = self.get_dict_values_section(
            profile=profile, section=SECTION_PRIORITY
        )
        exists = self.exists_in_dict_values_section(
            dict_values_section, parameter_name=parameter_name
        )
        if exists:
            return self.update_priority(
                profile=profile, parameter_name=parameter_name, value=value
            )
        else:
            return self.insert_priority(
                profile=profile, parameter_name=parameter_name, value=value
            )

    def get_priorities(self, profile: str):
        '''
        Obtener pioridades
        '''
        dict_values_section = self.get_dict_values_section( profile, SECTION_PRIORITY )
        dict_priorities = {}
        for line in dict_values_section['line_values']:
            split_line = line.split('=')
            dict_priorities.update( { split_line[0]: split_line[1] }  )
        return dict_priorities

    def remove_priority( self, profile: str, value: str ):
        return self.remove_simple_value( profile, SECTION_PRIORITY, value )


    # IgnoreFiles IgnoreMods IncludeMods ExclusiveMods
    def save_ignore_file( self, profile: str, value: str ):
        return self.save_simple_value( profile, SECTION_IGNORE_FILES, value )

    def remove_ignore_file( self, profile: str, value: str ):
        return self.remove_simple_value( profile, SECTION_IGNORE_FILES, value )

    def get_ignore_files(self, profile:str ):
        return self.get_simple_values( profile, SECTION_IGNORE_FILES )

    def save_ignore_mod( self, profile: str, value: str ):
        return self.save_simple_value( profile, SECTION_IGNORE_MODS, value )

    def get_ignore_mods(self, profile:str ):
        return self.get_simple_values( profile, SECTION_IGNORE_MODS )

    def save_include_mod( self, profile: str, value: str ):
        return self.save_simple_value( profile, SECTION_INCLUDE_MODS, value )

    def get_include_mods(self, profile:str ):
        return self.get_simple_values( profile, SECTION_INCLUDE_MODS )

    def save_exclusive_mod( self, profile: str, value: str ):
        return self.save_simple_value( profile, SECTION_EXCLUSIVE_MODS, value )

    def get_exclusive_mods(self, profile:str ):
        return self.get_simple_values( profile, SECTION_EXCLUSIVE_MODS )
