import subprocess
import sys
import os

def install_packages():
    """Install required packages"""
    packages = [
        'pandas==2.1.3',
        'numpy==1.24.3',
        'scikit-learn==1.3.2',
        'nltk==3.8.1',
        'python-docx==0.8.11',
        'joblib==1.3.2'
    ]
    
    print("Installing required packages...")
    for package in packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}")
    
    print("\nDownloading NLTK data...")
    try:
        import nltk
        nltk.download('punkt', quiet=False)
        nltk.download('stopwords', quiet=False)
        nltk.download('wordnet', quiet=False)
        print("NLTK data downloaded successfully!")
    except Exception as e:
        print(f"Error downloading NLTK data: {e}")

def create_directories():
    """Create necessary directories"""
    directories = ['data', 'models', 'utils', 'app']
    
    print("\nCreating project directories...")
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created: {directory}/")
        else:
            print(f"Already exists: {directory}/")

def main():
    print("=" * 60)
    print("AI Resume Screening System - Setup")
    print("=" * 60)
    
    create_directories()
    install_packages()
    
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Place your Resume.csv file in the data/ directory")
    print("2. Run: python train_model.py")
    print("3. Run: python main.py")

if __name__ == "__main__":
    main()