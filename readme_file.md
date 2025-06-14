# AI Flashcard Generator

A powerful web application that transforms any educational content into interactive flashcards using AI technology. Simply paste your text or upload PDF/TXT files, and let the AI generate high-quality flashcards for effective studying.

## 🌟 Features

- **AI-Powered Generation**: Uses advanced language models to create intelligent flashcards
- **Multiple Input Methods**: Support for text input and file uploads (PDF, TXT)
- **Interactive Review**: Flip-card interface for studying
- **Edit & Customize**: Modify generated flashcards to suit your needs
- **Multiple Export Formats**: Export to JSON, CSV, TXT, Anki, and Quizlet formats
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Real-time Processing**: Fast generation with loading indicators

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Node.js (for development)
- Together.ai API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sxtyxm123/ai-flashcard-generator.git
   cd ai-flashcard-generator
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   - Get your API key from [Together.ai](https://together.ai)
   - Replace the API key in `flask_app.py` (line 19)
   ```python
   TOGETHER_API_KEY = "your_api_key_here"
   ```

4. **Run the Flask backend**
   ```bash
   python flask_app.py
   ```

5. **Open the frontend**
   - Open `react_app.html` in your web browser
   - Or serve it using a local server for better performance

## 📁 Project Structure

```
ai-flashcard-generator/
├── flask_app.py           # Flask backend server
├── react_app.html         # React frontend application
├── requirements.txt       # Python dependencies
├── uploads/              # Temporary file storage
├── README.md             # This file
├── LICENSE               # MIT License
└── .gitignore           # Git ignore rules
```

## 🔧 API Endpoints

### Generate Flashcards
- **URL**: `/api/generate-flashcards`
- **Method**: `POST`
- **Body**: Form data with `text_input` and/or `file`
- **Response**: JSON with generated flashcards

### Export Flashcards
- **URL**: `/api/export-flashcards`
- **Method**: `POST`
- **Body**: JSON with flashcards array and format
- **Response**: Exported data in specified format

### Health Check
- **URL**: `/api/health`
- **Method**: `GET`
- **Response**: Server status

## 🎯 Usage

1. **Generate Flashcards**:
   - Enter your educational content in the text area
   - Or upload a PDF/TXT file
   - Click "Generate Flashcards" and wait for AI processing

2. **Review & Edit**:
   - Switch to the "Review" tab
   - Click on any flashcard to edit question/answer
   - Delete unwanted flashcards

3. **Export**:
   - Go to the "Export" tab
   - Choose your preferred format (JSON, CSV, TXT, Anki, Quizlet)
   - Download your flashcards

## 🔒 Security Notes

- **API Key**: Never commit your actual API key to version control
- **File Uploads**: Files are temporarily stored and automatically deleted
- **Input Validation**: All inputs are validated and sanitized

## 🛠️ Configuration

### Supported File Types
- `.txt` - Plain text files
- `.pdf` - PDF documents

### File Size Limits
- Maximum file size: 16MB
- Maximum content length: 5000 characters for text input

### AI Model
- Currently uses: `meta-llama/Llama-2-70b-chat-hf`
- Generates 10-20 flashcards per request
- Fallback system for reliable operation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🚨 Troubleshooting

### Common Issues

1. **Server not starting**:
   - Check if port 5000 is available
   - Ensure all dependencies are installed

2. **API errors**:
   - Verify your Together.ai API key is valid
   - Check internet connection

3. **File upload issues**:
   - Ensure file is under 16MB
   - Check file format (only .txt and .pdf supported)

4. **CORS errors**:
   - Make sure Flask-CORS is installed
   - Check if backend server is running

### Getting Help

- Open an issue on GitHub
- Check the [Issues](https://github.com/sxtyxm123/ai-flashcard-generator/issues) page for known problems

## 🔮 Future Enhancements

- [ ] Database integration for persistent storage
- [ ] User authentication and accounts
- [ ] More AI model options
- [ ] Advanced flashcard scheduling
- [ ] Mobile app version
- [ ] Collaborative studying features
- [ ] Analytics and progress tracking

## 📊 Tech Stack

- **Backend**: Python, Flask, Together.ai API
- **Frontend**: React, Tailwind CSS, Font Awesome
- **File Processing**: PyPDF2 for PDF extraction
- **Export**: Multiple format support

## 🙏 Acknowledgments

- Together.ai for providing the AI API
- React community for the excellent documentation
- Tailwind CSS for the beautiful styling system

---

**Made with ❤️ by [sxtyxm123](https://github.com/sxtyxm123)**

For more information, visit the [project homepage](https://github.com/sxtyxm123/ai-flashcard-generator).