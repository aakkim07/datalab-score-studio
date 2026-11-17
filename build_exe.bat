@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: PyCharm virtual environment was not found at .venv\Scripts\python.exe
    pause
    exit /b 1
)

".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Could not install build dependencies.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" -m PyInstaller --noconfirm --clean --onefile --windowed --name DataLab-minimal main.py
if errorlevel 1 (
    echo ERROR: EXE build failed.
    pause
    exit /b 1
)

echo.
echo Done. Launch dist\DataLab-minimal.exe
pause
