@echo off
cd /d "%~dp0"
title Bharat Alpha - Push to GitHub for 24/7 Cloud Deployment
echo =========================================================================
echo  🚀 BHARAT ALPHA: 24/7 CLOUD DEPLOYMENT HELPER (GITHUB + RENDER)
echo =========================================================================
echo.

git --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Git is not installed. Please install Git from https://git-scm.com/
    pause
    exit /b 1
)

git config user.email "admin@bharatalpha.internal" >nul 2>&1
git config user.name "Bharat Alpha" >nul 2>&1

echo [*] Staging all files and committing changes...
git add .
git commit -m "Update Bharat Alpha deployment files" >nul 2>&1

echo.
echo =========================================================================
echo  3 EASY STEPS TO GO LIVE 24/7 IN THE CLOUD:
echo =========================================================================
echo.
echo  STEP 1: Create a New GitHub Repository
echo  --------------------------------------
echo  Open your browser and visit: https://github.com/new
echo  - Name it: bharat-alpha
echo  - Choose: Private (or Public)
echo  - Click "Create repository"
echo.
echo  STEP 2: Push your code
echo  ----------------------
echo  Copy the repository URL shown on GitHub, then paste and run:
echo.
echo      git remote add origin https://github.com/YOUR_USERNAME/bharat-alpha.git
echo      git branch -M main
echo      git push -u origin main
echo.
echo  STEP 3: Deploy Free 24/7 on Render.com
echo  ---------------------------------------
echo  Visit https://dashboard.render.com
echo  - Click "New +" -^> "Web Service"
echo  - Select your "bharat-alpha" repository
echo  - Click "Deploy Web Service"
echo.
echo  Render will build automatically using the included Dockerfile/render.yaml
echo  and give you a permanent 24/7 worldwide address (e.g. https://bharat-alpha.onrender.com)!
echo =========================================================================
pause
