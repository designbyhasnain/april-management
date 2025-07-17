# 🚀 Deploy April Management to Render

## Prerequisites
- Git repository on GitHub/GitLab
- Render account (free tier available)

## Step 1: Prepare Your Project
Create `render.yaml` in your project root:

```yaml
databases:
  - name: april-management-db
    databaseName: april_management
    user: april_user

services:
  - type: web
    name: april-management
    env: python
    buildCommand: "pip install -r requirements.txt && python manage.py collectstatic --noinput"
    startCommand: "python manage.py migrate && gunicorn manyumba.wsgi"
    envVars:
      - key: DEBUG
        value: False
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: april-management-db
          property: connectionString
      - key: ALLOWED_HOSTS
        value: "*"
```

## Step 2: Deploy from Git
1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select your repository
5. Configure:
   - **Name**: april-management
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command**: `python manage.py migrate && gunicorn manyumba.wsgi`

## Step 3: Add Database
1. Click "New +" → "PostgreSQL"
2. Name: april-management-db
3. Copy the connection string

## Step 4: Set Environment Variables
In your web service settings:
- `DEBUG=False`
- `SECRET_KEY=your-secret-key`
- `DATABASE_URL=your-postgres-connection-string`
- `ALLOWED_HOSTS=your-app.onrender.com`

## Step 5: Deploy
1. Click "Create Web Service"
2. Render will automatically build and deploy
3. Monitor the build logs

## ✅ Your app will be live at: https://your-app.onrender.com

## 🔧 Features
- Free tier available (with limitations)
- Automatic deployments from Git
- Built-in PostgreSQL
- Custom domains
- SSL certificates
- Environment variables
- Build and deploy logs
