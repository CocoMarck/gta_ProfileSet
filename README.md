# gtaProfileSet
Un launcher que te permite cambiar el perfil de modlader en gta sa

### Dependencias para compilación
* [Archivo con todas las dependencias necesarias] (dependencies.txt)

### Como compilar
- Cliente para consola
pyinstaller --onefile --console --uac-admin --icon=.\gta_ProfileSet.ico .\gta_ProfileSet_shell.py
pyinstaller --console --icon=.\resources\gta_ProfileSet.ico .\gta_ProfileSet_shell.py

- Cliente para interfaz
pyinstaller --windowed --icon=.\resources\gta_ProfileSet.ico .\gta_ProfileSet_Qt.py

- gta with parameters
pyinstaller --console --icon=.\resources\gta_ProfileSet.ico .\gta_withparameters.py

- Borrar lo demas
del *.spec

- En linux
pyinstaller --onefile ./gta_ProfileSet_Qt.py
