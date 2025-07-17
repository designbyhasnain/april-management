# PowerShell script to deploy April Management to Netlify
# Run this script to automatically deploy your static site to Netlify

Write-Host "🚀 April Management - Netlify Deployment Script" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# Check if static site exists
if (-not (Test-Path "static_site")) {
    Write-Host "❌ Static site not found. Generating static site..." -ForegroundColor Red
    python generate-static-site.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to generate static site. Please check for errors." -ForegroundColor Red
        exit 1
    }
}

Write-Host "✅ Static site found in 'static_site' folder" -ForegroundColor Green

# Check if Netlify CLI is installed
$netlifyInstalled = Get-Command netlify -ErrorAction SilentlyContinue
if (-not $netlifyInstalled) {
    Write-Host "⚠️  Netlify CLI not found. Installing..." -ForegroundColor Yellow
    npm install -g netlify-cli
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install Netlify CLI. Please install Node.js first." -ForegroundColor Red
        Write-Host "📥 Download Node.js from: https://nodejs.org/" -ForegroundColor Cyan
        exit 1
    }
}

Write-Host "✅ Netlify CLI is available" -ForegroundColor Green

# Change to static_site directory
Set-Location static_site

Write-Host "🔐 Please login to Netlify..." -ForegroundColor Cyan
netlify login

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to login to Netlify" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Logged in to Netlify successfully" -ForegroundColor Green

# Deploy to Netlify
Write-Host "🚀 Deploying to Netlify..." -ForegroundColor Cyan
netlify deploy

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Draft deployment successful!" -ForegroundColor Green
    Write-Host "🌐 Your draft site is now live. Check the URL above." -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🎯 To deploy to production, run:" -ForegroundColor Yellow
    Write-Host "   netlify deploy --prod" -ForegroundColor White
    Write-Host ""
    
    $deployProd = Read-Host "Deploy to production now? (y/N)"
    if ($deployProd -eq "y" -or $deployProd -eq "Y") {
        Write-Host "🚀 Deploying to production..." -ForegroundColor Cyan
        netlify deploy --prod
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "🎉 Production deployment successful!" -ForegroundColor Green
            Write-Host "🌐 Your site is now live!" -ForegroundColor Cyan
        } else {
            Write-Host "❌ Production deployment failed" -ForegroundColor Red
        }
    }
} else {
    Write-Host "❌ Deployment failed" -ForegroundColor Red
}

# Return to original directory
Set-Location ..

Write-Host ""
Write-Host "📖 For more deployment options, see DEPLOYMENT_GUIDE.md" -ForegroundColor Cyan
Write-Host "🔧 For full Django functionality, consider Heroku, Railway, or Render" -ForegroundColor Cyan
