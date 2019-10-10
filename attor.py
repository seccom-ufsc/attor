'''Module for matching Sympla check-ins with UFSC's classes.'''
from __future__ import annotations

from datetime import date as Date
from getpass import getpass
from pathlib import Path
from sys import argv
from textwrap import dedent
from typing import Iterable, List, NamedTuple, Optional, Any, Tuple


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
    cpf: Optional[str] = None
    classes: List[str] = []


class Ticket(NamedTuple):
    number: int
    ticket_id: str
    name: str
    surname: str
    ticket_type: str
    value: str
    order_date: Date
    order_id: str
    email: str
    state: str
    checked_in: str
    checkin_date: Optional[Date]
    discount_code: str
    pay_method: str
    pdv: str
    cpf: str
    student_id: str
    classes: List[str]

    @staticmethod
    def from_row(row) -> Ticket:
        row = [
            cell.value if cell.value else ''
            for cell in row
        ]
        return Ticket(
            int(row[0]),
            *row[1:6],
            Date.fromisoformat(row[6].split(' ')[0]),
            *row[7:11],
            Date.fromisoformat(row[11].split(' ')[0]) if row[11] else None,
            *row[12:17],
            row[17].split(','),
        )


def iter_as_tickets(sheet_range) -> Iterable[Ticket]:
    for row in sheet_range:
        if all(cell.value is None for cell in row):
            return

        yield Ticket.from_row(row)


def strip_join(c: Tuple[str, str]) -> str:
    return ' '.join(s.strip() for s in list(c)).strip()


def retrieve_attenders(source: Path) -> List[Attender]:
    wb = load_workbook(filename=source.resolve(), read_only=True)
    sheet = wb['Lista de participantes']
    rows = [
        (strip_join((ticket.name, ticket.surname)), ticket.checked_in == 'Sim', ticket.student_id)
        for ticket in iter_as_tickets(
            sheet.iter_rows(
                min_row=9,
                min_col=1,
                max_col=18,
            )
        )
        if (ticket.name, ticket.name) != (None, None) and
           ticket.checked_in == 'Sim'
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
