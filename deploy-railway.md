# 🚀 Deploy April Management to Railway

## Prerequisites
- Git repository
- Railway account (free tier available)

## Step 1: Prepare Your Project
```bash
cd AprilManagemnt-main
```

## Step 2: Create railway.json (optional)
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn manyumba.wsgi",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

## Step 3: Deploy Options

### Option A: GitHub Integration (Recommended)
1. Push your code to GitHub
2. Go to [railway.app](https://railway.app)
3. Click "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect Django and deploy

### Option B: Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

## Step 4: Set Environment Variables
In Railway dashboard:
- `DEBUG=False`
- `SECRET_KEY=your-secret-key`
- `ALLOWED_HOSTS=your-domain.railway.app`

## Step 5: Add Database
1. In Railway dashboard, click "New Service"
2. Select "PostgreSQL"
3. Railway will automatically set DATABASE_URL

## ✅ Your app will be live at: https://your-project.railway.app

## 🔧 Features
- Automatic deployments from Git
- Built-in PostgreSQL
- Free tier: $5/month credit
- Custom domains
- Environment variables
- Logs and monitoring
