'''Module for matching Sympla check-ins with UFSC's classes.'''
from pathlib import Path
from typing import NamedTuple, Optional, Any, Tuple


from cagrex import CAGR
from openpyxl import load_workbook


@dataclass
class Class:
    subject_id: str
    class_id: str
    semester: str


class Attender(NamedTuple):
    name: str
    attended: bool = True
    student_id: Optional[str] = None


def join(c: Tuple[Any, Any]) -> str:
    return ' '.join(s.value.strip() for s in list(c)).strip()


def retrieve_attendances(source: Path):
    wb = load_workbook(filename=path.resolve(), read_only=True)
    sheet = wb['Lista de participantes']
    rows = [
        (join(c), k.value, q.value)
        for c, (k, *_), (q, *_) in zip(
            sheet['C9:D500'],
            sheet['K9:K500'],
            sheet['Q9:Q500'],
        )
        if (c[0].value, c[1].value) != (None, None) and
           k.value == 'Sim'
    ]

    return [
        Attender(
            fullname.title(),
            *row
        )
        for fullname, *row in rows
    ]


def attendances_from_class(source: Path, class_: Class):
    pass


def main():
    pass


if __name__ == '__main__':
    main()
