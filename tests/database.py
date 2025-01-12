from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db
from app.database import Base
import pytest
from alembic import command

# SQLACHEMY_DATABASE_URL = 'postgresql://postgres:emna123@localhost:5432/fastapi_test'
SQLACHEMY_DATABASE_URL =f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLACHEMY_DATABASE_URL)


TestingSessionLocal = sessionmaker(autocommit= False, autoflush=False, bind=engine)






# client = TestClient(app)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    #  we can use alembic : command.upgrade("head")
    # command.downgrade("base")
    db = TestingSessionLocal()
    try:
        yield db 
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def overrid_get_db():
   
        try:
            yield session 
        finally:
            session.close()
    app.dependency_overrides[get_db] = overrid_get_db

    yield TestClient(app)

