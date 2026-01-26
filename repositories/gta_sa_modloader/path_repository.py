from utils.resource_loader import ResourceLoader
from core.text_util import not_repeat_item
import pathlib

resource_loader = ResourceLoader()

MODLOADER_NAME = 'modloader'
MODLOADER_FILENAME = f'{MODLOADER_NAME}.ini'
MOD_EXTENSIONS = [ '.cs', '.asi' ]

class PathRepository:
    def __init__(self, gta_sa_dir:pathlib.Path):
        self.gta_sa_dir = gta_sa_dir
        self.modloader_dir = self.gta_sa_dir.joinpath( MODLOADER_NAME )
        self.modloader_file = self.modloader_dir.joinpath( MODLOADER_FILENAME )

    def get_dict_path(self, path):
        return resource_loader.get_recursive_tree( path )

    def get_dirs(self):
        return self.get_dict_path( self.modloader_dir )['directory']

    def get_files(self):
        return self.get_dict_path( self.modloader_dir )['file']

    def get_mod_dirs(self):
        mods = []
        for path in sorted( self.modloader_dir.glob("*") ):
            if path.is_dir():
                mods.append( path )
        return mods

    def is_mod_file( self, path: pathlib.Path ):
        return path.suffix.lower() in MOD_EXTENSIONS

    def get_only_mod_files(self, files):
        mod_files = []
        for f in files:
            if self.is_mod_file( f ):
                mod_files.append( f )
        return not_repeat_item( mod_files )

    def get_mod_files(self):
        return self.get_only_mod_files( self.get_files() )

    def get_mods_dir(self, mod_dir: str):
        '''
        Obtener mods de directorio.
        '''
        path = self.modloader_dir.joinpath( mod_dir )
        return self.get_only_mod_files( self.get_dict_path( path )['file'] )



