'''Module for matching Sympla check-ins with UFSC's classes.'''
from getpass import getpass
from pathlib import Path
from sys import argv
from textwrap import dedent
from typing import List, NamedTuple, Optional, Any, Tuple


from cagrex import CAGR
from openpyxl import load_workbook


class Class(NamedTuple):
    subject_id: str
    class_id: str
    semester: str


class Attender(NamedTuple):
    name: str
    attended: bool = True
    student_id: Optional[str] = None


def join(c: Tuple[Any, Any]) -> str:
    return ' '.join(s.value.strip() for s in list(c)).strip()


def retrieve_attenders(source: Path) -> List[Attender]:
    wb = load_workbook(filename=source.resolve(), read_only=True)
    sheet = wb['Lista de participantes']
    rows = [
        (join((c, d)), k.value == 'Sim', str(q.value))
        for (c, d), (k, *_), (q, *_) in zip(
            sheet['C9:D500'],
            sheet['K9:K500'],
            sheet['Q9:Q500'],
        )
        if (c.value, d.value) != (None, None) and
           k.value == 'Sim'
    ]

    return [
        Attender(
            fullname.title(),
            *row
        )
        for fullname, *row in rows
    ]


def attenders_from_class(source: Path, class_: Class) -> List[Attender]:
    attenders = retrieve_attenders(source)

    cagr = CAGR()

    print('**CAGR Login**')
    cagr.login(input('UFSC ID: '), getpass('Password: '))

    students = cagr.students_from_class(*class_)
    student_ids = [student.student_id for student in students]

    return [
        attender for attender in attenders
        if attender.student_id in student_ids
    ]


def main():
    program = argv[0]
    try:
        source, *class_ = argv[1:]
        class_ = Class(*class_)
    except:
        print(dedent(f'''
            Usage: {program} <XLSX file> <subject ID> <class ID> <semester>
            Example:
                $ {program} SomeDayCheckins.xlsx INE5417 04208A 20192
        ''').strip())
        exit(1)

    for attender in attenders_from_class(Path(source), class_):
        print(f'{attender.student_id},{attender.name}')


if __name__ == '__main__':
    main()
