from models.gta_sa_modloader import GTASAModloaderModel
from repositories.gta_sa_modloader import GTASAModloaderRepository
from controllers.gta_sa_modloader import GTASAModloaderController

# Paths
from utils.resource_loader import ResourceLoader
resource_loader = ResourceLoader()




# Modloader
modloader_model = GTASAModloaderModel()
modloader_repository = GTASAModloaderRepository( resource_loader.base_dir )
modloader_controller = GTASAModloaderController( modloader_model, modloader_repository )

print( modloader_repository.get_text_lines() )

modloader_controller.get_current_profile()
print( modloader_model.profile )

print( modloader_controller.get_profiles() )

modloader_repository.write_profile( 'Esta es mi primera chamba', formatted=True )
modloader_controller.get_current_profile()
print( modloader_model.profile )
