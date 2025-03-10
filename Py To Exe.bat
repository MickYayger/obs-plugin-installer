@echo off
pyinstaller --clean --onefile --windowed --add-data "MickFX Required Sources/*;MickFX Required Sources/" ^
--icon="Mick Logo.ico" ^
--noupx ^
--hidden-import PyQt5 ^
--noconsole ^
--optimize=2 ^
"mickfx-plugin-installer.py"
pause