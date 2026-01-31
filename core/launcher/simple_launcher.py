from core.system_util import get_system
from core.runners.wine_runner import WineRunner
from core.runners.native_runner import NativeRunner
import pathlib

class SimpleLauncher:
    def __init__(self, file_path: pathlib.Path):
        self.file_path = file_path
        self.system = get_system() # simple string `win` or `linux`.
        self.runner = None

    def launch(self):
        if self.runner is None:
            if self.system == 'win':
                self.runner = NativeRunner(self.file_path)
            elif self.system == 'linux':
                self.runner = WineRunner(self.file_path)
            else:
                raise RunTimeError('Unsupported system')
            return self.runner.run()
        else:
            return False

    def stop(self):
        if self.runner:
            self.runner.stop()
