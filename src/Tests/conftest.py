import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 

from Database.Config import Base, getDB
from Admin import createAdminRole, createAdminUser
from Index import app
from Models.Role import Role
from Models.User import User
from API.Authentication import hashPassword
from Colors import bcolors


# constants
testDbUrl = "sqlite:///./src/Tests/test_db.db"
adminEmail = "TestAdmin@pbt.com"
adminFullName = "Test Admin"
adminPassword = "password"
adminPhone = "9098990989"

testEngine = create_engine(testDbUrl,connect_args={"check_same_thread": False})
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=testEngine)
Base.metadata.create_all(bind=testEngine)
db = TestSession()
role: Role = createAdminRole(db)
user: User = User(emailId = adminEmail, fullName = adminFullName, 
passwordHash = hashPassword(adminPassword), phoneNumber = adminPhone,
roleId = role.id)
duplicateUser = db.query(User).filter(User.fullName == user.fullName or User.phoneNumber == user.phoneNumber).first()
if duplicateUser == None:
	createAdminUser(db, user)
else:
	print(f"{bcolors.WARNING}**************************** Admin user exists in db ****************************{bcolors.ENDC}")
db.close()


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
