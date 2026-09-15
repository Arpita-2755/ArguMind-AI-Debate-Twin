from sqlalchemy import text

from db.database import engine


def test_database_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

        assert result.scalar() == 1


if __name__ == "__main__":
    test_database_connection()
    print("PostgreSQL database connection test passed!")