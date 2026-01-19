from models.gta_sa_modloader import ProfileModel, FolderModel
from repositories.gta_sa_modloader.path_repository import PathRepository
from repositories.gta_sa_modloader.text_repository import TextRepository
from repositories.gta_sa_modloader.folder_repository import FolderRepository
from repositories.gta_sa_modloader.profile_repository import ProfileRepository
from controllers.gta_sa_modloader.gta_sa_modloader_controller import GTASAModloaderController

# Paths
from utils.resource_loader import ResourceLoader
resource_loader = ResourceLoader()




# Models
profile_model = ProfileModel()
folder_model = FolderModel()

# Repository
path_repository = PathRepository( resource_loader.base_dir )

# Controller
modloader_controller = GTASAModloaderController( folder_model, profile_model, path_repository )
modloader_controller.sync_active_profile()
print(
    f'{profile_model.ignore_all_mods}\n'
    f'{profile_model.exclude_all_mods}\n'
    f'{profile_model.parents}\n'

    f'{profile_model.priority}\n'
    f'{profile_model.ignore_files}\n'
    f'{profile_model.ignore_mods}\n'
    f'{profile_model.include_mods}\n'
    f'{profile_model.exclusive_mods}'
)
modloader_controller.save_profile( 'comida clasica' )
modloader_controller.set_folder_profile('Default')

modloader_controller.select_profile( 'aiuda-chavales' )
modloader_controller.save_priority( 'wakaneanos-de-las-montañas', 32 )
print( profile_model.priority )
