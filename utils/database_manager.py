import sqlite3
import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional

class DatabaseManager:
    def __init__(self, db_path: str = "resumes.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create applicants table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS applicants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            resume_text TEXT,
            file_path TEXT,
            category TEXT,
            score REAL,
            missing_skills TEXT,
            processed_date TIMESTAMP,
            added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create skills table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            applicant_id INTEGER,
            skill_category TEXT,
            skill_name TEXT,
            FOREIGN KEY (applicant_id) REFERENCES applicants (id)
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_applicant(self, applicant_data: Dict) -> int:
        """Add a new applicant to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO applicants 
        (name, email, phone, resume_text, file_path, category, score, missing_skills, processed_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            applicant_data.get('name', ''),
            applicant_data.get('email', ''),
            applicant_data.get('phone', ''),
            applicant_data.get('resume_text', ''),
            applicant_data.get('file_path', ''),
            applicant_data.get('category', 'Unknown'),
            applicant_data.get('score', 0.0),
            applicant_data.get('missing_skills', ''),
            applicant_data.get('processed_date', datetime.now())
        ))
        
        applicant_id = cursor.lastrowid
        
        # Add skills if provided
        if 'skills' in applicant_data:
            for category, skills in applicant_data['skills'].items():
                for skill in skills:
                    cursor.execute('''
                    INSERT INTO skills (applicant_id, skill_category, skill_name)
                    VALUES (?, ?, ?)
                    ''', (applicant_id, category, skill))
        
        conn.commit()
        conn.close()
        return applicant_id
    
    def get_all_applicants(self, order_by_score: bool = False) -> pd.DataFrame:
        """Get all applicants from database"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
        SELECT 
            id, name, email, phone, category, score, 
            missing_skills, processed_date, added_date
        FROM applicants
        '''
        
        if order_by_score:
            query += ' ORDER BY score DESC'
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def get_applicant_by_id(self, applicant_id: int) -> Optional[Dict]:
        """Get applicant details by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT * FROM applicants WHERE id = ?
        ''', (applicant_id,))
        
        row = cursor.fetchone()
        if not row:
            conn.close()
            return None
        
        # Get column names
        cursor.execute('PRAGMA table_info(applicants)')
        columns = [col[1] for col in cursor.fetchall()]
        
        # Create dictionary
        applicant = dict(zip(columns, row))
        
        # Get skills
        cursor.execute('''
        SELECT skill_category, skill_name FROM skills WHERE applicant_id = ?
        ''', (applicant_id,))
        
        skills = {}
        for category, skill in cursor.fetchall():
            if category not in skills:
                skills[category] = []
            skills[category].append(skill)
        
        applicant['skills'] = skills
        conn.close()
        return applicant
    
    def search_applicants(self, keyword: str, min_score: float = 0.0) -> pd.DataFrame:
        """Search applicants by keyword"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
        SELECT 
            id, name, email, phone, category, score, 
            missing_skills, processed_date
        FROM applicants
        WHERE (name LIKE ? OR email LIKE ? OR resume_text LIKE ?)
          AND score >= ?
        ORDER BY score DESC
        '''
        
        search_term = f'%{keyword}%'
        df = pd.read_sql_query(query, conn, params=(search_term, search_term, search_term, min_score))
        conn.close()
        return df
    
    def delete_applicant(self, applicant_id: int) -> bool:
        """Delete applicant from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Delete skills first
            cursor.execute('DELETE FROM skills WHERE applicant_id = ?', (applicant_id,))
            
            # Delete applicant
            cursor.execute('DELETE FROM applicants WHERE id = ?', (applicant_id,))
            
            conn.commit()
            conn.close()
            return cursor.rowcount > 0
        except:
            return False
    
    def clear_all_data(self):
        """Clear all data from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM skills')
        cursor.execute('DELETE FROM applicants')
        
        # Reset autoincrement
        cursor.execute('DELETE FROM sqlite_sequence WHERE name="applicants"')
        cursor.execute('DELETE FROM sqlite_sequence WHERE name="skills"')
        
        conn.commit()
        conn.close()
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM applicants')
        total_applicants = cursor.fetchone()[0]
        
        cursor.execute('SELECT AVG(score) FROM applicants WHERE score > 0')
        avg_score = cursor.fetchone()[0] or 0
        
        cursor.execute('''
        SELECT category, COUNT(*) as count, AVG(score) as avg_score
        FROM applicants 
        GROUP BY category 
        ORDER BY count DESC
        ''')
        
        categories = []
        for row in cursor.fetchall():
            categories.append({
                'category': row[0],
                'count': row[1],
                'avg_score': row[2] or 0
            })
        
        conn.close()
        
        return {
            'total_applicants': total_applicants,
            'average_score': avg_score,
            'categories': categories
        }