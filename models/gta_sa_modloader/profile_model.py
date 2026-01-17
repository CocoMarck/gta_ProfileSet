class ProfileModel:
    def __init__(self):
        # Config
        self.profile: str
        self.ignore_all_mods : bool
        self.include_all_mods : bool
        self.exclude_all_mods : bool
        self.parents :  [ str ]

        # Others
        self.priority : { str : int }
        self.ignore_files : [ str ]
        self.ignore_mods : [ str ]
        self.include_mods: [ str ]
        self.exclusive_mods : [ str ]
