"""
Student Management System — Web Application

Run with:
    python web_app.py

Then open http://127.0.0.1:5000 in a browser.
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash

from app.exceptions import StudentManagementError
from app import storage

app = Flask(__name__)
app.secret_key = 'your-secret-key'


# ==================== Routes ====================

@app.route('/')
def index():
    stats = storage.compute_statistics()
    return render_template('index.html', stats=stats)


@app.route('/students')
def list_students():
    search_query = request.args.get('q', '')
    try:
        students = storage.search_students(search_query)
    except StudentManagementError as e:
        flash(str(e), 'danger')
        students = []
    return render_template('students.html', students=students, search_query=search_query)


@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        try:
            storage.add_student(
                name=request.form.get('name'),
                age=request.form.get('age'),
                grade=request.form.get('grade'),
                email=request.form.get('email'),
                phone=request.form.get('phone'),
            )
            flash('Student added successfully!', 'success')
            return redirect(url_for('list_students'))
        except StudentManagementError as e:
            flash(str(e), 'danger')
            return render_template('add_student.html', form=request.form)

    return render_template('add_student.html', form={})


@app.route('/edit/<student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    try:
        student = storage.get_student(student_id)
    except StudentManagementError as e:
        flash(str(e), 'danger')
        return redirect(url_for('list_students'))

    if request.method == 'POST':
        try:
            storage.update_student(
                student_id,
                name=request.form.get('name'),
                age=request.form.get('age'),
                grade=request.form.get('grade'),
                email=request.form.get('email'),
                phone=request.form.get('phone'),
            )
            flash('Student updated successfully!', 'success')
            return redirect(url_for('list_students'))
        except StudentManagementError as e:
            flash(str(e), 'danger')
            return render_template('edit_student.html', student=student)

    return render_template('edit_student.html', student=student)


@app.route('/delete/<student_id>', methods=['POST'])
def delete_student(student_id):
    try:
        storage.delete_student(student_id)
        flash('Student deleted successfully!', 'success')
    except StudentManagementError as e:
        flash(str(e), 'danger')
    return redirect(url_for('list_students'))


@app.route('/statistics')
def statistics():
    stats = storage.compute_statistics()
    return render_template('statistics.html', stats=stats)


# ==================== Error handlers ====================

@app.errorhandler(500)
def server_error(e):
    flash('Something went wrong on our end. Please try again.', 'danger')
    return redirect(url_for('index'))


# ==================== Run App ====================

if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
