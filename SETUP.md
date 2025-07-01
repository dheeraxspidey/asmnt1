# Quick Setup Guide

## Prerequisites
- Python 3.8+
- Google AI API Key (get from https://makersuite.google.com/app/apikey)
- Cloud PostgreSQL database (already configured)

## Setup Steps

1. **Configure Environment**
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env with your Google API key and database URL
   ```

2. **Install Dependencies & Start Backend**
   ```bash
   pip install -r requirements.txt
   python main.py
   ```

3. **Start Frontend (in new terminal)**
   ```bash
   cd frontend
   python -m http.server 3000
   ```

4. **Access Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

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
