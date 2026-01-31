import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'pandas',
        'numpy', 
        'sklearn',
        'nltk',
        'joblib'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def main():
    """Train models and save them to disk"""
    
    print("=" * 60)
    print("AI Resume Screening System - Model Training")
    print("=" * 60)
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print("\nMissing dependencies:")
        for package in missing:
            print(f"  - {package}")
        print("\nPlease run: python setup.py")
        return
    
    # Paths
    data_path = "data/Resume.csv"
    model_dir = "models"
    
    # Create directories
    os.makedirs(model_dir, exist_ok=True)
    
    print("\nLoading data...")
    
    try:
        from utils.data_loader import DataLoader
        from utils.model_trainer import ModelTrainer
        
        data_loader = DataLoader(data_path)
        df = data_loader.load_csv_data()
        
        if df.empty:
            print("Error: No data loaded. Please check:")
            print(f"  1. Is Resume.csv in the data/ directory?")
            print(f"  2. Does the CSV file contain 'Resume_str' and 'Category' columns?")
            return
        
        print(f"Loaded {len(df)} resumes")
        
        categories = data_loader.get_all_categories()
        if categories:
            print(f"Categories found: {len(categories)}")
            print("Sample categories:", categories[:5])
        else:
            print("Warning: No categories found in data")
        
        # Prepare training data
        texts, labels = data_loader.prepare_training_data()
        
        if not texts or not labels:
            print("Error: No training data available.")
            print("Check that 'Resume_str' and 'Category' columns exist in CSV.")
            return
        
        print(f"\nTraining data prepared: {len(texts)} resumes, {len(labels)} labels")
        
        print("\nTraining models...")
        trainer = ModelTrainer()
        
        # Train category classifier
        results = trainer.train_category_classifier(texts, labels)
        
        print("\n" + "=" * 60)
        print("TRAINING RESULTS")
        print("=" * 60)
        print(f"Accuracy: {results['accuracy']:.2%}")
        print(f"Number of classes: {len(results['classes'])}")
        print("\nClassification Report:")
        print(results['report'])
        
        # Save models
        trainer.save_models(model_dir)
        print(f"\nModels saved to {model_dir}/")
        
        # Test predictions
        print("\n" + "=" * 60)
        print("SAMPLE PREDICTIONS")
        print("=" * 60)
        
        # Get some sample data
        sample_df = data_loader.get_sample_data(3)
        if not sample_df.empty and 'Resume_str' in sample_df.columns and 'Category' in sample_df.columns:
            for idx, row in sample_df.iterrows():
                if idx < 3:  # Show first 3
                    text = row['Resume_str'][:200] + "..." if len(row['Resume_str']) > 200 else row['Resume_str']
                    category, confidence = trainer.predict_category(row['Resume_str'])
                    actual = row['Category'] if 'Category' in row else 'Unknown'
                    print(f"\nResume {idx + 1}:")
                    print(f"  Sample text: {text}")
                    print(f"  Predicted: {category} (confidence: {confidence:.2%})")
                    print(f"  Actual: {actual}")
        else:
            # Use first few training samples
            for i in range(min(3, len(texts))):
                text = texts[i][:200] + "..." if len(texts[i]) > 200 else texts[i]
                category, confidence = trainer.predict_category(texts[i])
                print(f"\nResume {i + 1}:")
                print(f"  Sample text: {text}")
                print(f"  Predicted: {category} (confidence: {confidence:.2%})")
                print(f"  Actual: {labels[i]}")
        
        print("\n" + "=" * 60)
        print("Training completed successfully!")
        print("You can now run: python main.py")
        print("=" * 60)
        
    except ImportError as e:
        print(f"\nImport Error: {e}")
        print("Make sure all dependencies are installed.")
        print("Run: python setup.py")
    except Exception as e:
        print(f"\nError during training: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()