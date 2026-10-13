@echo off
title InsightLab - Advanced EDA Platform
echo ====================================================
echo Starting InsightLab Streamlit Dashboard...
echo ====================================================
call "%~dp0venv\Scripts\activate.bat"
streamlit run "%~dp0app.py"
pause
