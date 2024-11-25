from sqlalchemy.orm import Session
from contextlib import contextmanager

class UnitOfWork:
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self.session = None

    def __enter__(self):
        self.session = self.session_factory()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.session.commit()
        else:
            self.session.rollback()
        self.session.close()

    def get_session(self) -> Session:
        if self.session is None:
            raise RuntimeError("Session is not initialized. Use UnitOfWork as a context manager.")
        return self.session
