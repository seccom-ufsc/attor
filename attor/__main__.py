'''Module for matching Sympla check-ins with UFSC's classes.'''
from datetime import date as Date, time as Time
from getpass import getpass
from pathlib import Path
from pprint import pprint
from typing import Tuple

from carl import command, REQUIRED
from carl.carl import Command
from cagrex import CAGR

from .blocks import (
    attendance_block_from_sheet,
    block_for_timespan,
    filter_class_schedule,
    keep_only_students,
    AttendanceBlock,
    TimeBlock,
)
from .db import Class, ClassNotFound, Database, Schedule, Students
from .report import make_pdf
from .sympla import Sheet


DEFAULT_DB = Path('./attor.db')


def load_db_or_create(path: Path) -> Database:
    try:
        return Database.load(path)
    except FileNotFoundError:
        return Database(path=path)


def load_cagr_class(
    subject_id: str,
    class_id: str,
    semester: str
) -> Tuple[Class, Students]:
    '''Accesses CAGR and fetches class information.'''
    cagr = CAGR()
    subject = cagr.subject(subject_id, semester)

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
    title: str,
    date: str,
    start: str,
    end: str,
    db: Path = DEFAULT_DB,
):
    '''Imports a time block as a Sympla attendance XLSX file into database.'''
    date_ = Date.fromisoformat(date)
    start_ = Time.fromisoformat(start)
    end_ = Time.fromisoformat(end)

    database = load_db_or_create(db)
    database.add_block(TimeBlock(
        title=title,
        date=date_,
        start=start_,
        end=end_,
    ))
    database.save()


@main.subcommand
def import_attendances(
    source: Path,
    threshold: int = 15,
    db: Path = DEFAULT_DB,
):
    '''Imports a time block as a Sympla attendance XLSX file into database.'''
    database = load_db_or_create(db)
    sheet = Sheet.load(source)

    attendances = attendance_block_from_sheet(sheet)
    attendances = AttendanceBlock(
        block=block_for_timespan(
            sheet.date,
            sheet.start,
            sheet.end,
            database.blocks,
            threshold=Time(0, threshold, 0),
        ),
        attenders=attendances.attenders,
    )
    print(f'Fit into {attendances.block}')

    database.add_attendances(attendances)
    database.save()
    print('Done.')


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
    database = load_db_or_create(db)
    try:
        print(f'Looking for cache...')
        class_ = database.load_class(subject_id, class_id, semester)
        students = database.students_with_ids(class_.students)
        print(f'Class found in cache.')
    except ClassNotFound:
        print(
            f'Class {subject_id}-{class_id} not cached. Loading from CAGR...'
        )
        class_, students = load_cagr_class(subject_id, class_id, semester)
        database.add_students(students)
        database.add_class(class_)

    database.save()

    attendances = filter_class_schedule(database.attendances, class_)
    print(f'\n==== Blocks considering class schedule:')
    for sched, attlist in attendances.items():
        print('    --- ')
        print(f'    Blocks for {sched}:')
        for att in attlist:
            print('        --- ')
            print(f'        {att.block.title}:')
            print(f'           Start: {att.block.start}')
            print(f'           End: {att.block.end}')
            print(f'           Attenders: {sorted(list(att.attenders))}')

    print('Students in class:')
    pprint(sorted(class_.students))

    attendances = {
        sched: keep_only_students(att, class_)
        for sched, att in attendances.items()
    }

    class_name = f'{class_.subject_id}-Turma-{class_.class_id}'
    make_pdf(attendances, students, output_dir, class_name)


if __name__ == '__main__':
    main.run()
