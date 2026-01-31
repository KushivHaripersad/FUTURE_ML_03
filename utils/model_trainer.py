import joblib
import numpy as np
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from typing import Tuple, Dict, Any, List

class ModelTrainer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            stop_words='english',
            min_df=2,
            max_df=0.8
        )
        self.label_encoder = LabelEncoder()
        self.category_classifier = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        )
        
    def train_category_classifier(self, texts: List[str], labels: List[str]) -> Dict[str, Any]:
        """Train category classification model"""
        # Clean texts
        cleaned_texts = self._clean_texts(texts)
        
        # Encode labels
        encoded_labels = self.label_encoder.fit_transform(labels)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            cleaned_texts, encoded_labels,
            test_size=0.2, random_state=42, stratify=encoded_labels
        )
        
        # Vectorize texts
        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)
        
        # Train classifier
        self.category_classifier.fit(X_train_vec, y_train)
        
        # Evaluate
        y_pred = self.category_classifier.predict(X_test_vec)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, target_names=self.label_encoder.classes_)
        
        return {
            'accuracy': accuracy,
            'report': report,
            'classes': self.label_encoder.classes_.tolist()
        }
    
    def _clean_texts(self, texts: List[str]) -> List[str]:
        """Clean a list of texts"""
        cleaned = []
        for text in texts:
            if isinstance(text, str):
                # Basic cleaning
                text = text.lower()
                text = ' '.join(text.split())  # Remove extra whitespace
                cleaned.append(text)
            else:
                cleaned.append('')
        return cleaned
    
    def predict_category(self, text: str) -> Tuple[str, float]:
        """Predict category for a single resume"""
        if not isinstance(text, str):
            return "Unknown", 0.0
        
        # Clean text
        cleaned_text = text.lower()
        cleaned_text = ' '.join(cleaned_text.split())
        
        # Vectorize
        text_vec = self.vectorizer.transform([cleaned_text])
        
        # Predict
        proba = self.category_classifier.predict_proba(text_vec)[0]
        pred_idx = np.argmax(proba)
        confidence = proba[pred_idx]
        
        # Get category name
        try:
            category = self.label_encoder.inverse_transform([pred_idx])[0]
        except:
            category = "Unknown"
        
        return category, confidence
    
    def save_models(self, model_dir: str):
        """Save trained models to disk"""
        os.makedirs(model_dir, exist_ok=True)
        
        joblib.dump(self.vectorizer, f'{model_dir}/tfidf_vectorizer.pkl')
        joblib.dump(self.label_encoder, f'{model_dir}/label_encoder.pkl')
        joblib.dump(self.category_classifier, f'{model_dir}/category_classifier.pkl')
    
    def load_models(self, model_dir: str):
        """Load trained models from disk"""
        try:
            self.vectorizer = joblib.load(f'{model_dir}/tfidf_vectorizer.pkl')
            self.label_encoder = joblib.load(f'{model_dir}/label_encoder.pkl')
            self.category_classifier = joblib.load(f'{model_dir}/category_classifier.pkl')
            return True
        except Exception as e:
            print(f"Error loading models: {e}")
            return False