# 🚀 Deploy April Management to Heroku

## Prerequisites
- Git installed
- Heroku CLI installed
- Heroku account

## Step 1: Install Heroku CLI
```bash
# Windows (using npm)
npm install -g heroku

# Or download from: https://devcenter.heroku.com/articles/heroku-cli
```

## Step 2: Login to Heroku
```bash
heroku login
```

## Step 3: Initialize Git Repository (if not already done)
```bash
cd AprilManagemnt-main
git init
git add .
git commit -m "Initial commit"
```

## Step 4: Create Heroku App
```bash
heroku create april-management-app
# Or with custom name:
heroku create your-custom-name
```

## Step 5: Set Environment Variables
```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY="your-secret-key-here"
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"
```

## Step 6: Add PostgreSQL Database
```bash
heroku addons:create heroku-postgresql:mini
```

## Step 7: Deploy
```bash
git push heroku main
```

## Step 8: Run Migrations
```bash
heroku run python manage.py migrate
heroku run python manage.py collectstatic --noinput
heroku run python manage.py createsuperuser
```

## Step 9: Open Your App
```bash
heroku open
```

## ✅ Your app will be live at: https://your-app-name.herokuapp.com

## 🔧 Troubleshooting
- Check logs: `heroku logs --tail`
- Restart app: `heroku restart`
- Run commands: `heroku run python manage.py shell`
