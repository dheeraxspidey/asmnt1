from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    
    # Personal Information
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    linkedin = Column(String)
    github = Column(String)
    address = Column(Text)
    
    # Skills
    core_skills = Column(JSON)
    soft_skills = Column(JSON)
    
    # Education
    education = Column(JSON)
    
    # Experience
    work_experience = Column(JSON)
    
    # Projects
    projects = Column(JSON)
    
    # Additional Information
    certifications = Column(JSON)
    languages_known = Column(JSON)
    hobbies = Column(JSON)
    
    # AI Analysis
    resume_rating = Column(String)
    improvement_areas = Column(JSON)
    upskill_suggestions = Column(JSON)
    
    # Raw text
    raw_text = Column(Text)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)
