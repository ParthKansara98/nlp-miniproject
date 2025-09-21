# Gujarati News Translator & Summarizer

![Gujarati Translator](https://img.shields.io/badge/Language-Gujarati-orange) ![Python](https://img.shields.io/badge/Python-3.11-blue) ![React](https://img.shields.io/badge/React-18-61dafb) ![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688) ![Docker](https://img.shields.io/badge/Docker-Ready-2496ed)

A full-stack AI-powered web application that extracts, translates, and summarizes Gujarati news articles using state-of-the-art machine learning models.

## ✨ Features

### 🔄 Core Functionality
- **URL Processing**: Extract content from Gujarati news websites
- **Direct Text Input**: Process raw Gujarati text directly
- **Translation**: Gujarati to English using HuggingFace Transformers
- **Summarization**: Generate concise summaries of translated content
- **Batch Processing**: Handle multiple articles efficiently

### 📊 Dashboard & Analytics
- **Real-time Statistics**: Track processing metrics and performance
- **Interactive Charts**: Visualize usage patterns with Recharts
- **Recent Activity**: Monitor processing history
- **Performance Metrics**: Analyze translation and summarization quality

### 🎨 User Experience
- **Modern UI**: Clean, responsive design with Tailwind CSS
- **Gujarati Font Support**: Proper rendering of Gujarati text
- **Real-time Processing**: Live status updates and progress indicators
- **Copy to Clipboard**: Easy sharing of results
- **Mobile Responsive**: Works seamlessly on all devices

## 🏗️ Architecture

```
project-root/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # FastAPI application
│   │   ├── models/         # Data models and database
│   │   ├── services/       # ML services (translation, summarization)
│   │   └── utils/          # Helper functions
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Backend container
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/         # Main application pages
│   │   ├── services/      # API communication
│   │   └── utils/         # Helper functions  
│   ├── package.json       # Node dependencies
│   └── Dockerfile        # Frontend container
├── docker-compose.yml     # Development setup
├── docker-compose.prod.yml # Production setup
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose**: For containerized deployment
- **Python 3.11+**: For local backend development
- **Node.js 18+**: For local frontend development
- **Git**: For version control

### 🐳 Docker Deployment (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd gujarati-news-translator
   ```

2. **Start with Docker Compose**
   ```bash
   # Development mode
   docker-compose up --build
   
   # Production mode  
   docker-compose -f docker-compose.prod.yml up --build -d
   ```

3. **Access the application**
   - **Frontend**: http://localhost (or http://localhost:3000 in dev mode)
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs

### 💻 Local Development

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configurations
   ```

5. **Run the backend**
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configurations
   ```

4. **Run the frontend**
   ```bash
   npm start
   ```

## 🔧 Configuration

### Backend Environment Variables

```env
# Server Configuration
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Model Configuration
TRANSLATION_MODEL=Helsinki-NLP/opus-mt-gu-en
SUMMARIZATION_MODEL=facebook/bart-large-cnn

# Database Configuration
DATABASE_URL=sqlite:///./app_data.db

# CORS Configuration
CORS_ORIGINS=["http://localhost:3000", "http://localhost"]

# Processing Configuration
MAX_TEXT_LENGTH=5000
MAX_SUMMARY_LENGTH=150
MIN_SUMMARY_LENGTH=50
REQUEST_TIMEOUT=30
```

### Frontend Environment Variables

```env
# API Configuration
REACT_APP_API_URL=http://localhost:8000

# Build Configuration
GENERATE_SOURCEMAP=false
REACT_APP_VERSION=1.0.0
```

## 📡 API Endpoints

### Core Processing Endpoints

#### `POST /translate`
Translate Gujarati text to English.

```json
{
  "text": "ગુજરાતી ટેક્સ્ટ",
  "source_lang": "gu",
  "target_lang": "en"
}
```

#### `POST /summarize`
Summarize English text.

```json
{
  "text": "English text to summarize",
  "max_length": 150,
  "min_length": 50
}
```

#### `POST /process`
Complete processing pipeline (extract → translate → summarize).

```json
{
  "input_type": "url",  // or "text"
  "content": "https://example.com/news-article",
  "translate": true,
  "summarize": true
}
```

### Analytics Endpoints

#### `GET /stats`
Get application statistics.

#### `GET /recent-activity`
Get recent processing activity.

#### `GET /health`
Health check endpoint.

## 🤖 AI Models

### Translation Model
- **Model**: `Helsinki-NLP/opus-mt-gu-en`
- **Purpose**: Gujarati to English translation
- **Framework**: MarianMT via HuggingFace Transformers

### Summarization Model
- **Model**: `facebook/bart-large-cnn`
- **Purpose**: English text summarization
- **Framework**: BART via HuggingFace Transformers

### News Extraction
- **Library**: `newspaper3k`
- **Purpose**: Extract article content from URLs
- **Features**: Title, text, metadata extraction

## 🚀 Deployment Options

### 1. Docker Compose (Recommended)

```bash
# Development
docker-compose up --build

# Production
docker-compose -f docker-compose.prod.yml up --build -d
```

### 2. Cloud Deployment

#### Render
1. Connect your GitHub repository
2. Create a new Web Service
3. Set build command: `docker-compose build`
4. Set start command: `docker-compose up`

#### Railway
1. Connect your GitHub repository
2. Deploy with Docker
3. Set environment variables
4. Configure custom domain (optional)

#### DigitalOcean App Platform
1. Create new app from GitHub
2. Configure Docker build
3. Set environment variables
4. Deploy

### 3. Manual Deployment

#### Backend (FastAPI)
```bash
# Using Gunicorn
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Using PM2
npm install -g pm2
pm2 start "uvicorn app.main:app --host 0.0.0.0 --port 8000" --name gujarati-translator-api
```

#### Frontend (React)
```bash
# Build for production
npm run build

# Serve with nginx or any static file server
npx serve -s build -p 3000
```

## 🔍 Monitoring & Logging

### Health Checks
- **Backend**: `GET /health`
- **Database**: SQLite connection check
- **ML Models**: Model loading status

### Logging
- **Format**: Structured JSON logging
- **Levels**: DEBUG, INFO, WARNING, ERROR
- **Rotation**: Daily log rotation
- **Storage**: Local files + optional cloud logging

### Metrics
- **Processing Time**: Average response times
- **Success Rate**: Translation/summarization success rates
- **Usage Statistics**: Request counts, user patterns
- **Model Performance**: Accuracy and quality metrics

## 🛠️ Development

### Code Structure

#### Backend
```python
# Service Pattern
from app.services.translation_service import translator_service
result = translator_service.translate_text(text, "gu", "en")

# Database Operations
from app.models.database import db
db.log_translation(original, translated, "gu", "en", time)

# Utilities
from app.utils.helpers import validate_gujarati_text
is_gujarati = validate_gujarati_text(text)
```

#### Frontend
```javascript
// API Calls
import { processContent } from '../services/api';
const result = await processContent('url', url, true, true);

// Utilities
import { formatDuration, copyToClipboard } from '../utils/helpers';
const formattedTime = formatDuration(seconds);

// Components
import InputForm from '../components/InputForm';
<InputForm onSubmit={handleSubmit} loading={loading} />
```

### Testing

#### Backend Testing
```bash
cd backend
pip install pytest pytest-asyncio
pytest tests/ -v
```

#### Frontend Testing
```bash
cd frontend
npm test
npm run test:coverage
```

#### Integration Testing
```bash
# Start services
docker-compose up -d

# Run integration tests
npm run test:integration
```

## 📋 Common Issues & Solutions

### Model Loading Issues
```bash
# Clear HuggingFace cache
rm -rf ~/.cache/huggingface/

# Restart with fresh models
docker-compose down -v
docker-compose up --build
```

### Memory Issues
```yaml
# In docker-compose.yml, increase memory limits
deploy:
  resources:
    limits:
      memory: 4G
```

### CORS Issues
```python
# Update CORS origins in backend/.env
CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]
```

### Database Issues
```bash
# Reset database
rm backend/app_data.db
docker-compose restart backend
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

### Development Guidelines

- **Code Style**: Follow PEP 8 for Python, Prettier for JavaScript
- **Testing**: Add tests for new features
- **Documentation**: Update README and API docs
- **Commits**: Use conventional commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **HuggingFace**: For providing state-of-the-art ML models
- **FastAPI**: For the excellent Python web framework
- **React**: For the powerful frontend framework
- **Tailwind CSS**: For the utility-first CSS framework
- **Newspaper3k**: For news article extraction capabilities

## 📞 Support

- **Documentation**: Check this README and API docs
- **Issues**: Open a GitHub issue for bugs
- **Discussions**: Use GitHub Discussions for questions
- **Email**: [Your Email] for direct support

---

**Built with ❤️ for the Gujarati community and NLP enthusiasts worldwide.**