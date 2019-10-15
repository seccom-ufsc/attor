'''Management of attendance and classes databases.'''
from datetime import date as Date
from pathlib import Path
from typing import List

from cagrex.cagr import Student, Class

from .blocks import AttendanceBlock


def import_attendances(path: Path):
    '''Imports a well-formatted xlsx or csv file into database.'''
    pass


def import_class(path: Path):
    '''Imports a well-'''
    pass


def load_students(student_ids: List[str]) -> List[Student]:
    '''Returns all students with given ids.'''
    pass


def load_classes(subject_id: str, class_id: str, semester: str) -> List[Class]:
    pass


def load_day_attendances(date: Date) -> List[AttendanceBlock]:
    '''Returns all attendances from an specific day.'''
    pass
