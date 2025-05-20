# gtaProfileSet
Un launcher que te permite cambiar parametros del modloader.ini
Esta aplicación permite la gestión de mods de manera mas visual y rapida.

### Dependencias para compilación
[Lista de las dependencias necesarias] (dependencies.txt)

### Como compilar
- Cliente de consola (Windows)
```
pyinstaller --onefile --console --uac-admin --icon=.\gta_ProfileSet.ico .\gta_ProfileSet_shell.py
pyinstaller --console --icon=.\resources\gta_ProfileSet.ico .\gta_ProfileSet_shell.py
```

- Cliente con interfaz (Windows) 
```
pyinstaller --windowed --icon=.\resources\gta_ProfileSet.ico .\gta_ProfileSet_Qt.py
```

- gta with parameters (Windows)
```
pyinstaller --console --icon=.\resources\gta_ProfileSet.ico .\gta_withparameters.py
```

- Cliente con interfaz (Linux)
```
pyinstaller --onefile ./gta_ProfileSet_Qt.py
```

- Borrar lo demas
```
del *.spec
```
