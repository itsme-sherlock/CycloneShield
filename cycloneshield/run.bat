@echo off
title CycloneShield Command Center
cd /d "%~dp0"
echo Starting CycloneShield Dashboard on http://localhost:8501 ...
.\.venv\Scripts\python.exe -m streamlit run app.py
pause
