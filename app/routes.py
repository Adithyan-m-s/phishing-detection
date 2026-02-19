from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import joblib
import os
import mysql.connector
from app.utils.feature_extraction import extract_features
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Model Loading
MODEL_PATH = os.path.join('ml', 'phishing_model.pkl')
model_data = None
if os.path.exists(MODEL_PATH):
    model_data = joblib.load(MODEL_PATH)
else:
    print("Warning: Model file not found. Prediction will be mock-only.")

# Database Connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'phishing_db')
        )
        return conn
    except Exception as e:
        print(f"Database error: {e}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    # Extract features
    features = extract_features(url)
    
    prediction_result = "Safe"
    confidence = 0.95
    
    if model_data:
        # Convert features to DataFrame with proper column order
        feat_df = pd.DataFrame([features])[model_data['feature_names']]
        pred = model_data['model'].predict(feat_df)[0]
        probs = model_data['model'].predict_proba(feat_df)[0]
        
        prediction_result = "Phishing" if pred == 1 else "Safe"
        confidence = float(max(probs))
    
    # Store in DB
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO scan_logs (url, prediction, confidence) VALUES (%s, %s, %s)",
            (url, prediction_result, confidence * 100)
        )
        conn.commit()
        cursor.close()
        conn.close()
    
    return jsonify({
        'url': url,
        'prediction': prediction_result,
        'confidence': round(confidence * 100, 2)
    })

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM admin_users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user:
                session['logged_in'] = True
                return redirect(url_for('admin'))
        
        return render_template('login.html', error="Invalid credentials")
    
    return render_template('login.html')

@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    logs = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM scan_logs ORDER BY created_at DESC")
        logs = cursor.fetchall()
        cursor.close()
        conn.close()
        
    return render_template('admin.html', logs=logs)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
