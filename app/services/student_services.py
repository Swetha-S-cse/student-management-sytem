"""
Student Service - Business Logic Layer
Handles all CRUD operations with file persistence
"""

import json
import os
from models.student import Student
from app.exceptions.custom_exceptions import ValidationError, StudentNotFoundError, DuplicateStudentError
from app.utils.validators import Validators


class StudentService:
    """Service class for student operations"""
    
    def __init__(self, data_file="app/data/students.json"):
        self.data_file = data_file
        self.students = []
        self._load_data()
    
    def _load_data(self):
        """Load students from JSON file"""
        try:
            # Ensure data directory exists
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.students = [Student.from_dict(item) for item in data]
            else:
                self.students = []
        except Exception as e:
            print(f"Error loading data: {e}")
            self.students = []
    
    def _save_data(self):
        """Save students to JSON file"""
        try:
            # Ensure data directory exists
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            data = [student.to_dict() for student in self.students]
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def get_next_id(self):
        """Generate next student ID"""
        if not self.students:
            return 'S001'
        
        # Get all IDs
        ids = [s.get_student_id() for s in self.students]
        # Extract numbers and find max
        numbers = [int(id[1:]) for id in ids if id.startswith('S')]
        if not numbers:
            return 'S001'
        next_num = max(numbers) + 1
        return f'S{next_num:03d}'
    
    # ==================== CRUD Operations ====================
    
    def create_student(self, name, age, grade, email, phone):
        """Add new student with validation"""
        # Validate inputs
        is_valid, error = Validators.validate_name(name)
        if not is_valid:
            raise ValidationError(error)
        
        is_valid, error, age_int = Validators.validate_age(age)
        if not is_valid:
            raise ValidationError(error)
        
        is_valid, error = Validators.validate_grade(grade)
        if not is_valid:
            raise ValidationError(error)
        
        is_valid, error = Validators.validate_email(email)
        if not is_valid:
            raise ValidationError(error)
        
        is_valid, error = Validators.validate_phone(phone)
        if not is_valid:
            raise ValidationError(error)
        
        # Generate ID and create student
        student_id = self.get_next_id()
        student = Student(student_id, name, age_int, grade, email, phone)
        self.students.append(student)
        self._save_data()
        return student
    
    def get_all_students(self):
        """Get all students"""
        return self.students.copy()
    
    def get_student_by_id(self, student_id):
        """Get student by ID"""
        for student in self.students:
            if student.get_student_id() == student_id:
                return student
        return None
    
    def search_students(self, query):
        """Search students by name, ID, or grade"""
        query = query.lower().strip()
        if not query:
            return []
        
        results = []
        for student in self.students:
            if (query in student.get_name().lower() or
                query in student.get_student_id().lower() or
                query in student.get_grade().lower()):
                results.append(student)
        return results
    
    def update_student(self, student_id, **kwargs):
        """Update student details"""
        student = self.get_student_by_id(student_id)
        if not student:
            raise StudentNotFoundError(f"Student {student_id} not found")
        
        # Update fields with validation
        if 'name' in kwargs:
            is_valid, error = Validators.validate_name(kwargs['name'])
            if not is_valid:
                raise ValidationError(error)
            student.set_name(kwargs['name'])
        
        if 'age' in kwargs:
            is_valid, error, age_int = Validators.validate_age(str(kwargs['age']))
            if not is_valid:
                raise ValidationError(error)
            student.set_age(age_int)
        
        if 'grade' in kwargs:
            is_valid, error = Validators.validate_grade(kwargs['grade'])
            if not is_valid:
                raise ValidationError(error)
            student.set_grade(kwargs['grade'])
        
        if 'email' in kwargs:
            is_valid, error = Validators.validate_email(kwargs['email'])
            if not is_valid:
                raise ValidationError(error)
            student.set_email(kwargs['email'])
        
        if 'phone' in kwargs:
            is_valid, error = Validators.validate_phone(kwargs['phone'])
            if not is_valid:
                raise ValidationError(error)
            student.set_phone(kwargs['phone'])
        
        self._save_data()
        return student
    
    def delete_student(self, student_id):
        """Delete student by ID"""
        student = self.get_student_by_id(student_id)
        if not student:
            raise StudentNotFoundError(f"Student {student_id} not found")
        
        self.students = [s for s in self.students if s.get_student_id() != student_id]
        self._save_data()
        return True
    
    def get_statistics(self):
        """Get statistics"""
        total = len(self.students)
        
        if total == 0:
            return {
                'total': 0,
                'average_age': 0,
                'grade_distribution': {},
                'age_distribution': {},
                'oldest': None,
                'youngest': None
            }
        
        ages = [s.get_age() for s in self.students]
        avg_age = sum(ages) / total
        
        grade_dist = {}
        age_dist = {}
        
        for student in self.students:
            grade = student.get_grade()
            grade_dist[grade] = grade_dist.get(grade, 0) + 1
            
            age = student.get_age()
            age_dist[age] = age_dist.get(age, 0) + 1
        
        # Find oldest and youngest
        oldest = max(self.students, key=lambda s: s.get_age())
        youngest = min(self.students, key=lambda s: s.get_age())
        
        return {
            'total': total,
            'average_age': round(avg_age, 1),
            'grade_distribution': grade_dist,
            'age_distribution': age_dist,
            'oldest': oldest.to_dict(),
            'youngest': youngest.to_dict()
        }