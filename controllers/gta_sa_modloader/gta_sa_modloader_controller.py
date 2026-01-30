from config.constants import MAX_PRIORITY, DEFAULT_PRIORITY, DEFAULT_PROFILE

from core.system_util import get_system
import subprocess
import pathlib

from models.gta_sa_modloader import ProfileModel, FolderModel
from repositories.gta_sa_modloader.path_repository import PathRepository
from repositories.gta_sa_modloader.text_repository import TextRepository
from repositories.gta_sa_modloader.folder_repository import FolderRepository
from repositories.gta_sa_modloader.profile_repository import ProfileRepository

# Validator
from core.validators.gta_sa_modloader_ini_validator import GTASAModloaderIniValidator

# Constructor de ini
from core.builders.gta_sa_modloader_ini_builder import GTASAModloaderIniBuilder

# Servicies
from core.servicies.gta_sa_modloader_profile_resolver import GTASAModloaderProfileResolver

# Log
from utils.wrappers.log_helper import LogHelper




# Controller
class GTASAModloaderController():
    def __init__(
        self, folder_model: FolderModel, profile_model: ProfileModel,
        gta_sa_dir: pathlib.Path, log_level='debug', save_log=True
    ):
        self.folder_model = folder_model
        self.profile_model = profile_model

        # Repository
        self.path_repository = PathRepository( gta_sa_dir )
        self.text_repository = TextRepository( self.path_repository.modloader_file )
        self.folder_repository = FolderRepository( self.text_repository )
        self.profile_repository = ProfileRepository( self.text_repository )

        # Validator
        self.ini_validator = GTASAModloaderIniValidator()

        # Builder
        self.ini_builder = GTASAModloaderIniBuilder()

        # Servicies
        self.profile_resolver = GTASAModloaderProfileResolver(
            self.profile_repository, self.path_repository
        )

        # Log
        self.log_helper = LogHelper(
            name="GTASAModloaderController", filename = "gta_sa_modloader_controller", verbose=True, log_level=log_level, save_log=save_log, only_the_value=True
        )


    def get_profiles(self):
        return self.profile_repository.get_profiles()


    def load_profile(self):
        '''
        Actualizar modelo de perfil
        '''
        if self.profile_model.profile in self.profile_repository.get_profiles():
            self.profile_model.ignore_all_mods = self.profile_repository.get_ignore_all_mods(
                self.profile_model.profile
            )
            self.profile_model.exclude_all_mods = self.profile_repository.get_exclude_all_mods(
                self.profile_model.profile
            )
            self.profile_model.parents = self.profile_repository.get_parents(
                self.profile_model.profile
            )
            self.profile_model.priority = self.profile_repository.get_priorities(
                self.profile_model.profile
            )
            self.profile_model.ignore_files = self.profile_repository.get_ignore_files(
                self.profile_model.profile
            )
            self.profile_model.ignore_mods = self.profile_repository.get_ignore_mods(
                self.profile_model.profile
            )
            self.profile_model.include_mods = self.profile_repository.get_include_mods(
                self.profile_model.profile
            )
            self.profile_model.exclusive_mods = self.profile_repository.get_exclusive_mods(
                self.profile_model.profile
            )
        else:
            self.profile_model.ignore_all_mods = None
            self.profile_model.exclude_all_mods = None
            self.profile_model.parents = None
            self.profile_model.priority = None
            self.profile_model.ignore_files = None
            self.profile_model.ignore_mods = None
            self.profile_model.include_mods = None
            self.profile_model.exclusive_mods = None
            self.set_and_sync_to_default_profile()


    # Folder section
    def load_folder_profile(self):
        '''
        Establecer perfil en modelos folder y profile. En profile sus parametros y secciones.
        '''
        self.folder_model.profile = self.folder_repository.get_profile()

    def profile_exists(self, profile:str):
        exists = self.profile_repository.exists( profile )
        if exists:
            self.log_helper.log( f'Profile `{profile}` exists', 'info' )
        else:
            self.log_helper.log( f'Profile `{profile}` not exists', 'error' )
        return exists

    def set_folder_profile(self, name):
        write = False
        if name in self.profile_repository.get_profiles():
            write = self.folder_repository.write_profile( name )
        if write:
            self.load_folder_profile()
            self.log_helper.log( f'Writing folder profile as `{name}`', 'info' )
        else:
            self.log_helper.log( f'The folder profile cloud not be writted as `{name}`', 'warning' )
        return write

    # Otros
    def sync_active_profile(self):
        self.load_folder_profile()
        if self.profile_repository.exists(self.folder_model.profile):
            self.profile_model.profile = self.folder_model.profile
        else:
            self.profile_model.profile = DEFAULT_PROFILE
        self.load_profile()

    def set_and_sync_to_default_profile(self):
        self.set_folder_profile( DEFAULT_PROFILE )
        self.sync_active_profile()

    # Seleccionar perfil
    def select_profile(self, name):
        exists = self.profile_repository.exists( name )
        if exists:
            self.profile_model.profile = name
            self.load_profile()
            self.log_helper.log( f'Loading profile `{name}`', 'info' )
        else:
            self.log_helper.log(
                f"That profile doesn't exists `{name}` | Keeping `{self.profile_model.profile}`",
                'warning'
            )
        return exists

    # Guardar nuevo perfil
    def save_profile(self, name):
        safe_name = None
        if isinstance( name, str ):
            safe_name = self.profile_repository.save( name )

        save = isinstance( safe_name, str )
        if save:
            self.log_helper.log( f'Saving profile `{name}` -> `{safe_name}`', 'info' )
        else:
            self.log_helper.log( f'The profile `{name}` was not saved ', 'warning' )

        return save

    def remove_profile(self, name):
        remove = False
        if isinstance(name, str):
            remove = self.profile_repository.remove( name )
        if remove:
            self.set_and_sync_to_default_profile()
            self.log_helper.log( f'Removing profile `{name}`', 'info' )
        else:
            self.log_helper.log( f'The profile `{name}` was not removed', 'warning' )
        return remove

    def rename_profile(self, name, new_name):
        safe_name = None
        if isinstance(name, str) and isinstance(self.profile_model.profile, str):
            safe_name = self.profile_repository.rename( name, new_name )

        rename = isinstance(safe_name, str)
        if rename:
            self.set_and_sync_to_default_profile()
            self.log_helper.log(
                f'Raname profile `{name}` to `{new_name}` -> `{safe_name}`', 'info'
            )
        else:
            self.log_helper.log(
                f'The profile `{name}` could not be renamed to `{new_name}`', 'warning'
            )
        return rename

    # Boleanos
    def update_ignore_all_mods(self, value):
        update = self.profile_repository.update_ignore_all_mods(self.profile_model.profile, value)
        if update:
            self.profile_model.ignore_all_mods = value
            self.log_helper.log(
                f'In `{self.profile_model.profile}` ignore all mods in `{value}`', 'info'
            )
        return update

    def update_exclude_all_mods(self, value):
        update = self.profile_repository.update_exclude_all_mods(self.profile_model.profile, value)
        if update:
            self.profile_model.exclude_all_mods = value
            self.log_helper.log(
                f'In `{self.profile_model.profile}` exclude all mods in `{value}`', 'info'
            )
        return update

    # Pioridades, lista
    def save_parents(self, parents):
        save = self.profile_repository.write_parents( self.profile_model.profile, parents )
        if save:
            self.load_profile()
            self.log_helper.log(
                f'The parents `{parents}` was saved in `{self.profile_model.profile}`', 'info'
            )
        else:
            self.log_helper.log(
                f'The parents `{parents}` were not saved in `{self.profile_model.profile}`', 'warning'
            )
        return save

    def remove_parents(self, parents):
        remove = self.profile_repository.remove_parents( self.profile_model.profile, parents )
        if remove:
            self.load_profile()
            self.log_helper.log(
                f'The parents `{parents}` was removed from `{self.profile_model.profile}`', 'info'
            )
        else:
            self.log_helper.log(
                f'The parents `{parents}` ware not removed from `{self.profile_model.profile}`', 'warning'
            )
        return remove

    # Secciones
    ## Pioridad, diccionario
    def save_priority(self, name, value=DEFAULT_PRIORITY):
        save = self.profile_repository.save_priority( self.profile_model.profile, name, value )
        if save:
            self.load_profile()
            self.log_helper.log(
                f'The priority mod `{name}={value}` was saved in `{self.profile_model.profile}`', 'info'
            )
        else:
            self.log_helper.log(
                f'The priority mod `{name}` was not saved in `{self.profile_model.profile}`', 'warning'
            )
        return save

    def remove_priority(self, name, value):
        remove = self.profile_repository.remove_priority( self.profile_model.profile, name, value)
        if remove:
            self.load_profile()
            self.log_helper.log(
                f'The priority mod `{name}` was removed form `{self.profile_model.profile}`', 'info'
            )
        else:
            self.log_helper.log(
                f'The priority mod `{name}` could not be removed from `{self.profile_model.profile}`', 'warning'
            )
        return remove

    ## IgnoreFiles
    def save_ignore_file(self, value):
        save = self.profile_repository.save_ignore_file( self.profile_model.profile, value )
        if save:
            self.load_profile()
            self.log_helper.log(
                f'The ignore file `{value}` was saved in `{self.profile_model.profile}`', 'info'
            )
        else:
            self.log_helper.log(
                f'The ignore file `{value}` was not saved in `{self.profile_model.profile}`', 'warning'
            )
        return save

    def remove_ignore_file(self, value):
        remove = self.profile_repository.remove_ignore_file( self.profile_model.profile, value )
        if remove:
            self.load_profile()
            self.log_helper.log(
                f'The ignore file `{value}` was removed form `{self.profile_model.profile}`', 'info'
            )
        else:
            self.log_helper.log(
                f'The ignore file `{value}` could not be removed from `{self.profile_model.profile}`', 'warning'
            )
        return remove

    ## IgnoreMods
    def save_ignore_mod(self, value):
        save = self.profile_repository.save_ignore_mod( self.profile_model.profile, value )
        if save:
            self.load_profile()
            self.log_helper.log(
                f'The ignore mod `{value}` was saved in `{self.profile_model.profile}`', 'info'
            )
        else:
            self.log_helper.log(
                f'The ignore mod `{value}` was not saved in `{self.profile_model.profile}`', 'warning'
            )
        return save

    def remove_ignore_mod(self, value):
        remove = self.profile_repository.remove_ignore_mod( self.profile_model.profile, value )
        if remove:
            self.load_profile()
            self.log_helper.log(
                f'The ignore mod `{value}` was removed form `{self.profile_model.profile}`', 'info'
            )
        else:
            self.log_helper.log(
                f'The ignore mod `{value}` could not be removed from `{self.profile_model.profile}`', 'warning'
            )
        return remove

    ## IncludeMods
    def save_include_mod(self, value):
        save = self.profile_repository.save_include_mod( self.profile_model.profile, value )
        if save:
            self.load_profile()
            self.log_helper.log(
                f'The include mod `{value}` was saved in `{self.profile_model.profile}`', 'info'
            )
        else:
            self.log_helper.log(
                f'The include mod `{value}` was not saved in `{self.profile_model.profile}`', 'warning'
            )
        return save

    def remove_include_mod(self, value):
        remove = self.profile_repository.remove_include_mod( self.profile_model.profile, value )
        if remove:
            self.load_profile()
            self.log_helper.log(
                f'The include mod `{value}` was removed form `{self.profile_model.profile}`', 'info'
            )
        else:
            self.log_helper.log(
                f'The include mod `{value}` could not be removed from `{self.profile_model.profile}`', 'warning'
            )
        return remove

    ## ExclusiveMods
    def save_exclusive_mod(self, value):
        save = self.profile_repository.save_exclusive_mod( self.profile_model.profile, value )
        if save:
            self.load_profile()
            self.log_helper.log(
                f'The exclusive mod `{value}` was saved in `{self.profile_model.profile}`', 'info'
            )
        else:
            self.log_helper.log(
                f'The exclusive mod `{value}` was not saved in `{self.profile_model.profile}`', 'warning'
            )
        return save

    def remove_exclusive_mod(self, value):
        remove = self.profile_repository.remove_exclusive_mod( self.profile_model.profile, value )
        if remove:
            self.load_profile()
            self.log_helper.log(
                f'The exclusive mod `{value}` was removed form `{self.profile_model.profile}`', 'info'
            )
        else:
            self.log_helper.log(
                f'The exclusive mod `{value}` could not be removed from `{self.profile_model.profile}`', 'warning'
            )
        return remove

    ## Mod Files, and Directorys
    def get_mod_file_names(self):
        return list( set([f.name for f in self.path_repository.get_mod_files()]) )

    def get_mod_dir_names(self):
        return [d.name for d in self.path_repository.get_mod_dirs()]


    # Obtener texto
    def get_ini_text(self):
        return self.text_repository.get_text()

    def ensure_and_validate_ini(self):
        # Craer o no ini
        create_ini = (
            self.path_repository.modloader_dir.is_dir() and
            not( self.path_repository.modloader_file.is_file() )
        )
        if create_ini:
            self.text_repository.write_lines( self.ini_builder.build_default() )

        # Validar
        lines = self.text_repository.get_lines()
        self.ini_validator.lines = lines
        validate, dict_existing_lines = self.ini_validator.validate()

        for key, value in dict_existing_lines.items():
            self.log_helper.log( f'{key} | {value} | `{lines[value]}`', 'debug' )
        if validate:
            self.log_helper.log( 'Validation successful | Existing lines', 'info' )
        else:
            self.log_helper.log( 'Validation failed | Lines do not exist', 'error' )

        return validate

    def exists(self):
        return self.profile_exists( self.profile_model.profile )

    # service
    def get_profile_mods_dir(self, profile: str):
        if self.profile_exists( profile ):
            self.log_helper.log( f'Get mods in profile `{profile}`', 'info' )
            return self.profile_resolver.get_mods_dir( profile )
        return None

    def get_mods_dir(self):
        return self.get_profile_mods_dir( self.profile_model.profile )



