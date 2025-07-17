@echo off
echo 🚀 April Management - Netlify Deployment
echo =========================================

REM Check if static site exists
if not exist "static_site" (
    echo ❌ Static site not found. Generating...
    python generate-static-site.py
    if errorlevel 1 (
        echo ❌ Failed to generate static site
        pause
        exit /b 1
    )
)

echo ✅ Static site found

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found. Please install Node.js first
    echo 📥 Download from: https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Node.js is available

REM Install Netlify CLI if not present
netlify --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Installing Netlify CLI...
    npm install -g netlify-cli
    if errorlevel 1 (
        echo ❌ Failed to install Netlify CLI
        pause
        exit /b 1
    )
)

echo ✅ Netlify CLI is ready

REM Change to static_site directory
cd static_site

echo 🔐 Opening Netlify login...
netlify login

echo 🚀 Deploying to Netlify...
netlify deploy

echo.
echo 🎯 To deploy to production, run:
echo    netlify deploy --prod
echo.
echo 📖 See DEPLOYMENT_GUIDE.md for more options
echo 🔧 For full functionality, use Heroku/Railway/Render

cd ..
pause
