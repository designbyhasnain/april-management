# 🏠 April Management - Property Management System

A comprehensive Django-based property management system for managing tenants, properties, and rental operations.

## 🚀 Features

- **Property Management**: Add, edit, and manage properties
- **Tenant Management**: Track tenant information and lease details
- **User Authentication**: Secure login with Django Allauth
- **Responsive Design**: Mobile-friendly interface
- **Email Integration**: SendGrid email notifications
- **Image Management**: Cloudinary integration for image uploads
- **Admin Dashboard**: Comprehensive admin interface

## 🛠️ Technology Stack

- **Backend**: Django 4.0.6
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: SQLite (development), PostgreSQL (production)
- **Email**: SendGrid
- **Image Storage**: Cloudinary
- **Authentication**: Django Allauth
- **Deployment**: Heroku, Railway, Render ready

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/designbyhasnain/april-management.git
cd april-management
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables Setup

**IMPORTANT**: Create a `.env` file in the project root with your API keys:

```bash
cp .env.example .env
```

Edit the `.env` file with your actual values:

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Email Configuration (SendGrid)
SENDGRID_API_KEY=your-sendgrid-api-key-here

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Database (for production)
DATABASE_URL=your-database-url-here
```

### 5. Database Setup

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Collect Static Files

```bash
python manage.py collectstatic
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

## 🔑 API Keys Configuration

### SendGrid Email Setup
1. Sign up at [SendGrid](https://sendgrid.com/)
2. Create an API key
3. Add to `.env`: `SENDGRID_API_KEY=your-key-here`

### Cloudinary Image Storage
1. Sign up at [Cloudinary](https://cloudinary.com/)
2. Get your cloud name, API key, and API secret
3. Add to `.env`:
   ```
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret
   ```

## 🚀 Deployment

### Deploy to Heroku
```bash
heroku create april-management-app
heroku config:set DEBUG=False
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set SENDGRID_API_KEY="your-sendgrid-key"
heroku addons:create heroku-postgresql:mini
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Deploy to Railway
See `deploy-railway.md` for detailed instructions.

### Deploy to Render
See `deploy-render.md` for detailed instructions.

## 📁 Project Structure

```
april-management/
├── HouseListing/          # Main app for property management
├── Portfolio/             # Portfolio/landing page app
├── manyumba/             # Django project settings
├── static/               # Static files (CSS, JS, images)
├── staticfiles/          # Collected static files
├── templates/            # HTML templates
├── media/                # User uploaded files
├── .env.example          # Environment variables template
├── requirements.txt      # Python dependencies
└── manage.py            # Django management script
```

## 🔒 Security Notes

- Never commit the `.env` file to version control
- Use strong, unique API keys for production
- Set `DEBUG=False` in production
- Use HTTPS in production
- Regularly rotate API keys

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For support or questions, please contact the development team or create an issue on GitHub.

---

**⚠️ Important**: Make sure to configure all environment variables before running the application!
