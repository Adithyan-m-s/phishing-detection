-- Create Database
CREATE DATABASE IF NOT EXISTS phishing_db;
USE phishing_db;

-- Scan Logs Table
CREATE TABLE IF NOT EXISTS scan_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url TEXT NOT NULL,
    prediction VARCHAR(20) NOT NULL,
    confidence FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Admin Users Table
CREATE TABLE IF NOT EXISTS admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Initial Admin (Password should be hashed in production, using 'admin123' here for demo)
INSERT IGNORE INTO admin_users (username, password) VALUES ('admin', 'admin123');
