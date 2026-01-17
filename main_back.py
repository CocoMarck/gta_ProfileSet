from models.gta_sa_modloader import ProfileModel, FolderModel
from repositories.gta_sa_modloader import GTASAModloaderRepository
from controllers.gta_sa_modloader import GTASAModloaderController

# Paths
from utils.resource_loader import ResourceLoader
resource_loader = ResourceLoader()




# Modloader
profile_model = ProfileModel()
folder_model = FolderModel()
modloader_repository = GTASAModloaderRepository( resource_loader.base_dir )
modloader_controller = GTASAModloaderController( folder_model, profile_model, modloader_repository )

modloader_controller.get_profiles()

folder_model.profile = 'Default'
modloader_controller.set_profile()
modloader_controller.get_current_profile()
print( folder_model.profile )
print( profile_model.ignore_mods )
