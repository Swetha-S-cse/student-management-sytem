"""
Student Management System - Web Application
"""

from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key'

DATA_FILE = 'data/students.json'

# ==================== Student Class ====================

class Student:
    def __init__(self, student_id, name, age, grade, email, phone):
        self._student_id = student_id
        self._name = name
        self._age = age
        self._grade = grade
        self._email = email
        self._phone = phone
    
    def get_student_id(self):
        return self._student_id
    
    def get_name(self):
        return self._name
    
    def get_age(self):
        return self._age
    
    def get_grade(self):
        return self._grade
    
    def get_email(self):
        return self._email
    
    def get_phone(self):
        return self._phone
    
    def to_dict(self):
        return {
            'student_id': self._student_id,
            'name': self._name,
            'age': self._age,
            'grade': self._grade,
            'email': self._email,
            'phone': self._phone
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data['student_id'],
            data['name'],
            data['age'],
            data['grade'],
            data['email'],
            data['phone']
        )

# ==================== File Functions ====================

def load_students():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                return [Student.from_dict(item) for item in data]
        return []
    except:
        return []

def save_students(students):
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        data = [s.to_dict() for s in students]
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except:
        return False

def get_next_id(students):
    if not students:
        return 'S001'
    ids = [s.get_student_id() for s in students]
    numbers = [int(id[1:]) for id in ids if id.startswith('S')]
    if not numbers:
        return 'S001'
    next_num = max(numbers) + 1
    return f'S{next_num:03d}'

# ==================== Routes ====================

@app.route('/')
def index():
    students = load_students()
    total = len(students)
    
    if total > 0:
        ages = [s.get_age() for s in students]
        avg_age = sum(ages) / total
        grade_dist = {}
        age_dist = {}
        for s in students:
            grade = s.get_grade()
            grade_dist[grade] = grade_dist.get(grade, 0) + 1
            age = s.get_age()
            age_dist[age] = age_dist.get(age, 0) + 1
        oldest = max(students, key=lambda s: s.get_age())
        youngest = min(students, key=lambda s: s.get_age())
    else:
        avg_age = 0
        grade_dist = {}
        age_dist = {}
        oldest = None
        youngest = None
    
    stats = {
        'total': total,
        'average_age': round(avg_age, 1),
        'grade_distribution': grade_dist,
        'age_distribution': age_dist,
        'oldest': oldest.to_dict() if oldest else None,
        'youngest': youngest.to_dict() if youngest else None
    }
    
    return render_template('index.html', stats=stats)

@app.route('/students')
def list_students():
    students = load_students()
    search_query = request.args.get('q', '')
    
    if search_query:
        query_lower = search_query.lower()
        results = []
        for s in students:
            if (query_lower in s.get_name().lower() or
                query_lower in s.get_student_id().lower() or
                query_lower in s.get_grade().lower()):
                results.append(s)
        students = results
    
    return render_template('students.html', students=students, search_query=search_query)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            age = request.form.get('age', '').strip()
            grade = request.form.get('grade', '').strip()
            email = request.form.get('email', '').strip()
            phone = request.form.get('phone', '').strip()
            
            if not all([name, age, grade, email, phone]):
                flash('All fields are required!', 'danger')
                return render_template('add_student.html')
            
            students = load_students()
            student_id = get_next_id(students)
            
            student = Student(student_id, name, int(age), grade, email, phone)
            students.append(student)
            save_students(students)
            
            flash(f'Student {name} added successfully!', 'success')
            return redirect(url_for('list_students'))
            
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('add_student.html')

@app.route('/edit/<student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    students = load_students()
    student = None
    for s in students:
        if s.get_student_id() == student_id:
            student = s
            break
    
    if not student:
        flash('Student not found!', 'danger')
        return redirect(url_for('list_students'))
    
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            age = request.form.get('age', '').strip()
            grade = request.form.get('grade', '').strip()
            email = request.form.get('email', '').strip()
            phone = request.form.get('phone', '').strip()
            
            students.remove(student)
            updated = Student(student_id, name, int(age), grade, email, phone)
            students.append(updated)
            save_students(students)
            
            flash('Student updated successfully!', 'success')
            return redirect(url_for('list_students'))
            
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('edit_student.html', student=student)

@app.route('/delete/<student_id>', methods=['POST'])
def delete_student(student_id):
    try:
        students = load_students()
        students = [s for s in students if s.get_student_id() != student_id]
        save_students(students)
        flash('Student deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('list_students'))

@app.route('/statistics')
def statistics():
    students = load_students()
    total = len(students)
    
    if total > 0:
        ages = [s.get_age() for s in students]
        avg_age = sum(ages) / total
        grade_dist = {}
        age_dist = {}
        for s in students:
            grade = s.get_grade()
            grade_dist[grade] = grade_dist.get(grade, 0) + 1
            age = s.get_age()
            age_dist[age] = age_dist.get(age, 0) + 1
        oldest = max(students, key=lambda s: s.get_age())
        youngest = min(students, key=lambda s: s.get_age())
    else:
        avg_age = 0
        grade_dist = {}
        age_dist = {}
        oldest = None
        youngest = None
    
    stats = {
        'total': total,
        'average_age': round(avg_age, 1),
        'grade_distribution': grade_dist,
        'age_distribution': age_dist,
        'oldest': oldest.to_dict() if oldest else None,
        'youngest': youngest.to_dict() if youngest else None
    }
    
    return render_template('statistics.html', stats=stats)

# ==================== Run App ====================

if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)