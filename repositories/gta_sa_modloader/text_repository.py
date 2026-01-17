from core.text_util import read_text, ignore_comment
import pathlib

ENCODING = 'utf-8'


class TextRepository:
    def __init__(self, modloader_file:pathlib.Path):
        self.modloader_file = modloader_file

    def write_lines( self, lines ):
        with open(self.modloader_file, 'w', encoding=ENCODING) as text:
            text.write( '\n'.join(lines) )

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


    def format_profile(self, profile):
        return self.text_repository.in_kebab_format( text=profile )
