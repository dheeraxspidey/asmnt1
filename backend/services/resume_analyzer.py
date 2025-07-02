import google.generativeai as genai
from config import settings
import json
import os
from typing import Dict, Any

class ResumeAnalyzer:
    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def create_analysis_prompt(self, resume_text: str) -> str:
        return f"""
You are a resume analysis expert. Extract information from the following resume text and return ONLY a valid JSON object.

REQUIRED JSON FORMAT (return exactly this structure):
{{
  "name": "candidate full name",
  "email": "email address",
  "phone": "phone number", 
  "linkedin": "LinkedIn URL or empty string",
  "github": "GitHub URL or empty string",
  "address": "full address or empty string",
  "core_skills": ["skill1", "skill2", "skill3"],
  "soft_skills": ["communication", "leadership"], 
  "education": [{{"degree": "degree name", "institution": "school name", "year": "graduation year", "gpa": "gpa if available"}}],
  "work_experience": [{{"company": "company name", "position": "job title", "duration": "employment period", "description": "job responsibilities and achievements"}}],
  "projects": [{{"name": "project name", "description": "project description", "technologies_used": ["tech1", "tech2"]}}],
  "certifications": ["certification1", "certification2"],
  "languages_known": ["English", "Spanish"],
  "hobbies": ["hobby1", "hobby2"],
  "resume_rating": "X/10",
  "improvement_areas": ["area1", "area2", "area3"],
  "upskill_suggestions": ["suggestion1", "suggestion2", "suggestion3"]
}}

CRITICAL INSTRUCTIONS:
1. Return ONLY the JSON object - no other text, no markdown, no explanations
2. For work_experience: Look for ANY employment history including jobs, internships, work experience, professional experience, career history
3. Extract ALL work positions found in the resume 
4. If no work experience found, use empty array: []
5. For missing fields, use empty string "" or empty array []
6. Provide realistic resume_rating from 1-10
7. Give 3-5 improvement_areas and upskill_suggestions

Resume Text:
{resume_text}
"""

    def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        """Analyze resume text using Gemini and return structured data"""
        try:
            prompt = self.create_analysis_prompt(resume_text)
            response = self.model.generate_content(prompt)
            
            # Check if response has text
            if not response.text:
                return self._get_default_structure()
            
            # Clean response text
            response_text = response.text.strip()
            
            # Remove markdown formatting if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            parsed_data = json.loads(response_text)
            
            # Ensure work_experience is properly formatted
            if 'work_experience' in parsed_data:
                work_exp = parsed_data['work_experience']
                if isinstance(work_exp, str) or not isinstance(work_exp, list):
                    parsed_data['work_experience'] = []
                else:
                    # Ensure each item in the list is a proper dict
                    formatted_work_exp = []
                    for exp in work_exp:
                        if isinstance(exp, dict):
                            formatted_exp = {
                                'company': exp.get('company', ''),
                                'position': exp.get('position', ''),
                                'duration': exp.get('duration', ''),
                                'description': exp.get('description', '')
                            }
                            formatted_work_exp.append(formatted_exp)
                    parsed_data['work_experience'] = formatted_work_exp
            else:
                parsed_data['work_experience'] = []
            
            # Check if data is nested and flatten it
            if "PERSONAL INFORMATION" in parsed_data or "SKILLS & EXPERIENCE" in parsed_data:
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
                    
            # Ensure work_experience is not None or invalid
            if not parsed_data.get('work_experience') or not isinstance(parsed_data['work_experience'], list):
                parsed_data['work_experience'] = []
            
            return parsed_data
            
        except json.JSONDecodeError as e:
            return self._get_default_structure()
        except Exception as e:
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
