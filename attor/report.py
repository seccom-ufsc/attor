'''Module for report handling of attendance lists.'''
from pathlib import Path

from .blocks import AttendanceBlock
from .db import Students


def make_pdf(
    block: AttendanceBlock,
    students: Students,
    output: Path,
):
    for student in block.attenders:
        print(f'{student}: {students["students"]}')
