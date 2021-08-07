import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 

from Database.Config import Base, getDB
from Index import app


# constants
testDbUrl = "sqlite:///./src/Tests/test_db.db"
testEngine = create_engine(testDbUrl,connect_args={"check_same_thread": False})
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=testEngine)
Base.metadata.create_all(bind=testEngine)

def getTestDB():
	try:
		db = TestSession()
		yield db
	finally:
		db.close()

@pytest.fixture(scope="session")
def testSession():
	try:
		app.dependency_overrides[getDB] = getTestDB
		client = TestClient(app)
		yield client
	finally:
		Base.metadata.drop_all(bind=testEngine)
