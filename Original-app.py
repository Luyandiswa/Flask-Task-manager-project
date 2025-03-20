import re
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for using sessions

# Simple in-memory store for tasks and users
tasks = []
users = {"admin": "password123"}  # Simple user management (in-memory)

# Dummy function to check if a user is logged in
def is_logged_in():
    return 'username' in session

# Password validation function
def validate_password(password):
    """ Validate password with these requirements:
    - At least 8 characters
    - At least one uppercase letter
    - At least one number
    - At least one special symbol
    """
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):  # Check for uppercase letter
        return False
    if not re.search(r"[0-9]", password):  # Check for numbers
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):  # Check for special symbols
        return False
    return True

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check password validity
        if not validate_password(password):
            flash("Password must be at least 8 characters long, include one uppercase letter, one number, and one special symbol.")
            return redirect(url_for('register'))
        
        # Check if the username already exists
        if username in users:
            flash("Username already exists! Please choose another one.")
            return redirect(url_for('register'))
        
        # If validation passes, create a new user
        users[username] = password
        flash('User registered successfully!')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/')
def home():
    if not is_logged_in():
        return redirect(url_for('login'))  # Redirect to login if not logged in
    return render_template('task_list.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if not is_logged_in():
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        task = {'title': title, 'description': description}
        tasks.append(task)
        flash('Task added successfully!')
        return redirect(url_for('home'))
    return render_template('home.html')

@app.route('/edit/<int:task_index>', methods=['GET', 'POST'])
def edit_task(task_index):
    if not is_logged_in():
        return redirect(url_for('login'))
    
    task = tasks[task_index]
    if request.method == 'POST':
        task['title'] = request.form['title']
        task['description'] = request.form['description']
        flash('Task updated successfully!')
        return redirect(url_for('home'))
    
    return render_template('home.html', task=task)

@app.route('/delete/<int:task_index>')
def delete_task(task_index):
    if not is_logged_in():
        return redirect(url_for('login'))
    
    tasks.pop(task_index)
    flash('Task deleted successfully!')
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the credentials are correct (basic authentication)
        if username in users and users[username] == password:
            session['username'] = username  # Store the username in the session
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials!')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove user from session
    flash('Logged out successfully!')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
