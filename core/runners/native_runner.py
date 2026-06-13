import subprocess
import pathlib
import os
import signal
import atexit

class NativeRunner:
    def __init__(self, file_path: pathlib.Path):
        self.file_path = file_path
        self.executors = []
        self.process = None

        # Registramos el stop automáticamente para asegurar el exit impecable
        atexit.register(self.stop)

    def the_file_path_is_correct(self):
        if self.file_path.exists():
            return self.file_path.is_file()
        else:
            return False

    def is_running(self):
        return self.process and self.process.poll() is None

    def run(self):
        if not self.the_file_path_is_correct():
            return False

        if self.is_running():
            return self.process

        # Establecemos instrucciones
        instructions = list(self.executors) + [str(self.file_path)]

        # Ejecutarmos instrucciones
        env = os.environ.copy()
        self.process = subprocess.Popen(
            instructions,
            cwd=self.file_path.parent,
            env=env,
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return self.process

    def stop(self):
        if self.is_running():
            try:
                os.killpg(self.process.pid, signal.SIGTERM)

                try:
                    # Esperamos un momento a cerrarlo por SIGTERM
                    self.process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    # Si no cierra matarlo.
                    os.killpg( os.getpgid(self.process.pid), signal.SIGKILL )
            except ProcessLookupError:
                # Por si el proceso ya se habia cerrado justo en ese milisegundo.
                pass
            except Exception:
                pass
            finally:
                self.process = None
