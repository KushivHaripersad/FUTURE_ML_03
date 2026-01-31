import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from typing import List, Set, Dict
import string

# Download NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

class TextProcessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.skill_patterns = self._load_skill_patterns()
        
    def _load_skill_patterns(self) -> Dict[str, List[str]]:
        """Load skill patterns and keywords for extraction"""
        skill_dict = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'go', 'rust',
                           'typescript', 'sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'oracle'],
            'ml_ai': ['machine learning', 'deep learning', 'neural network', 'tensorflow', 'pytorch', 'scikit-learn',
                     'nlp', 'natural language processing', 'computer vision', 'ai', 'artificial intelligence'],
            'web_dev': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring', 'express'],
            'data_science': ['pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly', 'tableau', 'power bi', 'spark', 'hadoop'],
            'soft_skills': ['communication', 'leadership', 'teamwork', 'problem solving', 'critical thinking', 'time management'],
            'cloud': ['aws', 'azure', 'google cloud', 'docker', 'kubernetes', 'terraform', 'jenkins'],
            'tools': ['git', 'jira', 'confluence', 'slack', 'trello', 'github', 'gitlab']
        }
        return skill_dict
    
    def clean_text(self, text: str) -> str:
        """Clean and preprocess text"""
        if not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize_text(self, text: str) -> List[str]:
        """Tokenize and lemmatize text"""
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        processed_tokens = []
        for token in tokens:
            if token not in self.stop_words and len(token) > 2:
                lemma = self.lemmatizer.lemmatize(token)
                processed_tokens.append(lemma)
        
        return processed_tokens
    
    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """Extract skills from text"""
        skills_found = {category: [] for category in self.skill_patterns.keys()}
        text_lower = text.lower()
        
        for category, skill_list in self.skill_patterns.items():
            for skill in skill_list:
                # Check for exact skill matches
                if skill in text_lower:
                    skills_found[category].append(skill)
                # Check for variations
                elif skill.replace(' ', '') in text_lower.replace(' ', ''):
                    skills_found[category].append(skill)
        
        # Remove empty categories
        skills_found = {k: v for k, v in skills_found.items() if v}
        
        return skills_found
    
    def extract_keywords(self, text: str, top_n: int = 20) -> List[str]:
        """Extract important keywords using TF-IDF like approach"""
        tokens = self.tokenize_text(text)
        
        # Calculate frequency
        freq_dist = nltk.FreqDist(tokens)
        
        # Get most common words
        keywords = [word for word, freq in freq_dist.most_common(top_n)]
        
        return keywords
    
    def preprocess_batch(self, texts: List[str]) -> List[str]:
        """Preprocess a batch of texts"""
        return [self.clean_text(text) for text in texts]