# Quick Setup Guide

## 🚀 Simple 3-Command Setup

### Prerequisites
- Python 3.8+
- Google AI API Key (get from https://makersuite.google.com/app/apikey)
- Cloud PostgreSQL database (already configured)

## Setup Steps

1. **Setup Environment & Install Dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r backend/requirements.txt
   ```

2. **Configure & Start Backend**
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env with your Google API key and database URL
   python main.py
   ```


3. **Start Frontend (in new terminal)**
   ```bash
   cd frontend
   python -m http.server 3000
   # Or open index.html with live server extension
   ```

### Access Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Alternative for Windows Users

### Command Prompt:
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r backend/requirements.txt
cd backend && python main.py
```

### PowerShell:
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
cd backend; python main.py
```


>>>>>>> a31a79b369417daa58d80c1fe5fa18907c01ca5b
## Testing

Test the API:
```bash
python test_api.py
```

## Troubleshooting

**Common Issues:**
1. **Database connection errors**: Check cloud PostgreSQL credentials are correct in .env
2. **Gemini API errors**: Verify API key is valid and has quota
3. **File upload errors**: Ensure `sample_data` directory exists and is writable
4. **CORS errors**: Check backend is running on expected port (8000)

For detailed instructions, see README.md
