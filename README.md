# Phishing Website Detection System

A modern, full-stack cybersecurity project that uses Machine Learning to detect phishing URLs with high confidence.

## 🚀 Features

- **URL Scanning**: Real-time extraction of URL features (length, HTTPS, suspicious keywords, etc.).
- **ML Prediction**: Uses a Random Forest Classifier to predict if a URL is "Safe" or "Phishing".
- **Modern UI**: Sleek, glassmorphic design with micro-animations and responsive layouts.
- **Admin Dashboard**: Secure portal to view all scanned URLs, prediction results, and logs.
- **Data Persistence**: Stores results in a MySQL database for administrative review.

## 🛠️ Tech Stack

- **Frontend**: HTML5, Vanilla CSS, JavaScript
- **Backend**: Python (Flask)
- **Machine Learning**: Scikit-learn, Pandas, Joblib
- **Database**: MySQL

## 📦 Installation & Setup

### 1. Prerequisites

- Python 3.8+
- MySQL Server

### 2. Database Configuration

1. Login to your MySQL server.
2. Run the script located at `database/schema.sql` to create the database and tables.

   ```bash
   mysql -u root -p < database/schema.sql
   ```

3. Create a `.env` file in the root directory and add your credentials:

   ```env
   DB_HOST=localhost
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_NAME=phishing_db
   ```

### 3. Application Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Train the Machine Learning model:

   ```bash
   python ml/train.py
   ```

3. Run the application:

   ```bash
   python run.py
   ```

4. Open `http://127.0.0.1:5000` in your browser.

## 📊 Admin Portal

- **Login**: `http://127.0.0.1:5000/login`
- **Default Credentials**:
  - Username: `admin`
  - Password: `admin123`

## 📁 Project Structure

```text
phishing_detection/
├── app/
│   ├── static/          # Modern CSS and JS
│   ├── templates/       # HTML content
│   ├── utils/           # Feature extraction logic
│   └── routes.py        # Flask endpoints
├── ml/
│   ├── train.py         # Model training script
│   └── phishing_model.pkl # Trained model (generated)
├── database/
│   └── schema.sql       # SQL initialization
├── .env                 # Env variables (you create this)
├── requirements.txt     # Dependencies
└── run.py               # Application entry point
```
