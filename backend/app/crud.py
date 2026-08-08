from sqlalchemy.orm import Session
from . import models, schemas


def get_scholarships(db: Session):
    return db.query(models.Scholarship).all()



def create_scholarship(
    db: Session,
    scholarship: schemas.ScholarshipCreate
):
    db_scholarship = models.Scholarship(
        **scholarship.model_dump()
    )

    db.add(db_scholarship)
    db.commit()
    db.refresh(db_scholarship)

    return db_scholarship
def get_scholarship(db: Session, scholarship_id: int):
    return db.query(models.Scholarship).filter(
        models.Scholarship.id == scholarship_id
    ).first()
def update_scholarship(
    db: Session,
    scholarship_id: int,
    scholarship_update: schemas.ScholarshipUpdate
):
    scholarship = db.query(models.Scholarship).filter(
        models.Scholarship.id == scholarship_id
    ).first()

    if scholarship is None:
        return None

    for field, value in scholarship_update.model_dump().items():
        setattr(scholarship, field, value)

    db.commit()
    db.refresh(scholarship)

    return scholarship
def delete_scholarship(
    db: Session,
    scholarship_id: int
):
    scholarship = db.query(models.Scholarship).filter(
        models.Scholarship.id == scholarship_id
    ).first()

    if scholarship is None:
        return None

    db.delete(scholarship)
    db.commit()

    return scholarship

def get_students(db: Session):
    return db.query(models.Student).all()

def create_student(
    db: Session,
    student: schemas.StudentCreate
):
    db_student = models.Student(**student.model_dump())

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student

def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

def update_student(
    db: Session,
    student_id: int,
    student_update: schemas.StudentUpdate
):
    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if student is None:
        return None

    for field, value in student_update.model_dump().items():
        setattr(student, field, value)

    db.commit()
    db.refresh(student)

    return student

def delete_student(
    db: Session,
    student_id: int
):
    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if student is None:
        return None

    db.delete(student)
    db.commit()

    return student
