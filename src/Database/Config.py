from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import secrets

engine = create_engine('mysql+mysqldb://{0}:{1}@{2}:{3}/{4}'.format(
	secrets.dbUserName, secrets.dbPassword,
	secrets.dbHost, secrets.dbPort, secrets.dbName), echo=True)

LocalSession = sessionmaker(autocommit=False,autoflush=False, bind=engine)

Base = declarative_base()

def sessionMaker():
	db = LocalSession()
	try:
		yield db
	finally:
		db.close()