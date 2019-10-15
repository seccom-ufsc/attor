'''Module to deal with sympla attendance spreadsheets.'''
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date as Date, time as Time
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

from openpyxl import load_workbook
from openpyxl.cell.read_only import ReadOnlyCell


@dataclass(frozen=True)
class Attender:
    name: str
    attended: bool = True
    student_id: Optional[str] = None
    cpf: Optional[str] = None
    classes: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class Ticket:
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
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            Date.fromisoformat(row[6].split(' ')[0]),
            row[7],
            row[8],
            row[9],
            row[10],
            Date.fromisoformat(row[11].split(' ')[0]) if row[11] else None,
            row[12],
            row[13],
            row[14],
            row[15],
            row[16],
            row[17].split(','),
        )


@dataclass
class Sheet:
    name: str
    date: Date
    start: Time
    end: Time
    tickets: List[Ticket]

    @staticmethod
    def load(path: Path, date: Date, start: Time, end: Time) -> Sheet:
        pass


def iter_as_tickets(
    sheet_range: Iterable[Tuple[ReadOnlyCell]]
) -> Iterable[Ticket]:
    for row in sheet_range:
        if all(cell.value is None for cell in row):
            return

        yield Ticket.from_row(row)


def strip_join(c: Tuple[str, str]) -> str:
    return ' '.join(s.strip() for s in list(c)).strip()


def retrieve_attenders(source: Path) -> List[Attender]:
    wb = load_workbook(filename=source.resolve(), read_only=True)
    sheet = wb.active

    row_iter = sheet.iter_rows(min_row=9, min_col=1, max_col=18)
    rows = [
        (strip_join((ticket.name, ticket.surname)).title(),
         ticket.checked_in == 'Sim',
         ticket.student_id, )
        for ticket in iter_as_tickets(row_iter)
        if ticket.checked_in == 'Sim'
    ]

    return [Attender(*row) for row in rows]
