# GTASAModloaderController
from models.gta_sa_modloader import ProfileModel, FolderModel
from controllers.gta_sa_modloader.gta_sa_modloader_controller import GTASAModloaderController
from core.launcher.gta_sa_launcher import GTASALauncher

from interface.cli.gta_sa_modloader_cli import GTASAModloaderCLI


# Rutas
from config.paths import GTA_SA_DIR

# Controller
profile_model = ProfileModel()
folder_model = FolderModel()
modloader_controller = GTASAModloaderController( folder_model, profile_model, GTA_SA_DIR )

# Launcher
gta_sa_launcher = GTASALauncher( GTA_SA_DIR )


# Contruir app
if __name__ == "__main__":
    modloader_controller.sync_active_profile()
    cli = GTASAModloaderCLI(modloader_controller, gta_sa_launcher)
    cli.run()
