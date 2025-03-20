import re
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key')  # Better secret key management
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///tasks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tasks = db.relationship('Task', backref='owner', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

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
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

# Authentication decorator
def login_required(f):    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check password validity
        if not validate_password(password):
            flash("Password must be at least 8 characters long, include one uppercase letter, one number, and one special symbol.", "danger")
            return redirect(url_for('register'))
        
        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists! Please choose another one.", "danger")
            return redirect(url_for('register'))
        
        # Create new user
        new_user = User(username=username)
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
    
    return render_template('register.html')

@app.route('/')
@login_required
def home():
    user_tasks = Task.query.filter_by(user_id=session['user_id']).order_by(Task.created_at.desc()).all()
    return render_template('task_list.html', tasks=user_tasks)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        
        if not title:
            flash('Title is required!', 'danger')
            return redirect(url_for('add_task'))
            
        new_task = Task(
            title=title,
            description=description,
            user_id=session['user_id']
        )
        
        try:
            db.session.add(new_task)
            db.session.commit()
            flash('Task added successfully!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
            
    return render_template('add_task.html')

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    # Security check: ensure user can only edit their own tasks
    if task.user_id != session['user_id']:
        flash('You do not have permission to edit this task', 'danger')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        title = request.form['title']
        
        if not title:
            flash('Title is required!', 'danger')
            return redirect(url_for('edit_task', task_id=task_id))
            
        task.title = title
        task.description = request.form['description']
        
        try:
            db.session.commit()
            flash('Task updated successfully!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
    
    return render_template('edit_task.html', task=task)

@app.route('/toggle/<int:task_id>')
@login_required
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    # Security check
    if task.user_id != session['user_id']:
        flash('You do not have permission to modify this task', 'danger')
        return redirect(url_for('home'))
    
    task.completed = not task.completed
    
    try:
        db.session.commit()
        status = "completed" if task.completed else "marked as incomplete"
        flash(f'Task {status}!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred: {str(e)}', 'danger')
        
    return redirect(url_for('home'))

@app.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    # Security check
    if task.user_id != session['user_id']:
        flash('You do not have permission to delete this task', 'danger')
        return redirect(url_for('home'))
    
    try:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred: {str(e)}', 'danger')
        
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page or url_for('home'))
        else:
            flash('Invalid username or password!', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug=os.environ.get('FLASK_DEBUG', 'True') == 'True')
