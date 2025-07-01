import pdfplumber
from docx import Document
import os
from typing import Optional

def extract_text_from_pdf_pdfplumber(file_path: str) -> str:
    """Extract text from PDF using pdfplumber"""
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
        # Use pdfplumber only (no PyMuPDF)
        text = extract_text_from_pdf_pdfplumber(file_path)
        return text if text else None
    
    elif file_extension in ['.docx', '.doc']:
        return extract_text_from_docx(file_path)
    
    else:
        return None

class DocumentParser:
    """Unified document parser class for deployment compatibility"""
    
    def __init__(self):
        pass
    
    def extract_text(self, file_path: str) -> str:
        """Extract text from PDF or DOCX file using deployment-friendly libraries"""
        result = extract_text_from_file(file_path)
        if result is None:
            raise ValueError(f"Could not extract text from {file_path}")
        return result
