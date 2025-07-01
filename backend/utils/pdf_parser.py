import fitz  # PyMuPDF
import pdfplumber
from docx import Document
import os
from typing import Optional

def extract_text_from_pdf_pymupdf(file_path: str) -> str:
    """Extract text from PDF using PyMuPDF"""
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text.strip()
    except Exception as e:
        print(f"Error extracting text with PyMuPDF: {e}")
        return ""

def extract_text_from_pdf_pdfplumber(file_path: str) -> str:
    """Extract text from PDF using pdfplumber (fallback)"""
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error extracting text with pdfplumber: {e}")
        return ""

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX file"""
    try:
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return ""

def extract_text_from_file(file_path: str) -> Optional[str]:
    """Extract text from file based on extension"""
    if not os.path.exists(file_path):
        return None
    
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        # Try PyMuPDF first, fallback to pdfplumber
        text = extract_text_from_pdf_pymupdf(file_path)
        if not text:
            text = extract_text_from_pdf_pdfplumber(file_path)
        return text if text else None
    
    elif file_extension in ['.docx', '.doc']:
        return extract_text_from_docx(file_path)
    
    else:
        return None
