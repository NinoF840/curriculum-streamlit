#!/usr/bin/env python3
"""
Streamlit Runner - Simple launcher for Nino Medical AI
======================================================

Simple script to launch the main Streamlit application.

Author: Antonino Piacenza
Email: ninomedical.ai@gmail.com
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Launch the main Streamlit application."""
    app_path = Path("nino_medical_ai_app.py")
    
    if not app_path.exists():
        print("❌ Main app file not found: nino_medical_ai_app.py")
        sys.exit(1)
    
    print("🚀 Launching Nino Medical AI...")
    print("📍 App will be available at: http://localhost:8501")
    
    # Launch Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "nino_medical_ai_app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Nino Medical AI stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
