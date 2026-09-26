"""
CycloneShield - Root Application Launcher
Delegates execution to cycloneshield/app.py
"""
import os
import sys

cycloneshield_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cycloneshield")
if cycloneshield_dir not in sys.path:
    sys.path.insert(0, cycloneshield_dir)

app_path = os.path.join(cycloneshield_dir, "app.py")
with open(app_path, "r", encoding="utf-8") as f:
    code = f.read()

exec(code, {"__name__": "__main__", "__file__": app_path})
