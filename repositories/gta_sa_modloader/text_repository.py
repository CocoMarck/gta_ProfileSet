from core.text_util import read_text, ignore_comment
import pathlib

ENCODING = 'utf-8'


class TextRepository:
    def __init__(self, modloader_file:pathlib.Path):
        self.modloader_file = modloader_file

    def write_lines( self, lines ):
        with open(self.modloader_file, 'w', encoding=ENCODING) as text:
            text.write('\n'.join(lines) + '\n')

    def get_lines(self):
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

    def in_kebab_format(self, text):
        '''
        Formatear texto, tipo `kebab-case`
        '''
        return text.lower().replace(' ', '-')

    def dismiss_comment( self, text ):
        return ignore_comment( text, ';')

    def list_to_str(self, value: list):
        text = ''
        for i in value:
            text += f'{i}, '
        if text != '':
            text = text[:-2]
        return text

    def str_to_list(self, text: ''):
        return text.replace(' ', '').split(',')

    def normalize_text(self, text):
        return ignore_comment( text.replace(' ', '').lower(), '#' )

    def detect_line_as_parameter(self, line, parameter_name):
        return self.normalize_text( line ).startswith( self.normalize_text(f'{parameter_name}=') )


    def get_text(self):
        '''
        Obtener lineas de texto, del archivo `modlaoder.ini`
        '''
        text = ''
        if self.modloader_file.exists():
            # Leer el archivo, establecer lineas.
            text = read_text(
                file_and_path=self.modloader_file, option='ModeText', encoding=ENCODING
            )

        return text
