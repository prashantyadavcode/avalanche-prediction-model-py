#!/bin/bash
# Build script for Render deployment

echo "Starting build process..."
echo "Current directory: $(pwd)"
echo "Files in current directory:"
ls -la

echo "Checking for requirements.txt..."
if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt found"
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "❌ requirements.txt not found"
    echo "Creating requirements.txt..."
    cat > requirements.txt << EOF
Flask==2.3.3
Flask-CORS==4.0.0
pandas==1.5.3
numpy==1.21.6
scikit-learn==1.0.2
python-dateutil==2.8.2
Werkzeug==2.3.7
Jinja2==3.1.2
MarkupSafe==2.1.3
itsdangerous==2.1.2
click==8.1.7
blinker==1.6.2
gunicorn==21.2.0
EOF
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

echo "Build completed successfully!"
