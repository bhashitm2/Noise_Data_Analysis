#!/bin/bash

# Setup script for Noise Pollution Dashboard
echo "🔧 Setting up Noise Pollution Dashboard for GitHub deployment..."

# Initialize git repository if not already done
if [ ! -d ".git" ]; then
    echo "📝 Initializing Git repository..."
    git init
else
    echo "✅ Git repository already initialized"
fi

# Add all files except those in .gitignore
echo "📂 Adding files to Git..."
git add .

# Create initial commit
echo "💾 Creating initial commit..."
git commit -m "🎉 Initial commit: Noise Pollution Monitoring Dashboard

Features:
- Interactive Streamlit dashboard
- Multi-city noise pollution analysis
- Temporal trend analysis
- Zone-wise violation monitoring
- Station-wise detailed reports
- Ready for deployment on Streamlit Cloud

Tech Stack: Streamlit, Pandas, Plotly, NumPy, Matplotlib"

echo ""
echo "🎯 Next Steps:"
echo "1. Create a new repository on GitHub (https://github.com/new)"
echo "2. Don't add README, .gitignore, or license (we already have them)"
echo "3. Copy the remote URL from GitHub"
echo "4. Run: git remote add origin <your-github-repo-url>"
echo "5. Run: git branch -M main"
echo "6. Run: git push -u origin main"
echo ""
echo "🚀 Then deploy on Streamlit Cloud:"
echo "1. Go to https://share.streamlit.io"
echo "2. Sign in with your GitHub account"
echo "3. Click 'Deploy an app'"
echo "4. Select your repository and app.py"
echo "5. Click 'Deploy!'"
echo ""
echo "✅ Setup complete! Your project is ready for independent deployment."
