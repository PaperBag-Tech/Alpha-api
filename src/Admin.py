from sqlalchemy.orm import session
from Database.Config import LocalSession, Base, engine
from Models.Policy import Policy
from Models.Category import Category
from Models.Role import Role
from Models.User import User
from API.Authentication import hashPassword
from Colors import bcolors



def getAdminRoleData():
	roleList = list()
	for table in Base.metadata.tables.keys():
		roleList.append(f"{table}:write")
		roleList.append(f"{table}:read")
		roleList.append(f"{table}:update")
		roleList.append(f"{table}:delete")
	roleStr = ",".join(roleList)
	admin = Role()
	admin.name = "Admin"
	admin.desp = "Full access"
	admin.permissions = roleStr
	return admin

def getAdminUserData(roleId:int):
	name: str = input("Enter user full name: ")
	emailId: str = input("Enter user email id: ")
	password: str = input("password: ")
	confirmPassword: str = input("Confirm password: ")
	if password != confirmPassword:
		raise Exception("password doesn't match")
	phoneNumber: str = input("Enter phone number: ")
	user = User(emailId=emailId, fullName=name, passwordHash=hashPassword(password), 
	phoneNumber=phoneNumber, roleId=roleId)
	return user

def createAdminRole(db:session):
	role = db.query(Role).filter(Role.name == "Admin").first()
	if role == None:
		role = getAdminRoleData()
		db.add(role)
		db.commit()
		db.refresh(role)
		print(f"{bcolors.OKGREEN}**************************** Admin role created ****************************{bcolors.ENDC}")
	else:
		print(f"{bcolors.WARNING}**************************** Admin role exists in db ****************************{bcolors.ENDC}")
	return role

def createAdminUser(db: session, user: User):
	db.add(user)
	db.commit()
	print(f"{bcolors.OKGREEN}**************************** Admin user created ****************************{bcolors.ENDC}")


if __name__ == "__main__":
	Base.metadata.create_all(engine)
	db = LocalSession()
	role = createAdminRole()
	user = db.query(User).filter(User.roleId == role.id).first()
	if user == None:
		user = getAdminUserData(role.id)
		createAdminUser(db, user)
	else:
		print(f"{bcolors.WARNING}**************************** Admin user exists in db ****************************{bcolors.ENDC}")
