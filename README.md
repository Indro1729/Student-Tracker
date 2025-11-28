# Student Performance Tracker

A simple Flask web application to manage students and their grades.  
Allows teachers to add students, record grades by subject, view student details and averages, and list all students. Uses SQLite for storage.

---

## Table of Contents

- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [Folder Structure](#folder-structure)  
- [Installation](#installation)  
- [Configuration](#configuration)  
- [Database](#database)  
- [Running Locally](#running-locally)  
- [Usage](#usage)  
- [API / Form Endpoints](#api--form-endpoints)  
- [Deployment (Heroku / Render)](#deployment-heroku--render)  
- [Troubleshooting](#troubleshooting)  
- [Contributing](#contributing)  
- [License](#license)

---

## Features

- Add new students (name + roll number).  
- Add grades per student per subject.  
- View student details and subject-wise grades.  
- Calculate and display average marks.  
- List all students.  
- Simple HTML templates (Jinja2) and CSS support.  
- Uses SQLite (file-based) for persistence.

---

## Tech Stack

- Python 3.8+  
- Flask  
- SQLite3  
- Gunicorn (for production)

---

## Folder Structure

