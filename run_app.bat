@echo off
cd /d %~dp0
echo Starting HemoTrack...
python -m streamlit run app.py
pause