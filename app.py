from flask import Flask, render_template, request, redirect, url_for, flash, session
import psycopg2
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = '9fce27c5bd0b2ba35607b8dafafed0021875a46ef656c7ea'

# Database configuration
DB_HOST = 'localhost'
DB_NAME = 'lms'
DB_USER = 'postgres'
DB_PASSWORD = 'dheerajpostgres'

# Define database connection function
def connect_to_database():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    return conn

# Function to authenticate user
def authenticate_user(username, password):
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user and check_password_hash(user[2], password):  # Assuming password is hashed
        return user
    else:
        return None

# Function to register a new user
def register_user(username, password, role):
    conn = connect_to_database()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
    conn.commit()
    cur.close()
    conn.close()

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = authenticate_user(username, password)
        if user:
            session['user_id'] = user[0]  # Store user ID in session
            flash(f'Welcome, {username}!', 'success')
            if user[3] == 'student':
                return redirect(url_for('student_dashboard'))
            elif user[3] == 'teacher':
                return redirect(url_for('teacher_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

# Route for logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

# Route for student dashboard
@app.route('/student/dashboard')
def student_dashboard():
    if 'user_id' in session:
        # Implementation of student dashboard (not provided)
        return render_template('student_dashboard.html')
    else:
        return redirect(url_for('login'))


# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']  # Assuming role is provided in the form
        register_user(username, password, role)
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Route for teacher dashboard
@app.route('/teacher/dashboard')
def teacher_dashboard():
    if 'user_id' in session:
        # Implementation of teacher dashboard (not provided)
        return render_template('teacher_dashboard.html')
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
