from controllers.gta_sa_modloader.gta_sa_modloader_controller import GTASAModloaderController
from config.constants import SECTION_IGNORE_FILES

# GUI
from .simple_section_form import SimpleSectionForm

class IgnoreFilesForm(SimpleSectionForm):
    def __init__(self, modloader_controller: GTASAModloaderController, *args, **kwargs):
        super().__init__(
            modloader_controller=modloader_controller, section=SECTION_IGNORE_FILES, *args, **kwargs
        )
