'''Definition of events time block.

A TimeBlock is just a time span made merely for comparison/filtering purposes.
A full attendance is represented by an AttendanceBlock, which is an aggregate
of a TimeBlock and a list of attending students.
'''
from dataclasses import dataclass
from datetime import date as Date, time as Time
from typing import List

from cagrex.cagr import Class, Weekday

from .sympla import Sheet


StudentID = str


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
    return (
        Weekday(block.date.weekday()) == weekday
        and time >= block.start and time <= block.end
    )


def filter_from_class(
    blocks: List[AttendanceBlock],
    class_: Class
) -> List[AttendanceBlock]:
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


def attendance_block_from_sheet(sheet: Sheet) -> AttendanceBlock:
    pass
