import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost:5432/resume_db")
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "../sample_data")
    
    class Config:
        env_file = ".env"

settings = Settings()
