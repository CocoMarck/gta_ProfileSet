from utils import ResourceLoader

resource_loader = ResourceLoader()

# Subcarpeta
ICON_DIR = resource_loader.resources_dir.joinpath( 'icons' )
NOTA_DEFAULT_DIR = resource_loader.resources_dir.joinpath( 'nota' )

# Archivos
ICON_FILE = ICON_DIR.joinpath( 'gta-sa-modloader-controller.png' )

# XML GUI
VIEWS_DIR = resource_loader.base_dir.joinpath( 'views' )
CONFIG_FORM_UI_FILE = VIEWS_DIR.joinpath('xml', 'config_form.ui')
MAIN_WINDOW_UI_FILE = VIEWS_DIR.joinpath('xml', 'main_window.ui')

# GTA SA dirs
GTA_SA_DIR = resource_loader.base_dir
