# Resume Intelligence App

A simple application that helps you analyze resumes using AI. Upload your resume, and get insights on how to improve it.

## What It Does

- Upload your resume (PDF or DOCX)
- See information extracted from your resume
- Get AI-powered feedback on how to improve it
- View your previously uploaded resumes

## How to Run

You only need three simple commands to get the app running:

```bash
# 1. Set up your environment
python -m venv venv && source venv/bin/activate && pip install -r backend/requirements.txt

# 2. Start the backend server
cd backend && cp .env.example .env
# Edit .env file to add your Google API key
python main.py

# 3. Start the frontend (in a new terminal)
cd frontend && python -m http.server 3000
```

Then just open http://localhost:3000 in your browser!

### What You'll Need

- Python 3.8 or newer
- A Google Gemini API key (get one at https://makersuite.google.com/app/apikey)
- The database is already configured for you

### For Windows Users

If you're on Windows, use these commands instead:

Command Prompt:
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r backend/requirements.txt
cd backend && python main.py
```

PowerShell:
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
cd backend; python main.py
```

Remember to start the frontend in a separate terminal with:
```bash
cd frontend
python -m http.server 3000
```

## Using the App

Once the app is running:

1. **Upload a Resume**
   - Click the "Upload Resume" tab
   - Drag and drop your PDF or DOCX file
   - Wait a few seconds for the AI analysis

2. **View Your Resume History**
   - Click the "Resume History" tab
   - See all your past uploads
   - Click "Details" on any resume to see the full analysis

## Troubleshooting Tips

Having problems? Try these quick fixes:

- Make sure you added your Google API key to the `.env` file
- Check that both the frontend and backend are running
- If uploads fail, make sure the `sample_data` directory exists
- For database connection errors, check your PostgreSQL credentials in the `.env` file
- If you get Gemini API errors, verify your API key is valid and has quota
- For CORS errors, check that the backend is running on port 8000

## Screenshots

### Upload Your Resume
![Screenshot from 2025-07-01 20-55-01](https://github.com/user-attachments/assets/6b6acc74-380c-4b3c-b433-7bcd27e6f6c4)

![Resume Upload Screen](/screenshots/Screenshot%20from%202025-07-01%2016-39-00.png)
*Simple drag and drop interface for uploading your resume*

### See the Analysis
![Resume Analysis](/screenshots/Screenshot%20from%202025-07-01%2017-29-31.png)
*Get helpful feedback on your resume*

### View Your History
![Resume History](/screenshots/Screenshot%20from%202025-07-01%2017-32-04.png)
*Access all your previously uploaded resumes*
