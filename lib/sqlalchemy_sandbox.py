#!/usr/bin/env python3

from datetime import datetime

from requests import Session
from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.orm import declarative_base

from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    __table_args__ = (
        PrimaryKeyConstraint(
            'id',
            name='id_pk'
        ),
        UniqueConstraint(
            'email',
            name= 'unique_email'
        ),
        CheckConstraint(
            'grade BETWEEN 1 AND 12',
            name='grade_between_1_and_12'
        )
    )

    Index('index_name', 'name')

    id = Column(Integer())
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())

    def __repr__(self):
        return f"Student {self.id}: " \
            + f"{self.name}, " \
            + f"Grade {self.grade}"

if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    albert_einstein = Student(
        name = "Albert Einstein",
        email = "Albert.einstein@zurich.edu",
        grade = 6,
        birthday=datetime(
            year=1879,
            month=3,
            day=14
        )
    )

    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(
            year=1912,
            month=6,
            day=23
        ),
    )

    session.bulk_save_objects([alan_turing,albert_einstein])
    session.commit()

    # print(f"New student ID is {albert_einstein.id}.")
    # print(f"New student ID is {alan_turing.id}.")

    # Selecting specific column
    names = [name for name in session.query(Student.name)]
    print(names)

    # Ordering Results descending order
    students_by_name = [student for student in session.query(Student.name).order_by(desc(Student.name))]
    print(students_by_name)

    # Limiting
    oldest_student_1 = [student for student in session.query(Student.name, Student.grade).order_by(desc(Student.grade)).limit(1)]
    print(oldest_student_1)

    # Limiting using first() method
    oldest_student = session.query(Student.name, Student.birthday).order_by(desc(Student.grade)).first()
    print(oldest_student)

    # count()
    student_count = session.query(func.count(Student.id)).first()
    print(student_count)

    # Filtering
    query = session.query(Student).filter(Student.name.like('%Alan%'), Student.grade == 11)
    for record in query:
        print(record.name)

    # Updating Data
    session.query(Student).update({
        Student.grade: Student.grade + 1
    })

    print([(
        student.name,
        student.grade
    ) for student in session.query(Student)])

    # Deleting Data
    delete_query = session.query(Student).filter(
        Student.name == "Albert Einstein"
    )
    delete_query.delete()
    albert_einstein = query.first()
    session.commit()

    print(albert_einstein)