from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from models import get_db, Resume
from services.resume_analyzer import ResumeAnalyzer
from utils.pdf_parser import extract_text_from_file
from config import settings
import os
import uuid
from datetime import datetime
from typing import List

router = APIRouter()
resume_analyzer = ResumeAnalyzer()

@router.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload and analyze a resume"""
    
    # Validate file type
    if not file.filename.lower().endswith(('.pdf', '.docx', '.doc')):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")
    
    try:
        # Create upload directory if it doesn't exist
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
        
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Extract text from file
        extracted_text = extract_text_from_file(file_path)
        if not extracted_text:
            raise HTTPException(status_code=400, detail="Could not extract text from file")
        
        # Analyze resume using Gemini
        analysis_result = resume_analyzer.analyze_resume(extracted_text)
        
        # Create resume record
        resume = Resume(
            file_name=file.filename,
            raw_text=extracted_text,
            **analysis_result
        )
        
        db.add(resume)
        db.commit()
        db.refresh(resume)
        
        # Return structured response
        return {
            "id": resume.id,
            "file_name": resume.file_name,
            "upload_date": resume.upload_date,
            **analysis_result
        }
        
    except Exception as e:
        # Clean up file if error occurs
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")

@router.get("/resumes")
def get_resumes(db: Session = Depends(get_db)):
    """Get list of all resumes with basic info"""
    resumes = db.query(Resume).all()
    
    return [
        {
            "id": resume.id,
            "name": resume.name or "Unknown",
            "email": resume.email or "Unknown",
            "phone": resume.phone or "Unknown",
            "file_name": resume.file_name,
            "upload_date": resume.upload_date
        }
        for resume in resumes
    ]

@router.get("/resume/{resume_id}")
def get_resume_details(resume_id: int, db: Session = Depends(get_db)):
    """Get detailed information for a specific resume"""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    return {
        "id": resume.id,
        "file_name": resume.file_name,
        "upload_date": resume.upload_date,
        "name": resume.name,
        "email": resume.email,
        "phone": resume.phone,
        "linkedin": resume.linkedin,
        "github": resume.github,
        "address": resume.address,
        "core_skills": resume.core_skills,
        "soft_skills": resume.soft_skills,
        "education": resume.education,
        "work_experience": resume.work_experience,
        "projects": resume.projects,
        "certifications": resume.certifications,
        "languages_known": resume.languages_known,
        "hobbies": resume.hobbies,
        "resume_rating": resume.resume_rating,
        "improvement_areas": resume.improvement_areas,
        "upskill_suggestions": resume.upskill_suggestions
    }

@router.delete("/resume/{resume_id}")
def delete_resume(resume_id: int, db: Session = Depends(get_db)):
    """Delete a resume record"""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    db.delete(resume)
    db.commit()
    
    return {"message": "Resume deleted successfully"}
