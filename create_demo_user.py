#!/usr/bin/env python
"""
Script to create demo user for April Management application
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manyumba.settings')
django.setup()

from django.contrib.auth.models import User
from HouseListing.models import UserProfile, Tenant

def create_demo_user():
    """Create demo user for testing authentication"""

    # Demo user credentials
    username = 'demo@aprilmanagement.com'
    email = 'demo@aprilmanagement.com'
    password = 'AprilRocks'

    # Check if user already exists
    if User.objects.filter(username=username).exists():
        print(f"Demo user '{username}' already exists!")
        user = User.objects.get(username=username)
        # Update password in case it changed
        user.set_password(password)
        user.save()
        print("Password updated for existing demo user.")
    else:
        # Create new demo user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name='Demo',
            last_name='User',
            is_active=True
        )
        print(f"Created demo user: {username}")

def create_admin_user():
    """Create admin user for testing admin functionality"""

    # Admin user credentials
    username = 'admin@aprilmanagement.com'
    email = 'admin@aprilmanagement.com'
    password = 'AdminRocks123'

    # Check if admin user already exists
    if User.objects.filter(username=username).exists():
        print(f"Admin user '{username}' already exists!")
        user = User.objects.get(username=username)
        # Update password and ensure superuser status
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        print("Password updated for existing admin user.")
    else:
        # Create new admin user
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name='Admin',
            last_name='User'
        )
        print(f"Created admin user: {username}")

    return user
    
    # Create or update user profile
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={
            'user_account_type': 'Landlord',
            'full_name': 'Demo User',
            'phone_number': '+1234567890',
            'email': email,
            'account_verified': True,
        }
    )
    
    if created:
        print("Created user profile for demo user")
    else:
        print("Demo user profile already exists")

    # Create or update tenant record for demo user
    tenant, tenant_created = Tenant.objects.get_or_create(
        t_user=user,
        defaults={
            'user': user,  # The landlord/property manager who created this tenant
            'first_name': 'Demo',
            'last_name': 'Tenant',
            'id_number': '123456789',
            'gender': 'Other',
            'email': email,
            'contact': '+1234567890',
        }
    )

    if tenant_created:
        print("Created tenant record for demo user")
    else:
        print("Demo tenant record already exists")

    print(f"Demo user setup complete!")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"User ID: {user.id}")
    print(f"Is Active: {user.is_active}")
    print(f"Tenant ID: {tenant.id if tenant else 'None'}")

if __name__ == '__main__':
    create_demo_user()
    admin_user = create_admin_user()
    print(f"\nAdmin user setup complete!")
    print(f"Admin Username: admin@aprilmanagement.com")
    print(f"Admin Password: AdminRocks123")
    print(f"Admin User ID: {admin_user.id}")
    print(f"Is Superuser: {admin_user.is_superuser}")
    print(f"Is Staff: {admin_user.is_staff}")
