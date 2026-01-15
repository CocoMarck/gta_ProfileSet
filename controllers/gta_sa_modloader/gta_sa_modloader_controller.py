from core.system_util import get_system
import subprocess

from models.gta_sa_modloader import GTASAModloaderModel
from repositories.gta_sa_modloader import GTASAModloaderRepository




def get_text( text ):
    return str(text)




# Controller
class GTASAModloaderController():
    def __init__(
        self, gta_sa_modloader_model: GTASAModloaderModel,
        gta_sa_modloader_repository: GTASAModloaderRepository
    ):
        self.model = gta_sa_modloader_model
        self.repository = gta_sa_modloader_repository

    def get_current_profile(self):
        '''
        Obtener perfil de configruación actual.
        '''
        self.model.profile = self.repository.get_current_profile()


    def get_profiles(self):
        '''
        Obtener perfiles. Devuelve una lista de los perfiles.
        '''
        return self.repository.get_profiles()

    def set_profile(self):
        '''
        Establecer profile. `Profile=profile`
        '''
        if self.model.profile in self.get_profiles():
            return self.repository.write_profile( profile=self.model.profile )
        return False


