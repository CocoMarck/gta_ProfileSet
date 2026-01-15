class GTASAModloaderModel:
    def __init__(self):
        # Config
        self.profile: str
        self.exclude_all_mods: bool
        self.ignore_all_mods: bool
        self.parents: list

        # Mods files, and dirs
        self.ignore_files: list
        self.ignore_mods: list
        self.include_mods: list
        self.exclusive_mods: list
