from core.system_util import get_system
import subprocess

from models.gta_sa_modloader import FolderModel, ProfileModel
from repositories.gta_sa_modloader import GTASAModloaderRepository




def get_text( text ):
    return str(text)




# Controller
class GTASAModloaderController():
    def __init__(
        self, folder_model: FolderModel, profile_model: ProfileModel,
        gta_sa_modloader_repository: GTASAModloaderRepository
    ):
        self.folder_model = folder_model
        self.profile_model = profile_model
        self.repository = gta_sa_modloader_repository

    def get_current_profile(self):
        '''
        Obtener perfil de configruación actual.
        '''
        self.folder_model.profile = self.repository.get_current_profile()
        self.profile_model.profile = self.folder_model.profile
        self.profile_model.ignore_mods = self.repository.get_profile_ignore_mods( self.profile_model.profile )

    def get_profiles(self):
        '''
        Obtener perfiles. Devuelve una lista de los perfiles.
        '''
        self.folder_model.profiles = self.repository.get_profiles()

    def set_profile(self):
        '''
        Establecer profile. `Profile=profile`
        '''
        self.get_profiles()
        if self.folder_model.profile in self.folder_model.profiles:
            return self.repository.write_profile( profile=self.folder_model.profile )
        return False


