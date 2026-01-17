from core.text_util import ignore_comment
from .text_repository import TextRepository

DOMAIN_FOLDER = 'Folder'
SECTION_CONFIG = 'Config'
PROFILE_PARAMETER = "Profile"


class FolderRepository:
    def __init__(self, text_repository: TextRepository):
        self.text_repository = text_repository

    def build_section(self, section ):
        return f'[{DOMAIN_FOLDER}.{section}]'

    def get_config_line_number(self):
        '''
        Obtener numero de linea, que sea [Folder.Config]. Solo primer coincidencia.
        '''
        folder_config_line_number = None
        line_number = 0
        for line in self.text_repository.get_lines():
            if (
                line.replace(' ', '').startswith( self.build_section(SECTION_CONFIG) ) and
                folder_config_line_number == None
            ):
                folder_config_line_number = line_number
                break
            line_number += 1

        return folder_config_line_number

    def get_profile(self):
        '''
        Obtener perfil de configruación actual.
        '''
        config_line_number = self.get_config_line_number()
        profile = None

        if isinstance(config_line_number, int):
            text_lines = self.text_repository.get_lines()
            ready_text =  ''
            line_number = 0

            while True:
                # Establecer el texto del profile actual
                line_number += 1
                current_line_number = config_line_number + line_number
                if current_line_number < len(text_lines):
                    text_line = ignore_comment(
                        text_lines[current_line_number], ';'
                    ).replace( ' ', '' )
                    if text_line.startswith( f'{PROFILE_PARAMETER}=' ):
                        profile = text_line.split('=')[1]
                        break
                else:
                    break

        return profile


    def write_profile(self, profile, formatted=False):
        '''
        Establecer profile. `Profile=profile`. Indicar si sera formateado o no.
        '''
        if formatted:
            profile = self.text_repository.format_profile( profile=profile )

        text_changed = False
        ready_lines = []
        for line in self.text_repository.get_lines():
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
            ready_lines.append(line)

        if text_changed:
            # Escibir texto
            self.text_repository.write_lines( ready_lines )

        return text_changed

