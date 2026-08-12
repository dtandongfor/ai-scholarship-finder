from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./scholarships.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def migrate_schema():
    """Add missing SQLite columns without deleting existing data."""

    inspector = inspect(engine)

    table_names = inspector.get_table_names()

    # ==========================================
    # SCHOLARSHIP MIGRATION
    # ==========================================

    if "scholarships" in table_names:

        required_scholarship_columns = {
            "state": "VARCHAR",
            "citizenship": "VARCHAR",
            "interests": "VARCHAR",
            "skills": "VARCHAR",
            "projects": "VARCHAR",
            "leadership": "VARCHAR",
            "volunteer": "VARCHAR",
            "certifications": "VARCHAR",
            "weights": "JSON",
            "source_name": "VARCHAR",
            "source_id": "VARCHAR",
            "source_url": "VARCHAR",
            "application_url": "VARCHAR",
            "description": "VARCHAR",
            "requirements_raw": "VARCHAR",
            "requirements": "JSON",
            "requirements_complete": "BOOLEAN NOT NULL DEFAULT 0",
            "last_verified_at": "DATETIME",
            "is_active": "BOOLEAN NOT NULL DEFAULT 1",
            "eligible_student_types": "VARCHAR",
            "max_household_income": "INTEGER",
            "min_sat_score": "INTEGER",
            "min_act_score": "INTEGER",
        }

        existing_scholarship_columns = {
            column["name"]
            for column in inspector.get_columns("scholarships")
        }

        with engine.begin() as connection:
            for name, column_type in required_scholarship_columns.items():

                if name not in existing_scholarship_columns:

                    connection.execute(
                        text(
                            f"ALTER TABLE scholarships "
                            f"ADD COLUMN {name} {column_type}"
                        )
                    )

                    print(
                        f"Added missing scholarship column: {name}"
                    )

    # ==========================================
    # STUDENT MIGRATION
    # ==========================================

    if "students" in table_names:

        required_student_columns = {
            "state": "VARCHAR",
            "citizenship": "VARCHAR",
            "interests": "VARCHAR",
            "skills": "VARCHAR",
            "projects": "VARCHAR",
            "leadership": "VARCHAR",
            "volunteer": "VARCHAR",
            "certifications": "VARCHAR",
            "languages": "VARCHAR",
            "awards": "VARCHAR",
            "affiliations": "VARCHAR",
            "demonstrated_financial_need": "BOOLEAN",
            "planned_term_credits": "INTEGER",
            "student_type": "VARCHAR",
            "household_income": "INTEGER",
            "sat_score": "INTEGER",
            "act_score": "INTEGER",
            "financial_aid_submitted": "BOOLEAN",
            "pell_eligible": "BOOLEAN",
            "enrollment_status": "VARCHAR",
            "completed_credits": "INTEGER",
            "volunteer_hours": "INTEGER",
            "work_hours": "INTEGER",
            "disciplinary_good_standing": "BOOLEAN",
            "accepts_service_commitment": "BOOLEAN",
            "is_first_generation": "BOOLEAN",
            "eligible_for_women_tech_scholarships": "BOOLEAN",
            "can_seek_security_clearance": "BOOLEAN",
        }

        existing_student_columns = {
            column["name"]
            for column in inspector.get_columns("students")
        }

        with engine.begin() as connection:
            for name, column_type in required_student_columns.items():

                if name not in existing_student_columns:

                    connection.execute(
                        text(
                            f"ALTER TABLE students "
                            f"ADD COLUMN {name} {column_type}"
                        )
                    )

                    print(
                        f"Added missing student column: {name}"
                    )
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
