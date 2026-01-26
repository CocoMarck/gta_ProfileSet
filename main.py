# App
from views.app.qt.main_window import build_app

# GTASAModloaderController
from models.gta_sa_modloader import ProfileModel, FolderModel
from controllers.gta_sa_modloader.gta_sa_modloader_controller import GTASAModloaderController
from core.launcher.gta_sa_launcher import GTASALauncher

# Rutas
from config.paths import GTA_SA_DIR

# Controller
profile_model = ProfileModel()
folder_model = FolderModel()
modloader_controller = GTASAModloaderController( folder_model, profile_model, GTA_SA_DIR )

# Launcher
gta_sa_launcher = GTASALauncher( GTA_SA_DIR )


# Contruir app
if __name__ == '__main__':
    if modloader_controller.ensure_and_validate_ini():
        modloader_controller.sync_active_profile()
        build_app( modloader_controller, gta_sa_launcher )
    else:
        from PyQt6.QtWidgets import QApplication, QMessageBox
        import sys
        app = QApplication(sys.argv)
        QMessageBox.critical(
            None,
            'Modloader error',
            'The `modloader.ini` file is invalid or incomplete.'
        )
        sys.exit(1)



