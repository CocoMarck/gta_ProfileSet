from .text_repository import TextRepository
from .profile_repository import ProfileRepository
from .folder_repository import FolderRepository
import pathlib


class ModloaderRepository:
    def __init__(self, (self, gta_sa_dir:pathlib.Path):
        self.gta_sa_dir = gta_sa_dir
        self.gta_sa_file = self.gta_sa_dir.joinpath( 'gta_sa.exe' )
        self.modloader_dir = self.gta_sa_dir.joinpath( MODLOADER_NAME )
        self.modloader_file = self.modloader_dir.joinpath( MODLOADER_FILENAME )

        # Objetos para chamba
        self.text_repository = TextRepository( modlaoder_file )
        self.folder_repository = FolderRepository( text_repository )
        self.profile_repository = ProfileRepository( text_repository )
