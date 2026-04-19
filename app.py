from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
import mysql.connector
import os
import time
from werkzeug.security import generate_password_hash, check_password_hash
import ml_models
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import requests

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection function
def get_db():
    # Create a new connection with buffered=True to avoid unread result errors
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='api_tester_db'
    )

# Function to initialize database tables
def init_db():
    # Use connection with buffered cursor
    with get_db() as conn:
        # Create a buffered cursor to avoid unread result errors
        cursor = conn.cursor(buffered=True)
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE,
                password VARCHAR(255)
            );
        ''')
        # Create api_tests table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_tests (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                api_url TEXT,
                method VARCHAR(10),
                headers TEXT,
                body TEXT,
                response TEXT,
                status_code INT,
                test_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        ''')
        # Create reports table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                report_path TEXT,
                generated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        ''')
        conn.commit()

# Run this once at startup to set up tables
init_db()

# --- Routes ---

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_pw = generate_password_hash(password)
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
                conn.commit()
                cursor.close()
            return redirect(url_for('login'))
        except mysql.connector.Error:
            error = 'Username already exists or database error.'
    return render_template('signup.html', error=error)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with get_db() as conn:
            cursor = conn.cursor(dictionary=True, buffered=True)
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            user = cursor.fetchone()
            cursor.close()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('index'))
        else:
            error = 'Invalid credentials.'
    return render_template('login.html', error=error)

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Main page
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

# Route for API Tester page
@app.route('/api_tester')
def api_tester():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('api_tester.html')

# API test route
@app.route('/api/test', methods=['POST'])
def api_test():
    if 'user_id' not in session:
        return jsonify({'error':'Unauthorized'}), 401
    data = request.get_json()
    results = []

    for api in data.get('apis', []):
        url = api.get('url')
        method = api.get('method', 'GET').upper()
        headers = api.get('headers', {})
        body = api.get('body', {})

        try:
            resp = requests.request(method, url, headers=headers, json=body, timeout=10)
            response_text = resp.text
            status_code = resp.status_code

            # Save to database
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO api_tests (user_id, api_url, method, headers, body, response, status_code)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', (session['user_id'], url, method, str(headers), str(body), response_text, status_code))
                conn.commit()
                cursor.close()

            results.append({
                'url': url,
                'method': method,
                'headers': headers,
                'body': body,
                'response': response_text,
                'status_code': status_code
            })

        except Exception as e:
            results.append({
                'url': url,
                'method': method,
                'headers': headers,
                'body': body,
                'response': str(e),
                'status_code': None
            })

    # Call ML models
    labels = ml_models.classify_results(results)
    clusters = ml_models.kmeans_clustering(results)

    # Generate PDF report
    report_dir = 'reports'
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    report_filename = f'report_{session["username"]}_{int(time.time())}.pdf'
    report_path = os.path.join(report_dir, report_filename)

    c = canvas.Canvas(report_path, pagesize=letter)
    width, height = letter
    y_position = height - 50

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y_position, f"API Test Report for {session['username']}")
    y_position -= 30

    # Summary
    c.setFont("Helvetica", 12)
    c.drawString(50, y_position, f"Total API Calls: {len(results)}")
    y_position -= 20

    # Results
    for idx, result in enumerate(results, 1):
        if y_position < 100:
            c.showPage()
            y_position = height - 50
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_position, f"{idx}. URL: {result['url']}")
        y_position -= 15
        c.setFont("Helvetica", 10)
        c.drawString(60, y_position, f"Method: {result['method']}")
        y_position -= 12
        c.drawString(60, y_position, f"Status Code: {result['status_code']}")
        y_position -= 12
        c.drawString(60, y_position, "Response:")
        y_position -= 12
        text_obj = c.beginText(70, y_position)
        for line in result['response'].splitlines():
            if y_position < 50:
                c.showPage()
                y_position = height - 50
                text_obj = c.beginText(70, y_position)
            text_obj.textLine(line)
            y_position -= 12
        c.drawText(text_obj)
        y_position -= 10

    c.save()

    # Save report info in database
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO reports (user_id, report_path) VALUES (%s, %s)', (session['user_id'], report_path))
        conn.commit()
        cursor.close()

    # Generate report URL for frontend
    report_url = '/' + report_path.replace('\\', '/')

    # Return results and report URL
    return jsonify({'results': results, 'report_url': report_url})

# Serve report files
@app.route('/reports/<path:filename>')
def serve_report(filename):
    return send_from_directory('reports', filename)

# View user's reports
@app.route('/my_reports')
def my_reports():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    with get_db() as conn:
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute('SELECT * FROM reports WHERE user_id=%s ORDER BY generated_time DESC', (session['user_id'],))
        reports = cursor.fetchall()
        cursor.close()
    return render_template('my_reports.html', reports=reports)

# View API test results
@app.route('/api_results')
def api_results():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    with get_db() as conn:
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute('SELECT * FROM api_tests WHERE user_id=%s ORDER BY test_time DESC', (session['user_id'],))
        results = cursor.fetchall()
        cursor.close()
    return render_template('api_results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True) 
