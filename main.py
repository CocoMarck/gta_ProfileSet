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
    profile_repository.get_profiles(),
    profile_repository.write_parents( 'Default', ['hola', 'adios'] ),
    profile_repository.get_parents( 'Default' ),
    profile_repository.save_priority( 'Default', 'cocos' ),
    profile_repository.get_priorities( 'Default' ),
    profile_repository.save_ignore_file( 'Default', 'big-headshot.asi' ),
    profile_repository.save_ignore_file( 'Default', 'shell.asi' ),
    profile_repository.remove_ignore_file( 'Default', 'shell.asi' ),
    profile_repository.get_ignore_files( 'Default' ),
    profile_repository.save_ignore_mod( 'Default', 'Aiuda chavales' ),
    profile_repository.get_ignore_mods( 'Default' ),
    profile_repository.save_include_mod( 'Default', 'ModIncluidoPascalCase' ),
    profile_repository.get_include_mods( 'Default' ),
    profile_repository.save_exclusive_mod( 'Default', 'SoloVip' ),
     profile_repository.get_exclusive_mods( 'Default' ),
)
