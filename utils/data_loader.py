import pandas as pd
import os
from typing import List, Dict, Tuple
import re

class DataLoader:
    def __init__(self, csv_path: str = None):
        self.csv_path = csv_path
        self.df = None
        
    def load_csv_data(self) -> pd.DataFrame:
        """Load and prepare resume data from CSV for training"""
        if not self.csv_path or not os.path.exists(self.csv_path):
            print(f"Warning: CSV file not found at {self.csv_path}")
            return pd.DataFrame()
            
        try:
            self.df = pd.read_csv(self.csv_path)
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return pd.DataFrame()
        
        # Basic cleaning
        if 'Resume_str' in self.df.columns:
            self.df['Resume_str'] = self.df['Resume_str'].astype(str)
        else:
            print("Warning: 'Resume_str' column not found in CSV")
            
        if 'Category' in self.df.columns:
            self.df['Category'] = self.df['Category'].astype(str)
        else:
            print("Warning: 'Category' column not found in CSV")
            
        # Create ID mapping
        if 'ID' in self.df.columns:
            self.df['ID'] = self.df['ID'].astype(str)
            
        return self.df
    
    def extract_text_from_docx(self, docx_path: str) -> str:
        """Extract text from Word document"""
        try:
            # Try to import docx
            try:
                from docx import Document
            except ImportError:
                print("Error: python-docx module not installed.")
                print("Please install it with: pip install python-docx")
                return ""
            
            doc = Document(docx_path)
            text = []
            for paragraph in doc.paragraphs:
                text.append(paragraph.text)
            return '\n'.join(text)
        except Exception as e:
            print(f"Error reading Word document {docx_path}: {e}")
            return ""
    
    def extract_resume_info_from_docx(self, docx_path: str) -> Dict:
        """Extract resume information from Word document"""
        text = self.extract_text_from_docx(docx_path)
        if not text:
            return {}
        
        # Extract basic info (simplified - in real app, use more sophisticated parsing)
        filename = os.path.basename(docx_path)
        name = self._extract_name_from_text(text, filename)
        email = self._extract_email_from_text(text)
        phone = self._extract_phone_from_text(text)
        
        return {
            'filename': filename,
            'name': name,
            'email': email,
            'phone': phone,
            'text': text,
            'file_path': docx_path
        }
    
    def _extract_name_from_text(self, text: str, filename: str) -> str:
        """Extract name from resume text"""
        # Simple extraction - first line often contains name
        lines = text.strip().split('\n')
        for line in lines[:3]:  # Check first 3 lines
            line = line.strip()
            if line and len(line.split()) <= 4:  # Likely a name if 4 or fewer words
                return line
        return os.path.splitext(filename)[0]
    
    def _extract_email_from_text(self, text: str) -> str:
        """Extract email from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else ""
    
    def _extract_phone_from_text(self, text: str) -> str:
        """Extract phone number from text"""
        phone_pattern = r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
        phones = re.findall(phone_pattern, text)
        return phones[0] if phones else ""
    
    def get_resume_by_category(self, category: str) -> pd.DataFrame:
        """Filter resumes by category"""
        if self.df is None:
            self.load_csv_data()
        if self.df is not None and not self.df.empty and 'Category' in self.df.columns:
            return self.df[self.df['Category'] == category]
        return pd.DataFrame()
    
    def get_all_categories(self) -> List[str]:
        """Get list of all unique categories"""
        if self.df is None:
            self.load_csv_data()
        if self.df is not None and not self.df.empty and 'Category' in self.df.columns:
            return sorted(self.df['Category'].unique().tolist())
        return []
    
    def prepare_training_data(self) -> Tuple[List[str], List[str]]:
        """Prepare text and labels for model training"""
        if self.df is None:
            self.load_csv_data()
        
        if self.df is not None and not self.df.empty:
            if 'Resume_str' in self.df.columns and 'Category' in self.df.columns:
                texts = self.df['Resume_str'].tolist()
                labels = self.df['Category'].tolist()
                return texts, labels
        
        return [], []
    
    def get_sample_data(self, n_samples: int = 5) -> pd.DataFrame:
        """Get sample data for testing"""
        if self.df is None:
            self.load_csv_data()
        if self.df is not None and not self.df.empty:
            return self.df.head(n_samples)
        return pd.DataFrame()