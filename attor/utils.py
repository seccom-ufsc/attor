'''General utility functions.'''
from datetime import (
    date as Date,
    datetime as DateTime,
    time as Time,
    timedelta as TimeDelta,
)
from typing import Union


def advance_time(a: Time, b: Union[Time, TimeDelta]) -> Time:
    a_ = DateTime.combine(Date.today(), a)

    if isinstance(b, Time):
        b = TimeDelta(minutes=b.minute)

    return (a_ + b).time()


def rewind_time(a: Time, b: Union[Time, TimeDelta]) -> Time:
    a_ = DateTime.combine(Date.today(), a)

    if isinstance(b, Time):
        b = TimeDelta(minutes=b.minute)

    return (a_ - b).time()
