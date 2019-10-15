'''Module for matching Sympla check-ins with UFSC's classes.'''
from datetime import date as Date, time as Time
from getpass import getpass
from pathlib import Path
from typing import Tuple

from carl import command, REQUIRED
from carl.carl import Command
from cagrex import CAGR

from .blocks import attendance_block_from_sheet, filter_from_class
from .db import Class, ClassNotFound, Database, Schedule, Students
from .report import make_pdf
from .sympla import Sheet


DEFAULT_DB = Path('./attor.db')


def load_cagr_class(
    subject_id: str,
    class_id: str,
    semester: str
) -> Tuple[Class, Students]:
    cagr = CAGR()
    subject = cagr.subject()

    classes = [c for c in subject.classes if c.class_id == class_id]

    if not classes:
        raise ClassNotFound(
            f'No class {subject_id}-{class_id} in {semester} (CAGR)'
        )

    class_ = classes[0]

    print('**CAGR Login**')
    cagr.login(input('UFSC ID: '), getpass('Password: '))

    students: Students = {
        s.student_id: s.name
        for s in cagr.students_from_class(subject_id, class_id, semester)
    }

    return Class(
        subject_id=subject_id,
        class_id=class_id,
        semester=semester,
        students=[s for s in students.keys()],
        schedule=[
            Schedule(sched.weekday, sched.time, sched.duration)
            for sched in class_.schedule
        ],
    ), students


@command
def main(subcommand: Command = REQUIRED):
    pass


@main.subcommand
def add_block(
    source: Path,
    title: str,
    date: Date,
    start: Time,
    end: Time,
    db: Path = DEFAULT_DB
):
    '''Imports a time block as a Sympla attendance XLSX file into database.'''
    database = Database.load(db)
    sheet = Sheet.load(source, date, start, end)
    sheet.name = title

    database.add_attendances(attendance_block_from_sheet(sheet))


@main.subcommand
def validate(
    subject_id: str,
    class_id: str,
    semester: str,
    output_dir: Path,
    db: Path = DEFAULT_DB
):
    '''Validates attendances from a class and outputs into csv file. Class
    members are cached into database.'''
    database = Database.load(db)
    try:
        class_ = database.load_class(subject_id, class_id, semester)
    except ClassNotFound:
        class_, students = load_cagr_class(subject_id, class_id, semester)
        database.add_students(students)

    attendances = filter_from_class(database.attendances, class_)
    for block in attendances:
        make_pdf(block, output_dir / block.block.title)


if __name__ == '__main__':
    main.run()
