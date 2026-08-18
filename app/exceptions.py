"""
Custom exceptions for the Student Management System.

Using specific exception classes (instead of a bare `except:` or a
generic `except Exception`) lets the Flask routes tell the difference
between "the user typed something invalid" and "the data file couldn't
be read" and show a precise, useful message for each — rather than
silently swallowing every error the same way.
"""


class StudentManagementError(Exception):
    """Base class for all student-management-specific errors."""
    pass


class InvalidDataError(StudentManagementError):
    """Raised when user-submitted form data fails validation."""
    pass


class StudentNotFoundError(StudentManagementError):
    """Raised when a requested student ID does not exist."""
    pass


class DataStorageError(StudentManagementError):
    """Raised when reading from or writing to the data file fails."""
    pass
