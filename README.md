<h1 align="center">
⚡ API TESTER
</h1>
<p align="center">
  <b>A Full-Stack Intelligent API Testing Platform with Machine Learning Integration</b>
</p>

<p align="center">
  🚀 Automate API Testing • 📊 Analyze Responses • 📄 Generate Reports • 🤖 ML Insights
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Backend-Flask-blue?style=for-the-badge&logo=flask">
  <img src="https://img.shields.io/badge/Frontend-HTML%20CSS%20JS-orange?style=for-the-badge&logo=html5">
  <img src="https://img.shields.io/badge/Database-MySQL-blue?style=for-the-badge&logo=mysql">
  <img src="https://img.shields.io/badge/Machine%20Learning-KMeans%20%7C%20Classification-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/PDF-ReportLab-red?style=for-the-badge">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge">
</p>

---
## 🚀 Introduction

**API TESTER** is a powerful, full-stack web application designed to simplify and automate the process of testing Application Programming Interfaces (APIs). Built using **Flask (Python)** for backend development and **HTML, CSS, JavaScript** for frontend interaction, the system provides a seamless and interactive environment for API validation.

This platform enables users to send API requests, analyze responses in real-time, and generate detailed PDF reports. It also integrates **Machine Learning models** to classify and cluster API responses, providing intelligent insights into API performance and behavior.

With features like **automated testing, secure authentication, real-time analysis, and report generation**, API TESTER serves as a complete solution for developers, testers, and students working with APIs.

---

## 💡 Highlights

- ⚡ Automated API Testing (GET, POST, PUT, DELETE)  
- 📊 Real-Time Response Analysis  
- 🤖 Machine Learning-Based Insights  
- 📄 PDF Report Generation  
- 🔐 Secure User Authentication  
- 🗄️ MySQL-Based Data Management  

---

## 📌 Table of Contents

