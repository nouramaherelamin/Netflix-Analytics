@echo off
cd /d "%~dp0.."
python -m streamlit run app\app.py
pause
