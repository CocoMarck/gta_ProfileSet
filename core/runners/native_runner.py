import subprocess
import pathlib

class NativeRunner:
    def __init__(self, file_path: pathlib.Path):
        self.file_path = file_path
        self.executors = []

    def the_file_path_is_correct(self):
        if self.file_path.exists():
            return self.file_path.is_file()
        else:
            return False

    def run(self):
        if self.the_file_path_is_correct():
            instructions = [str(self.file_path)]
            instructions.extend( self.executors )
            return subprocess.Popen(
                instructions, cwd=self.file_path.parent
            )
        else:
            return False
