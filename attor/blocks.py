'''Definition of events time block.

A TimeBlock is just a time span made merely for comparison/filtering purposes.
A full attendance is represented by an AttendanceBlock, which is an aggregate
of a TimeBlock and a list of attending students.
'''
from dataclasses import dataclass
from datetime import date as Date, time as Time
from typing import List

from cagrex.cagr import Weekday

from .types import StudentID


@dataclass(frozen=True)
class TimeBlock:
    '''An event time block (check module description).'''
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


def filter_from_class(block: AttendanceBlock, class_: Class) -> List[AttendanceBlock]:
    pass
