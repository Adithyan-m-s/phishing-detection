import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
import sys

# Add parent directory to path to import feature_extraction
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.utils.feature_extraction import extract_features

def generate_synthetic_data(n_samples=500):
    """
    Generates a synthetic dataset for training.
    In a real scenario, we'd use a CSV from Kaggle or UCI.
    """
    data = []
    
    # Example patterns for "Safe" URLs
    safe_patterns = [
        "https://www.google.com",
        "https://www.github.com",
        "https://www.amazon.in",
        "https://www.nytimes.com",
        "https://en.wikipedia.org",
        "https://docs.python.org",
    ]
    
    # Example patterns for "Phishing" URLs
    phish_patterns = [
        "http://login-secure-verify.com",
        "http://192.168.1.1/admin",
        "http://amaz0n-check.net",
        "http://paypal-security.xyz",
        "https://login-check.top",
    ]
    
    for _ in range(n_samples // 10):
        for base in safe_patterns:
            url = base + "/" + str(np.random.randint(100, 9999))
            feats = extract_features(url)
            feats['label'] = 0
            data.append(feats)
        for base in phish_patterns:
            url = base + "/" + str(np.random.randint(100, 9999))
            feats = extract_features(url)
            feats['label'] = 1
            data.append(feats)
        
    return pd.DataFrame(data)

def train_model():
    print("Generating training data...")
    df = generate_synthetic_data(5000)
    
    X = df.drop('label', axis=1)
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save the model and feature list
    model_path = os.path.join(os.path.dirname(__file__), 'phishing_model.pkl')
    feature_names = X.columns.tolist()
    
    model_data = {
        'model': model,
        'feature_names': feature_names
    }
    
    joblib.dump(model_data, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_model()
