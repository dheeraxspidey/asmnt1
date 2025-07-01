import google.generativeai as genai
from config import settings
import json
from typing import Dict, Any

class ResumeAnalyzer:
    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def create_analysis_prompt(self, resume_text: str) -> str:
        return f"""
Analyze the following resume text and extract information in STRICT JSON format. Return ONLY valid JSON without any additional text or markdown formatting.

You MUST return a FLAT JSON structure with ALL these exact field names:

{{
  "name": "Full name of candidate",
  "email": "Email address",
  "phone": "Phone number", 
  "linkedin": "LinkedIn URL",
  "github": "GitHub URL",
  "address": "Full address",
  "core_skills": ["skill1", "skill2", "skill3"],
  "soft_skills": ["soft1", "soft2"], 
  "education": [{{"degree": "degree", "institution": "school", "year": "year", "gpa": "gpa"}}],
  "work_experience": [{{"company": "company", "position": "role", "duration": "period", "description": "desc"}}],
  "projects": [{{"name": "project", "description": "desc", "technologies_used": ["tech1", "tech2"]}}],
  "certifications": ["cert1", "cert2"],
  "languages_known": ["lang1", "lang2"],
  "hobbies": ["hobby1", "hobby2"],
  "resume_rating": "8/10",
  "improvement_areas": ["Add more metrics", "Include keywords", "Better formatting"],
  "upskill_suggestions": ["Cloud computing", "Advanced Python", "Project management"]
}}

CRITICAL REQUIREMENTS:
1. Return FLAT JSON structure - NO nested categories
2. Use exact field names as shown above
3. MUST provide resume_rating (e.g., "7/10", "8/10")
4. MUST provide 3-5 improvement_areas 
5. MUST provide 3-5 upskill_suggestions
6. If field not found, use empty string "" or empty array []

Resume Text:
{resume_text}

Return ONLY the flat JSON object:
"""

    def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        """Analyze resume text using Gemini and return structured data"""
        try:
            prompt = self.create_analysis_prompt(resume_text)
            
            # Use the direct Gemini API
            response = self.model.generate_content(prompt)
            
            # Check if response has text
            if not response.text:
                print("No response text from Gemini")
                return self._get_default_structure()
            
            # Clean response text
            response_text = response.text.strip()
            print(f"Raw Gemini response: {response_text[:500]}...")  # Debug print
            
            # Remove markdown formatting if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Parse JSON
            parsed_data = json.loads(response_text)
            
            # Check if data is nested and flatten it
            if "PERSONAL INFORMATION" in parsed_data or "SKILLS & EXPERIENCE" in parsed_data:
                print("Detected nested structure, flattening...")
                flattened_data = {}
                
                # Extract personal info
                if "PERSONAL INFORMATION" in parsed_data:
                    flattened_data.update(parsed_data["PERSONAL INFORMATION"])
                
                # Extract skills and experience
                if "SKILLS & EXPERIENCE" in parsed_data:
                    flattened_data.update(parsed_data["SKILLS & EXPERIENCE"])
                
                # Extract AI analysis
                if "AI ANALYSIS" in parsed_data:
                    flattened_data.update(parsed_data["AI ANALYSIS"])
                
                parsed_data = flattened_data
            
            # Validate and set defaults for required fields
            default_data = {
                "name": "",
                "email": "",
                "phone": "",
                "linkedin": "",
                "github": "",
                "address": "",
                "core_skills": [],
                "soft_skills": [],
                "education": [],
                "work_experience": [],
                "projects": [],
                "certifications": [],
                "languages_known": [],
                "hobbies": [],
                "resume_rating": "0/10",
                "improvement_areas": [],
                "upskill_suggestions": []
            }
            
            # Merge with defaults
            for key, default_value in default_data.items():
                if key not in parsed_data:
                    parsed_data[key] = default_value
            
            print(f"Parsed data rating: {parsed_data.get('resume_rating')}")  # Debug print
            print(f"Improvement areas: {parsed_data.get('improvement_areas')}")  # Debug print
            
            return parsed_data
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Raw response: {response_text}")
            return self._get_default_structure()
        except Exception as e:
            print(f"Error analyzing resume: {e}")
            return self._get_default_structure()
    
    def _get_default_structure(self) -> Dict[str, Any]:
        """Return default structure when analysis fails"""
        return {
            "name": "",
            "email": "",
            "phone": "",
            "linkedin": "",
            "github": "",
            "address": "",
            "core_skills": [],
            "soft_skills": [],
            "education": [],
            "work_experience": [],
            "projects": [],
            "certifications": [],
            "languages_known": [],
            "hobbies": [],
            "resume_rating": "0/10",
            "improvement_areas": ["Unable to analyze resume"],
            "upskill_suggestions": []
        }
