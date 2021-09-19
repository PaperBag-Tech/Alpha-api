from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, session

import Secrets

engine = create_engine('mysql+mysqldb://{0}:{1}@{2}:{3}/{4}'.format(
	Secrets.dbUserName, Secrets.dbPassword,
	Secrets.dbHost, Secrets.dbPort, Secrets.dbName), echo=True)

LocalSession = sessionmaker(autocommit=False,autoflush=False, bind=engine)

Base = declarative_base()

def getDB():
	db: session = LocalSession()
	try:
		db.expire_on_commit = False
		yield db
	finally:
		db.close()