- [📖 Overview](#-overview)
- [✨ Features](#-features)
- [🧠 Technology Stack](#-technology-stack)
- [🏗️ System Architecture](#️-system-architecture)
- [⚙️ Installation & Setup](#️-installation--setup)
- [🗄️ Database Schema](#️-database-schema)
- [📸 Screenshots](#-screenshots)
- [🌐 Live Demo](#-live-demo)
- [🔐 Security](#-security)
- [📜 License](#-license)
- [👨‍💻 Author](#-author)

---

## 📖 Overview

**API TESTER** is a comprehensive API testing platform designed to simplify and automate the process of validating APIs. It integrates modern web technologies with machine learning techniques to provide intelligent insights into API behavior.

The system allows users to:
- Test multiple APIs simultaneously  
- Analyze responses in real-time  
- Store and track test history  
- Generate downloadable PDF reports  
- Perform intelligent analysis using ML models  

This project demonstrates a strong integration of **backend development, database management, API handling, and machine learning**, making it suitable for real-world applications and academic projects.

---

## ✨ Features

### 🔐 Authentication & User Management
- Secure signup and login system  
- Password hashing using **Werkzeug security**  
- Session-based authentication  
- Protected routes for authorized access  

---

### ⚡ API Testing Engine
- Supports HTTP methods: **GET, POST, PUT, DELETE**  
- Batch API testing (multiple APIs in one request)  
- Custom headers and request body support  
- Real-time response capture  

---

### 📊 Machine Learning Integration
- Classification of API responses  
- Clustering using **K-Means algorithm**  
- Pattern recognition and anomaly detection  

---

### 📄 Report Generation
- Automated PDF reports using **ReportLab**  
- Includes:
  - API request details  
  - Response data  
  - Status codes  
  - Execution summaries  
- Reports stored for future access  

---

### 🗄️ Data Management
- MySQL-based relational database  
- Stores users, API tests, and reports  
- Efficient query handling and structured storage  

---

## 🧠 Technology Stack

| Category        | Technology |
|----------------|-----------|
| Backend        | Flask (Python) |
| Frontend       | HTML, CSS, JavaScript |
| Database       | MySQL |
| Machine Learning | Custom ML Models (K-Means, Classification) |
| API Requests   | Python Requests Library |
| PDF Generation | ReportLab |
| Security       | Werkzeug (Password Hashing) |

---

## 🏗️ System Architecture

```text
          +---------------------------+
          |     User Interface        |
          | (HTML, CSS, JavaScript)   |
          +-------------+-------------+
                        |
                        v
          +---------------------------+
          |   Flask Backend Layer     |
          | - Routing & Logic         |
          | - Authentication          |
          | - API Processing          |
          +-------------+-------------+
                        |
                        v
          +---------------------------+
          |     Database (MySQL)      |
          | - Users                   |
          | - API Tests               |
          | - Reports                 |
          +-------------+-------------+
                        |
                        v
          +---------------------------+
          | Machine Learning Layer    |
          | - Classification          |
          | - Clustering (K-Means)    |
          +-------------+-------------+
                        |
                        v
          +---------------------------+
          | Report Generation         |
          | (ReportLab PDF Engine)    |
          +---------------------------+
```
---

## ⚙️ Installation & Setup
🔹 Prerequisites
- Python 3.x(flask)
- MySQL Server
- pip
  
🔹 Clone Repository
```bash
git clone https://github.com/dhruv-005/API-TESTER.git
cd API-TESTER
```
🔹 Install Dependencies
```bash
pip install flask mysql-connector-python requests reportlab bcrypt
```
🔹 Setup Database
```bash
CREATE DATABASE api_tester_db;

USE api_tester_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(255)
);

CREATE TABLE api_tests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    api_url TEXT,
    method VARCHAR(10),
    headers TEXT,
    body TEXT,
    response TEXT,
    status_code INT,
    test_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    report_path TEXT,
    generated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
🔹 Run Application
```bash
python app.py
```
🔹 Open in browser
```bash
http://127.0.0.1:5000
```
---

## 🗄️ Database Schema
- Users Table
```text
| Field    | Type    | Description     |
| -------- | ------- | --------------- |
| id       | INT     | Primary Key     |
| username | VARCHAR | Unique user     |
| password | VARCHAR | Hashed password |
```

- API Tests Table
```text
| Field       | Type    | Description  |
| ----------- | ------- | ------------ |
| api_url     | TEXT    | API endpoint |
| method      | VARCHAR | HTTP method  |
| response    | TEXT    | API response |
| status_code | INT     | Status code  |
```

- Reports Table
```text
| Field          | Type      | Description  |
| -------------- | --------- | ------------ |
| report_path    | TEXT      | PDF location |
| generated_time | TIMESTAMP | Created time |
```

---

## 📸 Screenshots
-  Login Page
<img width="1366" height="646" alt="Screenshot_2026-04-19_14_49_32" src="https://github.com/user-attachments/assets/0756f36a-6b8e-4779-a31c-66774c6c993c" />
<img width="1366" height="646" alt="Screenshot_2026-04-19_14_49_24" src="https://github.com/user-attachments/assets/ce70af0a-bb51-4e19-872a-0934880a4029" />
<img width="1366" height="649" alt="Screenshot_2026-04-19_14_43_24" src="https://github.com/user-attachments/assets/2e1e03f9-8283-45df-9909-23ec6c751f77" />
<img width="1366" height="647" alt="Screenshot_2026-04-19_14_43_38" src="https://github.com/user-attachments/assets/5bfad126-71a6-4ceb-8630-cfba7b91edd5" />
- Features
<img width="1366" height="647" alt="Screenshot_2026-04-19_13_30_55" src="https://github.com/user-attachments/assets/04cb383c-fa59-454a-abea-5de8a186b167" />
- About
<img width="1366" height="643" alt="Screenshot_2026-04-19_13_31_12" src="https://github.com/user-attachments/assets/a4172972-1837-451b-bc15-a2c0f0353f35" />
<img width="1366" height="649" alt="Screenshot_2026-04-19_13_31_25" src="https://github.com/user-attachments/assets/70017627-5ecb-4d98-8691-a46f456a9aa4" />
- Contact
<img width="1358" height="635" alt="Screenshot_2026-04-19_13_31_44" src="https://github.com/user-attachments/assets/8f5f47fd-60c2-4ea0-8347-d607f44534bc" />
-  API Testing Dashboard
 <img width="1366" height="647" alt="Screenshot_2026-04-19_13_32_58" src="https://github.com/user-attachments/assets/395df77e-b55a-4e1c-95e3-5d168041c14d" />

-  Results Page
<img width="1366" height="647" alt="Screenshot_2026-04-19_13_32_58" src="https://github.com/user-attachments/assets/0609af9e-9d12-4751-9331-289799211b29" />
<img width="1366" height="654" alt="Screenshot_2026-04-19_13_33_06" src="https://github.com/user-attachments/assets/162ad17d-3cc8-4a5a-b854-2160f6c6a88f" />

---
## 🔐 Security

- Password hashing using secure algorithms
- Session-based authentication
- Protected API routes
- Secure database interaction

---
## 📜 License
This project is licensed under the MIT License.

MIT License

Copyright (c) 2025 Dhruv Sonani

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.

---
## 👨‍💻 Author
- Dhruv Sonani
- 🔗 GitHub:https://github.com/dhruv-005
---
