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
    """Add new SQLite columns without deleting existing scholarship data."""

    if "scholarships" not in inspect(engine).get_table_names():
        return

    required_columns = {
        "source_name": "VARCHAR",
        "source_id": "VARCHAR",
        "source_url": "VARCHAR",
        "application_url": "VARCHAR",
        "description": "VARCHAR",
        "requirements_raw": "VARCHAR",
        "last_verified_at": "DATETIME",
        "is_active": "BOOLEAN NOT NULL DEFAULT 1",
    }

    existing_columns = {
        column["name"]
        for column in inspect(engine).get_columns("scholarships")
    }

    with engine.begin() as connection:
        for name, column_type in required_columns.items():
            if name not in existing_columns:
                connection.execute(
                    text(
                        f"ALTER TABLE scholarships "
                        f"ADD COLUMN {name} {column_type}"
                    )
                )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
