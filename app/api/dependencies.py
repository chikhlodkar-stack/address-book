from app.db.session import SessionLocal


def get_db():
    """
    Dependency function that yields a SQLAlchemy database session.
    Ensures the session is always closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
