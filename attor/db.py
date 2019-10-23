'''Management of attendance and classes databases.'''
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date as Date, time as Time
from pathlib import Path
from typing import Dict, List
import re

from cagrex.cagr import Weekday
import toml

from .blocks import AttendanceBlock, Schedule, TimeBlock


StudentID = str
Students = Dict[StudentID, str]


class DuplicatedBlockError(Exception):
    pass


class DuplicatedClassError(Exception):
    pass


class ClassNotFound(Exception):
    pass


@dataclass
class Class:
    subject_id: str
    class_id: str
    semester: str
    students: List[StudentID]
    schedule: List[Schedule]


class InvalidWeekdayFormat(Exception):
    pass


def _weekday_from_str(s: str) -> Weekday:
    match = re.compile(r'<Weekday.\w+: (\d+)>').match(s)
    if match is None:
        raise InvalidWeekdayFormat(f'Could not build weekday from {s}')
    return Weekday(int(match.groups()[0]))


@dataclass
class Database:
    path: Path
    blocks: List[TimeBlock] = field(default_factory=list)
    attendances: List[AttendanceBlock] = field(default_factory=list)
    classes: List[Class] = field(default_factory=list)
    students: Students = field(default_factory=dict)

    @staticmethod
    def load(path: Path) -> Database:
        with open(path) as f:
            data = toml.load(f)

        return Database(
            path=path,
            blocks=[TimeBlock(**block) for block in data['blocks']],
            attendances=[
                AttendanceBlock(
                    block=TimeBlock(**block['block']),
                    attenders=set(block['attenders'])
                )
                for block in data['attendances']
            ],
            classes=[
                Class(
                    subject_id=class_['subject_id'],
                    class_id=class_['class_id'],
                    semester=class_['semester'],
                    students=class_['students'],
                    schedule=[
                        Schedule(
                            weekday=_weekday_from_str(sched['weekday']),
                            time=sched['time'],
                            credits=sched['credits'],
                        )
                        for sched in class_['schedule']
                    ]
                ) for class_ in data['classes']
            ],
            students=data['students']
        )

    def save(self):
        _asdict = asdict(self)
        del _asdict['path']
        with open(self.path, 'w') as f:
            toml.dump(_asdict, f)

    def add_attendances(self, att: AttendanceBlock):
        dups = [
            stored
            for stored in self.attendances
            if stored.block.title == att.block.title
        ]

        if dups:
            dup = dups[0]
            dup.attenders.update(att.attenders)
        else:
            self.attendances.append(att)

    def add_students(self, students: Students):
        for id_, name in students.items():
            self.students[id_] = name

    def add_class(self, class_: Class):
        if any(class_ == stored_class for stored_class in self.classes):
            raise DuplicatedClassError(
                f'Class {class_.class_id} already exists on database.'
            )

        self.classes.append(class_)

    def add_block(self, block: TimeBlock):
        if any(block.title == stored.title for stored in self.blocks):
            raise DuplicatedBlockError(
                f'Time block {block.title} already exists on database.'
            )

        self.blocks.append(block)

    def students_with_ids(self, student_ids: List[StudentID]) -> Students:
        '''Returns all students with given ids.'''
        return {
            id_: self.students[id_]
            for id_ in student_ids
            if id_ in self.students.keys()
        }

    def load_class(
        self,
        subject_id: str,
        class_id: str,
        semester: str
    ) -> Class:
        for class_ in self.classes:
            if (
                (class_.subject_id, class_.class_id, class_.semester)
                == (subject_id, class_id, semester)
            ):
                return class_

        raise ClassNotFound(
            f'No class {subject_id}-{class_id} in {semester} (Database)'
        )


if __name__ == '__main__':
    attendances = [
        AttendanceBlock(
            block=TimeBlock(
                title='Test time',
                date=Date.today(),
                start=Time(10, 15),
                end=Time(12, 30),
            ),
            attenders=set()
        )
    ]

    students = {
        '14200743': 'Tiz',
        '15100643': 'Who?',
    }
    db = Database(Path('test.db'), [], attendances, [], students)
    db.save()
    print('Loaded from Database:')
    print(Database.load(Path('test.db')))
