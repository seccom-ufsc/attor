'''Module for report handling of attendance lists.'''
from functools import reduce
from datetime import timedelta as TimeDelta
from pathlib import Path
from textwrap import dedent
from typing import Dict, List
import operator

from .blocks import AttendanceBlock, Schedule, TimeBlock
from .db import Students
from .utils import advance_time


def make_sched_title(sched: Schedule) -> str:
    return f'{sched.weekday.name}-{sched.time.hour}h{sched.time.minute}'


def make_pdf(
    atts: Dict[Schedule, List[AttendanceBlock]],
    students: Students,
    output: Path,
):
    week = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']

    merged_atts = {
        sched: AttendanceBlock(
            block=TimeBlock(
                title=make_sched_title(sched),
                date=attlist[0].block.date,
                start=sched.time,
                end=advance_time(sched.time, TimeDelta(minutes=sched.credits * 50)),
            ),
            attenders=reduce(
                operator.or_,
                (b.attenders for b in attlist),
                set()
            )
        ) for sched, attlist in atts.items()
    }

    for sched, att in merged_atts.items():
        print(dedent(f'''
        Attendance for {att.block.title}:
        - Date: {week[att.block.date.weekday()]}, {att.block.date}
        - Time: {att.block.start} to {att.block.end}
        - Attenders:
        ''').strip())
        for student in att.attenders:
            print(f'    {student}: {students[student]}')
