#!/usr/bin/env python
"""
Test script to verify Supabase database connection
Run this after setting up your DATABASE_URL in .env
"""

import os
import sys
import django
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manyumba.settings')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line

def test_database_connection():
    """Test the database connection"""
    try:
        print("🔄 Testing Supabase database connection...")
        
        # Test basic connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"✅ Connected to PostgreSQL: {version}")
        
        # Test Django ORM
        from django.contrib.auth.models import User
        user_count = User.objects.count()
        print(f"✅ Django ORM working. User count: {user_count}")
        
        print("\n🎉 Supabase connection successful!")
        print("📋 Next steps:")
        print("1. Run: python manage.py migrate")
        print("2. Run: python manage.py createsuperuser")
        print("3. Run: python manage.py runserver")
        
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your DATABASE_URL in .env file")
        print("2. Verify your Supabase project is running")
        print("3. Check your password and project reference")
        print("4. Try the direct connection string instead")
        return False

if __name__ == "__main__":
    test_database_connection()
