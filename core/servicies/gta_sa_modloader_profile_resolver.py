from repositories.gta_sa_modloader.profile_repository import ProfileRepository
from repositories.gta_sa_modloader.path_repository import PathRepository
import pathlib

class GTASAModloaderProfileResolver:
    def __init__(self, profile_repository: ProfileRepository, path_repository: PathRepository):
        self.profile_repository = profile_repository
        self.path_repository = path_repository

    def get_mods_dir(self, profile: str, visited=None):
        # Evitar recursividad
        if visited is None:
            visited = set()
        if profile in visited:
            return []
        visited.add(profile)

        # listas
        mod_dir_names = []
        mod_file_names = []
        parents_file_names = []

        # Bool
        exclude_all_mods = self.profile_repository.get_exclude_all_mods( profile )
        ignore_all_mods = self.profile_repository.get_ignore_all_mods( profile )

        # List
        add_files = []
        ignore_files = []
        if ignore_all_mods:
            mod_dir_names = ( self.profile_repository.get_exclusive_mods(profile) )
        elif exclude_all_mods:
            mod_dir_names = ( self.profile_repository.get_include_mods(profile) )
            ignore_files = ( self.profile_repository.get_ignore_files(profile) )


        for d in mod_dir_names:
            add_files.extend( self.path_repository.get_mods_dir( d ) )

        parents = self.profile_repository.get_parents(profile)
        for p in parents:
            if self.profile_repository.exists( p ):
                parents_file_names.extend( self.get_mods_dir( p, visited=visited) )
        for name in parents_file_names:
            if not( name in ignore_files):
                mod_file_names.append( name )

        # Mods files
        for f in add_files:
            if isinstance(f, pathlib.Path):
                if not( f.name in ignore_files):
                    mod_file_names.append( f.name )

        # Retornar mods en profile, o todos
        if exclude_all_mods or ignore_all_mods:
            return mod_file_names
        else:
            files = []
            for f in self.path_repository.get_mod_files():
                files.append( f.name )
            return files
