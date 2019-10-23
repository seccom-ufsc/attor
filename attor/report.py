'''Module for report handling of attendance lists.'''
from functools import reduce
from pathlib import Path
from textwrap import dedent
from typing import Dict, List
import csv
import operator

from .blocks import schedule_end, AttendanceBlock, Schedule, TimeBlock
from .db import Students

WEEK = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']


def make_sched_title(sched: Schedule) -> str:
    return f'{WEEK[sched.weekday-2]}-{sched.time.hour}h{sched.time.minute}'


def timeblock_for_sched(
    sched: Schedule,
    attlist: List[AttendanceBlock],
) -> TimeBlock:
    title = make_sched_title(sched)
    try:
        return TimeBlock(
            title=title,
            date=attlist[0].block.date,
            start=sched.time,
            end=schedule_end(sched),
        )
    except IndexError:
        print(f'Attlist for {title}: {attlist}')
        exit(1)


def make_pdf(
    atts: Dict[Schedule, List[AttendanceBlock]],
    students: Students,
    output_dir: Path,
    class_name: str,
):
    merged_atts = {
        sched: AttendanceBlock(
            block=timeblock_for_sched(sched, attlist),
            attenders=reduce(
                operator.or_,
                (b.attenders for b in attlist),
                set()
            )
        ) for sched, attlist in atts.items()
    }

    if not output_dir.exists():
        output_dir.mkdir()

    FIELDS = ['Matrícula', 'Nome']
    for sched, att in merged_atts.items():
        output = output_dir / f'{class_name}-{att.block.title}.csv'
        with open(output, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)

            writer.writeheader()
            writer.writerows(
                {'Matrícula': student,
                 'Nome': students[student]} for student in att.attenders
            )

    for sched, att in merged_atts.items():
        print(dedent(f'''
        Attendance for {att.block.title}:
        - Date: {WEEK[att.block.date.weekday()]}, {att.block.date}
        - Time: {att.block.start} to {att.block.end}
        - Attenders:
        ''').strip())
        for student in att.attenders:
            print(f'    {student}: {students[student]}')
