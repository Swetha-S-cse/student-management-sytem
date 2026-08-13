"""
Student Management System - Streamlit Version
Converted from Flask to Streamlit for deployment
"""

import streamlit as st
import os
import json

st.set_page_config(page_title="Student Management System", layout="wide")

DATA_FILE = 'data/students.json'

# ==================== Student Class (Same as your Flask app) ====================

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

# ==================== File Functions (Same as your Flask app) ====================

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

# ==================== Streamlit UI ====================

st.title("📚 Student Management System")

# Sidebar Menu
menu = st.sidebar.selectbox(
    "Menu",
    ["🏠 Home", "➕ Add Student", "📋 View Students", "🔍 Search Students", "📊 Statistics"]
)

# ==================== HOME PAGE ====================
if menu == "🏠 Home":
    st.header("🏠 Dashboard")
    students = load_students()
    total = len(students)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Students", total)
    with col2:
        if total > 0:
            ages = [s.get_age() for s in students]
            avg_age = sum(ages) / total
            st.metric("Average Age", f"{avg_age:.1f}")
        else:
            st.metric("Average Age", "0")
    with col3:
        if total > 0:
            grade_dist = {}
            for s in students:
                grade = s.get_grade()
                grade_dist[grade] = grade_dist.get(grade, 0) + 1
            st.metric("Grade Categories", len(grade_dist))
        else:
            st.metric("Grade Categories", "0")
    with col4:
        st.metric("Records Stored", total)
    
    if total > 0:
        st.subheader("📊 Grade Distribution")
        grade_dist = {}
        for s in students:
            grade = s.get_grade()
            grade_dist[grade] = grade_dist.get(grade, 0) + 1
        st.bar_chart(grade_dist)
        
        st.subheader("📊 Age Distribution")
        age_dist = {}
        for s in students:
            age = s.get_age()
            age_dist[age] = age_dist.get(age, 0) + 1
        st.bar_chart(age_dist)

# ==================== ADD STUDENT ====================
elif menu == "➕ Add Student":
    st.header("➕ Add New Student")
    
    with st.form("add_form"):
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=1, max_value=150, step=1)
        grade = st.selectbox("Grade", ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'F'])
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        submitted = st.form_submit_button("Add Student")
        
        if submitted:
            if all([name, age, grade, email, phone]):
                students = load_students()
                student_id = get_next_id(students)
                student = Student(student_id, name, int(age), grade, email, phone)
                students.append(student)
                save_students(students)
                st.success(f"✅ Student '{name}' added successfully!")
                st.balloons()
            else:
                st.error("❌ All fields are required!")

# ==================== VIEW STUDENTS ====================
elif menu == "📋 View Students":
    st.header("📋 All Students")
    students = load_students()
    
    if students:
        data = []
        for s in students:
            data.append({
                "ID": s.get_student_id(),
                "Name": s.get_name(),
                "Age": s.get_age(),
                "Grade": s.get_grade(),
                "Email": s.get_email(),
                "Phone": s.get_phone()
            })
        st.dataframe(data, use_container_width=True)
        st.info(f"Total: {len(students)} student(s)")
    else:
        st.info("ℹ️ No students found. Add some students!")

# ==================== SEARCH STUDENTS ====================
elif menu == "🔍 Search Students":
    st.header("🔍 Search Students")
    search_query = st.text_input("Enter search term (name or ID)")
    
    if search_query:
        students = load_students()
        query_lower = search_query.lower()
        results = []
        for s in students:
            if (query_lower in s.get_name().lower() or
                query_lower in s.get_student_id().lower() or
                query_lower in s.get_grade().lower()):
                results.append(s)
        
        if results:
            data = []
            for s in results:
                data.append({
                    "ID": s.get_student_id(),
                    "Name": s.get_name(),
                    "Age": s.get_age(),
                    "Grade": s.get_grade(),
                    "Email": s.get_email(),
                    "Phone": s.get_phone()
                })
            st.dataframe(data, use_container_width=True)
            st.success(f"✅ Found {len(results)} student(s)")
        else:
            st.warning("ℹ️ No students found matching your search.")

# ==================== STATISTICS ====================
elif menu == "📊 Statistics":
    st.header("📊 Statistics")
    students = load_students()
    total = len(students)
    
    if total > 0:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📈 Grade Distribution")
            grade_dist = {}
            for s in students:
                grade = s.get_grade()
                grade_dist[grade] = grade_dist.get(grade, 0) + 1
            st.bar_chart(grade_dist)
        
        with col2:
            st.subheader("📊 Age Distribution")
            age_dist = {}
            for s in students:
                age = s.get_age()
                age_dist[age] = age_dist.get(age, 0) + 1
            st.bar_chart(age_dist)
        
        ages = [s.get_age() for s in students]
        avg_age = sum(ages) / total
        oldest = max(students, key=lambda s: s.get_age())
        youngest = min(students, key=lambda s: s.get_age())
        
        col3, col4 = st.columns(2)
        with col3:
            st.info(f"**Oldest Student:** {oldest.get_name()} ({oldest.get_age()} years)")
        with col4:
            st.info(f"**Youngest Student:** {youngest.get_name()} ({youngest.get_age()} years)")
        
        st.success(f"**Total Students:** {total} | **Average Age:** {avg_age:.1f} years")
    else:
        st.info("ℹ️ No data available. Add some students first!")