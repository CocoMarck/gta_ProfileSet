# Compila los `ui` en PyQt6
[Como compilar a `ui` a `.py`](https://doc.qt.io/qtforpython-6/tutorials/basictutorial/uifiles.html). Se tendra que cambiar el código. En vez de cargar los files, cargar los modulos.

Ejemplo:
```bash
pyside6-uic main_window.ui -o ui_main_window.py
```

```python
from ui_main_window import Ui_MainWindow

class ...
    ...
    self.ui = Ui_MainWindow
    self.ui.setupUi(self)
```
