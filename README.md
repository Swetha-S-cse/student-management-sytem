# Student Management System

A Python web application for managing student records — add, search, edit,
delete, and view statistics. Built with **Flask** and simple **JSON file
storage**.

Built as an internship project to demonstrate CRUD operations, object-oriented
design, search/filtering, and a small stats dashboard in a real, runnable web
app.

## Features

- **Student Management** — add, edit, delete, and list students (ID, name,
  age, grade, email, phone)
- **Search** — look up students by name, student ID, or grade
- **Statistics Dashboard** — total student count, average age, grade
  distribution, age distribution, and oldest/youngest student
- **Data Storage** — persisted in a local JSON file (`data/students.json`),
  created automatically on first run
- **Exception Handling** — form validation (all fields required) and
  try/except around file reads/writes and student lookups, with clear
  flash messages instead of crashes

## Project structure

```
students-management-system/
├── web_app.py              # Flask routes (the web application)
├── app/                    # Application helpers
├── models/                 # Student model / data classes
├── templates/               # Jinja2 HTML templates
├── data/
│   └── students.json        # Generated automatically — not tracked in git
├── requirements.txt
└── README.md
```

## Getting started

### 1. Requirements

- Python 3.9+

### 2. Set up a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate       # on Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python web_app.py
```

The data file `data/students.json` is created automatically on first run —
no manual setup needed. Open your browser to:

```
http://127.0.0.1:5000
```

## Using the app

1. **Add a student** → fill in name, age, grade, email, and phone.
2. **Students list** → search by name, ID, or grade.
3. **Edit/Delete** → update or remove a student record.
4. **Statistics** → view total students, average age, and grade/age breakdowns.

## Tech stack

| Layer      | Choice                          |
|------------|----------------------------------|
| Backend    | Python, Flask                   |
| Storage    | JSON file (`data/students.json`) |
| Frontend   | Jinja2 templates                |

## Publishing to GitHub

```bash
git init
git add .
git commit -m "Student Management System"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

(`data/*.json` and `__pycache__/` are excluded via `.gitignore` since the
data file is generated locally — each clone starts with an empty student
list.)

## Possible extensions

- Move from JSON storage to SQLite
- User authentication (teacher/admin login)
- CSV export of student records
- Pagination for large student lists
