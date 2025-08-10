@echo off
title Nino Medical AI Pro Ultimate - Master Build Script
color 0B

echo.
echo ===============================================================
echo              🏥 NINO MEDICAL AI PRO ULTIMATE
echo                   Master Build Script
echo               Developed by Antonino Piacenza
echo ===============================================================
echo.
echo This script will build both versions:
echo   1. Nino Medical AI Pro (No Imaging) - Lightweight version
echo   2. Nino Medical AI Pro Imaging - Full imaging capabilities
echo.
echo ===============================================================

:: Check Python installation
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.11.7 first.
    pause
    exit /b 1
)
echo ✅ Python found

:: Check PyInstaller
echo [2/6] Checking PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ Failed to install PyInstaller
        pause
        exit /b 1
    )
)
echo ✅ PyInstaller ready

:: Clean all previous builds
echo [3/6] Cleaning previous builds...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"
mkdir dist
echo ✅ Build environment cleaned

echo.
echo ===============================================================
echo            🚀 Building Version 1: No Imaging
echo ===============================================================

echo [4/6] Building No Imaging version...
pyinstaller --onefile ^
    --name "Nino Medical AI Pro" ^
    --add-data "*.py;." ^
    --hidden-import tkinter ^
    --hidden-import matplotlib ^
    --hidden-import pandas ^
    --hidden-import numpy ^
    --hidden-import plotly ^
    --hidden-import matplotlib.backends.backend_tkagg ^
    --noconsole ^
    --clean ^
    --distpath "dist" ^
    nino_medical_ai_desktop_no_imaging.py

if errorlevel 1 (
    echo ❌ No Imaging version build failed!
    goto :error
)

:: Rename and verify first build
if exist "dist\Nino Medical AI Pro.exe" (
    ren "dist\Nino Medical AI Pro.exe" "Nino Medical AI Pro.exe"
    echo ✅ No Imaging version built successfully
    for %%I in ("dist\Nino Medical AI Pro.exe") do (
        echo    📊 Size: %%~zI bytes
    )
) else (
    echo ❌ No Imaging executable not found!
    goto :error
)

echo.
echo ===============================================================
echo           🖼️ Building Version 2: Imaging Edition
echo ===============================================================

:: Clean build cache for second build
if exist "build" rmdir /s /q "build"

echo [5/6] Building Imaging version...
pyinstaller --onefile ^
    --name "Nino Medical AI Pro Imaging" ^
    --add-data "*.py;." ^
    --hidden-import tkinter ^
    --hidden-import matplotlib ^
    --hidden-import pandas ^
    --hidden-import numpy ^
    --hidden-import plotly ^
    --hidden-import PIL ^
    --hidden-import matplotlib.backends.backend_tkagg ^
    --noconsole ^
    --clean ^
    --distpath "dist" ^
    nino_medical_ai_desktop_pro.py

if errorlevel 1 (
    echo ❌ Imaging version build failed!
    goto :error
)

:: Verify second build
if exist "dist\Nino Medical AI Pro Imaging.exe" (
    echo ✅ Imaging version built successfully
    for %%I in ("dist\Nino Medical AI Pro Imaging.exe") do (
        echo    📊 Size: %%~zI bytes
    )
) else (
    echo ❌ Imaging executable not found!
    goto :error
)

echo.
echo ===============================================================
echo                    🎉 BUILD COMPLETED
echo ===============================================================

echo [6/6] Final verification...
echo.
echo 📁 Build Results:
echo ================

if exist "dist\Nino Medical AI Pro.exe" (
    echo ✅ Nino Medical AI Pro.exe
    for %%I in ("dist\Nino Medical AI Pro.exe") do (
        echo    📊 Size: %%~zI bytes (~%%~zI KB)
    )
) else (
    echo ❌ Nino Medical AI Pro.exe - MISSING
)

if exist "dist\Nino Medical AI Pro Imaging.exe" (
    echo ✅ Nino Medical AI Pro Imaging.exe  
    for %%I in ("dist\Nino Medical AI Pro Imaging.exe") do (
        echo    📊 Size: %%~zI bytes (~%%~zI KB)
    )
) else (
    echo ❌ Nino Medical AI Pro Imaging.exe - MISSING
)

echo.
echo 🎯 Usage Instructions:
echo ======================
echo • Nino Medical AI Pro.exe         - Lightweight version (No imaging)
echo • Nino Medical AI Pro Imaging.exe - Full version (With imaging)
echo.
echo Both executables are located in the 'dist' folder.
echo You can distribute them as standalone applications.

echo.
echo ===============================================================
echo                 ✨ SUCCESS! ✨
echo        Both versions built successfully!
echo ===============================================================

:: Clean temporary files
echo.
echo Cleaning temporary files...
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"

echo.
echo 🎉 All done! Press any key to exit...
pause >nul
exit /b 0

:error
echo.
echo ===============================================================
echo                     ❌ BUILD FAILED
echo ===============================================================
echo.
echo Please check the error messages above and try again.
echo.
echo Common issues:
echo • Missing Python dependencies - run: pip install -r requirements.txt
echo • Insufficient disk space
echo • Antivirus blocking PyInstaller
echo.
echo 📧 Need help? Contact: ninomedical.ai@gmail.com
echo.
pause
exit /b 1
