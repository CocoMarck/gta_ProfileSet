from controllers.gta_sa_modloader.gta_sa_modloader_controller import GTASAModloaderController
from config.constants import SECTION_INCLUDE_MODS

# GUI
from .simple_section_form import SimpleSectionForm

class IncludeModsForm(SimpleSectionForm):
    def __init__(self, modloader_controller: GTASAModloaderController, *args, **kwargs):
        super().__init__(
            modloader_controller=modloader_controller, section=SECTION_INCLUDE_MODS, *args, **kwargs
        )
