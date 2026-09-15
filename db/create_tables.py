from db.base import Base
from db.database import engine

# Import models so SQLAlchemy registers them with Base.metadata.
from db.models.reasoning_memory import ReasoningMemoryModel


def create_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully!")