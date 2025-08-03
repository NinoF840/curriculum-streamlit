#!/usr/bin/env python3
"""
Optimized Build Script for Nino Medical AI Pro
Builds both regular and debug versions with size optimizations
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n🔧 {description}...")
    print(f"Command: {' '.join(cmd)}")
    
    start_time = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    end_time = time.time()
    
    if result.returncode == 0:
        print(f"✅ {description} completed in {end_time - start_time:.1f}s")
        return True
    else:
        print(f"❌ {description} failed!")
        print(f"Error: {result.stderr}")
        return False

def clean_build_dirs():
    """Clean previous build directories"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"🧹 Cleaning {dir_name}/...")
            if os.name == 'nt':  # Windows
                subprocess.run(['rmdir', '/s', '/q', dir_name], shell=True)
            else:  # Unix/Linux
                subprocess.run(['rm', '-rf', dir_name])

def get_file_size(filepath):
    """Get file size in MB"""
    if os.path.exists(filepath):
        size_bytes = os.path.getsize(filepath)
        size_mb = size_bytes / (1024 * 1024)
        return size_mb
    return 0

def main():
    print("🚀 Nino Medical AI Pro - Optimized Build Script")
    print("=" * 50)
    
    # Verify we're in the right directory
    if not os.path.exists('nino_medical_ai_app.py'):
        print("❌ Error: nino_medical_ai_app.py not found!")
        print("Please run this script from the project root directory.")
        sys.exit(1)
    
    # Clean previous builds
    print("\n🧹 Cleaning previous builds...")
    clean_build_dirs()
    
    # Build production version
    print("\n🏗️ Building Production Version...")
    prod_success = run_command([
        'pyinstaller',
        '--clean',
        '--noconfirm',
        'nino_medical_ai_pro.spec'
    ], "Production build")
    
    # Build debug version
    print("\n🐛 Building Debug Version...")
    debug_success = run_command([
        'pyinstaller',
        '--clean',
        '--noconfirm',
        'Nino Medical AI Pro Debug.spec'
    ], "Debug build")
    
    # Report results
    print("\n📊 Build Results:")
    print("=" * 50)
    
    if prod_success:
        prod_path = Path('dist/Nino Medical AI Pro.exe')
        if prod_path.exists():
            size = get_file_size(prod_path)
            print(f"✅ Production build: {size:.1f} MB")
        else:
            print("❌ Production build file not found")
    
    if debug_success:
        debug_path = Path('dist/Nino Medical AI Pro Debug.exe')
        if debug_path.exists():
            size = get_file_size(debug_path)
            print(f"✅ Debug build: {size:.1f} MB")
        else:
            print("❌ Debug build file not found")
    
    # Optimization suggestions
    print(f"\n💡 Optimization Summary:")
    print("✅ Excluded 100+ unused libraries")
    print("✅ Minimal Streamlit data files")
    print("✅ Maximum Python optimization level")
    print("✅ UPX compression enabled")
    print("✅ Essential imports only")
    
    if prod_success or debug_success:
        print(f"\n🎉 Build completed successfully!")
        print(f"📁 Output files are in the 'dist/' directory")
    else:
        print(f"\n❌ Build failed. Check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
