'''Module for report handling of attendance lists.'''
from pathlib import Path
from textwrap import dedent

from .blocks import AttendanceBlock
from .db import Students


def make_pdf(
    block: AttendanceBlock,
    students: Students,
    output: Path,
):
    week = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
    print(dedent(f'''
    Attendance for block:
    - Title: {block.block.title}
    - Date: {week[block.block.date.weekday()]}, {block.block.date}
    - Time: {block.block.start}
    - Attenders:
    ''').strip())
    for student in block.attenders:
        print(f'    {student}: {students[student]}')
