# Task Manager Web Application

This is a simple **Task Manager** web application built using **Flask**, a lightweight Python web framework. The app allows users to register, log in, and manage tasks. It's a great example of how to build a basic web application with **Python** on the backend.

## Features

- **User Authentication**: Users can register, log in, and manage their sessions securely.
- **Task Management**: Once logged in, users can add, view, and delete tasks.
- **Password Validation**: Passwords must meet specific security requirements, including:
  - At least 8 characters long
  - At least one uppercase letter
  - At least one number
  - At least one special symbol
- **Added Features**
- User registration and authentication
- Create, read, update, and delete tasks
- Mark tasks as complete/incomplete
- Responsive design with Bootstrap
- Flash messages for user feedback
- Error handling pages (404, 500)
- Security features:
  - Password hashing
  - Password complexity requirements
  - Session-based authentication
  - Protection against unauthorized access to tasks

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Data Storage**: In-memory (for simplicity) — could be replaced by a database like SQLite or PostgreSQL in the future.
- **Authentication**: Built-in user authentication using **sessions** in Flask.
- **Password Validation**: Regular expressions for secure password validation.
# Task Manager Flask Application

## Project Structure
```
task_manager/
│
├── app.py                  # Main Flask application
│
├── static/                 # Static files (CSS, JS, images)
│   └── styles.css          # Custom styles (if needed)
│
├── templates/              # HTML templates
│   ├── base.html           # Base template with common elements
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── task_list.html      # Home page / task list
│   ├── add_task.html       # Add new task page
│   ├── edit_task.html      # Edit task page
│   ├── 404.html            # 404 error page
│   └── 500.html            # 500 error page
│
├── instance/               # Instance-specific files (created automatically)
│   └── tasks.db            # SQLite database
│
└── requirements.txt        # Project dependencies
```

## Setup Instructions

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. Install dependencies:
   ```
   pip install flask flask-sqlalchemy werkzeug
   ```

4. Create a requirements.txt file:
   ```
   pip freeze > requirements.txt
   ```

5. Run the application:
   ```
   python app.py
   ```

6. Access the application in your browser:
   ```
   http://127.0.0.1:5000/
   ```

## Environment Variables (Optional)

You can set these environment variables to configure the application:

- `SECRET_KEY`: Session encryption key (default: 'dev_secret_key')
- `DATABASE_URL`: Database URI (default: 'sqlite:///tasks.db')
- `FLASK_DEBUG`: Debug mode (True/False, default: True)

## Contributors

- [viincci](https://github.com/viincci)
- [Original Author - Luyandiswa](https://github.com/Luyandiswa)
