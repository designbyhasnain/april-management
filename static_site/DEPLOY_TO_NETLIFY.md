
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
