"""
Student model.

Encapsulates a single student record. Attributes are private
(prefixed with `_`) and accessed only through getter methods, and the
class knows how to convert itself to/from a plain dict for JSON storage.
"""


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
            'phone': self._phone,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['student_id'],
            data['name'],
            data['age'],
            data['grade'],
            data['email'],
            data['phone'],
        )

    def __repr__(self):
        return f"Student({self._student_id}, {self._name!r})"
