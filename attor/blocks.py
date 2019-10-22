'''Definition of events time block.

A TimeBlock is just a time span made merely for comparison/filtering purposes.
A full attendance is represented by an AttendanceBlock, which is an aggregate
of a TimeBlock and a list of attending students.
'''
from dataclasses import dataclass
from datetime import (
    date as Date,
    time as Time,
    timedelta as TimeDelta,
)
from pathlib import Path
from typing import Dict, List, Set, Union

from cagrex.cagr import Class, Weekday

from .sympla import Sheet
from .utils import advance_time, rewind_time


StudentID = str


class NoFittingBlock(Exception):
    pass


@dataclass(unsafe_hash=True)
class Schedule:
    weekday: Weekday
    time: Time
    credits: int


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
    attenders: Set[StudentID]


def fits_into(sched: Schedule, block: TimeBlock) -> bool:
    '''Checks if given weekday and time fits into given timeblock.'''
    block_weekday = Weekday(block.date.isoweekday() + 1)
    weekday_fits = block_weekday == sched.weekday

    start = sched.time
    end = advance_time(sched.time, TimeDelta(minutes=sched.credits * 50))

    time_fits = (
        (start >= block.start and start <= block.end)
        or (end >= block.start and end <= block.end)
    )
    return weekday_fits and time_fits


def filter_class_schedule(
    blocks: List[AttendanceBlock],
    class_: Class,
) -> Dict[Schedule, List[AttendanceBlock]]:
    '''Returns which blocks fit into given class's schedule.'''
    return {
        sched: [
            block
            for block in blocks
            if fits_into(sched, block.block)
        ] for sched in class_.schedule
    }


def keep_only_students(
    blocks: List[AttendanceBlock],
    class_: Class
) -> List[AttendanceBlock]:
    '''Returns back each block, but with attenders filtered by who is in given
    class.'''
    return [
        AttendanceBlock(
            block=block.block,
            attenders={
                student_id
                for student_id in block.attenders
                if student_id in class_.students
            },
        )
        for block in blocks
    ]


def filter_by_day(
    blocks: List[AttendanceBlock],
    date: Date
) -> List[AttendanceBlock]:
    return [block for block in blocks if block.block.date == date]


def block_for_timespan(
    date: Date,
    start: Time,
    end: Time,
    blocks: List[TimeBlock],
    threshold: Time = Time(0, 15, 0),
) -> TimeBlock:
    for block in blocks:
        s, e = block.start, block.end
        if (
            block.date.weekday() == date.weekday()
            and start >= rewind_time(s, threshold)
            and end <= advance_time(e, threshold)
        ):
            return block

    raise NoFittingBlock(
        f'No block between {start} and {end} found for day {date}.'
    )


def attendance_block_from_sheet(sheet: Union[Sheet, Path]) -> AttendanceBlock:
    if isinstance(sheet, Path):
        sheet = Sheet.load(sheet)

    return AttendanceBlock(
        block=TimeBlock(
            title=sheet.name,
            date=sheet.date,
            start=sheet.start,
            end=sheet.end,
        ),
        attenders={
            ticket.student_id
            for ticket in sheet.tickets
            if ticket.checked_in and ticket.student_id is not None
        }
    )
