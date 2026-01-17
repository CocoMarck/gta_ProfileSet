from utils.resource_loader import ResourceLoader
import pathlib

resource_loader = ResourceLoader()

GTA_SA_FILENAME = 'gta_sa.exe'
MODLOADER_NAME = 'modloader'
MODLOADER_FILENAME = f'{MODLOADER_NAME}.ini'

class PathRepository:
    def __init__(self, gta_sa_dir:pathlib.Path):
        self.gta_sa_dir = gta_sa_dir
        self.gta_sa_file = self.gta_sa_dir.joinpath( GTA_SA_FILENAME )
        self.modloader_dir = self.gta_sa_dir.joinpath( MODLOADER_NAME )
        self.modloader_file = self.modloader_dir.joinpath( MODLOADER_FILENAME )

    def get_dict_path(self):
        return resource_loader.get_recursive_tree( self.modloader_dir )

    def get_mods(self):
        return self.get_dict_path()['directory']

    def get_files(self):
        return self.get_dict_path()['file']


