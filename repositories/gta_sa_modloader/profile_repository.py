from core.text_util import ignore_comment, abc_list, ignore_text_filter, PREFIX_ABC, PREFIX_NUMBER
from .text_repository import TextRepository
from config.constants import (
    DOMAIN_PROFILES, SECTION_CONFIG, SECTION_PRIORITY, SECTION_IGNORE_FILES, SECTION_IGNORE_MODS,
    SECTION_INCLUDE_MODS, SECTION_EXCLUSIVE_MODS, PROFILE_SECTIONS,  IGNORE_ALL_MODS_PARAMETER,
    EXCLUDE_ALL_MODS_PARAMETER, PARENTS_PARAMETER, PROFILE_CONFIG_PARAMETERS, EMPTY_VALUE,
    MAX_PRIORITY, DEFAULT_PRIORITY, DEFAULT_PROFILE
)
PROFILE_NAME_PREFIX = PREFIX_ABC + '-_' + PREFIX_NUMBER


class ProfileRepository():
    def __init__(self, text_repository: TextRepository):
        self.text_repository = text_repository

    def is_profile_section( self, line ):
        return line.startswith( f'[{DOMAIN_PROFILES}.' )

    def _normalize_profile(self, profile:str):
        return ignore_text_filter(
            self.text_repository.in_kebab_format( text=profile ), PROFILE_NAME_PREFIX
        )

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
        return abc_list(profiles) # En orden abecadario

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

        La determiniación de la sección como la linea final, estaba mal, ahora deberia jalar.
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
        selected_section_line_number = None
        for line in text_lines:
            line = self.text_repository.dismiss_comment( line )
            if line_number > dict_section_line_numbers[section]:
                if self.is_profile_section( line ) and selected_section_line_number == None:
                    selected_section_line_number = line_number
                    break
                if line.replace(' ', '') != '':
                    dict_values_section['line_values'].append( line )
            line_number += 1
        the_section_is_the_final_line = line_number == len(text_lines)

        # Despues de lineas de valores, las lineas finales
        if not the_section_is_the_final_line and isinstance(selected_section_line_number, int):
            line_number = 0
            for line in text_lines:
                if line_number >= selected_section_line_number:
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
        final_text_lines.extend( abc_list(dict_values_section['line_values']) ) # Ordenar en abecadrio
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

    def get_exclude_all_mods(self, profile: str):
        value = False
        for line in self.get_dict_values_section( profile, SECTION_CONFIG )['line_values']:
            line = line.replace(' ', '')
            if self.text_repository.detect_line_as_parameter( line, EXCLUDE_ALL_MODS_PARAMETER ):
                if line.split( '=' )[1] == 'true':
                    value = True
                break
        return value

    def update_ignore_all_mods(self, profile: str, value: bool):
        update = False
        if isinstance(value, bool):
            update = self.update_config( profile, IGNORE_ALL_MODS_PARAMETER, str(value).lower() )
        return update

    def get_ignore_all_mods(self, profile: str):
        value = False
        for line in self.get_dict_values_section( profile, SECTION_CONFIG )['line_values']:
            line = line.replace(' ', '')
            if self.text_repository.detect_line_as_parameter( line, IGNORE_ALL_MODS_PARAMETER ):
                if line.split( '=' )[1] == 'true':
                    value = True
                break
        return value

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
                if not new_parent in parents:
                    new_parents.append( new_parent )
            if new_parents != []:
                parents.extend(new_parents)
                count = 0
                for parent in parents:
                    if parent == EMPTY_VALUE:
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
            new_parents = []
            index_to_ignore = []
            parents = self.get_parents( profile )
            count = 0
            for parent in parents:
                if parent in values:
                    index_to_ignore.append(count)
                    remove = True
                count += 1
            for index in range( 0, len(parents)):
                if not (index in index_to_ignore):
                    new_parents.append( parents[index] )
            if remove:
                parents_str = self.text_repository.list_to_str( new_parents )
                if parents_str == '':
                    parents_str = EMPTY_VALUE
                remove = self.update_config(
                    profile, PARENTS_PARAMETER, parents_str
                )
        return remove

    def clear_parents(self, profile):
        remove = self.update_config( profile, PARENTS_PARAMETER, EMPTY_VALUE )
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
        index_to_ignore = []
        new_lines = []
        for line in dict_values_section['line_values']:
            if (
                self.text_repository.normalize_text(line) ==
                self.text_repository.normalize_text(value)
            ):
                remove = True
                index_to_ignore.append(count)
            count += 1
        for index in range(0, len(dict_values_section['line_values']) ):
            if not (index in index_to_ignore):
                new_lines.append( dict_values_section['line_values'][index] )
        dict_values_section['line_values'] = new_lines
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

    def build_priority(self, name, value):
        return f'{name}={self.filter_priority(value)}'

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
            value=self.build_priority( parameter_name, value )
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
        Obtener diccionario de pioridades
        '''
        dict_values_section = self.get_dict_values_section( profile, SECTION_PRIORITY )
        dict_priorities = {}
        for line in dict_values_section['line_values']:
            split_line = line.split('=')
            dict_priorities.update( { split_line[0]: int(split_line[1]) }  )
        return dict_priorities

    def remove_build_priority( self, profile: str, value: str ):
        return self.remove_simple_value( profile, SECTION_PRIORITY, value )

    def remove_priority(self, profile, parameter_name, value ):
        remove = False
        if isinstance(parameter_name, str) and isinstance( value, int):
            text = self.build_priority( parameter_name, value )
            remove = self.remove_build_priority( profile, text )
        return remove


    def get_priority_list(self, profile:str ):
        '''
        Obtener lista de lineas de pioridades.
        '''
        return self.get_simple_values( profile, SECTION_PRIORITY )


    # IgnoreFiles
    def save_ignore_file( self, profile: str, value: str ):
        return self.save_simple_value( profile, SECTION_IGNORE_FILES, value )

    def remove_ignore_file( self, profile: str, value: str ):
        return self.remove_simple_value( profile, SECTION_IGNORE_FILES, value )

    def get_ignore_files(self, profile:str ):
        return self.get_simple_values( profile, SECTION_IGNORE_FILES )

    # IgnoreMods
    def save_ignore_mod( self, profile: str, value: str ):
        return self.save_simple_value( profile, SECTION_IGNORE_MODS, value )

    def remove_ignore_mod( self, profile: str, value: str ):
        return self.remove_simple_value( profile, SECTION_IGNORE_MODS, value )

    def get_ignore_mods(self, profile:str ):
        return self.get_simple_values( profile, SECTION_IGNORE_MODS )

    # IncludeMods
    def save_include_mod( self, profile: str, value: str ):
        return self.save_simple_value( profile, SECTION_INCLUDE_MODS, value )

    def remove_include_mod( self, profile: str, value: str ):
        return self.remove_simple_value( profile, SECTION_INCLUDE_MODS, value )

    def get_include_mods(self, profile:str ):
        return self.get_simple_values( profile, SECTION_INCLUDE_MODS )

    # ExclusiveMods
    def save_exclusive_mod( self, profile: str, value: str ):
        return self.save_simple_value( profile, SECTION_EXCLUSIVE_MODS, value )

    def remove_exclusive_mod( self, profile: str, value: str ):
        return self.remove_simple_value( profile, SECTION_EXCLUSIVE_MODS, value )

    def get_exclusive_mods(self, profile:str ):
        return self.get_simple_values( profile, SECTION_EXCLUSIVE_MODS )

    # Profile moment
    def get_new_lines(self, profile: str):
        new_lines = [
            f'[{DOMAIN_PROFILES}.{profile}.{SECTION_CONFIG}]',
            f'{IGNORE_ALL_MODS_PARAMETER}=false',
            f'{EXCLUDE_ALL_MODS_PARAMETER}=false',
            f'{PARENTS_PARAMETER}={EMPTY_VALUE}',
            '',
            f'[{DOMAIN_PROFILES}.{profile}.{SECTION_PRIORITY}]',
            '',
            f'[{DOMAIN_PROFILES}.{profile}.{SECTION_IGNORE_FILES}]',
            '',
            f'[{DOMAIN_PROFILES}.{profile}.{SECTION_IGNORE_MODS}]',
            '',
            f'[{DOMAIN_PROFILES}.{profile}.{SECTION_INCLUDE_MODS}]',
            '',
            f'[{DOMAIN_PROFILES}.{profile}.{SECTION_EXCLUSIVE_MODS}]',
            '',
            '',
        ]
        lines = self.text_repository.get_lines()
        lines.extend( new_lines )
        return lines

    ## insert profile
    def insert(self, profile: str):
        '''
        Insertar perfil
        '''
        profile = self._normalize_profile( profile )
        lines = self.get_new_lines( profile )
        self.text_repository.write_lines( lines )
        return True

    ## renombrar profile
    def rename(self, profile: str, new_name: str):
        '''
        Renombrar pefil
        '''
        profiles = self.get_profiles()
        new_name = self._normalize_profile( new_name )
        rename = (
            not (new_name in profiles) and
            new_name != self._normalize_profile(DEFAULT_PROFILE)
        )
        if rename:
            profile_line_numbers = self.get_section_line_numbers( profile ).values()
            lines = self.text_repository.get_lines()
            for number in profile_line_numbers:
                lines[number] = lines[number].replace( profile, new_name )
            self.text_repository.write_lines( lines )
        return rename

    ## remove profile
    def remove(self, profile: str ):
        '''
        Remover pefil
        '''
        exists = (profile in self.get_profiles())
        is_the_default_profile = profile == DEFAULT_PROFILE
        remove = exists and (not is_the_default_profile)
        if remove:
            profile_line_numbers = self.get_section_line_numbers( profile ).values()
            min_profile_number = min(profile_line_numbers)
            max_profile_number =  max(profile_line_numbers)

            lines = self.text_repository.get_lines()
            count = 0
            number_of_lines_to_ignore = []
            for line in lines:
                in_range = count >= min_profile_number and count <= max_profile_number
                out_range = count > max_profile_number
                ignore = False
                if in_range:
                    ignore = True
                if out_range:
                    if self.is_profile_section( line.replace(' ', '') ):
                        break
                    else:
                        ignore = True
                if ignore:
                    number_of_lines_to_ignore.append( count )
                count += 1

            # Nuevas lineas
            new_lines = []
            for index in range( 0, len(lines) ):
                if not (index in number_of_lines_to_ignore):
                    new_lines.append( lines[index] )

            self.text_repository.write_lines(new_lines)
        return remove

    def save(self, profile:str ):
        profile = self._normalize_profile( profile )
        exists = profile in self.get_profiles()
        if not exists:
            return self.insert( profile )
        else:
            return False



