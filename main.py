from models.gta_sa_modloader import ProfileModel, FolderModel
from repositories.gta_sa_modloader.path_repository import PathRepository
from repositories.gta_sa_modloader.text_repository import TextRepository
from repositories.gta_sa_modloader.folder_repository import FolderRepository
from repositories.gta_sa_modloader.profile_repository import ProfileRepository

# Paths
from utils.resource_loader import ResourceLoader
resource_loader = ResourceLoader()




# Models
profile_model = ProfileModel()
folder_model = FolderModel()

# Repository
path_repository = PathRepository( resource_loader.base_dir )
print(
    path_repository.get_files(),
    path_repository.get_mods()
)

text_repository = TextRepository( path_repository.modloader_file )
print(
    text_repository.get_lines(),
    text_repository.in_kebab_format( 'Hola como estas' )
)

folder_repository = FolderRepository( text_repository )
print(
    folder_repository.write_profile( 'Default' ),
    folder_repository.get_profile()
)

profile_repository = ProfileRepository( text_repository )
print(
    profile_repository.update_config( 'Default', 'ExcludeAllMods', True ),
    profile_repository.get_dict_values_section( 'Default', 'Config' )['line_values']
)
