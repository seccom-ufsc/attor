'''Management of attendance and classes databases.'''
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date as Date, time as Time
from pathlib import Path
from typing import Dict, List

from cagrex.cagr import Weekday
import toml

from .blocks import AttendanceBlock, TimeBlock


StudentID = str
Students = Dict[StudentID, str]


class DuplicatedBlockError(Exception):
    pass


class DuplicatedClassError(Exception):
    pass


class ClassNotFound(Exception):
    pass


@dataclass
class Schedule:
    weekday: Weekday
    time: Time
    credits: int


@dataclass
class Class:
    subject_id: str
    class_id: str
    semester: str
    students: List[StudentID]
    schedule: List[Schedule]


@dataclass
class Database:
    path: Path
    attendances: List[AttendanceBlock]
    classes: List[Class]
    students: Students

    @staticmethod
    def load(path: Path) -> Database:
        with open(path) as f:
            data = toml.load(f)

        return Database(
            path=path,
            attendances=[
                AttendanceBlock(
                    block=TimeBlock(**block['block']),
                    attenders=block['attenders']
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
                        Schedule(**sched)
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
            dup.attenders.extend(att.attenders)

    def add_students(self, students: Students):
        for id_, name in students.items():
            self.students[id_] = name

    def add_class(self, class_: Class):
        if any(class_ == stored_class for stored_class in self.classes):
            raise DuplicatedClassError(
                f'Class {class_.class_id} already stored.'
            )

        self.classes.append(class_)

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
            attenders=[]
        )
    ]

    students = {
        '14200743': 'Tiz',
        '15100643': 'Who?',
    }
    db = Database(Path('test.db'), attendances, [], students)
    db.save()
    print('Loaded from Database:')
    print(Database.load(Path('test.db')))
