# Quick Setup Guide

## 🚀 One-Command Start (All Operating Systems)

### Prerequisites
- Python 3.8+
- Google AI API Key (get from https://makersuite.google.com/app/apikey)
- Cloud PostgreSQL database (already configured)

### Steps

1. **Configure Environment**
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env with your Google API key and database URL
   ```

2. **Start Application**
   ```bash
   cd ..
   python start.py
   ```

3. **Access Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Alternative Startup Methods

### Windows Users:
```cmd
# Command Prompt
start.bat

# PowerShell
.\start.ps1
```

### Manual Setup (Advanced Users)

### Backend
```bash
cd backend
pip install -r requirements.txt
python init_db.py
python main.py
```

### Frontend
```bash
cd frontend
python -m http.server 3000
```

## Testing

Test the API:
```bash
python test_api.py
```

## Troubleshooting

**Common Issues:**
1. **PostgreSQL not running**: Check service status
2. **Missing API key**: Set GOOGLE_API_KEY in .env
3. **Port conflicts**: Change ports in config files
4. **Permission errors**: Ensure scripts are executable

For detailed instructions, see README.md
