"""
CycloneShield - Root Application Launcher
Supports both:
  1. `streamlit run app.py`
  2. Direct execution: `python app.py` (auto-detects virtualenv and starts Streamlit web server)
"""
import os
import sys
import subprocess

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CYCLONESHIELD_DIR = os.path.join(ROOT_DIR, "cycloneshield")
VENV_STREAMLIT = os.path.join(CYCLONESHIELD_DIR, ".venv", "Scripts", "streamlit.exe")
VENV_PYTHON = os.path.join(CYCLONESHIELD_DIR, ".venv", "Scripts", "python.exe")
TARGET_APP = os.path.join(CYCLONESHIELD_DIR, "app.py")

# Check if we are running inside an active Streamlit server context
inside_streamlit = False
try:
    import streamlit as st
    import streamlit.runtime
    inside_streamlit = streamlit.runtime.exists()
except Exception:
    inside_streamlit = False

if inside_streamlit:
    # Running inside `streamlit run app.py` - execute the app code directly
    if CYCLONESHIELD_DIR not in sys.path:
        sys.path.insert(0, CYCLONESHIELD_DIR)
    with open(TARGET_APP, "r", encoding="utf-8") as f:
        code = f.read()
    exec(code, {"__name__": "__main__", "__file__": TARGET_APP})
else:
    # User executed `python app.py` directly from terminal.
    # Launch Streamlit server automatically using the project's virtualenv.
    print("=" * 60)
    print("  CycloneShield - Launching Local Streamlit Server")
    print("=" * 60)
    
    cmd = []
    if os.path.exists(VENV_STREAMLIT):
        cmd = [VENV_STREAMLIT, "run", TARGET_APP, "--server.port=8501"]
    elif os.path.exists(VENV_PYTHON):
        cmd = [VENV_PYTHON, "-m", "streamlit", "run", TARGET_APP, "--server.port=8501"]
    else:
        cmd = [sys.executable, "-m", "streamlit", "run", TARGET_APP, "--server.port=8501"]

    print(f"[Launcher] Executing: {' '.join(cmd)}")
    print("[Launcher] Open in browser: http://localhost:8501")
    print("[Launcher] Press Ctrl+C in terminal to stop.")
    try:
        sys.exit(subprocess.call(cmd, cwd=CYCLONESHIELD_DIR))
    except KeyboardInterrupt:
        print("\n[Launcher] Server stopped by user.")

