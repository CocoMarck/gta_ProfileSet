from config.constants import (
    DOMAIN_PROFILES, DOMAIN_FOLDER, PROFILE_SECTIONS, SECTION_CONFIG, PROFILE_PARAMETER,
    EXCLUDE_ALL_MODS_PARAMETER, IGNORE_ALL_MODS_PARAMETER, PARENTS_PARAMETER, SECTION_PRIORITY,
    SECTION_IGNORE_MODS, SECTION_INCLUDE_MODS, SECTION_EXCLUSIVE_MODS, DEFAULT_PROFILE, SECTION_IGNORE_FILES
)
import pathlib

class GTASAModloaderIniValidator:
    def __init__(self, modloader_lines=None):
        self.lines = modloader_lines or []


    def get_dict_existing_lines(self, lines:list) -> dict:
        dict_existing_lines = {
            'folder_domain': None,
            'folder_profile': None,
            'profile_domain': None,
            'profile_exclude_all_mods': None,
            'profile_ignore_all_mods': None,
            'profile_parents': None,
            'profile_priority': None,
            'profile_ignore_mods': None,
            'profile_ignore_files': None,
            'profile_include_mods': None,
            'profile_exclusive_mods': None,
        }
        count = 0
        for line in lines:
            if dict_existing_lines['folder_domain'] == None:
                if (
                    line.replace(' ', '').startswith( f'[{DOMAIN_FOLDER}.{SECTION_CONFIG}' )
                ):
                    dict_existing_lines['folder_domain'] = count
            elif dict_existing_lines['folder_profile'] == None:
                if (
                    isinstance(dict_existing_lines['folder_domain'], int) and
                    dict_existing_lines['profile_domain'] == None and
                    line.replace(' ', '').startswith( f'{PROFILE_PARAMETER}=' )
                ):
                    dict_existing_lines['folder_profile'] = count


            # Profile
            not_exists_priority = dict_existing_lines['profile_priority'] == None
            not_exists_ignore_mods = dict_existing_lines['profile_ignore_mods'] == None
            not_exists_ignore_files = dict_existing_lines['profile_ignore_files'] == None
            not_exists_include_mods = dict_existing_lines['profile_include_mods'] == None
            not_exists_exclusive_mods = dict_existing_lines['profile_exclusive_mods'] == None
            not_exists_profile_sections = (
                not_exists_priority and
                not_exists_ignore_mods and
                not_exists_ignore_files and
                not_exists_include_mods and
                not_exists_exclusive_mods
            )
            exists_profile_domain = isinstance(dict_existing_lines['profile_domain'], int)
            if dict_existing_lines['profile_domain'] == None:
                if (
                    line.replace(' ', '')
                    .startswith( f'[{DOMAIN_PROFILES}.{DEFAULT_PROFILE}.{SECTION_CONFIG}' )
                ):
                    dict_existing_lines['profile_domain'] = count

            elif dict_existing_lines['profile_exclude_all_mods'] == None:
                if (
                    exists_profile_domain and
                    not_exists_profile_sections and
                    line.replace(' ', '').startswith( f'{EXCLUDE_ALL_MODS_PARAMETER}=' )
                ):
                    dict_existing_lines['profile_exclude_all_mods'] = count
            elif dict_existing_lines['profile_ignore_all_mods'] == None:
                if (
                    exists_profile_domain and
                    not_exists_profile_sections and
                    line.replace(' ', '').startswith( f'{IGNORE_ALL_MODS_PARAMETER}=' )
                ):
                    dict_existing_lines['profile_ignore_all_mods'] = count
            elif dict_existing_lines['profile_parents'] == None:
                if (
                    exists_profile_domain and
                    not_exists_profile_sections and
                    line.replace(' ', '').startswith( f'{PARENTS_PARAMETER}=' )
                ):
                    dict_existing_lines['profile_parents'] = count
            if not_exists_priority and exists_profile_domain:
                if (
                    line.replace(' ', '')
                    .startswith( f'[{DOMAIN_PROFILES}.{DEFAULT_PROFILE}.{SECTION_PRIORITY}' )
                ):
                        dict_existing_lines['profile_priority'] = count
            if not_exists_ignore_files and exists_profile_domain:
                if (
                    line.replace(' ', '')
                    .startswith( f'[{DOMAIN_PROFILES}.{DEFAULT_PROFILE}.{SECTION_IGNORE_FILES}' )
                ):
                    dict_existing_lines['profile_ignore_files'] = count
            if not_exists_ignore_mods and exists_profile_domain:
                if (
                    line.replace(' ', '')
                    .startswith( f'[{DOMAIN_PROFILES}.{DEFAULT_PROFILE}.{SECTION_IGNORE_MODS}' )
                ):
                    dict_existing_lines['profile_ignore_mods'] = count
            if not_exists_include_mods and exists_profile_domain:
                if (
                    line.replace(' ', '')
                    .startswith( f'[{DOMAIN_PROFILES}.{DEFAULT_PROFILE}.{SECTION_INCLUDE_MODS}' )
                ):
                    dict_existing_lines['profile_include_mods'] = count
            if not_exists_exclusive_mods and exists_profile_domain:
                if (
                    line.replace(' ', '')
                    .startswith( f'[{DOMAIN_PROFILES}.{DEFAULT_PROFILE}.{SECTION_EXCLUSIVE_MODS}' )
                ):
                    dict_existing_lines['profile_exclusive_mods'] = count

            count += 1

        return dict_existing_lines

    def validate(self) -> tuple[bool, dict]:
        if not isinstance(self.lines, list):
            return False, {}

        new_dict_existing_lines = {}
        dict_existing_lines = self.get_dict_existing_lines( self.lines )
        for key, value in dict_existing_lines.items():
            if value == None:
                return False, new_dict_existing_lines
            else:
                new_dict_existing_lines.update( {key: value})

        return True, new_dict_existing_lines

