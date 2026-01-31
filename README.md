AI Resume Screening System
A modern, desktop-based AI-powered resume screening application that automates the process of evaluating and ranking job applicants. Built with Python and machine learning, this system helps recruiters and HR professionals efficiently screen resumes against job descriptions.

✨ Features
🎯 Core Functionalities
AI-Powered Resume Screening: Automatically analyzes and scores resumes against job descriptions
Skill Extraction: Identifies technical and soft skills using NLP techniques
Candidate Ranking: Ranks applicants based on job fit using similarity scoring
Skill Gap Analysis: Highlights missing required skills for each candidate
Category Classification: Predicts job category (24 categories supported)

📁 Input Formats
Word Documents Only: Accepts resumes in .docx format
Job Descriptions: Can be typed directly or loaded from .txt/.docx files

💾 Database Management
Persistent Storage: Stores all applicant data in SQLite database
Advanced Search: Search by name, email, or keywords
Sort by Score: One-click ordering by highest match score
Statistics Dashboard: View analytics and performance metrics
Export Functionality: Export database to CSV format

🎨 Modern UI
Professional Interface: Clean, modern design with intuitive layout
Visual Indicators: Color-coded scores and status icons
Real-time Updates: Live progress bars and status notifications
Responsive Design: Adapts to different screen sizes

📋 Supported Job Categories
The system recognizes 24 different job categories:
HR
Designer
Information-Technology
Teacher
Advocate
Business-Development
Healthcare
Fitness
Agriculture
BPO
Sales
Consultant
Digital-Media
Automobile
Chef
Finance
Apparel
Engineering
Accountant
Construction
Public-Relations
Banking
Arts
Aviation

📊 How Resumes Are Scored
1. Keyword Matching (30% of total score)
The system analyzes the text content of both the resume and job description:
What it checks: Frequency and relevance of important words
How it works:
Extracts top 50 keywords from each document
Calculates overlap using Jaccard similarity
Example: If resume and JD share 30 of 50 keywords → 60% keyword match
Why this matters: Shows how well the resume addresses the job's language and requirements

2. Skill Matching (70% of total score)
This is the most important factor in the scoring:
What it checks: Specific skills mentioned in the job description
How it works:
System identifies skills from 7 categories:
Programming (Python, Java, etc.)
ML/AI (Machine Learning, TensorFlow, etc.)
Web Development (React, HTML, etc.)
Data Science (Pandas, Tableau, etc.)
Soft Skills (Communication, Leadership, etc.)
Cloud (AWS, Docker, etc.)
Tools (Git, Jira, etc.)
Calculates: (Matched Skills) ÷ (Total Required Skills)
Example: If JD requires 10 skills and resume has 7 → 70% skill match

🏆 Why Certain Candidates Rank Higher
1. Better Skill Coverage (Most Important)
Candidates who mention more of the required skills score significantly higher.
2. Specific vs. Vague Experience
Specific achievements beat general responsibilities.
3. Relevant Keywords Density
Candidates who naturally incorporate job description keywords score higher.
4. Format and Readability
Well-structured resumes are easier to analyze and get better matches.
5. Quantifiable Achievements
Numbers and metrics are easier for the system to recognize as valuable.

⚠️ What Skills Are Missing
How Missing Skills Are Identified
The system compares required skills from the job description against skills found in resume.

🚀 Quick Start
Prerequisites:
Python 3.8 or higher
pip package manager

Installation:
1. Clone the repository

2. Install dependencies
   pip install -r requirements.txt
   Or manually install then one by one should there be an error.

3. Download NLTK Data
   Run the following commands in Python shell:
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"

4. Setup training data
   Ensure the Resume.csv file is in the data/ directory.
   If there is an error with the csv file, please redownload it from: https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset

5. Train the ML models.
   python train_model.py

6. Run the application
   python main.py

🎮 Usage Guide
Step 1: Load Job Description
Type or paste job description in the text area
Or click "📂 Load" to import from a file (.txt or .docx)

Step 2: Add Resumes
Click "➕ Single" to add individual Word documents
Click "📚 Multiple" to add multiple resumes at once
All loaded resumes appear in the list

Step 3: Screen & Rank
Click "🔍 Screen & Rank" to analyze resumes
View ranked candidates with scores and missing skills
Color-coded results indicate match quality

Step 4: Save & Manage
Click "💾 Save to Database" to store results
Click "💾 View Database" to browse stored applicants
Use "🏆 Order by Score" to sort by highest match

Step 5: Analyze Details
Select a candidate and click "📊 Skill Analysis"
View detailed skill breakdown and gap analysis

🛠️ Technical Details
Machine Learning Models
TF-IDF Vectorizer: Text feature extraction
Random Forest Classifier: Job category prediction
Cosine Similarity: Resume-JD matching
Rule-based Skill Extraction: Keyword matching for skills

Database Schema
applicants table: Stores applicant details and scores
skills table: Stores extracted skills by category
SQLite database: Lightweight, file-based storage

Key Algorithms
Text Preprocessing: Tokenization, lemmatization, stopword removal
Skill Extraction: Pattern matching against skill dictionaries
Similarity Scoring: Combined keyword and skill matching
Category Prediction: Multi-class classification

📊 Performance Metrics
Category Prediction Accuracy: ~85-90% on test data
Processing Speed: ~100 resumes/minute
Storage Efficiency: Compressed database with indexing
Memory Usage: Optimized for desktop use

📧 Contact
For questions, feedback, or support:
Email: kushivharipersad8@gmail.com