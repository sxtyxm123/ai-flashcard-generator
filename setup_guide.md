# Setup Instructions for AI Flashcard Generator

This guide will help you set up the AI Flashcard Generator project on your local machine.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.7 or higher**
- **pip** (Python package installer)
- **Git** (for cloning the repository)
- **A web browser** (Chrome, Firefox, Safari, Edge)

## 🔑 API Key Setup

1. **Get a Together.ai API Key**:
   - Visit [Together.ai](https://together.ai)
   - Sign up for an account
   - Navigate to API section
   - Generate a new API key

2. **Configure the API Key**:
   - Open `flask_app.py`
   - Find line 19: `TOGETHER_API_KEY = "2842da1501acb96bdf13df898a71f9a7e8178f5714dd463f4279feb045f0b2be"`
   - Replace the existing key with your actual API key
   - **Important**: Never commit your real API key to version control

## 🚀 Installation Steps

### Step 1: Clone the Repository

```bash
git clone https://github.com/sxtyxm123/ai-flashcard-generator.git
cd ai-flashcard-generator
```

### Step 2: Create a Virtual Environment (Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Create Upload Directory

```bash
mkdir uploads
```

### Step 5: Start the Flask Server

```bash
python flask_app.py
```

You should see output similar to:
```
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
* Running on http://[your-ip]:5000
```

### Step 6: Open the Frontend

1. **Option 1: Direct File Opening**
   - Open `react_app.html` in your web browser
   - Navigate to the file and double-click

2. **Option 2: Local Server (Recommended)**
   - Open a new terminal/command prompt
   - Navigate to the project directory
   - Run a simple HTTP server:
   
   **Python 3:**
   ```bash
   python -m http.server 8000
   ```
   
   **Node.js (if installed):**
   ```bash
   npx serve .
   ```
   
   - Open `http://localhost:8000/react_app.html` in your browser

## 🧪 Testing the Setup

1. **Backend Test**:
   - Visit `http://127.0.0.1:5000/api/health`
   - You should see: `{"status": "healthy", "message": "Flashcard API is running"}`

2. **Frontend Test**:
   - Open the React app in your browser
   - Try entering some sample text and generating flashcards
   - Check if the UI responds correctly

## 🔧 Configuration Options

### File Upload Settings

In `flask_app.py`, you can modify:

```python
# Maximum file size (default: 16MB)
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

# Upload directory
UPLOAD_FOLDER = 'uploads'
```

### API Settings

```python
# Together.ai API URL
TOGETHER_API_URL = "https://api.together.xyz/inference"

# AI Model (you can change this)
"model": "meta-llama/Llama-2-70b-chat-hf"
```

### Frontend Settings

In `react_app.html`, modify the API base URL if needed:

```javascript
const API_BASE_URL = 'http://127.0.0.1:5000/api';
```

## 🚨 Troubleshooting

### Common Issues and Solutions

1. **Port 5000 is already in use**:
   ```bash
   # Change the port in flask_app.py (last line)
   app.run(debug=True, host='0.0.0.0', port=5001)
   
   # Update API_BASE_URL in react_app.html accordingly
   const API_BASE_URL = 'http://127.0.0.1:5001/api';
   ```

2. **CORS errors in browser**:
   - Ensure Flask-CORS is installed: `pip install Flask-CORS`
   - Check that CORS is enabled in `flask_app.py`

3. **Module not found errors**:
   ```bash
   # Reinstall requirements
   pip install --upgrade -r requirements.txt
   ```

4. **API key errors**:
   - Verify your Together.ai API key is correct
   - Check your account has sufficient credits
   - Ensure you're using the correct API endpoint

5. **File upload issues**:
   - Check file size (must be < 16MB)
   - Ensure file format is .txt or .pdf
   - Verify uploads directory exists and is writable

### Debug Mode

To enable detailed error logging:

1. In `flask_app.py`, ensure debug mode is on:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5000)
   ```

2. Check browser console for JavaScript errors
3. Check terminal for Python error messages

## 🔒 Security Considerations

1. **API Key Protection**:
   - Never commit your real API key
   - Consider using environment variables:
   ```python
   import os
   TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY', 'your-default-key')
   ```

2. **File Upload Security**:
   - Only upload trusted files
   - The app automatically deletes uploaded files after processing
   - File size limits are enforced

3. **CORS Configuration**:
   - In production, configure CORS for specific domains only
   - Current setup allows all origins for development

## 🌐 Production Deployment

For production deployment, consider:

1. **Use a production WSGI server** (e.g., Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 flask_app:app
   ```

2. **Set up a reverse proxy** (Nginx, Apache)
3. **Use environment variables** for sensitive configuration
4. **Enable HTTPS** for secure communication
5. **Set up proper logging** and monitoring

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://reactjs.org/docs/)
- [Together.ai API Documentation](https://together.ai/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

## 🆘 Getting Help

If you encounter issues:

1. Check this setup guide thoroughly
2. Look at the main README.md for additional information
3. Search existing GitHub issues
4. Open a new issue with detailed error information

---

**Happy coding! 🎉**