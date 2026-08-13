"""
Validation Utilities
"""

import re


class Validators:
    """Collection of validation methods"""
    
    @staticmethod
    def validate_student_id(student_id):
        """Validate student ID format"""
        if not student_id or not student_id.strip():
            return False, "Student ID cannot be empty"
        if len(student_id.strip()) < 2:
            return False, "Student ID must be at least 2 characters"
        if len(student_id.strip()) > 20:
            return False, "Student ID must not exceed 20 characters"
        if not re.match(r'^[A-Za-z0-9_-]+$', student_id):
            return False, "Student ID contains invalid characters (only letters, numbers, underscores, hyphens allowed)"
        return True, None
    
    @staticmethod
    def validate_name(name):
        """Validate student name"""
        if not name or not name.strip():
            return False, "Name cannot be empty"
        if len(name.strip()) < 2:
            return False, "Name must be at least 2 characters"
        if len(name.strip()) > 100:
            return False, "Name must not exceed 100 characters"
        return True, None
    
    @staticmethod
    def validate_age(age):
        """Validate age"""
        try:
            age_int = int(age)
            if age_int < 1:
                return False, "Age must be at least 1", None
            if age_int > 150:
                return False, "Age must not exceed 150", None
            return True, None, age_int
        except ValueError:
            return False, "Age must be a valid number", None
    
    @staticmethod
    def validate_grade(grade):
        """Validate grade"""
        valid_grades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'F']
        if not grade or not grade.strip():
            return False, "Grade cannot be empty"
        grade_upper = grade.strip().upper()
        if grade_upper not in valid_grades:
            return False, f"Grade must be one of: {', '.join(valid_grades)}"
        return True, None
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        if not email or not email.strip():
            return False, "Email cannot be empty"
        pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        if not re.match(pattern, email):
            return False, "Invalid email format (e.g., student@example.com)"
        if len(email) > 100:
            return False, "Email must not exceed 100 characters"
        return True, None
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number"""
        if not phone or not phone.strip():
            return False, "Phone number cannot be empty"
        clean_phone = re.sub(r'[\s\-\(\)\.]', '', phone)
        if not clean_phone.isdigit():
            return False, "Phone number contains invalid characters"
        if len(clean_phone) < 10:
            return False, "Phone number must be at least 10 digits"
        if len(clean_phone) > 15:
            return False, "Phone number must not exceed 15 digits"
        return True, None