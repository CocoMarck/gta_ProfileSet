from core.system_util import get_system
from core.runners.wine_runner import WineRunner
from core.runners.native_runner import NativeRunner
import pathlib

class SimpleLauncher:
    def __init__(self, file_path: pathlib.Path):
        self.file_path = file_path
        self.system = get_system() # simple string `win` or `linux`.

    def launch(self):
        if self.system == 'win':
            return NativeRunner(self.file_path).run()
        if self.system == 'linux':
            return WineRunner(self.file_path).run()
        raise RunTimeError('Unsupported system')
