"""
File handling + business logic for the Student Management System.

All JSON reads/writes and validation live here so web_app.py only
ever deals with Flask request/response plumbing. Every failure mode
raises a specific exception from app.exceptions instead of being
swallowed or reported generically.
"""

import os
import json

from models.student import Student
from app.exceptions import InvalidDataError, StudentNotFoundError, DataStorageError

DATA_FILE = 'data/students.json'
VALID_GRADES = None  # left open-ended; set e.g. {'A', 'B', 'C', 'D', 'F'} to restrict


# --------------------------------------------------------------------------
# Validation helpers
# --------------------------------------------------------------------------

def _require(value, field_name):
    if value is None or str(value).strip() == '':
        raise InvalidDataError(f"{field_name} is required.")
    return str(value).strip()


def _require_age(value):
    value = _require(value, "Age")
    try:
        age = int(value)
    except ValueError:
        raise InvalidDataError("Age must be a whole number.")
    if age <= 0 or age > 120:
        raise InvalidDataError("Age must be a realistic positive number.")
    return age


def _require_email(value):
    value = _require(value, "Email")
    if "@" not in value or "." not in value.split("@")[-1]:
        raise InvalidDataError("Enter a valid email address.")
    return value


# --------------------------------------------------------------------------
# File handling
# --------------------------------------------------------------------------

def load_students():
    """Read all students from the JSON data file.

    Returns an empty list if the file doesn't exist yet (first run).
    Raises DataStorageError if the file exists but can't be read/parsed,
    instead of silently pretending there's no data.
    """
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
        return [Student.from_dict(item) for item in data]
    except (json.JSONDecodeError, OSError) as e:
        raise DataStorageError(f"Could not read student data: {e}")
    except (KeyError, TypeError) as e:
        raise DataStorageError(f"Student data file is corrupted: {e}")


def save_students(students):
    """Write all students back to the JSON data file."""
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        data = [s.to_dict() for s in students]
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except OSError as e:
        raise DataStorageError(f"Could not save student data: {e}")


def get_next_id(students):
    if not students:
        return 'S001'
    numbers = [int(s.get_student_id()[1:]) for s in students if s.get_student_id().startswith('S')]
    if not numbers:
        return 'S001'
    return f'S{max(numbers) + 1:03d}'


# --------------------------------------------------------------------------
# Business operations (used by the Flask routes)
# --------------------------------------------------------------------------

def add_student(name, age, grade, email, phone):
    name = _require(name, "Name")
    age = _require_age(age)
    grade = _require(grade, "Grade")
    email = _require_email(email)
    phone = _require(phone, "Phone")

    students = load_students()
    student_id = get_next_id(students)
    student = Student(student_id, name, age, grade, email, phone)
    students.append(student)
    save_students(students)
    return student


def get_student(student_id):
    students = load_students()
    for s in students:
        if s.get_student_id() == student_id:
            return s
    raise StudentNotFoundError(f"Student {student_id} was not found.")


def update_student(student_id, name, age, grade, email, phone):
    name = _require(name, "Name")
    age = _require_age(age)
    grade = _require(grade, "Grade")
    email = _require_email(email)
    phone = _require(phone, "Phone")

    students = load_students()
    for i, s in enumerate(students):
        if s.get_student_id() == student_id:
            students[i] = Student(student_id, name, age, grade, email, phone)
            save_students(students)
            return students[i]
    raise StudentNotFoundError(f"Student {student_id} was not found.")


def delete_student(student_id):
    students = load_students()
    remaining = [s for s in students if s.get_student_id() != student_id]
    if len(remaining) == len(students):
        raise StudentNotFoundError(f"Student {student_id} was not found.")
    save_students(remaining)


def search_students(query):
    students = load_students()
    if not query:
        return students
    q = query.lower()
    return [
        s for s in students
        if q in s.get_name().lower()
        or q in s.get_student_id().lower()
        or q in s.get_grade().lower()
    ]


def compute_statistics():
    students = load_students()
    total = len(students)
    if total == 0:
        return {
            'total': 0,
            'average_age': 0,
            'grade_distribution': {},
            'age_distribution': {},
            'oldest': None,
            'youngest': None,
        }

    ages = [s.get_age() for s in students]
    grade_dist, age_dist = {}, {}
    for s in students:
        grade_dist[s.get_grade()] = grade_dist.get(s.get_grade(), 0) + 1
        age_dist[s.get_age()] = age_dist.get(s.get_age(), 0) + 1

    oldest = max(students, key=lambda s: s.get_age())
    youngest = min(students, key=lambda s: s.get_age())

    return {
        'total': total,
        'average_age': round(sum(ages) / total, 1),
        'grade_distribution': grade_dist,
        'age_distribution': age_dist,
        'oldest': oldest.to_dict(),
        'youngest': youngest.to_dict(),
    }
