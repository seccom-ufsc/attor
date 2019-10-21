'''Definition of events time block.

A TimeBlock is just a time span made merely for comparison/filtering purposes.
A full attendance is represented by an AttendanceBlock, which is an aggregate
of a TimeBlock and a list of attending students.
'''
from dataclasses import dataclass
from datetime import (
    date as Date,
    datetime as DateTime,
    time as Time,
    timedelta as TimeDelta,
)
from pathlib import Path
from textwrap import dedent
from typing import List, Union

from cagrex.cagr import Class, Weekday

from .sympla import Sheet


StudentID = str


class NoFittingBlock(Exception):
    pass


@dataclass(frozen=True)
class TimeBlock:
    '''An event time block (check module description).'''
    title: str
    date: Date
    start: Time
    end: Time


@dataclass(frozen=True)
class AttendanceBlock:
    '''An attendance list in an specific TimeBlock.'''
    block: TimeBlock
    attenders: List[StudentID]


def fits_into(weekday: Weekday, time: Time, block: TimeBlock) -> bool:
    '''Checks if given weekday and time fits into given timeblock.'''
    block_weekday = Weekday(block.date.isoweekday() + 1)
    weekday_fits = block_weekday == weekday
    time_fits = time >= block.start and time <= block.end
    checks = weekday_fits and time_fits

    print(dedent(f'''
    ____?= ({weekday}, {time}) fits into {block}?
        --> Weekday: {block_weekday} == {weekday} ? -> {weekday_fits}
        --> Time   : {time} in {block.start, block.end} ? -> {time_fits}
        --> {checks}
    '''))
    return checks


def filter_class_schedule(
    blocks: List[AttendanceBlock],
    class_: Class,
) -> List[AttendanceBlock]:
    '''Returns which blocks fit into given class's schedule.'''
    print(f'Class {class_.subject_id}-{class_.class_id} schedules: {class_.schedule}')
    return [
        block
        for block in blocks
        if any(
            fits_into(sched.weekday, sched.time, block.block)
            for sched in class_.schedule
        )
    ]


def keep_only_students(
    blocks: List[AttendanceBlock],
    class_: Class
) -> List[AttendanceBlock]:
    '''Returns back each block, but with attenders filtered by who is in given
    class.'''
    return [
        AttendanceBlock(
            block=block.block,
            attenders=[
                student_id
                for student_id in block.attenders
                if student_id in class_.students
            ],
        )
        for block in blocks
    ]


def filter_by_day(
    blocks: List[AttendanceBlock],
    date: Date
) -> List[AttendanceBlock]:
    return [block for block in blocks if block.block.date == date]


def block_for_timespan(
    start: Time,
    end: Time,
    blocks: List[TimeBlock],
    threshold: Time = Time(0, 15, 0),
) -> TimeBlock:
    def diff(a: Time, b: Time) -> Time:
        a_ = DateTime.combine(Date.today(), a)
        b_ = TimeDelta(minutes=b.minute)
        return (a_ - b_).time()

    def sum_(a: Time, b: Time) -> Time:
        a_ = DateTime.combine(Date.today(), a)
        b_ = TimeDelta(minutes=b.minute)
        return (a_ + b_).time()

    for block in blocks:
        s, e = block.start, block.end
        if start >= diff(s, threshold) and end <= sum_(e, threshold):
            print(f'Fit into {block}')
            return block

    raise NoFittingBlock(
        f'No block between {start} and {end} found.'
    )


def attendance_block_from_sheet(sheet: Union[Sheet, Path]) -> AttendanceBlock:
    if isinstance(sheet, Path):
        sheet = Sheet.load(sheet)

    return AttendanceBlock(
        block=TimeBlock(
            title=sheet.name,
            date=sheet.date,
            start=sheet.first_checkin,
            end=sheet.last_checkin,
        ),
        attenders=[ticket.student_id for ticket in sheet.tickets]
    )
