@echo off
cd /d "%~dp0"
title BHARAT ALPHA - Worldwide Public Live Broadcaster
".\.venv\Scripts\python.exe" live_tunnel.py
pause

