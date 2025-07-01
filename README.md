# Resume Intelligence Application

A full-stack application that analyzes resumes using AI (Google Gemini) and provides intelligent insights including resume rating, improvement suggestions, and skill recommendations.

## Features

- **Resume Upload & Analysis**: Upload PDF/DOCX resumes for automatic parsing and AI analysis
- **Structured Data Extraction**: Extract personal info, education, experience, projects, and skills
- **AI-Powered Insights**: Get resume ratings, improvement areas, and upskilling suggestions via Google Gemini
- **Resume History**: View and manage previously uploaded resumes
- **Responsive UI**: Clean, modern interface with detailed modal views
- **RESTful API**: FastAPI backend with PostgreSQL database

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **PostgreSQL**: Database for storing resume data
- **SQLAlchemy**: ORM for database operations
- **LangChain + Google Gemini**: AI analysis and structured data extraction
- **PyMuPDF & pdfplumber**: PDF text extraction
- **python-docx**: DOCX text extraction

### Frontend
- **HTML5/CSS3/JavaScript**: Vanilla frontend with Bootstrap
- **Bootstrap 5**: Responsive UI framework
- **Font Awesome**: Icons

## Setup Instructions

### Prerequisites
- Python 3.8+
- Google AI API key (Gemini)
- Cloud PostgreSQL database (pre-configured)

### Backend Setup

1. **Clone and navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings:
   # GOOGLE_API_KEY=your_gemini_api_key
   # DATABASE_URL=your_cloud_postgresql_url
   ```

4. **Run the backend server**
   ```bash
   python main.py
   ```
   
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Serve the frontend**
   
   Option A - Using Python's built-in server:
   ```bash
   python -m http.server 3000
   ```
   
   Option B - Using Node.js live-server:
   ```bash
   npx live-server --port=3000
   ```
   
   Option C - Open directly in browser:
   ```bash
   open index.html
   ```

3. **Access the application**
   
   Visit `http://localhost:3000` in your browser

### Database Setup

The application will automatically create the required tables on first run. The database schema includes:

- **resumes** table with columns for:
  - Personal information (name, email, phone, etc.)
  - Skills (core_skills, soft_skills as JSON)
  - Education, work experience, projects (as JSON arrays)
  - AI analysis results (rating, improvement areas, suggestions)

## API Endpoints

### POST `/api/upload_resume`
Upload and analyze a resume file
- **Input**: Multipart form data with file
- **Output**: Structured resume data with AI analysis

### GET `/api/resumes`
Get list of all uploaded resumes
- **Output**: Array of resume summaries

### GET `/api/resume/{id}`
Get detailed information for a specific resume
- **Output**: Complete resume data including AI analysis

### DELETE `/api/resume/{id}`
Delete a resume record
- **Output**: Success confirmation

## File Structure

```
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py              # Application configuration
│   ├── models.py              # SQLAlchemy database models
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example          # Environment variables template
│   ├── routes/
│   │   └── resume_routes.py   # API route handlers
│   ├── services/
│   │   └── resume_analyzer.py # LangChain + Gemini integration
│   └── utils/
│       └── pdf_parser.py      # PDF/DOCX text extraction
├── frontend/
│   ├── index.html            # Main HTML file
│   ├── styles.css            # Custom styles
│   └── script.js             # Frontend JavaScript logic
├── sample_data/              # Directory for uploaded resume files
└── README.md                 # This file
```

## Usage

1. **Upload Resume**: 
   - Go to "Upload Resume" tab
   - Drag and drop or click to select PDF/DOCX file
   - View parsed information and AI analysis

2. **View History**:
   - Go to "Resume History" tab
   - See table of all uploaded resumes
   - Click "Details" to view full analysis in modal
   - Click "Delete" to remove resume

3. **AI Analysis**:
   - Each resume gets a rating (X/10)
   - Improvement areas are highlighted
   - Upskilling suggestions provided
   - All insights powered by Google Gemini

## Environment Variables

Create a `.env` file in the backend directory:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql://username:password@localhost:5432/resume_db
UPLOAD_DIR=../sample_data
```

## Error Handling

- Invalid file types are rejected
- Database connection errors are handled gracefully
- AI analysis failures fall back to default structure
- Frontend displays user-friendly error messages

## Security Considerations

- File uploads are validated by type
- Database uses parameterized queries via SQLAlchemy
- CORS is configured for cross-origin requests
- Uploaded files are stored securely in designated directory

## Development

To extend the application:

1. **Add new AI analysis features**: Modify `resume_analyzer.py`
2. **Add new API endpoints**: Create routes in `resume_routes.py`
3. **Modify database schema**: Update `models.py` and create migrations
4. **Enhance frontend**: Modify `script.js` and add new UI components

## Troubleshooting

**Common Issues:**

1. **Database connection errors**: Check cloud PostgreSQL credentials are correct in .env
2. **Gemini API errors**: Verify API key is valid and has quota
3. **File upload errors**: Ensure `sample_data` directory exists and is writable
4. **CORS errors**: Check backend is running on expected port (8000)

## License

This project is for educational purposes.