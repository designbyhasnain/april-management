#!/usr/bin/env python
"""
Generate Static Site for Netlify Deployment
This script creates a static version of the Django site for Netlify deployment.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def setup_django():
    """Setup Django environment"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manyumba.settings')
    import django
    django.setup()

def create_static_directory():
    """Create directory for static site"""
    static_dir = Path('static_site')
    if static_dir.exists():
        shutil.rmtree(static_dir)
    static_dir.mkdir()
    return static_dir

def copy_static_files(static_dir):
    """Copy static files (CSS, JS, images)"""
    # Copy Portfolio static files
    portfolio_static = Path('Portfolio/static')
    if portfolio_static.exists():
        shutil.copytree(portfolio_static, static_dir / 'static', dirs_exist_ok=True)
    
    # Copy HouseListing static files
    house_static = Path('HouseListing/static')
    if house_static.exists():
        shutil.copytree(house_static, static_dir / 'static', dirs_exist_ok=True)
    
    # Copy media files
    media_dir = Path('media')
    if media_dir.exists():
        shutil.copytree(media_dir, static_dir / 'media', dirs_exist_ok=True)

def generate_html_pages(static_dir):
    """Generate static HTML pages"""
    from django.test import Client
    from django.urls import reverse
    
    client = Client()
    
    # Define pages to generate
    pages = {
        'index.html': '/',
        # Add more pages as needed
        # 'about.html': '/about/',
        # 'contact.html': '/contact/',
    }
    
    for filename, url in pages.items():
        try:
            response = client.get(url)
            if response.status_code == 200:
                # Write HTML file
                with open(static_dir / filename, 'w', encoding='utf-8') as f:
                    f.write(response.content.decode('utf-8'))
                print(f"✅ Generated {filename}")
            else:
                print(f"❌ Failed to generate {filename} (Status: {response.status_code})")
        except Exception as e:
            print(f"❌ Error generating {filename}: {e}")

def create_netlify_config(static_dir):
    """Create Netlify configuration"""
    netlify_toml = """
[build]
  publish = "."

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[build.environment]
  NODE_VERSION = "18"
"""
    
    with open(static_dir / 'netlify.toml', 'w') as f:
        f.write(netlify_toml)
    
    print("✅ Created netlify.toml")

def create_deployment_instructions(static_dir):
    """Create deployment instructions"""
    instructions = """
# Deploy Static Site to Netlify

## Option 1: Drag & Drop (Easiest)
1. Zip the contents of the `static_site` folder
2. Go to https://app.netlify.com/drop
3. Drag and drop the zip file
4. Your site will be live instantly!

## Option 2: Git Integration
1. Create a new repository on GitHub
2. Copy the contents of `static_site` to the repository
3. Push to GitHub
4. Connect the repository to Netlify
5. Deploy automatically on every push

## Option 3: Netlify CLI
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Deploy from static_site directory
cd static_site
netlify deploy

# Deploy to production
netlify deploy --prod
```

## Limitations of Static Version
- No dynamic functionality (forms, user accounts, etc.)
- No database interactions
- No server-side processing
- Only displays static content

## For Full Functionality
Use Heroku, Railway, or Render for the complete Django application.
"""

    with open(static_dir / 'DEPLOY_TO_NETLIFY.md', 'w', encoding='utf-8') as f:
        f.write(instructions)

    print("Created deployment instructions")

def main():
    """Main function"""
    print("Generating static site for Netlify deployment...")

    try:
        # Setup Django
        setup_django()

        # Create static directory
        static_dir = create_static_directory()
        print(f"Created directory: {static_dir}")

        # Copy static files
        copy_static_files(static_dir)
        print("Copied static files")

        # Generate HTML pages
        generate_html_pages(static_dir)

        # Create Netlify config
        create_netlify_config(static_dir)

        # Create deployment instructions
        create_deployment_instructions(static_dir)

        print(f"\nStatic site generated successfully!")
        print(f"Location: {static_dir.absolute()}")
        print(f"Read DEPLOY_TO_NETLIFY.md for deployment instructions")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
