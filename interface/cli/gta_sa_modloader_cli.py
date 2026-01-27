from controllers.gta_sa_modloader.gta_sa_modloader_controller import GTASAModloaderController
from core.launcher.gta_sa_launcher import GTASALauncher
from config.constants import (
    SECTION_PRIORITY, SECTION_IGNORE_FILES,
    SECTION_IGNORE_MODS, SECTION_INCLUDE_MODS, SECTION_EXCLUSIVE_MODS,
    IGNORE_ALL_MODS_PARAMETER, EXCLUDE_ALL_MODS_PARAMETER, PARENTS_PARAMETER,
    PROFILE_CONFIG_PARAMETERS
)
import argparse

class GTASAModloaderCLI:
    def __init__(
        self, modloader_controller: GTASAModloaderController, gta_sa_launcher: GTASALauncher
    ):
        # Controller
        self.modloader_controller = modloader_controller
        self.profile_model = modloader_controller.profile_model

        # Launcher
        self.gta_sa_launcher = gta_sa_launcher

        # Parser
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            '-sfp', '--set-folder-profile', help='Set folder profile'
        )
        self.parser.add_argument(
            '-p', '--profile', help='Selected profile'
        )

        # Need profile
        self.parser.add_argument(
            '-gs', '--get-section', help='Get section in profile'
        )
        self.parser.add_argument(
            '-gas', '--get-all-sections', action='store_true', help='Get all section in profile'
        )
        self.parser.add_argument(
            '-gcp', '--get-config-parameter', help='Get config parameter in profile'
        )
        self.parser.add_argument(
            '-gacp', '--get-all-config-parameters', action='store_true',
            help='Get all config parameters in profile'
        )
        self.parser.add_argument(
            '-gm', '--get-mods', action='store_true', help='Get mods'
        )

        ## Modificaciones potentes.
        ## `--save, --remove, --rename, --save_in_section, --mods`. Por ahora evitar.

        # Bools, need NOTHING
        self.parser.add_argument(
            '-lg', '--launch-game', action='store_true', help='Run the game'
        )
        self.parser.add_argument(
            '-gp', '--get-profiles', action='store_true', help='Get all profiles'
        )


    def get_section(self, section: str):
        if section == SECTION_PRIORITY:
            return self.profile_model.priority
        if section == SECTION_IGNORE_FILES:
            return self.profile_model.ignore_files
        if section == SECTION_IGNORE_MODS:
            return self.profile_model.ignore_mods
        if section == SECTION_INCLUDE_MODS:
            return self.profile_model.include_mods
        if section == SECTION_EXCLUSIVE_MODS:
            return self.profile_model.exclusive_mods
        raise RuntimeError('That section does not exists')

    def get_config_parameter(self, parameter: str):
        if parameter == IGNORE_ALL_MODS_PARAMETER:
            return self.profile_model.ignore_all_mods
        if parameter == EXCLUDE_ALL_MODS_PARAMETER:
            return self.profile_model.exclude_all_mods
        if parameter == PARENTS_PARAMETER:
            return self.profile_model.parents
        raise RuntimeError('That parameter does not exists')


    def run(self):
        args = self.parser.parse_args()

        if isinstance(args.set_folder_profile, str):
            self.modloader_controller.set_folder_profile( args.set_folder_profile )

        if args.get_profiles:
            print( self.modloader_controller.get_profiles() )
        if args.launch_game:
            print( self.gta_sa_launcher.launch() )

        # Se indico un perfil
        if isinstance(args.profile, str):
            if args.get_all_config_parameters:
                self.modloader_controller.select_profile( args.profile )
                for x in PROFILE_CONFIG_PARAMETERS:
                    print( f"{x}:", self.get_config_parameter(x) )
            if args.get_all_sections:
                self.modloader_controller.select_profile( args.profile )
                for x in (
                    SECTION_PRIORITY, SECTION_IGNORE_FILES, SECTION_IGNORE_MODS, SECTION_INCLUDE_MODS, SECTION_EXCLUSIVE_MODS
                ):
                    print( f"{x}:", self.get_section(x) )
            if args.get_mods:
                print( self.modloader_controller.get_profile_mods_dir(args.profile) )


            if isinstance(args.get_config_parameter, str):
                self.modloader_controller.select_profile( args.profile )
                print(
                    f"{args.get_config_parameter}:",
                    self.get_config_parameter(args.get_config_parameter)
                )
            if isinstance(args.get_section, str):
                self.modloader_controller.select_profile( args.profile )
                print( f"{args.get_section}:", self.get_section(args.get_section) )

