"""
Student Model - OOP Implementation with Encapsulation
"""

import re
from datetime import datetime


class Student:
    """Student class with encapsulation and validation"""
    
    def __init__(self, student_id, name, age, grade, email, phone):
        # Private attributes (encapsulation)
        self.__student_id = student_id
        self.__name = name
        self.__age = age
        self.__grade = grade
        self.__email = email
        self.__phone = phone
        self.__created_at = datetime.now().isoformat()
        self.__updated_at = datetime.now().isoformat()
        
        # Validate on creation
        self.validate()
    
    # ==================== Getters ====================
    
    def get_student_id(self):
        return self.__student_id
    
    def get_name(self):
        return self.__name
    
    def get_age(self):
        return self.__age
    
    def get_grade(self):
        return self.__grade
    
    def get_email(self):
        return self.__email
    
    def get_phone(self):
        return self.__phone
    
    def get_created_at(self):
        return self.__created_at
    
    def get_updated_at(self):
        return self.__updated_at
    
    # ==================== Setters with Validation ====================
    
    def set_name(self, name):
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")
        if len(name.strip()) < 2:
            raise ValueError("Name must be at least 2 characters")
        if len(name.strip()) > 100:
            raise ValueError("Name must not exceed 100 characters")
        self.__name = name.strip()
        self.__updated_at = datetime.now().isoformat()
    
    def set_age(self, age):
        if not isinstance(age, int):
            raise ValueError("Age must be a number")
        if age < 1 or age > 150:
            raise ValueError("Age must be between 1 and 150")
        self.__age = age
        self.__updated_at = datetime.now().isoformat()
    
    def set_grade(self, grade):
        valid_grades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'F']
        if not grade or grade.upper() not in valid_grades:
            raise ValueError(f"Grade must be one of: {', '.join(valid_grades)}")
        self.__grade = grade.upper()
        self.__updated_at = datetime.now().isoformat()
    
    def set_email(self, email):
        pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        if not re.match(pattern, email):
            raise ValueError("Invalid email format")
        self.__email = email
        self.__updated_at = datetime.now().isoformat()
    
    def set_phone(self, phone):
        if not phone or not phone.strip():
            raise ValueError("Phone cannot be empty")
        clean_phone = re.sub(r'[\s\-\(\)\.]', '', phone)
        if not clean_phone.isdigit():
            raise ValueError("Phone must contain only digits")
        if len(clean_phone) < 10:
            raise ValueError("Phone must be at least 10 digits")
        if len(clean_phone) > 15:
            raise ValueError("Phone must not exceed 15 digits")
        self.__phone = phone
        self.__updated_at = datetime.now().isoformat()
    
    # ==================== Validation ====================
    
    def validate(self):
        """Validate all fields"""
        # Validate name
        if not self.__name or len(self.__name.strip()) < 2:
            raise ValueError("Name must be at least 2 characters")
        
        # Validate age
        if not isinstance(self.__age, int) or self.__age < 1 or self.__age > 150:
            raise ValueError("Age must be between 1 and 150")
        
        # Validate grade
        valid_grades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'F']
        if not self.__grade or self.__grade.upper() not in valid_grades:
            raise ValueError(f"Grade must be one of: {', '.join(valid_grades)}")
        
        # Validate email
        pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        if not re.match(pattern, self.__email):
            raise ValueError("Invalid email format")
        
        # Validate phone
        clean_phone = re.sub(r'[\s\-\(\)\.]', '', self.__phone)
        if not clean_phone.isdigit() or len(clean_phone) < 10:
            raise ValueError("Phone must be at least 10 digits")
    
    # ==================== Serialization ====================
    
    def to_dict(self):
        """Convert to dictionary for JSON storage"""
        return {
            'student_id': self.__student_id,
            'name': self.__name,
            'age': self.__age,
            'grade': self.__grade,
            'email': self.__email,
            'phone': self.__phone,
            'created_at': self.__created_at,
            'updated_at': self.__updated_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create student from dictionary"""
        student = cls(
            data['student_id'],
            data['name'],
            data['age'],
            data['grade'],
            data['email'],
            data['phone']
        )
        if 'created_at' in data:
            student.__created_at = data['created_at']
        if 'updated_at' in data:
            student.__updated_at = data['updated_at']
        return student
    
    # ==================== Magic Methods ====================
    
    def __str__(self):
        return f"Student(ID: {self.__student_id}, Name: {self.__name})"
    
    def __repr__(self):
        return f"Student(student_id='{self.__student_id}', name='{self.__name}')"