from sqlalchemy.orm import session
from Database.Config import LocalSession, Base, engine
from Models.Policy import Policy
from Models.Category import Category
from Models.Schedule import Schedule
from Models.Role import Role
from Models.User import User
from API.Authentication import hashPassword
from Colors import bcolors
from Database.Enums import UserRole



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
	admin.type = UserRole.Admin
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

if __name__ == "__main__":
	Base.metadata.create_all(engine)
	db = LocalSession()
	role = db.query(Role).filter(Role.type == UserRole.Admin.name).first()
	if role == None:
		role = getAdminRoleData()
		db.add(role)
		db.commit()
		db.refresh(role)
		print(f"{bcolors.OKGREEN}**************************** Admin role created ****************************{bcolors.ENDC}")
	else:
		print(f"{bcolors.WARNING}**************************** Admin role exists in db ****************************{bcolors.ENDC}")
	user = db.query(User).filter(User.roleId == role.id).first()
	if user == None:
		user = getAdminUserData(role.id)
		db.add(user)
		db.commit()
		print(f"{bcolors.OKGREEN}**************************** Admin user created ****************************{bcolors.ENDC}")
	else:
		print(f"{bcolors.WARNING}**************************** Admin user exists in db ****************************{bcolors.ENDC}")
	db.close()
