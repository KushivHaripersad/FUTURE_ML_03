import tkinter as tk
import sys
import os
from pathlib import Path

def check_setup():
    """Check if setup is complete"""
    print("=" * 60)
    print("AI Resume Screening System (Word Documents Only)")
    print("Enhanced Visual Interface")
    print("=" * 60)
    
    # Check for required files and directories
    checks = []
    
    # Check data directory
    if not os.path.exists("data"):
        print("Creating data directory...")
        os.makedirs("data", exist_ok=True)
        checks.append(("data directory", "Created"))
    else:
        checks.append(("data directory", "OK"))
    
    # Check models directory
    if not os.path.exists("models"):
        print("Creating models directory...")
        os.makedirs("models", exist_ok=True)
        checks.append(("models directory", "Created"))
    else:
        checks.append(("models directory", "OK"))
    
    # Check for CSV file (for training only)
    csv_path = "data/Resume.csv"
    if not os.path.exists(csv_path):
        checks.append(("Resume.csv (training)", "Optional - for model training only"))
    else:
        checks.append(("Resume.csv (training)", "Found"))
    
    # Check for trained models
    model_files = ['tfidf_vectorizer.pkl', 'category_classifier.pkl', 'label_encoder.pkl']
    model_dir = "models"
    missing_models = []
    
    for model_file in model_files:
        if not os.path.exists(f"{model_dir}/{model_file}"):
            missing_models.append(model_file)
    
    if missing_models:
        checks.append(("Trained models", f"MISSING {len(missing_models)} files"))
    else:
        checks.append(("Trained models", "All found"))
    
    # Display check results
    print("\nSystem Check:")
    print("-" * 60)
    for check, status in checks:
        print(f"{check:30} {status}")
    print("-" * 60)
    
    # Ask for action if models are missing
    if missing_models:
        print("\nTrained models not found. You need to train the models first.")
        response = input("Do you want to train models now? (y/n): ")
        if response.lower() == 'y':
            import subprocess
            print("\nTraining models...")
            try:
                result = subprocess.run([sys.executable, "train_model.py"], 
                                      capture_output=True, text=True)
                print(result.stdout)
                if result.stderr:
                    print("Errors:", result.stderr)
            except Exception as e:
                print(f"Error training models: {e}")
        else:
            print("\nNote: Without trained models, category prediction won't work.")
            print("But you can still use the system for skill extraction and scoring.")
            print("Press Enter to continue...")
            input()
    
    return True

def main():
    """Main entry point"""
    try:
        # Check setup
        check_setup()
        
        # Import and start enhanced GUI
        print("\nStarting enhanced application...")
        
        # Add project root to path
        sys.path.append(str(Path(__file__).parent))
        
        from app.gui_enhanced import ResumeScreenerApp
        
        root = tk.Tk()
        app = ResumeScreenerApp(root)
        root.mainloop()
        
    except ImportError as e:
        print(f"\nImport Error: {e}")
        print("\nDependencies may be missing. Please run:")
        print("pip install -r requirements.txt")
        print("\nOr install manually:")
        print("pip install pandas numpy scikit-learn nltk python-docx joblib pillow")
    except Exception as e:
        print(f"\nError starting application: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()