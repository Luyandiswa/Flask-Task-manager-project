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
- **Responsive UI**: Basic user interface for easy interaction.

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Data Storage**: In-memory (for simplicity) — could be replaced by a database like SQLite or PostgreSQL in the future.
- **Authentication**: Built-in user authentication using **sessions** in Flask.
- **Password Validation**: Regular expressions for secure password validation.

## How to Run Locally

To run the application on your local machine, follow these steps:

1. **Clone the repository** to your local machine:
   ```bash
   git clone https://github.com/Luyandiswa/flask-project.git
