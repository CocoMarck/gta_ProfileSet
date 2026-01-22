from .simple_launcher import SimpleLauncher
import pathlib

GTA_SA_FILENAME = 'gta_sa.exe'

class GTASALauncher(SimpleLauncher):
    def __init__(self, gta_sa_path: pathlib.Path, *args, **kwargs):
        super().__init__( file_path=gta_sa_path.joinpath(GTA_SA_FILENAME), *args, **kwargs)
