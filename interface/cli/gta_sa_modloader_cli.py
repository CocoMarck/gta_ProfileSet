from controllers.gta_sa_modloader.gta_sa_modloader_controller import GTASAModloaderController
from core.launcher.gta_sa_launcher import GTASALauncher
from config.constants import (
    SECTION_CONFIG, SECTION_PRIORITY, SECTION_IGNORE_FILES,
    SECTION_IGNORE_MODS, SECTION_INCLUDE_MODS, SECTION_EXCLUSIVE_MODS
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
        self.parser.add_argument(
            '-l', '--load', help='Load profile'
        )
        self.parser.add_argument(
            '-gs', '--get-section', help='Get section in profile'
        )
        self.parser.add_argument(
            '-rn', '--raname', help='Reneme existing profile'
        )
        self.parser.add_argument(
            '-rm', '--remove', help='Remove existing profile'
        )
        self.parser.add_argument(
            '-s', '--save', help='Save profile'
        )
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


    def run(self):
        args = self.parser.parse_args()

        if isinstance(args.set_folder_profile, str):
            self.modloader_controller.set_folder_profile( args.set_folder_profile )

        if args.get_profiles:
            print( self.modloader_controller.get_profiles() )
        if args.launch_game:
            self.gta_sa_launcher.launch()

        if isinstance(args.get_section, str):
            print( self.get_section( args.get_section ) )

        if isinstance(args.profile, str):
            if isinstance(args.load_profile, str):
                self.modloader_controller.load_profile( args.profile )

            if args.rename:
                self.modloader_controller.raname_profile( args.profile, args.rename )
            if args.remove:
                self.modloader_controller.remove_profile( args.profile )
            if args.save:
                self.modloader_controller.save_profile( args.profile )

