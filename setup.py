#!/usr/bin/env python
"""
Setup script for April Management
Run this script to set up the development environment
"""

import os
import sys
import subprocess
import shutil

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}:")
        print(f"Command: {command}")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def create_env_file():
    """Create .env file from .env.example if it doesn't exist"""
    if os.path.exists('.env'):
        print("✅ .env file already exists")
        return True
    
    if os.path.exists('.env.example'):
        shutil.copy('.env.example', '.env')
        print("✅ Created .env file from .env.example")
        print("⚠️  Please edit .env file with your actual API keys")
        return True
    else:
        print("❌ .env.example file not found")
        return False

def main():
    """Main setup function"""
    print("🏠 April Management - Development Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Run migrations
    if not run_command("python manage.py migrate", "Running database migrations"):
        sys.exit(1)
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        sys.exit(1)
    
    # Check Django configuration
    if not run_command("python manage.py check", "Checking Django configuration"):
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your API keys")
    print("2. Create a superuser: python manage.py createsuperuser")
    print("3. Run the server: python manage.py runserver")
    print("4. Visit: http://127.0.0.1:8000")
    
    # Ask if user wants to create superuser
    create_superuser = input("\n❓ Would you like to create a superuser now? (y/n): ").lower().strip()
    if create_superuser in ['y', 'yes']:
        run_command("python manage.py createsuperuser", "Creating superuser")
    
    print("\n🚀 Ready to start development!")

if __name__ == "__main__":
    main()
