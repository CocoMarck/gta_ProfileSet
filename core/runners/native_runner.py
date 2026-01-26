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
            instructions = []
            for x in self.executors:
                instructions.append( x )
            instructions.append( str(self.file_path) )
            return subprocess.Popen(
                instructions, cwd=self.file_path.parent
            )
        else:
            return False
