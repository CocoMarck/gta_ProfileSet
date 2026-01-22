from .native_runner import NativeRunner

class WineRunner(NativeRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.executors = ['wine']
