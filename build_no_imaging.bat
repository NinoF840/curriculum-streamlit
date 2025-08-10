@echo off
echo ========================================
echo  Nino Medical AI Pro Ultimate
echo  Build Script - No Imaging Version
echo ========================================
echo.

:: Check if PyInstaller is installed
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

echo Building Nino Medical AI Pro Ultimate (No Imaging)...
echo.

:: Clean previous builds
if exist "dist\Nino Medical AI Pro.exe" del "dist\Nino Medical AI Pro.exe"
if exist "build" rmdir /s /q "build"

:: Build the executable
pyinstaller --onefile ^
    --name "Nino Medical AI Pro" ^
    --icon=medical_icon.ico ^
    --add-data "*.py;." ^
    --hidden-import tkinter ^
    --hidden-import matplotlib ^
    --hidden-import pandas ^
    --hidden-import numpy ^
    --hidden-import plotly ^
    --noconsole ^
    --clean ^
    nino_medical_ai_desktop_no_imaging.py

if errorlevel 1 (
    echo.
    echo ❌ Build failed! Check the errors above.
    pause
    exit /b 1
)

echo.
echo ✅ Build completed successfully!
echo.
echo 📁 Executable location: dist\Nino Medical AI Pro.exe
echo 📊 File size: 
for %%I in ("dist\Nino Medical AI Pro.exe") do echo    %%~zI bytes

echo.
echo Testing executable...
if exist "dist\Nino Medical AI Pro.exe" (
    echo ✅ Executable created successfully
    echo.
    echo You can now run: "dist\Nino Medical AI Pro.exe"
) else (
    echo ❌ Executable not found
)

echo.
echo ========================================
echo Build process completed
echo ========================================
pause
