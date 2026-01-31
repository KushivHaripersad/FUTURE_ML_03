import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple
from .text_processor import TextProcessor

class SimilarityScorer:
    def __init__(self):
        self.text_processor = TextProcessor()
        
    def calculate_similarity(self, resume_text: str, job_description: str) -> float:
        """Calculate similarity between resume and job description"""
        resume_clean = self.text_processor.clean_text(resume_text)
        jd_clean = self.text_processor.clean_text(job_description)
        
        # Extract keywords
        resume_keywords = set(self.text_processor.extract_keywords(resume_clean, 50))
        jd_keywords = set(self.text_processor.extract_keywords(jd_clean, 50))
        
        # Calculate Jaccard similarity for keywords
        if len(resume_keywords.union(jd_keywords)) > 0:
            keyword_similarity = len(resume_keywords.intersection(jd_keywords)) / len(resume_keywords.union(jd_keywords))
        else:
            keyword_similarity = 0
        
        # Extract skills
        resume_skills = self.text_processor.extract_skills(resume_text)
        jd_skills = self.text_processor.extract_skills(job_description)
        
        # Calculate skill matching score
        skill_score = self._calculate_skill_score(resume_skills, jd_skills)
        
        # Combine scores (weighted average)
        total_similarity = (keyword_similarity * 0.3) + (skill_score * 0.7)
        
        return min(1.0, total_similarity * 1.2)  # Cap at 1.0
    
    def _calculate_skill_score(self, resume_skills: Dict, jd_skills: Dict) -> float:
        """Calculate skill matching score"""
        if not jd_skills:
            return 0.0
        
        total_jd_skills = sum(len(skills) for skills in jd_skills.values())
        if total_jd_skills == 0:
            return 0.0
        
        matched_skills = 0
        for category, skills in jd_skills.items():
            if category in resume_skills:
                matched_skills += len(set(skills) & set(resume_skills[category]))
        
        return matched_skills / total_jd_skills
    
    def get_skill_gaps(self, resume_text: str, job_description: str) -> Dict[str, List[str]]:
        """Identify missing skills in resume compared to job description"""
        resume_skills = self.text_processor.extract_skills(resume_text)
        jd_skills = self.text_processor.extract_skills(job_description)
        
        skill_gaps = {}
        
        for category, skills in jd_skills.items():
            if category in resume_skills:
                missing = [skill for skill in skills if skill not in resume_skills[category]]
            else:
                missing = skills.copy()
            
            if missing:
                skill_gaps[category] = missing
        
        return skill_gaps
    
    def rank_candidates(self, resumes: List[Dict], job_description: str, 
                       top_n: int = None) -> List[Dict]:
        """Rank candidates based on similarity to job description"""
        ranked = []
        
        for i, resume in enumerate(resumes):
            similarity = self.calculate_similarity(resume['text'], job_description)
            skill_gaps = self.get_skill_gaps(resume['text'], job_description)
            
            ranked.append({
                'index': i,
                'id': resume.get('id', f'resume_{i}'),
                'similarity_score': similarity,
                'skill_gaps': skill_gaps,
                'missing_skills_count': sum(len(skills) for skills in skill_gaps.values()),
                'category': resume.get('category', 'Unknown'),
                'original_data': resume
            })
        
        # Sort by similarity score (descending)
        ranked.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        # Add rank position
        for i, candidate in enumerate(ranked):
            candidate['rank'] = i + 1
        
        if top_n:
            return ranked[:top_n]
        
        return ranked