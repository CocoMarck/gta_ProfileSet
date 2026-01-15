from models.gta_sa_modloader import GTASAModloaderModel
from controllers.gta_sa_modloader import GTASAModloaderController

# Paths
from utils.resource_loader import ResourceLoader
resource_loader = ResourceLoader()




# Modloader
modloader_model = GTASAModloaderModel()
modloader_controller = GTASAModloaderController( modloader_model, resource_loader.base_dir )

print( modloader_controller.get_modloader_text_lines() )

modloader_controller.get_current_profile()
print( modloader_model.profile )

print( modloader_controller.get_profiles() )
