"""
Custom Exceptions for Student Management System
"""

class StudentError(Exception):
    """Base exception for student management"""
    pass


class ValidationError(StudentError):
    """Raised when validation fails"""
    pass


class StudentNotFoundError(StudentError):
    """Raised when student is not found"""
    pass


class DuplicateStudentError(StudentError):
    """Raised when duplicate student is added"""
    pass


class FileOperationError(StudentError):
    """Raised when file operations fail"""
    pass