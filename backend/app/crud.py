from sqlalchemy.orm import Session
from . import models, schemas


def get_scholarships(db: Session):
    return db.query(models.Scholarship).all()



def create_scholarship(
    db: Session,
    scholarship: schemas.ScholarshipCreate
):
    db_scholarship = models.Scholarship(
        name=scholarship.name,
        provider=scholarship.provider,
        amount=scholarship.amount,
        deadline=scholarship.deadline,
        major=scholarship.major,
        gpa_requirement=scholarship.gpa_requirement,
        eligibility=scholarship.eligibility,
        state=scholarship.state,
        citizenship=scholarship.citizenship,
        interests=scholarship.interests,
        skills=scholarship.skills,
        projects=scholarship.projects,
        leadership=scholarship.leadership,
        volunteer=scholarship.volunteer,
        certifications=scholarship.certifications,
        weights=scholarship.weights
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

    scholarship.name = scholarship_update.name
    scholarship.provider = scholarship_update.provider
    scholarship.amount = scholarship_update.amount
    scholarship.deadline = scholarship_update.deadline
    scholarship.major = scholarship_update.major
    scholarship.gpa_requirement = scholarship_update.gpa_requirement
    scholarship.eligibility = scholarship_update.eligibility
    scholarship.state = scholarship_update.state
    scholarship.citizenship = scholarship_update.citizenship
    scholarship.interests = scholarship_update.interests

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
    db_student = models.Student(
        name=student.name,
        email=student.email,
        major=student.major,
        gpa=student.gpa,
        year=student.year,
        university=student.university,
        state=student.state,
        citizenship=student.citizenship,
        interests=student.interests,
        skills=student.skills,
        projects=student.projects,
        leadership=student.leadership,
        volunteer=student.volunteer,
        certifications=student.certifications,
        languages=student.languages,
        awards=student.awards
    )

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

    student.name = student_update.name
    student.email = student_update.email
    student.major = student_update.major
    student.gpa = student_update.gpa
    student.year = student_update.year
    student.university = student_update.university
    student.state = student_update.state
    student.citizenship = student_update.citizenship
    student.interests = student_update.interests

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